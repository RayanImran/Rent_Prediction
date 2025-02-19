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

##### Environment Variables (Recommended)
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

## Running the Application
### Navigate to the Project Directory
Open your terminal and go to the directory where you have saved `streamlit_app.py`.

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

