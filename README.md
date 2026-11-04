
# Flood Modeling and Forecasting Using Satellite and Hydrometeorological Data

**Authors:** Zhamila Anarbekkyzy, Ayazhan Ozbekhan  
**University:** Astana IT University

## Project Overview

This research investigates next-day river discharge forecasting in the Ulba River Basin, Kazakhstan, using Long Short-Term Memory (LSTM) neural networks.

The objective is to evaluate whether combining satellite and hydrometeorological observations improves forecasting accuracy compared with gauge-only models and simple baselines.

## Study Area

- River: Ulba River, East Kazakhstan
- Gauge: Ulba Perevalochnaya (11164)
- Study period: 2013–2023
- Forecast horizon: 1 day
- Input sequence length: 14 days

## Data Sources

- Kazhydromet: observed river discharge
- GPM IMERG: precipitation
- MODIS MOD10A1: snow cover
- ERA5-Land: air temperature
- ESA CCI: soil moisture

The current experiments use a provisional dataset. Its satellite variables were extracted using a 40 km radius rather than a verified upstream catchment.

The current pilot notebook uses discharge, precipitation, and snow cover. Temperature and soil moisture will be included after the corrected dataset becomes available.

## Forecasting Models

Three LSTM configurations are evaluated:

- **LSTM A:** historical river discharge only
- **LSTM B:** satellite and gridded predictors only
- **LSTM C:** combined river discharge and gridded predictors

Two baselines are also evaluated:

- Persistence
- Seasonal Climatology

## Model Configuration

- Framework: PyTorch
- LSTM hidden units: 32
- Lookback window: 14 days
- Forecast horizon: 1 day
- Optimizer: Adam
- Learning rate: 0.001
- Batch size: 32
- Maximum epochs: 100
- Early stopping patience: 10

## Data Splitting

- Training: 2013–2019
- Validation: 2020–2021
- Testing: 2022–2023

The models use chronological splitting to avoid training on future observations.

## Evaluation Metrics

Forecasting performance is evaluated using:

- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)
- Nash-Sutcliffe Efficiency (NSE)
- Kling-Gupta Efficiency (KGE)
- Percent Bias (PBIAS)

## Preliminary Results

The current pilot comparison uses 647 matching test dates.

| Model | RMSE (m³/s) | NSE | KGE |
|---|---:|---:|---:|
| LSTM A | 29.2326 | 0.9447 | 0.9528 |
| LSTM B | 120.7077 | 0.0568 | 0.0495 |
| LSTM C | 25.8860 | 0.9566 | 0.9176 |
| Persistence | 33.7565 | 0.9262 | 0.9621 |
| Seasonal Climatology | 80.2435 | 0.5832 | 0.6462 |

LSTM C achieved a 23.32% lower RMSE than Persistence in this pilot comparison.

This improvement is descriptive and should not be interpreted as statistically significant without considering the results of the statistical tests.

## Reproducibility

The experiment notebook is available in this repository.

To run the project:

1. Open `Ulba_Flood_Forecasting.ipynb` in Google Colab.
2. Install the libraries listed in `requirements.txt`.
3. Upload the required CSV dataset.
4. Run the notebook cells in order.

The project includes model comparison, an ablation study, and statistical testing.

### Software Environment

The pilot experiments were executed in Google Colab
using the following environment:

- Python 3.13.18
- NumPy 2.4.6
- Pandas 2.2.3
- Scikit-learn 1.6.1
- PyTorch 2.11.0+cpu
- Matplotlib 3.10.0
- SciPy 1.16.3

Dependencies are listed in requirements.txt.


## Limitations

- The current spatial extraction area is provisional.
- The final upstream catchment has not yet been verified.
- The pilot dataset does not include all planned predictors.
- Missing snow-cover observations reduce the common evaluation sample.
- Results may change after the final data collection and model retraining.

## Code Availability

The project code and experimental notebook are available in this GitHub repository.

The source code is released under the MIT License.

## Project Status

Pilot modeling and preliminary evaluation are implemented.

Final catchment verification, complete data integration, and final experimental validation remain in progress.
