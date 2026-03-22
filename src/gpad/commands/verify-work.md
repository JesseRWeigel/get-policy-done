---
name: verify-work
description: Run the 12-check policy analysis verification framework
---

<process>

## Verify Work

### Overview
Run post-hoc verification on completed phase work using the 12-check framework.

### Step 1: Collect Artifacts
Gather all output from the current phase:
- Analysis files (memos, briefs, RIA sections)
- Model files and computation results
- SUMMARY files from executors

### Step 2: Build Evidence Registry
Extract verification evidence from artifacts:
- Assumptions stated and used
- Data sources and their quality
- Sensitivity parameters tested
- Stakeholders identified and analyzed
- Convention usage

### Step 3: Run Verification
Spawn gpad-verifier with:
- All phase artifacts
- Evidence registry
- Convention locks
- LLM error catalog

### Step 4: Process Verdict
Parse the VERIFICATION-REPORT.md:
- If PASS: record in state, proceed
- If PARTIAL: create targeted gap-closure for MAJOR failures
- If FAIL: create gap-closure for CRITICAL failures, block downstream

### Step 5: Route Failures
For each failure, route to the appropriate agent:
- Assumption errors — gpad-executor (targeted re-analysis)
- Convention drift — convention resolution
- Evidence gaps — gpad-researcher + gpad-executor
- Methodology issues — gpad-modeler with specific task
- Stakeholder gaps — gpad-researcher for additional stakeholder survey

### Step 6: Update State
Record verification results in STATE.md:
- Verdict hash (content-addressed)
- Pass/fail counts
- Any unresolved issues

</process>
