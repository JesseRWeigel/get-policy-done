---
name: new-project
description: Initialize a new policy analysis project
---

<process>

## Initialize New Policy Analysis Project

### Step 1: Create project structure
Create the `.gpad/` directory and all required subdirectories:
- `.gpad/` — project state and config
- `.gpad/observability/sessions/` — session logs
- `.gpad/traces/` — execution traces
- `knowledge/` — policy knowledge base
- `.scratch/` — temporary working files (gitignored)

### Step 2: Gather project information
Ask the user:
1. **Project name**: What policy are you analyzing?
2. **Policy question**: What specific policy question are you investigating?
3. **Domain**: Which policy area? (environmental, health, labor, trade, tax, financial, education, energy, etc.)
4. **Model profile**: deep-analysis (default), standard, rapid-assessment, review, or brief-writing?
5. **Analysis mode**: explore, balanced (default), exploit, or adaptive?
6. **Regulatory framework**: OMB Circular A-4, EU Better Regulation, UK Green Book, or other?

### Step 3: Create initial ROADMAP.md
Based on the policy question, create a phase breakdown:

```markdown
# [Project Name] — Roadmap

## Phase 1: Policy Landscape Survey
**Goal**: Identify existing regulations, stakeholders, and evidence base for [topic]

## Phase 2: Problem Definition and Scoping
**Goal**: Precisely define the market failure, affected populations, and analytical scope

## Phase 3: Baseline Construction
**Goal**: Establish the counterfactual scenario and gather required data

## Phase 4: Cost-Benefit Analysis
**Goal**: Quantify costs and benefits of policy alternatives

## Phase 5: Distributional and Equity Analysis
**Goal**: Assess who gains and who loses across population subgroups

## Phase 6: Sensitivity and Uncertainty
**Goal**: Test robustness of results to alternative assumptions

## Phase 7: Verification
**Goal**: Independent verification of all analyses

## Phase 8: Report Writing
**Goal**: Write publication-ready policy brief or RIA
```

Adjust phases based on the specific policy question. Some projects need more phases (e.g., microsimulation), some need fewer.

### Step 4: Initialize state
Create STATE.md and state.json with:
- Project name and creation date
- Phase listing from ROADMAP
- Phase 1 set as active
- Analysis mode and autonomy mode

### Step 5: Initialize config
Create `.gpad/config.json` with user's choices.

### Step 6: Initialize git
If not already a git repo, initialize one. Add `.scratch/` to `.gitignore`.
Commit the initial project structure.

### Step 7: Convention prompting
Ask if the user wants to pre-set any conventions:
- Discount rate (3%? 7%? Both?)
- Time horizon
- VSL methodology
- Regulatory framework
- Currency and price year

Lock any conventions the user specifies.

### Step 8: Summary
Display:
- Project structure created
- Phases from roadmap
- Active conventions
- Next step: run `plan-phase` to begin Phase 1

</process>
