# Program Evaluation Protocols

> Step-by-step methodology guides for causal inference in policy and program evaluation.

## Protocol: Randomized Controlled Trials (RCTs) in Policy

### When to Use
Evaluating the causal effect of a policy or program when random assignment is feasible and ethical.

### Steps
1. **Define the estimand** — intention-to-treat (ITT: effect of assignment) or local average treatment effect (LATE/complier average causal effect: effect on those who comply with assignment)
2. **Determine the randomization unit** — individual, household, classroom, village, or cluster; cluster randomization requires adjusting sample size for the design effect (1 + (m−1)ρ, where m = cluster size, ρ = intracluster correlation)
3. **Conduct a power analysis** — minimum detectable effect size, significance level (α = 0.05), power (1−β = 0.80), expected attrition rate; register the trial and analysis plan (AEA RCT Registry, EGAP)
4. **Randomize and verify balance** — use stratified or block randomization on key covariates; report baseline balance tables (normalized differences < 0.25 SD)
5. **Estimate the ITT effect** — regress outcome on treatment assignment (OLS with robust SEs); control for stratification variables; for cluster RCTs, use cluster-robust SEs or hierarchical models
6. **Handle non-compliance** — if take-up is imperfect, estimate the LATE using assignment as an instrument for treatment receipt (2SLS/IV); report the first-stage F-statistic (>10) and compliance rate
7. **Assess attrition** — test for differential attrition (compare attrition rates across arms); if differential, apply Lee bounds or inverse probability weighting
8. **Report per CONSORT guidelines** — flow diagram, pre-specified outcomes, all subgroup analyses (whether significant or not), multiple testing corrections

### Common LLM Pitfalls
- Reporting per-protocol effects as if they were ITT effects (per-protocol introduces selection bias)
- Ignoring clustering in the standard errors when randomization was at the cluster level
- Not pre-registering the analysis plan (allows p-hacking and specification searching)
- Claiming causality from a mechanically underpowered trial (null result ≠ no effect; check the MDE)

---

## Protocol: Difference-in-Differences (DiD)

### When to Use
Estimating causal effects when treatment is assigned at the group level at a specific time, using a comparison group to control for common trends.

### Steps
1. **Identify the setup** — treatment group (exposed to the policy) and control group (not exposed), with data before and after the policy change
2. **State the parallel trends assumption** — in the absence of treatment, the treated and control groups would have followed the same trend; this is the core identifying assumption and CANNOT be tested directly
3. **Provide supporting evidence for parallel trends** — plot pre-treatment trends for both groups; run a formal pre-trend test (event study with leads); if pre-trends diverge, DiD is not credible
4. **Estimate the basic DiD** — Y_it = α + β₁ Treat_i + β₂ Post_t + β₃ (Treat_i × Post_t) + ε_it; β₃ is the DiD estimate (ATT under parallel trends)
5. **For staggered treatment timing**: do NOT use two-way fixed effects (TWFE) naively — it is biased when treatment effects are heterogeneous over time. Use Callaway-Sant'Anna, Sun-Abraham, or Borusyak-Jaravel-Spiess estimators
6. **Cluster standard errors** — at the level of treatment assignment (typically state or group); with few clusters (<30–50), use wild cluster bootstrap
7. **Run an event study specification** — estimate dynamic treatment effects (leads and lags) to visualize pre-trends and the evolution of the treatment effect over time
8. **Sensitivity analyses** — vary the control group, add covariates, test for anticipation effects (pre-treatment responses), placebo tests (apply the design to periods with no treatment)

### Common LLM Pitfalls
- Claiming parallel trends are "confirmed" because pre-treatment trends look similar (you can provide evidence, but you cannot prove the counterfactual)
- Using TWFE with staggered adoption without acknowledging the heterogeneity bias (this is a major methodological issue identified by Goodman-Bacon, de Chaisemartin-D'Haultfoeuille, and others)
- Clustering SEs at the individual level when treatment is at the state level (under-states uncertainty)
- Ignoring anticipation effects (if agents respond before the policy takes effect, the "pre" period is contaminated)

---

## Protocol: Regression Discontinuity Design (RDD)

### When to Use
Estimating causal effects when treatment is assigned based on a score crossing a known threshold (e.g., test scores, poverty indices, age cutoffs).

### Steps
1. **Identify the running variable and cutoff** — the variable (score, index, age) that determines assignment, and the threshold at which treatment status changes
2. **Determine the type** — sharp RDD (everyone above the cutoff is treated, everyone below is not) or fuzzy RDD (the cutoff creates a jump in the probability of treatment, but compliance is imperfect)
3. **Visualize the discontinuity** — plot the outcome against the running variable with a clear break at the cutoff; use local polynomial regression (rdplot in Stata/R)
4. **Estimate the treatment effect** — local linear regression on both sides of the cutoff with a bandwidth selected by data-driven methods (Imbens-Kalyanaraman, Calonico-Cattaneo-Titiunik/CCT optimal bandwidth)
5. **For fuzzy RDD**: use the cutoff as an instrument for treatment receipt; estimate via 2SLS; the estimate is a LATE for compliers near the cutoff
6. **Test for manipulation of the running variable** — apply the McCrary density test or Cattaneo-Jansson-Ma test; a discontinuity in the density at the cutoff suggests manipulation (invalidates the design)
7. **Placebo and robustness tests** — test for discontinuities at placebo cutoffs, vary the bandwidth (half and double CCT bandwidth), test for discontinuities in pre-treatment covariates at the cutoff (should be smooth)
8. **Report bandwidth, kernel, and polynomial order** — local linear (polynomial order 1) with triangular kernel is the standard; higher-order polynomials are discouraged (overfitting, boundary bias)

### Common LLM Pitfalls
- Using high-order global polynomials instead of local linear regression (Gelman and Imbens 2019 show this leads to misleading results)
- Not testing for manipulation of the running variable (if people can sort themselves to one side of the cutoff, the design is invalid)
- Extrapolating the RDD estimate away from the cutoff (the estimate is valid only at the cutoff; it is a local estimate)
- Ignoring bandwidth sensitivity (results should be qualitatively similar across a range of bandwidths)

---

## Protocol: Instrumental Variables (IV)

### When to Use
Estimating causal effects when treatment is endogenous (correlated with unobservables) and a valid instrument is available.

### Steps
1. **Identify the instrument Z** — a variable that (a) is correlated with the endogenous treatment D (relevance), (b) affects the outcome Y only through D (exclusion restriction), and (c) is as-if randomly assigned (independence/exogeneity)
2. **Argue the exclusion restriction** — this is the most critical and untestable assumption; provide institutional knowledge, theoretical arguments, and falsification tests
3. **Test for relevance (first stage)** — regress D on Z (and controls); report the first-stage F-statistic. If F < 10, the instrument is weak — use weak-instrument-robust methods (Anderson-Rubin test, conditional likelihood ratio)
4. **Estimate via 2SLS** — first stage: D̂ = π₀ + π₁Z + Xγ + ν; second stage: Y = β₀ + β₁D̂ + Xδ + ε; β₁ is the IV/LATE estimate
5. **Interpret as LATE** — the IV estimate identifies the effect for compliers (those whose treatment status is changed by the instrument), not the average treatment effect for the full population
6. **With multiple instruments**: test for overidentification (Sargan/Hansen J-test; rejection suggests at least one instrument violates the exclusion restriction)
7. **Compare IV to OLS** — if IV > OLS, consider whether compliers have a larger treatment effect (heterogeneity) or whether the instrument is invalid; Hausman test for endogeneity
8. **Report the complier population** — characterize who the compliers are (demographics, baseline values) to clarify external validity

### Common LLM Pitfalls
- Treating the exclusion restriction as testable (it is fundamentally untestable; it requires theoretical justification)
- Using weak instruments without robust inference methods (produces biased estimates that can be worse than OLS)
- Interpreting the IV estimate as an ATE when it is a LATE (the effect is specific to the complier subpopulation)
- Finding a "clever" instrument without providing a credible argument for why it satisfies the exclusion restriction

---

## Protocol: Propensity Score Matching (PSM)

### When to Use
Estimating treatment effects from observational data by matching treated and control units on the propensity to receive treatment.

### Steps
1. **Estimate the propensity score** — P(D=1|X) using logistic regression, probit, or machine learning methods (GBM, random forest); include all pre-treatment confounders
2. **Check common support** — verify that the distributions of propensity scores overlap for treated and control groups; trim or discard units outside the region of common support
3. **Choose the matching method** — nearest neighbor (1:1 or 1:k, with or without replacement), caliper matching (typically caliper = 0.2 SD of the logit propensity score), kernel matching, or optimal matching
4. **Assess covariate balance** — after matching, compute standardized mean differences (SMD) for all covariates; SMD < 0.10 indicates acceptable balance; also check variance ratios and higher moments
5. **Estimate the treatment effect** — ATT = (1/n_T) × Σ(Y_treated − Y_matched_control); use Abadie-Imbens standard errors for matching estimators (not standard OLS SEs)
6. **Sensitivity analysis** — apply Rosenbaum bounds to assess how strong an unmeasured confounder would need to be to explain away the result (Γ parameter)
7. **Consider alternatives** — inverse probability weighting (IPW), doubly robust estimators (augmented IPW/AIPW), or augmented matching that combine propensity scores with outcome modeling for added robustness
8. **Report** — matching method, caliper, number of matched pairs, balance statistics, estimated effect with confidence interval, and sensitivity to unmeasured confounding

### Common LLM Pitfalls
- Claiming PSM eliminates all confounding (it only adjusts for observed confounders; unmeasured confounding is still possible — this is the fundamental limitation vs RCTs)
- Reporting p-values for balance tests instead of standardized mean differences (p-values depend on sample size; SMD is preferred)
- Matching on post-treatment variables (introduces endogeneity; only match on pre-treatment covariates)
- Not assessing sensitivity to unmeasured confounding (without this, the reader cannot evaluate how robust the results are)
