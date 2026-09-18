"""
calculator.py

Pure calculation logic for CarbonTrace. No Streamlit, no I/O — this makes
it directly testable with pytest, and reusable if the UI ever changes.

calculate_footprint() takes a dict of activity inputs and returns:
  - total: float, total kg CO2e
  - breakdown: list of line items, each with the activity, the quantity
    entered, the factor used (value + full source info), and the
    resulting kg CO2e for that line

If any activity's factor hasn't been sourced yet, this raises
MissingEmissionFactorError (from emission_factors.py) rather than
skipping it silently or substituting a guess. The caller (app.py) is
responsible for catching this and showing the user a clear message.
"""

from dataclasses import dataclass, field
from emission_factors import get_factor, FactorRecord


@dataclass
class LineItem:
    activity_key: str
    activity_label: str
    quantity: float
    unit: str
    factor_value: float
    factor_source_name: str
    factor_source_url: str
    factor_confidence: str | None
    co2e_kg: float


@dataclass
class FootprintResult:
    total_kg_co2e: float
    breakdown: list[LineItem] = field(default_factory=list)


def calculate_footprint(inputs: dict[str, float]) -> FootprintResult:
    """
    inputs: dict mapping activity_key -> quantity entered by the user.
    Only keys with a non-zero, non-None quantity are included in the
    breakdown — we don't manufacture a zero-value line for things the
    user didn't enter.

    Example:
        calculate_footprint({
            "commute_petrol_car": 12.5,
            "electricity_grid": 250,
            "meal_meat": 4,
        })
    """
    line_items: list[LineItem] = []
    total = 0.0

    for activity_key, quantity in inputs.items():
        if quantity is None or quantity == 0:
            continue
        if quantity < 0:
            raise ValueError(
                f"Quantity for '{activity_key}' is negative ({quantity}). "
                f"Negative activity amounts aren't valid — check the input."
            )

        factor: FactorRecord = get_factor(activity_key)  # raises if unsourced
        co2e = quantity * factor.value
        total += co2e

        line_items.append(
            LineItem(
                activity_key=activity_key,
                activity_label=factor.activity,
                quantity=quantity,
                unit=factor.unit or "unknown",
                factor_value=factor.value,
                factor_source_name=factor.source_name or "unknown source",
                factor_source_url=factor.source_url or "",
                factor_confidence=factor.confidence,
                co2e_kg=co2e,
            )
        )

    return FootprintResult(total_kg_co2e=total, breakdown=line_items)
