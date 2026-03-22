"""Single source of truth for all directory/file names and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# -- Environment Variables --------------------------------------------------

ENV_GPAD_HOME = "GPAD_HOME"
ENV_GPAD_PROJECT = "GPAD_PROJECT"
ENV_GPAD_INSTALL_DIR = "GPAD_INSTALL_DIR"
ENV_GPAD_DEBUG = "GPAD_DEBUG"
ENV_GPAD_AUTONOMY = "GPAD_AUTONOMY"

# -- File Names -------------------------------------------------------------

STATE_MD = "STATE.md"
STATE_JSON = "state.json"
STATE_WRITE_INTENT = ".state-write-intent"
ROADMAP_MD = "ROADMAP.md"
CONFIG_JSON = "config.json"
CONVENTIONS_JSON = "conventions.json"

PLAN_PREFIX = "PLAN"
SUMMARY_PREFIX = "SUMMARY"
RESEARCH_MD = "RESEARCH.md"
RESEARCH_DIGEST_MD = "RESEARCH-DIGEST.md"
CONTINUE_HERE_MD = ".continue-here.md"

# -- Directory Names --------------------------------------------------------

GPAD_DIR = ".gpad"
OBSERVABILITY_DIR = "observability"
SESSIONS_DIR = "sessions"
TRACES_DIR = "traces"
KNOWLEDGE_DIR = "knowledge"
PAPER_DIR = "paper"
SCRATCH_DIR = ".scratch"

# -- Git --------------------------------------------------------------------

CHECKPOINT_TAG_PREFIX = "gpad-checkpoint"
COMMIT_PREFIX = "[gpad]"

# -- Autonomy Modes ---------------------------------------------------------

AUTONOMY_SUPERVISED = "supervised"
AUTONOMY_BALANCED = "balanced"
AUTONOMY_YOLO = "yolo"
VALID_AUTONOMY_MODES = {AUTONOMY_SUPERVISED, AUTONOMY_BALANCED, AUTONOMY_YOLO}

# -- Analysis Modes ---------------------------------------------------------

ANALYSIS_EXPLORE = "explore"
ANALYSIS_BALANCED = "balanced"
ANALYSIS_EXPLOIT = "exploit"
ANALYSIS_ADAPTIVE = "adaptive"
VALID_ANALYSIS_MODES = {ANALYSIS_EXPLORE, ANALYSIS_BALANCED, ANALYSIS_EXPLOIT, ANALYSIS_ADAPTIVE}

# -- Model Tiers ------------------------------------------------------------

TIER_1 = "tier-1"  # Highest capability
TIER_2 = "tier-2"  # Balanced
TIER_3 = "tier-3"  # Fastest

# -- Verification Severity --------------------------------------------------

SEVERITY_CRITICAL = "CRITICAL"  # Blocks all downstream work
SEVERITY_MAJOR = "MAJOR"        # Must resolve before conclusions
SEVERITY_MINOR = "MINOR"        # Must resolve before publication
SEVERITY_NOTE = "NOTE"          # Informational

# -- Convention Lock Fields (Policy Analysis) --------------------------------

CONVENTION_FIELDS = [
    "discount_rate",              # Social discount rate for CBA (e.g., 3%, 7%, Ramsey rule)
    "time_horizon",               # Analysis time horizon (e.g., 10yr, 20yr, 30yr, perpetuity)
    "population_projections",     # Source and vintage of population/demographic projections
    "baseline_scenario",          # Counterfactual/baseline definition (status quo, trend, etc.)
    "geographic_scope",           # Jurisdiction boundaries (federal, state, local, international)
    "currency_price_year",        # Currency and base year for all monetary values (e.g., 2024 USD)
    "elasticity_estimates",       # Source and values for behavioral/demand/supply elasticities
    "valuation_methodology",      # VSL, QALY, WTP, hedonic pricing, travel cost, etc.
    "distributional_weighting",   # Equal weights, income-weighted, Atkinson, prioritarian, etc.
    "regulatory_framework",       # Applicable legal/regulatory authority (e.g., OMB A-4, EU BIA)
]

# -- Verification Checks ---------------------------------------------------

VERIFICATION_CHECKS = [
    "assumption_consistency",     # Internal consistency of all stated assumptions
    "baseline_validity",          # Counterfactual/baseline is well-defined and defensible
    "evidence_quality",           # Sources are peer-reviewed, current, and relevant
    "sensitivity_coverage",       # Key parameters tested across plausible ranges
    "double_counting",            # No benefits or costs counted more than once
    "standing",                   # Whose costs/benefits are included (and excluded) is explicit
    "counterfactual_clarity",     # Clear definition of what happens without the policy
    "distributional_analysis",    # Effects disaggregated by income, race, geography, etc.
    "uncertainty_quantification", # Confidence intervals, Monte Carlo, scenario analysis
    "precedent_comparison",       # Results compared with similar past policies
    "methodological_compliance",  # Compliance with OMB Circular A-4 / applicable standards
    "stakeholder_coverage",       # All materially affected parties identified and analyzed
]


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved paths for a GPAD project."""

    root: Path

    @property
    def gpad_dir(self) -> Path:
        return self.root / GPAD_DIR

    @property
    def state_md(self) -> Path:
        return self.gpad_dir / STATE_MD

    @property
    def state_json(self) -> Path:
        return self.gpad_dir / STATE_JSON

    @property
    def state_write_intent(self) -> Path:
        return self.gpad_dir / STATE_WRITE_INTENT

    @property
    def roadmap_md(self) -> Path:
        return self.gpad_dir / ROADMAP_MD

    @property
    def config_json(self) -> Path:
        return self.gpad_dir / CONFIG_JSON

    @property
    def conventions_json(self) -> Path:
        return self.gpad_dir / CONVENTIONS_JSON

    @property
    def observability_dir(self) -> Path:
        return self.gpad_dir / OBSERVABILITY_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.observability_dir / SESSIONS_DIR

    @property
    def traces_dir(self) -> Path:
        return self.gpad_dir / TRACES_DIR

    @property
    def knowledge_dir(self) -> Path:
        return self.root / KNOWLEDGE_DIR

    @property
    def paper_dir(self) -> Path:
        return self.root / PAPER_DIR

    @property
    def scratch_dir(self) -> Path:
        return self.root / SCRATCH_DIR

    @property
    def continue_here(self) -> Path:
        return self.gpad_dir / CONTINUE_HERE_MD

    def phase_dir(self, phase: str) -> Path:
        return self.root / f"phase-{phase}"

    def plan_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{PLAN_PREFIX}-{plan_number}.md"

    def summary_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{SUMMARY_PREFIX}-{plan_number}.md"

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [
            self.gpad_dir,
            self.observability_dir,
            self.sessions_dir,
            self.traces_dir,
            self.knowledge_dir,
            self.scratch_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) looking for .gpad/ directory."""
    current = start or Path.cwd()
    while current != current.parent:
        if (current / GPAD_DIR).is_dir():
            return current
        current = current.parent
    raise FileNotFoundError(
        f"No {GPAD_DIR}/ directory found. Run 'gpad init' to create a project."
    )


def get_layout(start: Path | None = None) -> ProjectLayout:
    """Get the project layout, finding the root automatically."""
    env_project = os.environ.get(ENV_GPAD_PROJECT)
    if env_project:
        return ProjectLayout(root=Path(env_project))
    return ProjectLayout(root=find_project_root(start))
