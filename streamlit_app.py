# streamlit_app.py
import streamlit as st
import pandas as pd
from io import BytesIO

# Import flows
from prefect_flows import (
    property_value_estimate_flow,
    rental_estimates_flow
)


def main():
    st.title("Real Estate Analytics App")

    st.markdown("""
    **This app uses Prefect flows to get:**
    - 🏡 Property Value Estimates from RentCast
    - 📊 Rental Estimates & Trends
    """)

    st.sidebar.header("Input")

    flow_selection = st.sidebar.radio(
        "Select analysis:",
        ["Property Value Estimate", "Rental Estimates"]
    )

    address_input = st.sidebar.text_input(
        "Property Address:", value="5500 Grand Lake Drive, San Antonio, TX, 78244"
    )

    if st.sidebar.button("Run Analysis"):
        st.subheader(f"{flow_selection} for:")
        st.write(f"🏠 **{address_input}**")

        if flow_selection == "Property Value Estimate":
            with st.spinner("Fetching value estimate..."):
                df, chart_bytes = property_value_estimate_flow(address_input)

            if not df.empty:
                st.dataframe(df)
                if 'price' in df.columns and 'price_range_low' in df.columns and 'price_range_high' in df.columns:
                    st.write(f"**Estimated Value:** ${df['price'][0]:,.0f}")
                    st.write(
                        f"**Value Range:** ${df['price_range_low'][0]:,.0f} - ${df['price_range_high'][0]:,.0f}")
                else:
                    st.warning("Value data missing.")
            else:
                st.warning(
                    "No value data returned. Try another address.")

            if chart_bytes:
                st.image(chart_bytes, caption="Property Value Estimate Chart")
            else:
                st.info("No value chart available.")

        else:  # "Rental Estimates"
            with st.spinner("Fetching rental estimates..."):
                df, chart_bytes = rental_estimates_flow(address_input)

            if not df.empty:
                st.dataframe(df)
            else:
                st.warning(
                    "No rental data returned. Try another address.")

            if chart_bytes:
                st.image(chart_bytes, caption="Rent Estimate Chart")
            else:
                st.info("No rent chart available.")


if __name__ == "__main__":
    main()