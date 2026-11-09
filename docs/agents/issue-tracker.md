# Issue tracker: GitHub

Issues and specs live in `complooea/nvvcomp-gurobi`.
Use the `gh` CLI from this directory.

Before creating issues, verify the target with:
`gh repo view --json nameWithOwner`.

## Operations

- Publish a spec or ticket: `gh issue create --title "..." --body "..."`
- Read: `gh issue view <number> --json number,title,body,labels,comments`
- List: `gh issue list --state open`
- Comment: `gh issue comment <number> --body "..."`
- Labels: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`
- Close: post an explanation as a comment, then `gh issue close <number>`.

Use native GitHub sub-issues and issue dependencies when supported.
Otherwise, put `Part of #<parent>` and `Blocked by: #<number>` lines
at the top of the child issue body. A ticket is unblocked when all
its blockers are closed.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding

- Map: one issue labelled `wayfinder:map`, containing Notes,
  Decisions-so-far, and Fog.
- Children: sub-issues labelled `wayfinder:<type>`, where type is
  research, prototype, grilling, or task. If sub-issues are unavailable,
  use a task list in the map and a parent reference in each child.
- Frontier: open children with no open blockers and no assignee,
  selected in map order.
- Claim: assign the ticket to yourself before starting work.
- Resolve: comment with the answer, close the ticket, then append
  a gist and link to the map's Decisions-so-far section.
