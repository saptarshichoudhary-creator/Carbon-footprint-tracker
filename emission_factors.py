"""
emission_factors.py

Registry of emission factors used by CarbonTrace.

DESIGN PRINCIPLE (do not weaken this):
  get_factor() raises MissingEmissionFactorError if a factor hasn't been
  sourced yet. It never falls back to a guessed or placeholder number.
  If you're tempted to make this "just return something reasonable",
  don't — that's exactly the hardcoding this project is built to avoid.

HOW TO FILL THIS IN (Rohan):
  For each FactorRecord below with value=None, open the actual source
  document (DEFRA conversion factors spreadsheet, or India GHG Program
  factor tables) and fill in:
    - value            (the number itself)
    - unit             (e.g. "kg_co2e_per_km", "kg_co2e_per_kwh")
    - source_name      (e.g. "DEFRA 2024 Conversion Factors")
    - source_url       (direct link to the document/page)
    - publication_year (year the source data was published)
    - last_verified    (date YOU personally checked the source, not just
                         when the AI suggested it — format: "2026-09-18")
    - confidence        ("high" if activity-specific and India-relevant,
                         "medium" if using a global/regional proxy,
                         "low" if it's the best you could find but you're
                         not confident it applies well here)
    - notes            (anything a reviewer should know, e.g. "India-
                         specific factor unavailable, using DEFRA global
                         average as fallback")
"""

from dataclasses import dataclass
from typing import Optional


class MissingEmissionFactorError(Exception):
    """Raised when a factor hasn't been sourced yet. Never caught silently
    to substitute a guess — only caught to show the user a clear message."""
    pass


@dataclass
class FactorRecord:
    activity: str
    value: Optional[float]        # the actual number; None until sourced
    unit: Optional[str]           # e.g. "kg_co2e_per_km"
    source_name: Optional[str]
    source_url: Optional[str]
    publication_year: Optional[int]
    last_verified: Optional[str]  # "YYYY-MM-DD", set when a human checked it
    confidence: Optional[str] = None   # "high" / "medium" / "low"
    notes: Optional[str] = None


# --- Registry -----------------------------------------------------------
# Keys are the internal activity identifiers used by calculator.py and app.py.
# Every entry starts as a TODO. Fill in real values only — never invent one.

REGISTRY: dict[str, FactorRecord] = {
    "commute_petrol_car": FactorRecord(
        activity="Petrol car commute",
        value=None,  # TODO(Rohan): kg CO2e per km, DEFRA or India GHG Program
        unit="kg_co2e_per_km",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "commute_diesel_car": FactorRecord(
        activity="Diesel car commute",
        value=None,  # TODO(Rohan)
        unit="kg_co2e_per_km",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "commute_two_wheeler": FactorRecord(
        activity="Two-wheeler commute",
        value=None,  # TODO(Rohan)
        unit="kg_co2e_per_km",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "commute_bus": FactorRecord(
        activity="Bus commute",
        value=None,  # TODO(Rohan)
        unit="kg_co2e_per_km",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "electricity_grid": FactorRecord(
        activity="Grid electricity",
        value=None,  # TODO(Rohan): kg CO2e per kWh, India grid emission factor
        unit="kg_co2e_per_kwh",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "meal_meat": FactorRecord(
        activity="Meat-based meal",
        value=None,  # TODO(Rohan)
        unit="kg_co2e_per_meal",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "meal_vegetarian": FactorRecord(
        activity="Vegetarian meal",
        value=None,  # TODO(Rohan)
        unit="kg_co2e_per_meal",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
    "flight_domestic_short_haul": FactorRecord(
        activity="Domestic short-haul flight",
        value=None,  # TODO(Rohan): kg CO2e per km, economy class
        unit="kg_co2e_per_km",
        source_name=None,
        source_url=None,
        publication_year=None,
        last_verified=None,
    ),
}


def get_factor(activity_key: str) -> FactorRecord:
    """Return the FactorRecord for an activity, or raise if it hasn't been
    sourced yet. This is the single guardrail against invented numbers —
    do not modify it to return a default."""
    record = REGISTRY.get(activity_key)
    if record is None:
        raise MissingEmissionFactorError(
            f"No factor registered for activity '{activity_key}'."
        )
    if record.value is None:
        raise MissingEmissionFactorError(
            f"Factor for '{activity_key}' ({record.activity}) has not been "
            f"sourced yet. Fill in emission_factors.py before using this "
            f"activity in the calculator."
        )
    return record
