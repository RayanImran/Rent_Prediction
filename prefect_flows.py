# prefect_flows.py
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from urllib.parse import quote
from prefect import flow, task

# ---------------------------------------------------------------
# RentCast API Configuration
# ---------------------------------------------------------------
BASE_URL = "https://api.rentcast.io/v1"
API_KEY = ""

# ---------------------------------------------------------------
# 1. Property Value Estimate Flow (using /avm/value)
# ---------------------------------------------------------------


@task
def fetch_property_value_estimate(address: str, property_type="Single Family", bedrooms=3, bathrooms=2, square_footage=1500) -> dict:
    """
    Fetches property value estimate from RentCast API for a given address,
    using /avm/value endpoint.
    """
    endpoint = f"{BASE_URL}/avm/value"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}
    params = {
        "address": address,  # No manual encoding needed, requests handles it
        "propertyType": property_type,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "squareFootage": square_footage,
        "compCount": 5  # Include compCount as per API documentation
    }

    print(f"Fetching value estimate for '{address}'...")
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 400:
        print(f"Bad request error! Response: {response.text}")
        raise ValueError(
            f"Bad request! Check if the address '{address}' is correctly formatted.")

    response.raise_for_status()
    return response.json()


@task
def process_value_estimate_data(data: dict) -> pd.DataFrame:
    """
    Converts the property value estimate JSON response into a Pandas DataFrame.
    """
    return pd.json_normalize([data]) if data else pd.DataFrame()


@task
def visualize_value_estimate(df: pd.DataFrame, address: str) -> bytes:
    """
    Creates a bar chart comparing 'price', 'priceRangeLow', and 'priceRangeHigh'.
    Returns a PNG image in bytes.
    """
    if df.empty or 'price' not in df.columns:  # Use 'price' as per actual API response
        return b""

    values = [df['price'][0], df.get('priceRangeLow', pd.Series([None]))[
        0], df.get('priceRangeHigh', pd.Series([None]))[0]]
    labels = ['Est. Value', 'Low Range', 'High Range']

    plt.figure(figsize=(6, 5))
    plt.bar(labels, values, color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title(f"Property Value Estimate for: {address}")
    plt.ylabel("Value (USD)")

    for i, val in enumerate(values):
        if val is not None:
            # Formatted with commas
            plt.text(i, val + 1000, f"${val:,.0f}", ha='center', va='bottom')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()


@flow(name="property_value_estimate_flow")
def property_value_estimate_flow(address: str):
    """
    Fetches, processes, and visualizes a property's value estimate from RentCast.
    """
    data = fetch_property_value_estimate(address)
    df = process_value_estimate_data(data)
    chart_bytes = visualize_value_estimate(df, address)
    return df, chart_bytes


# ---------------------------------------------------------------
# 2. Rental Estimates Flow (using /avm/rent/long-term)
# ---------------------------------------------------------------
@task
def fetch_rent_estimates(address: str, property_type="Single Family", bedrooms=3, bathrooms=2, square_footage=1500) -> dict:
    """
    Fetches rent estimates from RentCast API for a given address.
    """
    endpoint = f"{BASE_URL}/avm/rent/long-term"
    headers = {"accept": "application/json", "X-Api-Key": API_KEY}
    params = {
        "address": address,
        "propertyType": property_type,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "squareFootage": square_footage
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


@task
def process_rent_data(rent_data: dict) -> pd.DataFrame:
    """
    Converts rent estimate JSON response into a Pandas DataFrame.
    """
    return pd.json_normalize([rent_data]) if rent_data else pd.DataFrame()


@task
def visualize_rent_trends(df: pd.DataFrame, address: str) -> bytes:
    """
    Creates a bar chart for 'rent', 'rentRangeLow', and 'rentRangeHigh'.
    Returns a PNG image in bytes.
    """
    if df.empty or 'rent' not in df.columns:
        return b""

    values = [df['rent'][0], df.get('rentRangeLow', pd.Series([None]))[
        0], df.get('rentRangeHigh', pd.Series([None]))[0]]
    labels = ['Est. Rent', 'Low Range', 'High Range']

    plt.figure(figsize=(6, 5))
    plt.bar(labels, values, color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.title(f"Rent Estimate for: {address}")
    plt.ylabel("Monthly Rent (USD)")

    for i, val in enumerate(values):
        if val is not None:
            # Formatted with commas
            plt.text(i, val + 50, f"${val:,.0f}", ha='center', va='bottom')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()


@flow(name="rental_estimates_flow")
def rental_estimates_flow(address: str):
    """
    Fetches, processes, and visualizes a property's rental estimate from RentCast.
    """
    data = fetch_rent_estimates(address)
    df = process_rent_data(data)
    chart_bytes = visualize_rent_trends(df, address)
    return df, chart_bytes
