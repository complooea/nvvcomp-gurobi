"""
code related to checking for counterexamples
"""

from pathlib import Path
import functools
import gzip
import datetime
import multiprocessing as mp
import sys

import numpy as np
import onnx
import onnxruntime as ort

# Prevent a bug in some environments
# https://github.com/microsoft/onnxruntime/issues/8313#issuecomment-1486097717
_default_session_options = ort.capi._pybind_state.get_default_session_options()
def get_default_session_options_new():
     _default_session_options.inter_op_num_threads = 1
     _default_session_options.intra_op_num_threads = 1
     return _default_session_options
ort.capi._pybind_state.get_default_session_options = get_default_session_options_new

from .vnnlib_v1 import read_vnnlib_simple, get_io_nodes

from cachier import cachier
CPU_PROVIDER = "CPUExecutionProvider"


# Consecutive counterexamples in a benchmark share a network (smart_turn is one
# network for all 50 instances), so parsing the model and building the session
# once per network instead of per check is the bulk of the speedup. Bounded to a
# couple of networks so memory stays flat -- the arena is off, so an evicted
# session frees its native allocations.
@functools.lru_cache(maxsize=2)
def _load_onnx(onnx_filename):
    'parse an onnx model once per network'
    return onnx.load(onnx_filename)

@functools.lru_cache(maxsize=2)
def _session_for(onnx_filename):
    'build the inference session once per network'
    sess_opt = ort.SessionOptions()
    sess_opt.intra_op_num_threads = 12
    sess_opt.inter_op_num_threads = 12
    # Return native allocations to the OS as soon as the session is dropped;
    # the arena retains them, so per-CE sessions accumulate memory until OOM.
    sess_opt.enable_cpu_mem_arena = False
    return ort.InferenceSession(
        _load_onnx(onnx_filename).SerializeToString(),
        sess_opt,
        providers=[CPU_PROVIDER],
    )

def predict_with_onnxruntime(onnx_filename, *inputs):
    'run an onnx model, reusing the cached session for this network'

    sess = _session_for(onnx_filename)
    names = [i.name for i in sess.get_inputs()]

    inp = dict(zip(names, inputs))
    res = sess.run(None, inp)

    return res[0]

def read_ce_file(ce_path):
    """get file contents"""

    if ce_path.endswith('.gz'):
        with gzip.open(ce_path, 'rb') as f:
            content = f.read().decode('utf-8')
    else:
        with open(ce_path, 'r', encoding='utf-8') as f:
            content = f.read()

    content = content.replace('\n', ' ').strip()

    return content

class CounterexampleResult:
    """enum for return value of is_correct_counterexample"""

    CORRECT = "correct"
    CORRECT_UP_TO_TOLERANCE = "correct_up_to_tolerance"
    NO_CE = "no_ce"
    EXEC_DOESNT_MATCH = "exec_doesnt_match"
    SPEC_NOT_VIOLATED = "spec_not_violated"
    WRONG_SHAPE = 'wrong_shape'
    MALFORMED_CE = "malformed_ce"
    UNSUPPORTED = "unsupported"


def get_ce_diff(onnx_filename, vnnlib_filename, ce_path, abs_tol, rel_tol):
    """get difference in execution"""

    try:
        content = read_ce_file(ce_path)
    except FileNotFoundError:
        return CounterexampleResult.NO_CE, f"Note: no counter example provided in {ce_path}"

    if len(content) < 2:
        return CounterexampleResult.NO_CE, f"Note: no counter example provided in {ce_path}"

    #print(f"CE CONTENT:\n{content}")
    
    assert content[0] == '(' and content[-1] == ')'
    content = content[1:-1]

    x_list = []
    y_list = []

    parts = content.split(')')
    for part in parts:
        part = part.strip()
                
        if not part:
            continue

        while "  " in part:
            part = part.replace("  ", " ")
        
        assert part[0] == '('
        part = part[1:]

        #print(f"part with len={len(part.split(' '))}: {part}")
        name, num = part.split(' ')
        assert name[0:2] in ['X_', 'Y_']

        if name[0:2] == 'X_':
            assert int(name[2:]) == len(x_list)
            x_list.append(float(num))
        else:
            assert int(name[2:]) == len(y_list)
            y_list.append(float(num))

    onnx_model = _load_onnx(onnx_filename)

    inp, _out, input_dtype = get_io_nodes(onnx_model)
    input_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in inp.type.tensor_type.shape.dim)

    x_in = np.array(x_list, dtype=input_dtype)
    flatten_order = 'C'
    # Only reshape if the total size matches
    if x_in.size == np.prod(input_shape):
        x_in = x_in.reshape(input_shape, order=flatten_order)
    else:
        with open('./cex_wrong_shape.csv', 'a') as f:
            f.write(f'{ce_path},{x_in.shape},{input_shape}\n')
        return CounterexampleResult.WRONG_SHAPE, f"Cannot reshape input of size {x_in.size} to shape {input_shape}"
    output = predict_with_onnxruntime(onnx_filename, x_in)

    flat_out = output.flatten(flatten_order)

    strict_vio, strict_msg = is_specification_vio(
        onnx_filename,
        vnnlib_filename,
        tuple(x_list),
        tuple(flat_out),
        input_tol=0.0,
        output_tol=0.0,
    )
    if strict_vio:
        return (
            CounterexampleResult.CORRECT,
            "Solver-provided output values ignored; ONNX CPU replay output satisfies the property with strict input bounds.\n"
            + strict_msg,
        )

    tolerant_vio, tolerant_msg = is_specification_vio(
        onnx_filename,
        vnnlib_filename,
        tuple(x_list),
        tuple(flat_out),
        input_tol=abs_tol,
        output_tol=0.0,
    )
    if tolerant_vio:
        return (
            CounterexampleResult.CORRECT_UP_TO_TOLERANCE,
            "Solver-provided output values ignored; ONNX CPU replay output satisfies the property, "
            f"but the input needs up to {abs_tol} absolute tolerance.\n{tolerant_msg}",
        )

    return (
        CounterexampleResult.SPEC_NOT_VIOLATED,
        "Solver-provided output values ignored; ONNX CPU replay output did not satisfy the property under strict or tolerated input bounds.\n"
        + tolerant_msg,
    )


@cachier(cache_dir='./cachier', stale_after=datetime.timedelta(days=365), wait_for_calc_timeout=30, pickle_reload=False, separate_files=True)
def is_specification_vio(onnx_filename, vnnlib_filename, x_list, expected_y, input_tol, output_tol=0.0):
    """check that the spec file was obeyed"""

    msg = f"Checking if spec was actually violated (input_tol={input_tol}, output_tol={output_tol})"
    onnx_model = _load_onnx(onnx_filename)

    inp, out, input_dtype = get_io_nodes(onnx_model)

    inp_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in inp.type.tensor_type.shape.dim)
    out_shape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in out.type.tensor_type.shape.dim)

    num_inputs = 1
    num_outputs = 1

    for n in inp_shape:
        num_inputs *= n

    for n in out_shape:
        num_outputs *= n

    box_spec_list = read_vnnlib_simple(vnnlib_filename, num_inputs, num_outputs)
    replay_x = np.asarray(x_list, dtype=input_dtype).ravel(order='C')

    rv = False

    for i, box_spec in enumerate(box_spec_list):
        input_box, spec_list = box_spec
        assert len(input_box) == len(replay_x), \
            f"input box len: {len(input_box)}, x_in len: {len(replay_x)}"

        inside_input_box = True
        max_input_violation = 0.0

        for (lb, ub), x in zip(input_box, replay_x):
            max_input_violation = max(max_input_violation, lb - x, x - ub, 0.0)
            if x < lb - input_tol or x > ub + input_tol:
                inside_input_box = False
                break

        if inside_input_box:
            msg += f"\nCE input X was inside box #{i}; max input violation={max_input_violation}"
            
            # check spec
            violated = False
                
            for j, (prop_mat, prop_rhs) in enumerate(spec_list):
                vec = prop_mat.dot(expected_y)
                sat = np.all(vec <= prop_rhs + output_tol)

                if sat:
                    msg += f"\nprop #{j} violated:\n{vec - prop_rhs}"
                    violated = True
                    break

            if violated:
                rv = True
                break
                
    return rv, msg
