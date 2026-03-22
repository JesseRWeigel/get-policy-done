---
name: plan-phase
description: Plan the current phase — research, plan, and validate before execution
---

<process>

## Plan Phase

### Overview
Before execution, create validated plans for the current phase:
1. Research the policy domain (gpad-researcher)
2. Create plans (gpad-planner)
3. Validate plans (gpad-verifier in plan-check mode)
4. Iterate until plans pass validation

### Step 1: Domain Research
Spawn gpad-researcher with:
- Phase goal from ROADMAP.md
- Current convention locks
- Analysis mode parameters

Collect RESEARCH.md output.

### Step 2: Plan Creation
Spawn gpad-planner with:
- Phase goal
- RESEARCH.md findings
- Convention locks
- Task sizing constraints (max 8-10 tasks per plan)

Collect PLAN-XX-YY.md files.

### Step 3: Plan Validation
For each plan, validate with:
- The PLAN.md
- Phase goal
- RESEARCH.md
- LLM error catalog

### Step 4: Revision Loop
If validation returns REVISE:
1. Feed revision recommendations back to gpad-planner
2. Planner revises the plan
3. Re-check
4. Maximum 3 iterations

If validation returns REJECT after 3 iterations:
- Present issues to user
- Ask for guidance on approach

### Step 5: Commit and Present
Once plans are validated:
1. Commit all PLAN.md files
2. Display plan summary to user
3. Show wave structure (what runs in parallel)
4. If autonomy is 'supervised': wait for user approval
5. If autonomy is 'balanced' or 'yolo': proceed to execute-phase

</process>
