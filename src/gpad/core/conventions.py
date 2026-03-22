"""Convention lock management for policy analysis parameter consistency.

Ensures analytical assumptions don't drift across phases of a policy project.
Adapted from GPD's conventions.py for policy analysis.
"""

from __future__ import annotations

from typing import Any

from .constants import CONVENTION_FIELDS
from .state import StateEngine, ConventionLock


# -- Convention Field Descriptions -------------------------------------------

CONVENTION_DESCRIPTIONS: dict[str, str] = {
    "discount_rate": (
        "Social discount rate for cost-benefit analysis. Common choices: "
        "3% (OMB low), 7% (OMB high), Ramsey rule (consumption-based), "
        "declining discount rate (Weitzman). Must be consistent across all "
        "present-value calculations."
    ),
    "time_horizon": (
        "Analysis time horizon over which costs and benefits are projected. "
        "Common choices: 10 years (short-term regulation), 20 years (standard), "
        "30+ years (infrastructure/climate), perpetuity (permanent programs). "
        "Must match the expected policy lifetime and discount rate choice."
    ),
    "population_projections": (
        "Source and vintage of population and demographic projections used "
        "for scaling effects. Common sources: Census Bureau, UN DESA, CBO. "
        "Must specify base year and projection scenario (low/medium/high)."
    ),
    "baseline_scenario": (
        "Definition of the counterfactual — what happens without the policy. "
        "Options: status quo (current law), current policy (including expected "
        "changes), trend extrapolation, or multiple baselines. Must be explicit "
        "about what existing regulations/programs are assumed to continue."
    ),
    "geographic_scope": (
        "Jurisdiction boundaries for the analysis. Federal, state, local, "
        "tribal, international, or multi-jurisdictional. Determines which "
        "populations have standing and which spillover effects to include."
    ),
    "currency_price_year": (
        "Currency and base year for all monetary values. Example: '2024 USD'. "
        "All costs, benefits, and transfers must be expressed in this unit. "
        "Specify the deflator used (CPI-U, GDP deflator, sector-specific)."
    ),
    "elasticity_estimates": (
        "Source and values for behavioral, demand, and supply elasticities "
        "used in the analysis. Must cite specific studies or meta-analyses. "
        "Key elasticities: price elasticity of demand, labor supply elasticity, "
        "compliance cost elasticity."
    ),
    "valuation_methodology": (
        "Methodology for monetizing non-market impacts. Options: "
        "VSL (Value of Statistical Life — EPA, DOT values), "
        "QALY (Quality-Adjusted Life Year), "
        "WTP (Willingness to Pay from stated/revealed preference), "
        "hedonic pricing, travel cost method, benefit transfer. "
        "Must be consistent with the regulatory framework."
    ),
    "distributional_weighting": (
        "How to weight costs and benefits across different populations. "
        "Options: equal weights (standard CBA), income-weighted (declining "
        "marginal utility), Atkinson inequality aversion parameter, "
        "prioritarian weights, or separate distributional table (OMB 2023)."
    ),
    "regulatory_framework": (
        "Applicable legal and methodological authority governing the analysis. "
        "Examples: OMB Circular A-4 (US federal), EU Better Regulation Guidelines, "
        "UK Green Book, OECD Best Practice, state-specific requirements. "
        "Determines required methodology, discount rates, and standing rules."
    ),
}

# -- Convention Validation ---------------------------------------------------

# Common valid values for quick validation
CONVENTION_EXAMPLES: dict[str, list[str]] = {
    "discount_rate": [
        "3% real (OMB A-4 low)",
        "7% real (OMB A-4 high)",
        "2% real (OMB 2023 revised central)",
        "1.7% real (Ramsey rule, current estimates)",
        "Declining: 3% years 1-30, 2% years 31-75, 1% years 76+",
    ],
    "time_horizon": [
        "10 years (short-term regulation)",
        "20 years (standard federal rule)",
        "30 years (infrastructure investment)",
        "50 years (climate/energy policy)",
        "Perpetuity with terminal value",
    ],
    "geographic_scope": [
        "United States — federal",
        "California — state",
        "New York City — municipal",
        "European Union — supranational",
        "Global (climate policy)",
    ],
    "valuation_methodology": [
        "VSL: $11.6M (EPA 2024)",
        "VSL: $13.2M (DOT 2024)",
        "QALY: $150,000 (HHS threshold)",
        "WTP: stated preference (contingent valuation)",
        "WTP: revealed preference (hedonic/travel cost)",
    ],
    "distributional_weighting": [
        "Equal weights (standard unweighted CBA)",
        "Income-weighted (η=1.0, log utility)",
        "Income-weighted (η=1.4, Atkinson)",
        "Separate distributional table (no weighting in primary)",
    ],
    "regulatory_framework": [
        "OMB Circular A-4 (2003)",
        "OMB Circular A-4 (2023 revised)",
        "EU Better Regulation Guidelines (2023)",
        "UK HM Treasury Green Book (2022)",
        "OECD Regulatory Impact Analysis Best Practice",
    ],
}


def get_field_description(field: str) -> str:
    """Get the description for a convention field."""
    return CONVENTION_DESCRIPTIONS.get(field, f"Convention field: {field}")


def get_field_examples(field: str) -> list[str]:
    """Get example values for a convention field."""
    return CONVENTION_EXAMPLES.get(field, [])


def list_all_fields() -> list[dict[str, Any]]:
    """List all convention fields with descriptions and examples."""
    return [
        {
            "field": f,
            "description": get_field_description(f),
            "examples": get_field_examples(f),
        }
        for f in CONVENTION_FIELDS
    ]


def check_conventions(engine: StateEngine) -> dict[str, Any]:
    """Check which conventions are locked and which are missing.

    Returns a report dict with locked, unlocked, and coverage stats.
    """
    state = engine.load()
    locked = {}
    unlocked = []

    for field in CONVENTION_FIELDS:
        if field in state.conventions:
            locked[field] = {
                "value": state.conventions[field].value,
                "locked_by": state.conventions[field].locked_by,
                "rationale": state.conventions[field].rationale,
            }
        else:
            unlocked.append(field)

    return {
        "locked": locked,
        "unlocked": unlocked,
        "coverage": f"{len(locked)}/{len(CONVENTION_FIELDS)}",
        "coverage_pct": round(100 * len(locked) / len(CONVENTION_FIELDS), 1)
        if CONVENTION_FIELDS
        else 100.0,
    }


def diff_conventions(
    engine: StateEngine,
    proposed: dict[str, str],
) -> dict[str, Any]:
    """Compare proposed convention values against current locks.

    Returns conflicts, new fields, and matching fields.
    """
    state = engine.load()
    conflicts = {}
    new_fields = {}
    matching = {}

    for field, proposed_value in proposed.items():
        if field in state.conventions:
            current = state.conventions[field].value
            if current != proposed_value:
                conflicts[field] = {
                    "current": current,
                    "proposed": proposed_value,
                }
            else:
                matching[field] = current
        else:
            new_fields[field] = proposed_value

    return {
        "conflicts": conflicts,
        "new_fields": new_fields,
        "matching": matching,
        "has_conflicts": bool(conflicts),
    }
