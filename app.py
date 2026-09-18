"""
app.py

CarbonTrace — Streamlit frontend.

Collects activity inputs, calls calculate_footprint(), and displays the
total, category breakdown chart, and source citations using Zenith's UI component.
"""

import streamlit as st
import pandas as pd

from calculator import calculate_footprint
from emission_factors import MissingEmissionFactorError
from results import render_results_screen

st.set_page_config(page_title="CarbonTrace", page_icon="🌍")

st.title("🌍 CarbonTrace")
st.caption(
    "Every number below is calculated from a real, cited emission factor — "
    "not a generic average."
)

with st.form("footprint_form"):
    st.subheader("Commute")
    commute_mode = st.selectbox(
        "Primary commute mode",
        ["None", "Petrol car", "Diesel car", "Two-wheeler", "Bus"],
    )
    commute_km = st.number_input(
        "Distance per day (km)", min_value=0.0, max_value=2000.0, value=0.0, step=0.5
    )

    st.subheader("Electricity")
    electricity_kwh = st.number_input(
        "Monthly electricity usage (kWh)",
        min_value=0.0,
        max_value=100000.0,
        value=0.0,
        step=1.0,
    )

    st.subheader("Diet (per week)")
    meat_meals = st.number_input(
        "Meat-based meals", min_value=0, max_value=100, value=0, step=1
    )
    veg_meals = st.number_input(
        "Vegetarian meals", min_value=0, max_value=100, value=0, step=1
    )

    st.subheader("Flights")
    flight_km = st.number_input(
        "Domestic short-haul flight distance this month (km)",
        min_value=0.0,
        max_value=20000.0,
        value=0.0,
        step=10.0,
    )

    submitted = st.form_submit_button("Calculate my footprint")

if submitted:
    commute_key_map = {
        "Petrol car": "commute_petrol_car",
        "Diesel car": "commute_diesel_car",
        "Two-wheeler": "commute_two_wheeler",
        "Bus": "commute_bus",
    }

    inputs = {}
    if commute_mode != "None" and commute_km > 0:
        inputs[commute_key_map[commute_mode]] = commute_km
    if electricity_kwh > 0:
        inputs["electricity_grid"] = electricity_kwh
    if meat_meals > 0:
        inputs["meal_meat"] = meat_meals
    if veg_meals > 0:
        inputs["meal_vegetarian"] = veg_meals
    if flight_km > 0:
        inputs["flight_domestic_short_haul"] = flight_km

    if not inputs:
        st.warning("Enter at least one activity before calculating.")
    else:
        try:
            result = calculate_footprint(inputs)
        except MissingEmissionFactorError as e:
            st.error(
                "We don't have a verified emission factor for one of your "
                "inputs yet, so we can't show a number we can't back up.\n\n"
                f"Details: {e}"
            )
        except ValueError as e:
            st.error(f"Check your input: {e}")
        else:
            # Prepare data dictionaries required by Zenith's render_results_screen()
            emissions_data = {
                li.activity_label: li.co2e_kg 
                for li in result.breakdown
            }
            
            sources_data = [
                {
                    "Category": li.activity_label,
                    "Factor Used": f"{li.factor_value} {li.unit}",
                    "Source": li.factor_source_name
                }
                for li in result.breakdown
            ]

            # Render UI
            render_results_screen(emissions_data, sources_data)
