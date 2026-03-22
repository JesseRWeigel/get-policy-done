# Cost-Benefit Analysis Protocols

> Step-by-step methodology guides for conducting policy cost-benefit analysis.

## Protocol: Standard Federal CBA (OMB A-4)

### When to Use
Federal regulatory analysis for economically significant rules (>$200M annual impact).

### Steps
1. **Define the policy problem** — what market failure or systemic issue motivates action?
2. **Establish the baseline** — what happens without this regulation? Lock as convention.
3. **Identify regulatory alternatives** — at least 3 options plus no-action
4. **Identify affected populations** — who has standing? Lock geographic scope.
5. **Enumerate cost categories**:
   a. Direct compliance costs (capital, operating, maintenance)
   b. Administrative costs (government implementation, monitoring)
   c. Indirect costs (behavioral responses, market adjustments)
   d. Opportunity costs
6. **Enumerate benefit categories**:
   a. Direct benefits (health, safety, environmental)
   b. Indirect benefits (productivity, innovation, co-benefits)
   c. Avoided costs
7. **Monetize where possible**:
   a. Use locked VSL for mortality risk reduction
   b. Use locked QALY values for morbidity
   c. Use WTP/WTA for non-market goods
   d. Document non-monetized benefits qualitatively
8. **Discount to present value** — use locked discount rate (OMB: 2% central, sensitivity at 1.3% and 2.7%)
9. **Calculate net benefits** — NPV, BCR, annualized values for each alternative
10. **Conduct sensitivity analysis** — one-way, scenario, break-even, Monte Carlo
11. **Assess distributional effects** — by income, race, geography, small entities
12. **Compare alternatives** — rank by net benefits, note non-quantified factors

### Common LLM Pitfalls
- Double counting (E001) — especially health benefits that overlap
- Transfer payment confusion (E002) — taxes/fees are not social costs
- False precision (E004) — reporting 10 significant figures
- Ignoring implementation costs (E014)

---

## Protocol: Quick Regulatory Assessment

### When to Use
Non-significant rules, preliminary analysis, or rapid policy screening.

### Steps
1. **State the policy question** in one sentence
2. **Identify the top 3-5 cost categories** — order of magnitude estimates only
3. **Identify the top 3-5 benefit categories** — order of magnitude estimates only
4. **Qualitative comparison** — is it plausible that benefits exceed costs?
5. **Identify showstoppers** — any single cost or equity concern that dominates?
6. **Recommend next steps** — full CBA needed? Which alternatives merit analysis?

### Common LLM Pitfalls
- Omitting major cost categories because data is hard to find
- Anchoring on benefits without reality-checking magnitudes

---

## Protocol: Ex-Post Policy Evaluation

### When to Use
Evaluating an already-implemented policy's actual effects vs. predicted effects.

### Steps
1. **Retrieve the original analysis** — what was predicted?
2. **Gather outcome data** — what actually happened?
3. **Construct counterfactual** — what would have happened without the policy?
   a. Difference-in-differences
   b. Synthetic control
   c. Regression discontinuity
   d. Pre/post comparison (weakest)
4. **Compare predicted vs. actual**:
   a. Were costs higher or lower than predicted?
   b. Were benefits higher or lower?
   c. Were there unintended consequences?
5. **Identify systematic prediction errors** — which assumptions were wrong?
6. **Extract lessons** — what should future analyses do differently?

### Common LLM Pitfalls
- Survivorship bias (E007) — only looking at metrics that improved
- Confusing correlation with causation in outcome data
- Not accounting for other policy changes during the evaluation period

---

## Protocol: Break-Even Analysis

### When to Use
When key benefits are hard to monetize but the policy has clear costs.

### Steps
1. **Estimate total costs** with reasonable precision
2. **Identify the primary non-monetized benefit** (e.g., lives saved, species preserved)
3. **Calculate the break-even value** — what would the benefit need to be worth per unit for NPV >= 0?
4. **Assess plausibility** — is the break-even value within reasonable range?
5. **Compare with benchmarks** — VSL, revealed preference studies, international comparisons
6. **Present decision framework** — "the policy is net beneficial if you believe X is worth at least $Y"

### Common LLM Pitfalls
- Using break-even analysis to avoid hard valuation questions (should be supplement, not substitute)
- Not testing break-even under different discount rates
