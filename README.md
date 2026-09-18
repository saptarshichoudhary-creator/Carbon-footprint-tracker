# CarbonTrace

A carbon footprint calculator that traces every emission figure to a real,
cited source (India GHG Program / DEFRA) instead of using generic averages.

## Design principles

1. **No invented numbers.** `get_factor()` in `emission_factors.py` raises
   `MissingEmissionFactorError` instead of returning a guess if a factor
   hasn't been sourced yet. Never weaken this to return a default.
2. **Calculation logic is pure and isolated.** `calculator.py` has no UI
   dependencies, so it can be tested directly with pytest.
3. **Every result shows its source.** The UI displays which factor, value,
   and source document was used for each line of the breakdown.
4. **Confidence is shown, not hidden.** Factors can be tagged `high`,
   `medium`, or `low` confidence — being upfront about data quality is
   part of the MRV framing, not a weakness to hide.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
pytest
```

## Current status

- [x] Form skeleton (`app.py`)
- [x] Factor registry structure (`emission_factors.py`) — values are TODO
- [x] Calculation logic (`calculator.py`)
- [x] Test suite scaffolded with fake fixture factors (`tests/test_calculator.py`)
- [ ] Real emission factors sourced and filled in (Rohan)
- [ ] Re-run test suite against real factors once filled in
- [ ] Manual hand-check of at least one real end-to-end scenario

## Next step

Fill in every `TODO` in `emission_factors.py` with a real, cited value from
DEFRA or the India GHG Program. Each entry needs: `value`, `unit`,
`source_name`, `source_url`, `publication_year`, `last_verified` (the date
a human — not an AI — checked the source), and `confidence`.
