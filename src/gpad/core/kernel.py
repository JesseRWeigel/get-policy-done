"""Content-addressed verification kernel.

Runs predicates over evidence registries and produces SHA-256 verdicts.
Adapted from GPD's kernel.py for policy analysis verification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .constants import VERIFICATION_CHECKS, SEVERITY_CRITICAL, SEVERITY_MAJOR, SEVERITY_MINOR, SEVERITY_NOTE


class Severity(str, Enum):
    CRITICAL = SEVERITY_CRITICAL
    MAJOR = SEVERITY_MAJOR
    MINOR = SEVERITY_MINOR
    NOTE = SEVERITY_NOTE


@dataclass
class CheckResult:
    """Result of a single verification check."""

    check_id: str
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    severity: Severity
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    """Complete verification verdict with content-addressed hashes."""

    registry_hash: str
    predicates_hash: str
    verdict_hash: str
    overall: str  # PASS | FAIL | PARTIAL
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    results: dict[str, CheckResult] = field(default_factory=dict)
    summary: str = ""

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.CRITICAL
        ]

    @property
    def major_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.MAJOR
        ]

    @property
    def all_failures(self) -> list[CheckResult]:
        return [r for r in self.results.values() if r.status == "FAIL"]

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "FAIL")

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_hash": self.registry_hash,
            "predicates_hash": self.predicates_hash,
            "verdict_hash": self.verdict_hash,
            "overall": self.overall,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "results": {
                k: {
                    "check_id": v.check_id,
                    "name": v.name,
                    "status": v.status,
                    "severity": v.severity.value,
                    "message": v.message,
                    "evidence": v.evidence,
                    "suggestions": v.suggestions,
                }
                for k, v in self.results.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# -- Predicate Type ---------------------------------------------------------

# A predicate takes an evidence registry and returns a CheckResult
Predicate = Callable[[dict[str, Any]], CheckResult]


# -- Built-in Policy Analysis Predicates ------------------------------------

def check_assumption_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check internal consistency of all stated assumptions."""
    assumptions = evidence.get("assumptions", [])
    contradictions = evidence.get("assumption_contradictions", [])

    if not assumptions:
        return CheckResult(
            check_id="assumption_consistency",
            name="Assumption Consistency",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No assumptions documented for verification.",
        )

    if contradictions:
        return CheckResult(
            check_id="assumption_consistency",
            name="Assumption Consistency",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(contradictions)} contradictory assumption(s).",
            evidence={"contradictions": contradictions},
            suggestions=[f"Resolve contradiction: {c}" for c in contradictions[:5]],
        )

    return CheckResult(
        check_id="assumption_consistency",
        name="Assumption Consistency",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {len(assumptions)} assumptions internally consistent.",
    )


def check_baseline_validity(evidence: dict[str, Any]) -> CheckResult:
    """Check counterfactual/baseline is well-defined and defensible."""
    baseline_defined = evidence.get("baseline_defined", False)
    baseline_issues = evidence.get("baseline_issues", [])

    if not baseline_defined:
        return CheckResult(
            check_id="baseline_validity",
            name="Baseline Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="No baseline/counterfactual scenario defined.",
            suggestions=["Define explicit counterfactual: what happens without this policy?"],
        )

    if baseline_issues:
        return CheckResult(
            check_id="baseline_validity",
            name="Baseline Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Baseline has {len(baseline_issues)} issue(s).",
            evidence={"issues": baseline_issues},
        )

    return CheckResult(
        check_id="baseline_validity",
        name="Baseline Validity",
        status="PASS",
        severity=Severity.CRITICAL,
        message="Baseline scenario well-defined and defensible.",
    )


def check_evidence_quality(evidence: dict[str, Any]) -> CheckResult:
    """Check sources are peer-reviewed, current, and relevant."""
    sources = evidence.get("sources", [])
    quality_issues = evidence.get("source_quality_issues", [])

    if not sources:
        return CheckResult(
            check_id="evidence_quality",
            name="Evidence Quality",
            status="WARN",
            severity=Severity.MAJOR,
            message="No sources documented.",
            suggestions=["Document all evidence sources with quality assessment."],
        )

    if quality_issues:
        return CheckResult(
            check_id="evidence_quality",
            name="Evidence Quality",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(quality_issues)} source quality issue(s) found.",
            evidence={"issues": quality_issues},
        )

    return CheckResult(
        check_id="evidence_quality",
        name="Evidence Quality",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(sources)} sources assessed as adequate quality.",
    )


def check_sensitivity_coverage(evidence: dict[str, Any]) -> CheckResult:
    """Check key parameters tested across plausible ranges."""
    parameters_tested = evidence.get("sensitivity_parameters", [])
    parameters_required = evidence.get("key_parameters", [])

    if not parameters_required:
        return CheckResult(
            check_id="sensitivity_coverage",
            name="Sensitivity Coverage",
            status="WARN",
            severity=Severity.MAJOR,
            message="No key parameters identified for sensitivity analysis.",
            suggestions=["Identify parameters with significant uncertainty."],
        )

    untested = [p for p in parameters_required if p not in parameters_tested]
    if untested:
        return CheckResult(
            check_id="sensitivity_coverage",
            name="Sensitivity Coverage",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(untested)} key parameter(s) not sensitivity-tested.",
            evidence={"untested": untested},
        )

    return CheckResult(
        check_id="sensitivity_coverage",
        name="Sensitivity Coverage",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(parameters_required)} key parameters sensitivity-tested.",
    )


def check_double_counting(evidence: dict[str, Any]) -> CheckResult:
    """Check no benefits or costs counted more than once."""
    double_counts = evidence.get("double_counting_instances", [])

    if double_counts:
        return CheckResult(
            check_id="double_counting",
            name="Double Counting",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Found {len(double_counts)} instance(s) of double counting.",
            evidence={"instances": double_counts},
            suggestions=["Ensure each cost/benefit is counted exactly once."],
        )

    return CheckResult(
        check_id="double_counting",
        name="Double Counting",
        status="PASS",
        severity=Severity.CRITICAL,
        message="No double counting detected.",
    )


def check_standing(evidence: dict[str, Any]) -> CheckResult:
    """Check whose costs/benefits are included is explicit."""
    standing_defined = evidence.get("standing_defined", False)
    standing_issues = evidence.get("standing_issues", [])

    if not standing_defined:
        return CheckResult(
            check_id="standing",
            name="Standing",
            status="FAIL",
            severity=Severity.MAJOR,
            message="Standing not explicitly defined — unclear whose welfare counts.",
            suggestions=[
                "Define geographic and demographic scope of affected parties.",
                "Justify any exclusions from standing.",
            ],
        )

    if standing_issues:
        return CheckResult(
            check_id="standing",
            name="Standing",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Standing has {len(standing_issues)} issue(s).",
            evidence={"issues": standing_issues},
        )

    return CheckResult(
        check_id="standing",
        name="Standing",
        status="PASS",
        severity=Severity.MAJOR,
        message="Standing clearly defined with justification.",
    )


def check_counterfactual_clarity(evidence: dict[str, Any]) -> CheckResult:
    """Check clear definition of what happens without the policy."""
    counterfactual_clear = evidence.get("counterfactual_specified", False)
    counterfactual_issues = evidence.get("counterfactual_issues", [])

    if not counterfactual_clear:
        return CheckResult(
            check_id="counterfactual_clarity",
            name="Counterfactual Clarity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="Counterfactual scenario not clearly specified.",
            suggestions=["Describe explicitly what the world looks like without this policy."],
        )

    if counterfactual_issues:
        return CheckResult(
            check_id="counterfactual_clarity",
            name="Counterfactual Clarity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Counterfactual has {len(counterfactual_issues)} issue(s).",
            evidence={"issues": counterfactual_issues},
        )

    return CheckResult(
        check_id="counterfactual_clarity",
        name="Counterfactual Clarity",
        status="PASS",
        severity=Severity.CRITICAL,
        message="Counterfactual scenario clearly specified.",
    )


def check_distributional_analysis(evidence: dict[str, Any]) -> CheckResult:
    """Check effects disaggregated by income, race, geography, etc."""
    dimensions_analyzed = evidence.get("distributional_dimensions", [])
    distributional_issues = evidence.get("distributional_issues", [])

    if not dimensions_analyzed:
        return CheckResult(
            check_id="distributional_analysis",
            name="Distributional Analysis",
            status="FAIL",
            severity=Severity.MAJOR,
            message="No distributional analysis conducted.",
            suggestions=[
                "Disaggregate effects by income quintile.",
                "Analyze differential impacts by race/ethnicity.",
                "Consider geographic variation in effects.",
            ],
        )

    if distributional_issues:
        return CheckResult(
            check_id="distributional_analysis",
            name="Distributional Analysis",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Distributional analysis has {len(distributional_issues)} issue(s).",
            evidence={"issues": distributional_issues},
        )

    return CheckResult(
        check_id="distributional_analysis",
        name="Distributional Analysis",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Effects analyzed across {len(dimensions_analyzed)} dimension(s).",
    )


def check_uncertainty_quantification(evidence: dict[str, Any]) -> CheckResult:
    """Check confidence intervals, Monte Carlo, scenario analysis."""
    uncertainty_methods = evidence.get("uncertainty_methods", [])
    uncertainty_issues = evidence.get("uncertainty_issues", [])

    if not uncertainty_methods:
        return CheckResult(
            check_id="uncertainty_quantification",
            name="Uncertainty Quantification",
            status="FAIL",
            severity=Severity.MAJOR,
            message="No uncertainty quantification performed.",
            suggestions=[
                "Provide confidence intervals for key estimates.",
                "Conduct Monte Carlo simulation for aggregate results.",
                "Present best-case / worst-case / most-likely scenarios.",
            ],
        )

    if uncertainty_issues:
        return CheckResult(
            check_id="uncertainty_quantification",
            name="Uncertainty Quantification",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Uncertainty analysis has {len(uncertainty_issues)} issue(s).",
            evidence={"issues": uncertainty_issues},
        )

    return CheckResult(
        check_id="uncertainty_quantification",
        name="Uncertainty Quantification",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Uncertainty quantified via {len(uncertainty_methods)} method(s).",
    )


def check_precedent_comparison(evidence: dict[str, Any]) -> CheckResult:
    """Check results compared with similar past policies."""
    precedents_checked = evidence.get("precedents_checked", [])
    precedent_mismatches = evidence.get("precedent_mismatches", [])

    if not precedents_checked:
        return CheckResult(
            check_id="precedent_comparison",
            name="Precedent Comparison",
            status="WARN",
            severity=Severity.MINOR,
            message="No precedent policies compared against.",
            suggestions=["Compare with similar policies in other jurisdictions or time periods."],
        )

    if precedent_mismatches:
        return CheckResult(
            check_id="precedent_comparison",
            name="Precedent Comparison",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"Results diverge from {len(precedent_mismatches)} precedent(s) without explanation.",
            evidence={"mismatches": precedent_mismatches},
        )

    return CheckResult(
        check_id="precedent_comparison",
        name="Precedent Comparison",
        status="PASS",
        severity=Severity.MINOR,
        message=f"Consistent with {len(precedents_checked)} precedent(s).",
    )


def check_methodological_compliance(evidence: dict[str, Any]) -> CheckResult:
    """Check compliance with OMB Circular A-4 / applicable standards."""
    framework = evidence.get("regulatory_framework", "")
    compliance_issues = evidence.get("compliance_issues", [])

    if not framework:
        return CheckResult(
            check_id="methodological_compliance",
            name="Methodological Compliance",
            status="WARN",
            severity=Severity.MAJOR,
            message="No regulatory framework specified for compliance check.",
            suggestions=["Specify applicable methodology standard (OMB A-4, EU BIA, etc.)."],
        )

    if compliance_issues:
        return CheckResult(
            check_id="methodological_compliance",
            name="Methodological Compliance",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Non-compliant with {framework}: {len(compliance_issues)} issue(s).",
            evidence={"issues": compliance_issues, "framework": framework},
        )

    return CheckResult(
        check_id="methodological_compliance",
        name="Methodological Compliance",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Compliant with {framework}.",
    )


def check_stakeholder_coverage(evidence: dict[str, Any]) -> CheckResult:
    """Check all materially affected parties identified and analyzed."""
    stakeholders_identified = evidence.get("stakeholders_identified", [])
    stakeholders_analyzed = evidence.get("stakeholders_analyzed", [])
    missing_stakeholders = evidence.get("missing_stakeholders", [])

    if not stakeholders_identified:
        return CheckResult(
            check_id="stakeholder_coverage",
            name="Stakeholder Coverage",
            status="FAIL",
            severity=Severity.MAJOR,
            message="No stakeholders identified.",
            suggestions=["Map all materially affected parties."],
        )

    unanalyzed = [s for s in stakeholders_identified if s not in stakeholders_analyzed]
    if unanalyzed or missing_stakeholders:
        all_gaps = unanalyzed + missing_stakeholders
        return CheckResult(
            check_id="stakeholder_coverage",
            name="Stakeholder Coverage",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(all_gaps)} stakeholder group(s) not adequately analyzed.",
            evidence={"gaps": all_gaps},
        )

    return CheckResult(
        check_id="stakeholder_coverage",
        name="Stakeholder Coverage",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(stakeholders_identified)} stakeholder group(s) analyzed.",
    )


# -- Default predicate registry ---------------------------------------------

DEFAULT_PREDICATES: dict[str, Predicate] = {
    "assumption_consistency": check_assumption_consistency,
    "baseline_validity": check_baseline_validity,
    "evidence_quality": check_evidence_quality,
    "sensitivity_coverage": check_sensitivity_coverage,
    "double_counting": check_double_counting,
    "standing": check_standing,
    "counterfactual_clarity": check_counterfactual_clarity,
    "distributional_analysis": check_distributional_analysis,
    "uncertainty_quantification": check_uncertainty_quantification,
    "precedent_comparison": check_precedent_comparison,
    "methodological_compliance": check_methodological_compliance,
    "stakeholder_coverage": check_stakeholder_coverage,
}


# -- Verification Kernel ----------------------------------------------------

class VerificationKernel:
    """Content-addressed verification kernel.

    Runs predicates over evidence registries and produces
    SHA-256 verdicts for reproducibility and tamper-evidence.
    """

    def __init__(self, predicates: dict[str, Predicate] | None = None):
        self.predicates = predicates or dict(DEFAULT_PREDICATES)

    def _hash(self, data: str) -> str:
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def verify(self, evidence: dict[str, Any]) -> Verdict:
        """Run all predicates against evidence and produce a verdict."""
        # Hash inputs
        evidence_json = json.dumps(evidence, sort_keys=True, default=str)
        registry_hash = self._hash(evidence_json)

        predicate_names = json.dumps(sorted(self.predicates.keys()))
        predicates_hash = self._hash(predicate_names)

        # Run predicates
        results: dict[str, CheckResult] = {}
        for check_id, predicate in self.predicates.items():
            try:
                result = predicate(evidence)
                results[check_id] = result
            except Exception as e:
                results[check_id] = CheckResult(
                    check_id=check_id,
                    name=check_id.replace("_", " ").title(),
                    status="FAIL",
                    severity=Severity.MAJOR,
                    message=f"Predicate raised exception: {e}",
                )

        # Determine overall status
        has_critical_fail = any(
            r.status == "FAIL" and r.severity == Severity.CRITICAL
            for r in results.values()
        )
        has_major_fail = any(
            r.status == "FAIL" and r.severity == Severity.MAJOR
            for r in results.values()
        )

        if has_critical_fail:
            overall = "FAIL"
        elif has_major_fail:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        # Hash the results for tamper-evidence
        results_json = json.dumps(
            {k: v.message for k, v in results.items()},
            sort_keys=True,
        )
        verdict_hash = self._hash(
            f"{registry_hash}:{predicates_hash}:{results_json}"
        )

        # Build summary
        pass_count = sum(1 for r in results.values() if r.status == "PASS")
        fail_count = sum(1 for r in results.values() if r.status == "FAIL")
        skip_count = sum(1 for r in results.values() if r.status == "SKIP")
        warn_count = sum(1 for r in results.values() if r.status == "WARN")

        summary = (
            f"{overall}: {pass_count} passed, {fail_count} failed, "
            f"{warn_count} warnings, {skip_count} skipped "
            f"out of {len(results)} checks."
        )

        return Verdict(
            registry_hash=registry_hash,
            predicates_hash=predicates_hash,
            verdict_hash=verdict_hash,
            overall=overall,
            results=results,
            summary=summary,
        )
