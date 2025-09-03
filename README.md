# Forecasting CO2 – Streamlit App

A simple web app to forecast yearly CO2 concentration/emissions using a pre-trained model. Built with Streamlit, Pandas, Statsmodels, and Altair.

## Features
- Forecast CO2 up to 30 years ahead.
- Interactive chart combining historical data and forecast.
- Download forecast results as an Excel file (.xlsx).
- Dataset preview tab.

## Prerequisites
- Python 3.9+ (recommended)
- Up-to-date pip
- OS: Windows, macOS, or Linux

## Installation (Local)
1) Clone this repository and cd into the project folder.
2) (Optional, recommended) Create and activate a virtual environment.
3) Install dependencies from `requirements.txt`.

Windows PowerShell example:

```powershell
# 1) (optional) create a virtual env
python -m venv .venv
.\.venv\Scripts\Activate

# 2) install dependencies
pip install -r requirements.txt
```

## Run the App
Start Streamlit with:

```powershell
streamlit run prediksi_co2.py
```

Then open the shown URL (typically http://localhost:8501) in your browser.

If port 8501 is in use:
```powershell
streamlit run prediksi_co2.py --server.port 8502
```

## Project Structure
- `prediksi_co2.py` — Main Streamlit app code.
- `prediksi_co2.sav` — Trained model file (loaded at runtime).
- `CO2 dataset.xlsx` — Historical CO2 dataset (loaded on startup).
- `prediksi_co2.ipynb` — Notebook for experimentation/training (optional).
- `requirements.txt` — Python dependencies.
- `LICENSE` — Project license.

## How It Works
- The app loads the model from `prediksi_co2.sav` and the dataset from `CO2 dataset.xlsx`.
- The `Year` column is parsed to datetime and set as a yearly time index.
- You choose the number of years to forecast (1–30); the app calls `model.forecast(n)` to produce future CO2 values.
- Forecast results are combined with historical data and visualized with Altair.
- A download button provides the forecast as an Excel file.

## Expected Dataset Format
- File: `CO2 dataset.xlsx`
- Minimum columns:
  - `Year` — a parseable year format (e.g., `1990` or `1990-01-01`).
  - `CO2` — annual CO2 concentration/emission value.

If you replace the dataset, keep the same file and column names or adjust the code in `prediksi_co2.py` accordingly.

## Troubleshooting
- ModuleNotFoundError or import errors: ensure all packages are installed via `pip install -r requirements.txt`.
- Excel read/engine errors: ensure `openpyxl` and `xlsxwriter` are installed (already listed in requirements).
- File not found: place `CO2 dataset.xlsx` and `prediksi_co2.sav` in the same directory as `prediksi_co2.py` when running the app.
- Port conflicts: run with `--server.port` as shown above.

## License
See the `LICENSE` file in this repo.

## Data Source and Credits
- Dataset: Air Quality Forecasting CO2 Emissions — Kaggle
  https://www.kaggle.com/datasets/rohitshirudkar/air-quality-forecasting-co2-emissions

## Contributing
Pull requests and issues are welcome. For major changes, please open an issue first to discuss what you’d like to change.
