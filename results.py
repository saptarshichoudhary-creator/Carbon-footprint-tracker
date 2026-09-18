import streamlit as st
import pandas as pd
import plotly.express as px

def render_results_screen(emissions_data: dict, sources_data: list):
    """
    emissions_data format:
    {
        'Petrol Car': 23.5,
        'Electricity': 150.0,
        'Bus': 0.0,
        'LPG': 12.0
    }
    sources_data format:  
    [  
        {"Category": "Petrol Car", "Factor Used": "0.235 kg CO2e/km", "Source": "DEFRA 2023"},  
        {"Category": "Electricity", "Factor Used": "0.82 kg CO2e/kWh", "Source": "India GHG Program"}  
    ]  
    """

    st.markdown("---")  
    st.header("📊 Carbon Footprint Results")

    # Calculate Total  
    total_emissions = sum(emissions_data.values())

    # ---------------------------------------------------------  
    # SECTION 1: Metric Card  
    # ---------------------------------------------------------  
    col1, col2 = st.columns([1, 2])

    with col1:  
        st.metric(  
            label="Total CO₂ Equivalent",  
            value=f"{total_emissions:.2f} kg CO2e",  
            help="Total calculated carbon footprint based on provided activity data."  
        )

    # ---------------------------------------------------------  
    # SECTION 2: Category Breakdown Chart  
    # ---------------------------------------------------------  
    st.subheader("Category Breakdown")

    # Check for zero total to prevent empty chart issues  
    if total_emissions == 0:  
        st.info("💡 Enter activity data in the form above to view your emissions breakdown chart.")  
    else:  
        # Prepare dataframe for plotting  
        df_emissions = pd.DataFrame([  
            {"Category": cat, "CO2e (kg)": val, "Percentage": (val / total_emissions) * 100}  
            for cat, val in emissions_data.items()  
            if val > 0  # Hide categories with 0 emissions  
        ])
        
        if not df_emissions.empty:
            # Donut Chart  
            fig = px.pie(  
                df_emissions,   
                values="CO2e (kg)",   
                names="Category",   
                hole=0.4,  
                title="Emissions Distribution (% per category)",  
                color_discrete_sequence=px.colors.qualitative.Set2  
            )  
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 No active emission sources to display.")

    # ---------------------------------------------------------  
    # SECTION 3: Source Citation Footer  
    # ---------------------------------------------------------  
    st.markdown("---")  
    with st.expander("📚 Data Sources & Emission Factors", expanded=True):  
        st.caption("Every calculation in this app is strictly derived from verified public emission factors.")
        
        if sources_data:  
            df_sources = pd.DataFrame(sources_data)  
            # Normalize column key names if mismatch exists
            if "Emission Factor" in df_sources.columns and "Factor Used" not in df_sources.columns:
                df_sources.rename(columns={"Emission Factor": "Factor Used"}, inplace=True)
            st.dataframe(df_sources, use_container_width=True, hide_index=True)  
        else:  
            st.write("Source citations loading...")

# --- QUICK TEST RUNNER ---
if __name__ == "__main__":
    # Test sample data to preview the layout
    sample_emissions = {
        'Petrol Car': 23.5,
        'Electricity': 150.0,
        'Bus': 0.0,
        'Domestic Flight': 85.2
    }
    sample_sources = [  
        {"Category": "Petrol Car", "Factor Used": "0.235 kg CO2e/km", "Source": "DEFRA 2023"},  
        {"Category": "Electricity", "Factor Used": "0.820 kg CO2e/kWh", "Source": "India GHG Program v3.2"},  
        {"Category": "Domestic Flight", "Factor Used": "0.255 kg CO2e/pkm", "Source": "DEFRA 2023"}  
    ]

    render_results_screen(sample_emissions, sample_sources)
