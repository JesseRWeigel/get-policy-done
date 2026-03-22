# Regulatory Impact Analysis Protocols

> Step-by-step methodology guides for conducting regulatory impact analysis.

## Protocol: Full Regulatory Impact Analysis

### When to Use
Major federal regulations expected to have annual economic impact > $200M or significant qualitative effects.

### Steps
1. **Statement of Need**
   a. Identify the market failure, externality, or information asymmetry
   b. Document the statutory authority for regulation
   c. Explain why the market cannot self-correct
   d. Quantify the magnitude of the problem (baseline harm)

2. **Regulatory Alternatives**
   a. Define at least 3 regulatory approaches:
      - Performance standard
      - Design/technology standard
      - Market-based instrument (cap-and-trade, tax, subsidy)
      - Information disclosure / labeling
      - Voluntary program
   b. Include "no action" as explicit alternative
   c. For each alternative, specify: stringency level, phase-in timeline, covered entities

3. **Affected Entities Analysis**
   a. Identify all regulated entities (firms, sectors, size distribution)
   b. Identify beneficiary populations
   c. Identify indirectly affected parties
   d. Small entity analysis (RFA/SBREFA if applicable)
   e. Tribal consultation requirements (E.O. 13175)

4. **Cost Estimation**
   a. **Compliance costs**: engineering cost analysis, survey data, or analogy
   b. **Administrative burden**: FTE estimates, IT systems, reporting requirements
   c. **Paperwork costs**: PRA analysis (hours, respondents, frequency)
   d. **Government costs**: inspection, enforcement, monitoring, adjudication
   e. **Indirect costs**: price increases, reduced output, innovation effects
   f. **Transition costs**: one-time vs. recurring, phase-in effects

5. **Benefit Estimation**
   a. **Health benefits**: mortality (VSL), morbidity (QALY/COI), avoided illness
   b. **Environmental benefits**: ecosystem services, recreation, non-use values
   c. **Safety benefits**: injury reduction, property damage avoided
   d. **Economic benefits**: productivity gains, reduced uncertainty
   e. **Non-quantified benefits**: list and describe qualitatively

6. **Net Benefit Comparison**
   a. Discount at locked rate (OMB 2023: 2% central)
   b. Present NPV for each alternative
   c. Calculate annualized net benefits
   d. Rank alternatives by net benefits
   e. Explain if recommended option is not highest NPV

7. **Distributional Analysis**
   a. Income distribution (quintiles)
   b. Racial/ethnic distribution
   c. Geographic distribution (urban/rural, regions, states)
   d. Age distribution
   e. Small vs. large entity burden
   f. Environmental justice communities (E.O. 14096)

8. **Uncertainty and Sensitivity**
   a. One-way sensitivity on each key parameter
   b. Multi-way scenario analysis (optimistic/pessimistic/central)
   c. Break-even analysis for non-monetized benefits
   d. Monte Carlo simulation if model supports it
   e. Identify switchover points (where ranking changes)

### Common LLM Pitfalls
- Baseline drift (E003) between cost and benefit sections
- Partial equilibrium bias (E006) for large interventions
- Jurisdiction confusion (E008) when borrowing parameters
- Ignoring implementation costs (E014) especially IT systems

---

## Protocol: Initial Regulatory Flexibility Analysis (IRFA)

### When to Use
Any proposed rule that may have significant impact on a substantial number of small entities.

### Steps
1. **Define "small entity"** for this industry (SBA size standards)
2. **Estimate number of small entities affected** and share of regulated universe
3. **Estimate per-entity compliance cost** for small vs. large entities
4. **Calculate cost as percentage of revenue** for small entities
5. **Identify significant alternatives** that minimize small entity burden:
   a. Tiered standards
   b. Extended compliance timelines
   c. Performance standards (vs. design standards)
   d. Simplified reporting requirements
   e. Exemptions (full or partial)
6. **Assess each alternative's** impact on benefits
7. **Document SBREFA panel results** if applicable

### Common LLM Pitfalls
- Using average firm costs instead of small-firm-specific costs
- Not accounting for fixed costs that disproportionately burden small firms
- Ignoring that small firms may exit the market rather than comply

---

## Protocol: Unfunded Mandates Analysis (UMRA)

### When to Use
Federal rules imposing enforceable duties on state/local/tribal governments or private sector exceeding $100M+ annually.

### Steps
1. **Identify the mandate** — what must regulated parties do?
2. **Estimate aggregate costs** to state/local/tribal governments
3. **Estimate aggregate costs** to private sector
4. **Determine if thresholds are exceeded** (currently ~$183M for governments, ~$183M for private sector, adjusted for inflation)
5. **Identify least costly alternative** that achieves the objective
6. **Describe extent of federal funding** available to offset mandate costs
7. **Assess impact on small governments** (population < 50,000)

### Common LLM Pitfalls
- Missing indirect mandate costs (e.g., monitoring requirements that require new staff)
- Not adjusting UMRA thresholds for inflation
- Confusing state expenditure requirements with state revenue losses
