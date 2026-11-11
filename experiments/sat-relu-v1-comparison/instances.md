# Per-instance comparison evidence

All comparisons are conditional where execution artifact binding is unavailable. Ratios are ABC/Gurobi measured time, not hardware-normalized speedups. W labels group structural descriptors only, not weights or properties.

| ID | Network | Inputs | Hidden widths | Elements | Width group | Match | Gurobi (validation) | ABC (validation) | Gurobi run s | ABC run s | ABC prep s | Comparison | ABC/G run |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| 0000 | sat_v27_c79_k0.onnx | 27 | [133] | 3992 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.20545829110778868 | 5.851499541 | 22.891761803 | both_same_answer | 28.480230753647966 |
| 0001 | unsat_v27_c79_k1.onnx | 27 | [133] | 3992 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.4506156670395285 | 6.412964596 | 19.250679229 | both_same_answer | 14.231561539198433 |
| 0002 | sat_v90_c810_k2.onnx | 90 | [990] | 92072 | W01 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.25794862513430417 | 5.862485548 | 19.229189072 | both_same_answer | 22.727337836934097 |
| 0003 | unsat_v90_c811_k3.onnx | 90 | [991] | 92165 | W01 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.00558524997905 | 6.702483914 | 19.229628026 | abc_only | None |
| 0004 | sat_v14_c20_k4.onnx | 14 | [48] | 818 | W02 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.1951379580423236 | 5.770316912 | 19.198172027 | both_same_answer | 29.570448363247056 |
| 0005 | unsat_v14_c20_k5.onnx | 14 | [48] | 818 | W02 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.21067679091356695 | 6.217560293 | 19.244679607 | both_same_answer | 29.51231726113979 |
| 0006 | sat_v29_c286_k6.onnx | 29 | [344] | 11010 | W03 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.21100254193879664 | 5.854545661 | 19.221034549 | both_same_answer | 27.746327637598647 |
| 0007 | unsat_v29_c287_k7.onnx | 29 | [345] | 11042 | W03 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.3305969589855522 | 6.437438189 | 19.214560507 | both_same_answer | 19.47216395684187 |
| 0008 | sat_v19_c40_k8.onnx | 19 | [78] | 1718 | W04 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.20187683287076652 | 5.833606381 | 19.257155776 | both_same_answer | 28.89685903054781 |
| 0009 | unsat_v19_c40_k9.onnx | 19 | [78] | 1718 | W04 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.21015229099430144 | 6.219026401 | 19.259420643 | both_same_answer | 29.592950767158836 |
| 0010 | sat_v29_c224_k10.onnx | 29 | [282] | 9026 | W03 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.21084720781072974 | 5.828877161 | 19.211777059 | both_same_answer | 27.64502893598848 |
| 0011 | unsat_v29_c225_k11.onnx | 29 | [283] | 9058 | W03 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.3305389580782503 | 6.41923834 | 19.218673449 | both_same_answer | 19.420519678894667 |
| 0012 | sat_v78_c478_k12.onnx | 78 | [634] | 51356 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.2108790830243379 | 5.835440708 | 19.216810079 | both_same_answer | 27.671974974049572 |
| 0013 | unsat_v78_c478_k13.onnx | 78 | [634] | 51356 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.00829637493007 | 6.484413487 | 19.225844471 | abc_only | None |
| 0014 | sat_v67_c139_k14.onnx | 67 | [273] | 19112 | W05 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.21064429194666445 | 5.836540669 | 19.211749651 | both_same_answer | 27.70804095882087 |
| 0015 | unsat_v67_c139_k15.onnx | 67 | [273] | 19112 | W05 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.3305246669333428 | 6.34864434 | 19.234617168 | both_same_answer | 19.20777773986937 |
| 0016 | sat_v91_c116_k16.onnx | 91 | [298] | 28014 | W06 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.21076954109594226 | 5.829016865 | 19.228541124 | both_same_answer | 27.655878713265462 |
| 0017 | unsat_v91_c116_k17.onnx | 91 | [298] | 28014 | W06 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01190445804968 | 6.385120552 | 19.186611751 | abc_only | None |
| 0018 | sat_v25_c249_k18.onnx | 25 | [299] | 8374 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.210003666812554 | 5.824838125 | 19.207391146 | both_same_answer | 27.736840091459737 |
| 0019 | unsat_v25_c249_k19.onnx | 25 | [299] | 8374 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.39080229215323925 | 6.418023425 | 19.235697252 | both_same_answer | 16.42268623768307 |
| 0020 | sat_v55_c288_k20.onnx | 55 | [398] | 23086 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.2661294168792665 | 5.839995486 | 19.222689044 | both_same_answer | 21.94419374784637 |
| 0021 | unsat_v55_c288_k21.onnx | 55 | [398] | 23086 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.39066995889879763 | 6.386185357 | 19.211698251 | both_same_answer | 16.346753087954557 |
| 0022 | sat_v68_c337_k22.onnx | 68 | [473] | 33585 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.2694840421900153 | 5.825980602 | 19.226218973 | both_same_answer | 21.619018902395915 |
| 0023 | unsat_v68_c337_k23.onnx | 68 | [473] | 33585 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01494395802729 | 6.438961672 | 19.231885242 | abc_only | None |
| 0024 | sat_v73_c501_k24.onnx | 73 | [647] | 49174 | W07 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8844043749850243 | 5.84260583 | 19.209088022 | both_same_answer | 6.60626066000514 |
| 0025 | unsat_v73_c501_k25.onnx | 73 | [647] | 49174 | W07 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01506695896387 | 6.517303931 | 19.230121693 | abc_only | None |
| 0026 | sat_v91_c889_k26.onnx | 91 | [1071] | 100676 | W06 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.9937092498876154 | 5.850219642 | 19.214992638 | both_same_answer | 5.887254891369519 |
| 0027 | unsat_v91_c889_k27.onnx | 91 | [1071] | 100676 | W06 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01528854086064 | 6.754592861 | 19.197513834 | abc_only | None |
| 0028 | sat_v23_c88_k28.onnx | 23 | [134] | 3486 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8145923749543726 | 5.837271279 | 19.247584289 | both_same_answer | 7.165880087358982 |
| 0029 | unsat_v23_c88_k29.onnx | 23 | [134] | 3486 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.8143749588634819 | 6.339334515 | 19.221829058 | both_same_answer | 7.784294502187287 |
| 0030 | sat_v65_c209_k30.onnx | 65 | [339] | 23054 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8699433750007302 | 5.826064559 | 19.207561689 | both_same_answer | 6.6970618162304065 |
| 0031 | unsat_v65_c209_k31.onnx | 65 | [339] | 23054 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01479241601191 | 6.378328462 | 19.256718661 | abc_only | None |
| 0032 | sat_v29_c167_k32.onnx | 29 | [225] | 7202 | W03 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8086946250405163 | 5.850579661 | 19.272986537 | both_same_answer | 7.23459694159199 |
| 0033 | unsat_v29_c167_k33.onnx | 29 | [225] | 7202 | W03 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.1146073339041322 | 6.385923461 | 19.23021713 | both_same_answer | 5.729303286236277 |
| 0034 | sat_v30_c79_k34.onnx | 30 | [139] | 4589 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8173150410875678 | 5.750215583 | 19.191601987 | both_same_answer | 7.035494630501872 |
| 0035 | unsat_v30_c79_k35.onnx | 30 | [139] | 4589 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.2346561250742525 | 6.346576128 | 19.204439996 | both_same_answer | 5.140359326867888 |
| 0036 | sat_v87_c231_k36.onnx | 87 | [405] | 36452 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.877855374943465 | 5.825800683 | 19.229761091 | both_same_answer | 6.636401449811922 |
| 0037 | unsat_v87_c231_k37.onnx | 87 | [405] | 36452 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01178508298472 | 6.411009903 | 19.223318837 | abc_only | None |
| 0038 | sat_v41_c90_k38.onnx | 41 | [172] | 7570 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8089112921152264 | 5.755883566 | 19.245713349 | both_same_answer | 7.115593047228837 |
| 0039 | unsat_v41_c90_k39.onnx | 41 | [172] | 7570 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.054581540869549 | 6.393233259 | 19.217010003 | both_same_answer | 6.06234132803851 |
| 0040 | sat_v45_c216_k40.onnx | 45 | [306] | 14690 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8733297500293702 | 5.821850536 | 19.216331456 | both_same_answer | 6.666268423587094 |
| 0041 | unsat_v45_c216_k41.onnx | 45 | [306] | 14690 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.6548837500158697 | 6.398628902 | 19.196604651 | both_same_answer | 3.866512618749588 |
| 0042 | sat_v35_c53_k42.onnx | 35 | [123] | 4676 | W08 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8052877921145409 | 5.74693628 | 19.206327609 | both_same_answer | 7.136499939865695 |
| 0043 | unsat_v35_c53_k43.onnx | 35 | [123] | 4676 | W08 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.0526067081373185 | 6.539870077 | 19.21839627 | both_same_answer | 6.213023369927866 |
| 0044 | sat_v17_c167_k44.onnx | 17 | [201] | 4022 | W09 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8236637499649078 | 5.833699474 | 19.205836543 | both_same_answer | 7.082622580207694 |
| 0045 | unsat_v17_c168_k45.onnx | 17 | [202] | 4042 | W09 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.1660140841268003 | 6.369220235 | 19.178162378 | both_same_answer | 5.462387051499258 |
| 0046 | sat_v88_c453_k46.onnx | 88 | [629] | 57241 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.9259407920762897 | 5.832728652 | 19.221920209 | both_same_answer | 6.299245806981828 |
| 0047 | unsat_v88_c453_k47.onnx | 88 | [629] | 57241 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01445154100657 | 6.483453838 | 19.242182346 | abc_only | None |
| 0048 | sat_v94_c784_k48.onnx | 94 | [972] | 94286 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.9846662501804531 | 5.838002595 | 19.251829759 | both_same_answer | 5.928915095780026 |
| 0049 | unsat_v94_c784_k49.onnx | 94 | [972] | 94286 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01514924992807 | 6.691452045 | 19.231559415 | abc_only | None |
| 0050 | sat_v38_c256_k50.onnx | 38 | [332] | 13614 | W10 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8079962080810219 | 5.841344206 | 19.208402923 | both_same_answer | 7.229420321010044 |
| 0051 | unsat_v38_c257_k51.onnx | 38 | [333] | 13655 | W10 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.414618375012651 | 6.445925498 | 19.221120858 | both_same_answer | 4.556653307958306 |
| 0052 | sat_v95_c183_k52.onnx | 95 | [373] | 36556 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8687017909251153 | 5.840896517 | 19.267030901 | both_same_answer | 6.723707235344588 |
| 0053 | unsat_v95_c183_k53.onnx | 95 | [373] | 36556 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01489900005981 | 6.394648885 | 19.23426368 | abc_only | None |
| 0054 | sat_v36_c216_k54.onnx | 36 | [288] | 11234 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8166332500986755 | 5.831927045 | 19.214856114 | both_same_answer | 7.14142737182856 |
| 0055 | unsat_v36_c216_k55.onnx | 36 | [288] | 11234 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.1661374168470502 | 6.394546344 | 19.26273695 | both_same_answer | 5.483527285565784 |
| 0056 | sat_v16_c97_k56.onnx | 16 | [129] | 2453 | W11 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8191042090766132 | 5.844415586 | 19.231553632 | both_same_answer | 7.135130696725983 |
| 0057 | unsat_v16_c98_k57.onnx | 16 | [130] | 2472 | W11 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.1146048340015113 | 6.258073407 | 19.220393258 | both_same_answer | 5.614611758440942 |
| 0058 | sat_v32_c263_k58.onnx | 32 | [327] | 11447 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8171902089379728 | 5.836563193 | 19.239011936 | both_same_answer | 7.1422333860133325 |
| 0059 | unsat_v32_c263_k59.onnx | 32 | [327] | 11447 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.2348195409867913 | 6.394419932 | 19.251664884 | both_same_answer | 5.178424635951239 |
| 0060 | sat_v77_c190_k60.onnx | 77 | [344] | 27522 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8792170418892056 | 5.749566091 | 19.208004933 | both_same_answer | 6.539416113506738 |
| 0061 | unsat_v77_c190_k61.onnx | 77 | [344] | 27522 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.2320986669510603 | 6.372718551 | 19.257894034 | both_same_answer | 5.17224693276381 |
| 0062 | sat_v51_c288_k62.onnx | 51 | [390] | 21062 | W12 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8734200419858098 | 5.832036802 | 19.242145762 | both_same_answer | 6.677241787056166 |
| 0063 | unsat_v51_c288_k63.onnx | 51 | [390] | 21062 | W12 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.00818595802411 | 6.377781442 | 19.222563672 | abc_only | None |
| 0064 | sat_v48_c405_k64.onnx | 48 | [501] | 25553 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8838967920746654 | 5.833226083 | 19.225866132 | both_same_answer | 6.599442531416326 |
| 0065 | unsat_v48_c405_k65.onnx | 48 | [501] | 25553 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.5943094580434263 | 6.419051869 | 19.214954741 | both_same_answer | 4.026227051853289 |
| 0066 | sat_v54_c179_k66.onnx | 54 | [287] | 16361 | W13 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8754713330417871 | 5.821569824 | 19.214374763 | both_same_answer | 6.649640718415312 |
| 0067 | unsat_v54_c179_k67.onnx | 54 | [287] | 16361 | W13 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.3487206248100847 | 6.371519497 | 19.252454595 | both_same_answer | 4.7241210520504815 |
| 0068 | sat_v67_c223_k68.onnx | 67 | [357] | 24992 | W05 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8756479169242084 | 5.823726878 | 19.224888758 | both_same_answer | 6.650763126869943 |
| 0069 | unsat_v67_c223_k69.onnx | 67 | [357] | 24992 | W05 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01481879106723 | 6.374691767 | 19.192900161 | abc_only | None |
| 0070 | sat_v47_c383_k70.onnx | 47 | [477] | 23852 | W14 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8714975002221763 | 5.815853507 | 19.260676607 | both_same_answer | 6.6734023970433975 |
| 0071 | unsat_v47_c384_k71.onnx | 47 | [478] | 23902 | W14 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01486770785414 | 6.459322257 | 19.250084151 | abc_only | None |
| 0072 | sat_v19_c158_k72.onnx | 19 | [196] | 4314 | W04 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8136694999411702 | 5.841601119 | 19.25165473 | both_same_answer | 7.179329100356298 |
| 0073 | unsat_v19_c158_k73.onnx | 19 | [196] | 4314 | W04 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.1684521248098463 | 6.431663762 | 19.233185587 | both_same_answer | 5.504430712594826 |
| 0074 | sat_v42_c119_k74.onnx | 42 | [203] | 9137 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8239486671518534 | 5.822063105 | 19.212005633 | both_same_answer | 7.066050759114822 |
| 0075 | unsat_v42_c119_k75.onnx | 42 | [203] | 9137 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.2720655829180032 | 6.369523866 | 19.222852962 | both_same_answer | 5.007229148821784 |
| 0076 | sat_v35_c321_k76.onnx | 35 | [391] | 14860 | W08 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8701772089116275 | 5.831311948 | 19.217208633 | both_same_answer | 6.701292435932104 |
| 0077 | unsat_v35_c321_k77.onnx | 35 | [391] | 14860 | W08 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.589340167120099 | 6.415996852 | 19.250076598 | both_same_answer | 4.036893413211756 |
| 0078 | sat_v75_c586_k78.onnx | 75 | [736] | 57410 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.9270576250273734 | 5.838078265 | 19.224343823 | both_same_answer | 6.297427589603847 |
| 0079 | unsat_v75_c586_k79.onnx | 75 | [736] | 57410 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.01436991686933 | 6.531259427 | 19.217601064 | abc_only | None |
| 0080 | sat_v5_c19_k80.onnx | 5 | [29] | 234 | W15 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.7989095838274807 | 5.833721229 | 19.226803909 | both_same_answer | 7.302104452235178 |
| 0081 | unsat_v5_c21_k81.onnx | 5 | [31] | 250 | W15 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.6945963338948786 | 6.201145216 | 19.264324886 | both_same_answer | 8.927696438055907 |
| 0082 | sat_v17_c46_k82.onnx | 17 | [80] | 1602 | W09 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8104707500897348 | 5.835523063 | 19.232998974 | both_same_answer | 7.200164919405043 |
| 0083 | unsat_v17_c46_k83.onnx | 17 | [80] | 1602 | W09 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.7542498749680817 | 6.227464631 | 19.219246045 | both_same_answer | 8.25650071372373 |
| 0084 | sat_v73_c76_k84.onnx | 73 | [222] | 16874 | W07 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8202805831097066 | 5.76788955 | 19.22939035 | both_same_answer | 7.031605610038664 |
| 0085 | unsat_v73_c76_k85.onnx | 73 | [222] | 16874 | W07 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.6433061668649316 | 6.41942542 | 19.259054806 | both_same_answer | 3.906408647055015 |
| 0086 | sat_v51_c282_k86.onnx | 51 | [384] | 20738 | W12 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8765700419899076 | 5.832365012 | 19.257131996 | both_same_answer | 6.653621196955247 |
| 0087 | unsat_v51_c282_k87.onnx | 51 | [384] | 20738 | W12 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.3515045421663672 | 6.3738565 | 19.240888326 | both_same_answer | 4.716119185055164 |
| 0088 | sat_v59_c154_k88.onnx | 59 | [272] | 16866 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8041267078369856 | 5.826012895 | 19.239984613 | both_same_answer | 7.245142883851412 |
| 0089 | unsat_v59_c154_k89.onnx | 59 | [272] | 16866 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.00661216606386 | 6.369156045 | 19.208599772 | abc_only | None |
| 0090 | sat_v39_c172_k90.onnx | 39 | [250] | 10502 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8178515830077231 | 5.835654242 | 19.18769473 | both_same_answer | 7.135346269721524 |
| 0091 | unsat_v39_c172_k91.onnx | 39 | [250] | 10502 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.4662345829419792 | 6.535855373 | 19.243858386 | both_same_answer | 4.457578240915514 |
| 0092 | sat_v54_c406_k92.onnx | 54 | [514] | 29300 | W13 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.9278835000004619 | 5.832315146 | 19.216145953 | both_same_answer | 6.285611443674876 |
| 0093 | unsat_v54_c406_k93.onnx | 54 | [514] | 29300 | W13 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.5343895840924233 | 6.411435426 | 19.244992468 | both_same_answer | 4.178492537012562 |
| 0094 | sat_v83_c233_k94.onnx | 83 | [399] | 34316 | W16 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8650269161444157 | 5.796328813 | 19.210495787 | both_same_answer | 6.700749658560111 |
| 0095 | unsat_v83_c233_k95.onnx | 83 | [399] | 34316 | W16 | source_verified_execution_unbound | unknown (—) | unsat (—) | 100.00921358400956 | 6.407354883 | 19.209289572 | abc_only | None |
| 0096 | sat_v83_c180_k96.onnx | 83 | [346] | 29758 | W16 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8731865000445396 | 5.826431863 | 19.205556927 | both_same_answer | 6.672608729867909 |
| 0097 | unsat_v83_c180_k97.onnx | 83 | [346] | 29758 | W16 | source_verified_execution_unbound | unsat (—) | unsat (—) | 1.9551102500408888 | 6.377190608 | 19.216196287 | both_same_answer | 3.2618061349055014 |
| 0098 | sat_v14_c43_k98.onnx | 14 | [71] | 1209 | W02 | source_verified_execution_unbound | sat (strict) | sat (strict) | 0.8132524171378464 | 5.824352749 | 19.204881231 | both_same_answer | 7.161801952582173 |
| 0099 | unsat_v14_c44_k99.onnx | 14 | [72] | 1226 | W02 | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.7492748340591788 | 6.227786174 | 19.209356649 | both_same_answer | 8.311751430728181 |

## Unmatched published rows

```json
[
  {
    "row": 101,
    "category": "inconsistent_paths",
    "version": "1.0",
    "network": "onnx/test_nano.onnx",
    "property": "vnnlib/test_nano.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 5.79962081,
    "preparation_seconds": 19.273089534,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  }
]
```
