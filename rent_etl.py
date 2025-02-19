import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from prefect import flow, task

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------
API_KEY = ""  
BASE_URL = "https://api.rentcast.io/v1"
# ---------------------------------------------------------------
# Prefect Tasks
# ---------------------------------------------------------------


@task
def fetch_rent_estimate(address: str, property_type: str = "Single Family", bedrooms: float = 4, bathrooms: float = 2, square_footage: float = 1600) -> dict:
    """Fetches rent estimate from RentCast API."""
    endpoint = f"{BASE_URL}/avm/rent/long-term"
    headers = {
        "accept": "application/json",
        "X-Api-Key": API_KEY  # Include API Key here
    }
    params = {
        "address": address,
        "propertyType": property_type,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "squareFootage": square_footage
    }

    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 401:
        raise ValueError("Unauthorized! Check if your API key is correct.")

    response.raise_for_status()
    return response.json()


@task
def extract_rent_data_for_plot(rent_data: dict) -> dict:
    """Extracts rent data for plotting."""
    extracted_data = {
        "estimated_rent": rent_data.get("rent"),
        "rent_range_low": rent_data.get("rentRangeLow"),
        "rent_range_high": rent_data.get("rentRangeHigh")
    }
    return extracted_data


@task
def visualize_rent_ranges_bar_chart(rent_values: dict, address: str, output_file: str) -> None:
    """Creates and saves rent range bar chart."""
    labels = ['Estimated Rent', 'Rent Range Low', 'Rent Range High']
    values = [rent_values.get("estimated_rent"), rent_values.get(
        "rent_range_low"), rent_values.get("rent_range_high")]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['skyblue', 'lightcoral', 'lightgreen'])
    plt.ylabel('Rent Amount ($)')
    plt.title(f'Rent Estimate and Range for Address: {address}')
    plt.ylim(min(values) * 0.9, max(values) * 1.1)

    for i, v in enumerate(values):
        plt.text(i, v + 10, str(v), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


@task
def save_rent_data_to_csv(rent_data: dict, filename: str) -> None:
    """Saves rent data to CSV file."""
    df = pd.DataFrame([rent_data])
    df.to_csv(filename, index=False)


@flow(name="rentcast_rent_estimate_flow")
def rent_estimate_pipeline(address_input: str, output_filename_base: str = "rent_estimate"):
    """Orchestrates the rent estimate flow."""
    rent_data = fetch_rent_estimate(address=address_input)
    plot_data = extract_rent_data_for_plot(rent_data)

    chart_output_file = f"{output_filename_base}_bar_chart.png"
    csv_output_file = f"{output_filename_base}.csv"

    visualize_rent_ranges_bar_chart(
        plot_data, address=address_input, output_file=chart_output_file)
    save_rent_data_to_csv(rent_data=rent_data, filename=csv_output_file)

    return chart_output_file


if __name__ == "__main__":
    property_address = "5500 Grand Lake Drive, San Antonio, TX, 78244"
    chart_path = rent_estimate_pipeline(
        address_input=property_address)
    print(
        f"ETL flow completed. Check for '{chart_path}' and 'rent_estimate.csv' in your directory.")