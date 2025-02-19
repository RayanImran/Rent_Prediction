# Real Estate Analytics App with Prefect and RentCast API

## Introduction
This project provides a real estate analytics tool that fetches property value and rental estimates using the RentCast API. It utilizes Prefect for workflow orchestration to manage data extraction, processing, and visualization, and Streamlit to create an interactive user interface.

## Prerequisites
Before running this application, ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)

You will also need:

- **RentCast API Key**: Obtain a valid API key from the [RentCast Developer Portal](https://www.rentcast.io/developers) to access their API services.

## Setup
### Install Python Packages
Navigate to the project directory in your terminal and run:

```bash
pip install prefect requests pandas matplotlib streamlit
```
# Real Estate Analytics App with Prefect and RentCast API

## Introduction
This project provides a real estate analytics tool that fetches property value and rental estimates using the RentCast API. It utilizes Prefect for workflow orchestration to manage data extraction, processing, and visualization, and Streamlit to create an interactive user interface.

## Prerequisites
Before running this application, ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)

You will also need:

- **RentCast API Key**: Obtain a valid API key from the [RentCast Developer Portal](https://www.rentcast.io/developers) to access their API services.

## Setup
### Install Python Packages
Navigate to the project directory in your terminal and run:

```bash
pip install prefect requests pandas matplotlib streamlit
```

### Set up your RentCast API Key
For security and best practices, it's recommended to set your API key as an environment variable. You can do this in a few ways, depending on your operating system:

#### Option 1: Environment Variables (Recommended)
##### Linux/macOS:
```bash
export RENTCAST_API_KEY="YOUR_RENTCAST_API_KEY_HERE"
```
Add this line to your shell configuration file (e.g., `.bashrc`, `.zshrc`) for persistence.

##### Windows:
```bash
setx RENTCAST_API_KEY "YOUR_RENTCAST_API_KEY_HERE"
```
(You may need to restart your command prompt or system for the variable to be recognized).

#### Option 2: Directly in `rent_etl.py` (Less Secure - For quick testing only)
Open `rent_etl.py` and replace the placeholder in the `API_KEY` variable with your actual API key:

```python
API_KEY = "YOUR_RENTCAST_API_KEY_HERE"  # Replace with your API key
```
**Warning:** Hardcoding API keys directly in the script is generally discouraged for production environments. Environment variables are a more secure approach.

## Running the Application
### Navigate to the Project Directory
Open your terminal and go to the directory where you have saved `rent_etl.py` and `streamlit_app.py`.

### Run the Streamlit App
Execute the Streamlit application using the following command:

```bash
streamlit run streamlit_app.py
```
Streamlit will automatically open the application in your web browser (usually at http://localhost:8501).

## Usage
### Select Analysis Type
In the sidebar of the Streamlit app, choose between **"Property Value Estimate"** and **"Rental Estimates"** using the radio buttons.

### Enter Property Address
Enter the address of the property you want to analyze in the **"Property Address"** text input field in the sidebar. A default address is pre-filled.

### Run Analysis
Click the **"Run Analysis"** button in the sidebar. The app will fetch the data from the RentCast API and display the results, including data tables and charts, directly in the Streamlit interface.

## Project Files
- **`rent_etl.py`**: Contains the Prefect flows and tasks for extracting, transforming, and loading real estate data from the RentCast API.
- **`streamlit_app.py`**: The Streamlit application that provides the user interface for interacting with the real estate analytics tool and displaying the results.
- **`prefect_flows.py` (assumed)**: This file (or functionality within `rent_etl.py`) is expected to contain the definitions of the Prefect flows used by the Streamlit app. **Note:** This file was mentioned in `streamlit_app.py` but was not explicitly provided in the code snippets. Ensure your Prefect flow definitions are accessible to `streamlit_app.py`.

