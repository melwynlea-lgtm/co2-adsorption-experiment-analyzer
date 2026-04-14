# CO2 Adsorption Experiment Analyzer

## Project summary
This is a functional Streamlit app for analyzing CO2 adsorption experiment data. It helps students and researchers reduce manual spreadsheet work by calculating adsorption capacity, removal efficiency, and producing clean plots and sample comparisons automatically.

## Problem solved
Adsorption experiments often produce raw time-series data that must be processed manually in spreadsheets. That process is repetitive, slow, and prone to calculation errors. This tool standardizes the workflow.

## Features
- Upload CSV or Excel data
- Calculate removal efficiency
- Calculate adsorption capacity (q_t)
- Plot concentration vs time
- Plot adsorption capacity vs time
- Compare final performance across samples
- Export processed results

## Required columns
- sample
- time_min
- C0
- Ct
- volume_L
- mass_g

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Formula used
q_t = ((C0 - Ct) * V) / m
