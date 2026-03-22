# Get Policy Done

> An AI copilot for autonomous policy analysis and impact assessment — from policy question to evidence-based analysis to publication-ready report.

**Inspired by [Get Physics Done](https://github.com/psi-oss/get-physics-done)** — the open-source AI copilot that autonomously conducts physics research. Get Policy Done adapts GPD's architecture for public policy analysis, regulatory impact assessment, and evidence-based policy research.

## Vision

Policy analysis requires synthesizing evidence from multiple disciplines, maintaining consistent assumptions across scenarios, and presenting findings that withstand scrutiny from diverse stakeholders. The quality bar is high — a flawed cost-benefit analysis can misallocate billions in public resources.

Get Policy Done wraps LLM capabilities in a verification-first framework that:
- **Locks analytical assumptions** across scenarios (discount rates, population projections, elasticity estimates, baseline definitions)
- **Verifies internal consistency** — assumptions don't contradict each other, sensitivity analysis covers key parameters
- **Decomposes analysis** into phases: problem definition → evidence gathering → baseline construction → impact estimation → sensitivity analysis → stakeholder perspectives → report writing
- **Runs multi-stakeholder review** — referee panel examines analysis from industry, public interest, environmental, and fiscal perspectives

## Architecture

Adapted from GPD's three-layer design:

### Layer 1 — Core Library (Python)
State management, phase lifecycle, git operations, convention locks, verification kernel.

### Layer 2 — MCP Servers
- `gpd-state` — Project state queries
- `gpd-conventions` — Analytical assumption lock management
- `gpd-protocols` — Policy methodology protocols (CBA, CEA, RIA, SROI, etc.)
- `gpd-patterns` — Cross-project learned patterns
- `gpd-verification` — Analytical consistency and evidence quality checks
- `gpd-errors` — Known LLM policy analysis failure modes

### Layer 3 — Agents & Commands
- `gpd-planner` — Analysis framework and task decomposition
- `gpd-executor` — Evidence gathering and analysis execution
- `gpd-verifier` — Consistency and methodological rigor verification
- `gpd-researcher` — Literature, data, and precedent research
- `gpd-modeler` — Economic modeling and scenario analysis
- `gpd-paper-writer` — Report and brief generation
- `gpd-referee` — Multi-stakeholder perspective review

## Convention Lock Fields

1. Discount rate (social, private, source justification)
2. Time horizon
3. Population and demographic projections (source and vintage)
4. Baseline scenario definition
5. Geographic scope
6. Currency and price year (constant vs nominal dollars)
7. Elasticity estimates (source and confidence)
8. Valuation methodology (VSL, QALY, WTP, etc.)
9. Distributional weighting approach
10. Regulatory framework and jurisdiction

## Verification Framework

1. **Assumption consistency** — no contradictions across model components
2. **Baseline validity** — baseline represents plausible no-action scenario
3. **Evidence quality** — sources graded, systematic vs cherry-picked
4. **Sensitivity coverage** — key parameters varied, break-even analysis included
5. **Double counting** — no benefit or cost counted twice
6. **Standing** — whose costs and benefits are included is explicit and consistent
7. **Counterfactual clarity** — impacts measured relative to correct baseline
8. **Distributional analysis** — who bears costs, who receives benefits
9. **Uncertainty quantification** — ranges, confidence intervals, scenario spreads
10. **Precedent comparison** — results compared with similar published analyses
11. **Methodological compliance** — follows OMB Circular A-4, EU Better Regulation, or relevant standard
12. **Stakeholder coverage** — all major affected groups considered

## Status

**Early development** — Scaffolding and initial design. Seeking domain expert contributors!

## Relationship to GPD

Assumption locking and sensitivity analysis verification adapt from GPD's convention locks and limiting case checks. Policy analysis adds multi-stakeholder perspective review and evidence quality assessment.

We plan to showcase this in the [GPD Discussion Show & Tell](https://github.com/psi-oss/get-physics-done/discussions) once operational.

## Contributing

We're looking for contributors with:
- Policy analysis or regulatory impact assessment experience
- Economics or public policy research background
- Cost-benefit analysis or program evaluation experience
- Familiarity with GPD's architecture

See the [Issues](../../issues) for specific tasks.

## License

MIT
