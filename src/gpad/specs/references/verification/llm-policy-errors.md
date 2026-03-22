# Known LLM Policy Analysis Failure Modes

> This catalog documents systematic failure patterns of LLMs in policy analysis and impact assessment.
> The verifier and plan-checker cross-reference against these patterns.

## Critical Errors (High Frequency)

### E001: Double Counting of Benefits
**Pattern**: Counting the same benefit under multiple categories (e.g., counting health improvements as both "reduced mortality" and "increased productivity").
**Example**: A pollution regulation counts avoided deaths (via VSL) AND avoided medical costs AND increased worker productivity — but the VSL already captures WTP for reduced mortality risk including medical and productivity effects.
**Guard**: Map each benefit to a single non-overlapping category. Check for subset relationships between categories.

### E002: Transfer Payment Confusion
**Pattern**: Counting government transfers (taxes, subsidies, fines) as social costs or benefits in efficiency analysis.
**Example**: Treating a carbon tax as a "cost" when it is a transfer from emitters to government — the social cost is the behavioral distortion, not the payment itself.
**Guard**: Distinguish resource costs from transfer payments. Transfers net to zero in social welfare calculations. Only count deadweight loss.

### E003: Baseline Drift
**Pattern**: Using an inconsistent baseline — the "no policy" scenario changes between different parts of the analysis.
**Example**: Assuming current emission trends for cost calculation but different emission trends for benefit calculation.
**Guard**: Define baseline once in a locked document. Reference it explicitly in every comparison.

### E004: False Precision in Estimates
**Pattern**: Presenting point estimates with implausible precision when underlying data is highly uncertain.
**Example**: "The policy will generate $3,847,291,506 in annual benefits" when the underlying parameters have 50%+ uncertainty.
**Guard**: Always present ranges alongside point estimates. Round to appropriate significant figures. Flag when CI width exceeds the point estimate.

### E005: Present Value Calculation Errors
**Pattern**: Incorrect discounting — wrong base year, mixing real and nominal rates, or applying discount rate to already-discounted values.
**Example**: Discounting at 7% nominal when using real (inflation-adjusted) dollar values, effectively double-counting inflation.
**Guard**: Lock currency/price year and discount rate type (real vs. nominal). Verify PV calculations with simple test cases.

## Serious Errors (Medium Frequency)

### E006: Partial Equilibrium Bias
**Pattern**: Ignoring general equilibrium effects when they are material — assuming prices, wages, or quantities in other markets don't change.
**Example**: Estimating job losses from a minimum wage increase using only the labor demand elasticity, ignoring product market price adjustments and consumer surplus changes.
**Guard**: Identify markets where the policy intervention is large relative to the market. Consider whether partial equilibrium is defensible.

### E007: Survivorship Bias in Precedent Selection
**Pattern**: Only citing past policies that "worked" and ignoring failed implementations or unintended consequences.
**Example**: Citing successful cap-and-trade programs while ignoring failed ones or contexts where they underperformed.
**Guard**: Systematically search for failures and null results. Include ex-post evaluations that found smaller effects than predicted.

### E008: Jurisdiction Confusion
**Pattern**: Applying elasticities, costs, or behavioral parameters from one jurisdiction or time period to a very different context.
**Example**: Using European healthcare cost estimates for a US policy analysis without adjusting for structural differences.
**Guard**: Document the source context for every parameter. Explicitly justify external validity.

### E009: Omitted Stakeholder Groups
**Pattern**: Missing materially affected populations, especially those with less political voice.
**Example**: Analyzing a housing regulation's effects on homeowners and developers but ignoring renters, unhoused populations, or adjacent communities.
**Guard**: Use a systematic stakeholder mapping framework. Check against standard categories (consumers, producers, workers, communities, government, environment).

### E010: Confusing Efficiency and Equity
**Pattern**: Treating distributional impacts as efficiency costs/benefits, or vice versa.
**Example**: Counting "reduced inequality" as a benefit in the main CBA rather than in the separate distributional analysis.
**Guard**: Keep efficiency analysis (Kaldor-Hicks) separate from distributional analysis. Note which framework each conclusion is drawn from.

## Moderate Errors (Common but Usually Caught)

### E011: Regulatory Baseline Confusion
**Pattern**: Confusing "current law" baseline with "current policy" baseline when scheduled changes exist.
**Example**: A tax provision set to expire in 2 years — does the baseline assume it expires (current law) or is extended (current policy)?
**Guard**: Explicitly state which baseline convention is used and why. Run analysis under both if they diverge significantly.

### E012: Scope Creep in Standing
**Pattern**: Inconsistently including or excluding affected parties across different parts of the analysis.
**Example**: Including consumer surplus for domestic consumers but also counting effects on foreign producers when they don't have standing.
**Guard**: Lock standing definition. Every cost/benefit line must map to a party with standing.

### E013: Elasticity Misapplication
**Pattern**: Using short-run elasticities for long-run analysis or vice versa, or applying elasticities outside their estimated range.
**Example**: Using a short-run price elasticity of gasoline demand (-0.1) for a 20-year climate policy analysis when the long-run elasticity is -0.6.
**Guard**: Match elasticity time horizon to analysis time horizon. Note the range over which the elasticity was estimated.

### E014: Ignoring Implementation Costs
**Pattern**: Estimating policy benefits but underestimating or omitting administrative, enforcement, and compliance costs.
**Example**: Estimating benefits of a new reporting requirement without counting firms' IT system modifications, training, and ongoing paperwork.
**Guard**: Include explicit implementation cost category for every policy option. Check against similar past implementations.

### E015: Anchoring on Initial Estimates
**Pattern**: Sensitivity analysis varies parameters but doesn't challenge structural assumptions.
**Example**: Testing discount rate sensitivity but never questioning whether the identified benefits actually exist.
**Guard**: Include structural sensitivity — alternative model specifications, not just alternative parameter values.

## How to Use This Catalog

1. **Plan-checker**: Before execution, identify tasks where specific errors are likely. Add explicit guards.
2. **Executor**: Consult relevant entries when performing work of that type. Follow guards.
3. **Verifier**: After execution, cross-reference results against applicable error patterns.
4. **Pattern library**: When a new error pattern is discovered, add it here.
