# Flood Modeling and Forecasting Using Satellite and Hydrometeorological Data

**Authors:** Zhamila Anarbekkyzy, Ayazhan Ozbekhan  
**Institution:** Astana IT University

## Overview

This project investigates **next-day Ulba River discharge forecasting** at the Ulba Perevalochnaya gauge (station 11164), East Kazakhstan, using LSTM neural networks, gauge observations and satellite/gridded data. The data cover **2013–2023**. Inputs are 14 consecutive past days; the target is the following day's river discharge (m³/s).

**Important: this repository includes distinct experiments. Their metrics must not be mixed.**

| Experiment | Inputs to combined LSTM C | Matched test dates | RMSE (m³/s) | NSE | Evidence |
|---|---|---:|---:|---:|---|
| New 5-source VS Code run | Discharge, precipitation, snow cover, temperature, soil moisture | 343 | 22.3964 | 0.9614 | Saved executed outputs in VS Code notebook |
| Research manuscript (previously reported) | Five-variable experiment as described in manuscript | 343 | 24.08 | 0.955 | Manuscript, **not independently reproduced by the new run** |

The new 5-source notebook's numerical results are **different** from those previously reported in the manuscript. Matching the number of test dates does not establish identical experimental samples or replication of the manuscript's metrics.

## Data sources

1. **Kazhydromet**: gauge discharge — `discharge_m3_s`
2. **GPM IMERG**: precipitation — `precipitation_mm`
3. **MODIS**: snow cover — `snow_cover_mean`
4. **ERA5-Land**: air temperature — `temperature_c`
5. **ESA CCI**: soil moisture — `soil_moisture`

The inputs are combined in **one daily CSV**, not necessarily five separate files. Satellite/gridded extraction is **provisional** (including an unverified 40 km extraction area), not a validated upstream catchment. Data coverage and permissions for redistributing the merged data must be checked before uploading it to GitHub.

## Models and experimental design

- **LSTM A**: river discharge history only.
- **LSTM B**: gridded/satellite features only (2 in the pilot; 4 in the five-source run).
- **LSTM C**: all available predictor features (3 in the pilot; 5 in the new run).
- **Baselines**: one-day persistence and seasonal climatology.

Chronological target-date splits: **train 2013–2019; validate 2020–2021; test 2022–2023**. The new B/C models use 1,196 training, 351 validation and **343 test** sequences. Short gaps in snow and soil moisture use past-only forward filling (maximum two days); sequences with remaining missing predictors are excluded.

The gauge-only model A was trained using more training windows than B/C. Model comparison uses the same 343 test dates, **but training sample sizes differ**; this limits direct causal interpretation of improvements.

Framework: PyTorch, hidden size 32, batch size 32, Adam (learning rate 0.001), up to 100 epochs, early-stopping patience 10, lookback 14 days, forecast horizon one day.

## Results of the new five-source run

| Model | RMSE (m³/s) ↓ | NSE ↑ |
|---|---:|---:|
| LSTM A (gauge) | 29.2008 | 0.9344 |
| LSTM B (4 gridded features) | 100.0009 | 0.2303 |
| **LSTM C (all five features)** | **22.3964** | **0.9614** |
| Persistence | 31.9819 | 0.9213 |
| Seasonal climatology | 75.7178 | 0.5587 |

These values are **transcribed from the saved notebook output**. The full-precision CSV exports of the new run should also be published in `results_5sources/` from the same executed run (not substituted with the older 647-date CSV files).

Ablation over seeds 17, 29, 41 yielded mean RMSE 23.7755 with all features, 21.9752 without snow cover and 22.8583 without soil moisture. Therefore, it would be incorrect to claim every additional input consistently improved accuracy.

Paired block sign-flip p-values in this run: LSTM C vs Persistence **0.0979**, vs LSTM A **0.0929**, vs LSTM B **0.0010**. At α = 0.05, the differences relative to Persistence and LSTM A were **not statistically significant** under the reported test. The dates are irregularly spaced after missing-data filtering, a limitation for time-series inference.

See [the five-source experiment methodology](docs/FIVE_SOURCE_EXPERIMENT.md) for further detail.

## Repository contents

- [`Ulba_Flood_Forecasting_(1).ipynb`](Ulba_Flood_Forecasting_(1).ipynb) — original three-input Colab pilot.
- [`Ulba_Flood_Forecasting_VSCode.ipynb`](Ulba_Flood_Forecasting_VSCode.ipynb) — five-source VS Code experiment, with saved training outputs.
- [`src/preprocessing.py`](src/preprocessing.py) — input preparation utilities.
- [`requirements.txt`](requirements.txt) — dependencies for the original pilot.
- [`requirements_5sources.txt`](requirements_5sources.txt) — dependencies for the five-source run.
- [`results/`](results/) — original pilot's figures and tables (**not** the five-source results).
- `results_5sources/` — intended location for five-source result CSVs after the actual exports are uploaded.

**Do not use CSVs from the 647-date pilot as five-source results.** If old pilot exports were accidentally uploaded under `docs/`, relocate them to an explicitly labeled pilot-results location.

## Reproducing the five-source run locally

1. Install Python and the dependencies: `python -m pip install -r requirements_5sources.txt` (install into the *same* Python/Jupyter kernel being used).
2. Put the authorized five-source daily CSV in the working directory or `data/`. It must contain all five predictor columns listed above, plus `date`.
3. Open `Ulba_Flood_Forecasting_VSCode.ipynb` in VS Code using a Python/Jupyter kernel and run cells in order. The notebook can clone the public repository using Git if the local repository is not already present.
4. The final cells save `results_5sources/model_comparison.csv`, `test_predictions.csv`, `ablation_results.csv`, `statistical_tests.csv`, and `run_config.json` in the working directory. Upload these **actual files** to the GitHub folder `results_5sources/`.

Depending on system libraries, PyTorch versions and hardware, exact numerical reproducibility may require additional environment details and checksums. The raw merged CSV is not included here; consult the dataset owners/terms before redistribution.

## Research status and limitations

This repository contains the initial pilot and a separate provisional five-source extension. The satellite extraction area remains unverified; snow/soil measurements contain missing observations; trained models did not use identical training-window coverage; and new outputs do not independently reproduce the historical manuscript values. These limitations need to be retained in any paper or presentation.

## License

Code is made available under the included [MIT License](LICENSE). This does **not** automatically grant permission to redistribute third-party datasets.
