# Five-source Ulba LSTM experiment (VS Code)

## What was evaluated

A provisional daily dataset from **2013-01-01 to 2023-12-31** with observations at station **11164** (Ulba Perevalochnaya). One-day-ahead discharge forecasting with a 14-day input lookback.

| Source | Predictor | Role |
|---|---|---|
| Kazhydromet gauge | `discharge_m3_s` | Target and gauge-based input |
| GPM IMERG | `precipitation_mm` | Satellite precipitation |
| MODIS | `snow_cover_mean` | Snow-cover indicator |
| ERA5-Land | `temperature_c` | Air temperature |
| ESA CCI | `soil_moisture` | Soil moisture |

The daily dataset is stored as **one merged five-source CSV**. It has 4,017 date rows in the saved local notebook run. Nonmissing snow values: **3,389**; nonmissing soil-moisture values: **2,180**. This is **provisional spatial coverage** rather than a verified upstream basin average.

## Methods

- The series is sorted by calendar date; unique dates are enforced by `src/preprocessing.py`.
- Snow cover and soil moisture are past-only forward-filled, **at most two days**.
- Input sequences are 14 previous days, followed by next-day discharge as the target.
- Sequences missing any remaining predictor are removed; B/C use identical valid dates.
- Chronological split by target date: train **2013–2019**, validation **2020–2021**, test **2022–2023**.
- Valid sequence counts: **1,196 train**, **351 validation**, **343 test** (for LSTM B/C).
- LSTM A: `discharge_m3_s` only; LSTM B: four gridded variables; LSTM C: all five inputs.
- PyTorch LSTM: 32 hidden units, batch size 32, Adam LR 0.001, max 100 epochs, early stopping 10, primary seed 17. Ablation seeds: 17, 29, 41.
- Five model/baseline forecasts are compared on the same **343 test target dates**, but LSTM A was **trained** with more gauge-only sequences, so training-set comparability is limited.

## Saved notebook results (343 common test dates)

| Model | RMSE (m³/s) | MAE (m³/s) | NSE | KGE | PBIAS (%) |
|---|---:|---:|---:|---:|---:|
| LSTM A | 29.2008 | 10.5509 | 0.9344 | 0.9561 | -1.1457 |
| LSTM B | 100.0009 | 65.2262 | 0.2303 | 0.4085 | -22.0233 |
| LSTM C | **22.3964** | 10.7774 | **0.9614** | 0.9326 | 2.0787 |
| Persistence | 31.9819 | 10.9102 | 0.9213 | 0.9581 | -1.2609 |
| Seasonal Climatology | 75.7178 | 51.8309 | 0.5587 | 0.5433 | -28.4171 |

The new LSTM C's RMSE is **29.97% lower** than the Persistence baseline's RMSE on these dates; that is a **descriptive** estimate, not evidence of a statistically significant improvement.

### Ablation (means across three seeds)

| Configuration | Mean RMSE | SD RMSE | Change from all-five |
|---|---:|---:|---:|
| All five sources | 23.7755 | 1.2791 | 0 |
| Without precipitation | 31.5657 | 1.5005 | +7.7902 |
| Without snow cover | 21.9752 | 0.7889 | -1.8003 |
| Without temperature | 24.2920 | 0.8948 | +0.5165 |
| Without soil moisture | 22.8583 | 0.7734 | -0.9172 |

Removing snow cover or soil moisture reduced average RMSE over these three seeds. These results do **not** support a claim that every predictor helps.

### Statistical comparisons

Moving-block bootstrap confidence intervals and a paired block sign-flip test were computed using 14-row blocks in the executed notebook.

| Comparison | RMSE reduction (%) | 95% bootstrap CI (%) | p-value |
|---|---:|---:|---:|
| LSTM C vs Persistence | 29.9718 | [-16.7980, 41.5633] | 0.0979 |
| LSTM C vs LSTM A | 23.3022 | [-17.2881, 29.3931] | 0.0929 |
| LSTM C vs LSTM B | 77.6038 | [74.5296, 87.3172] | 0.0010 |

Differences versus Persistence and LSTM A are not significant at p < 0.05 under this procedure. The 343 dates are not a contiguous daily test series because missing-data filtering excludes many dates; this should be considered when interpreting block-based inference.

## Distinguishing three result sets

- **Original 3-input pilot**: 647 dates; LSTM C RMSE **25.8860**, NSE **0.9566**. Original `results/` tables and `Ulba_Flood_Forecasting_(1).ipynb`.
- **Current five-input VS Code run**: 343 dates; LSTM C RMSE **22.3964**, NSE **0.9614**. `Ulba_Flood_Forecasting_VSCode.ipynb`.
- **Manuscript previously reported**: 343 dates; RMSE **24.08**, NSE **0.955**. The manuscript result is **not** equal to the new notebook run and should not be presented as automatically reproduced.

## Artifacts and reproduction

The notebook writes the following outputs on the machine where it is executed:

```
results_5sources/
  model_comparison.csv
  test_predictions.csv
  ablation_results.csv
  statistical_tests.csv
  run_config.json
```

The full-precision actual exports should be uploaded from that `results_5sources` directory (the output path printed by the notebook was `C:\Users\Zhalg\Downloads\results_5sources`). **Do not substitute the old pilot's 647-row CSV exports**, even if they are currently in `docs/`. Do not create simulated prediction rows merely to fill this directory.

A merged input CSV is not included in the GitHub snapshot. To reproduce the run, use the original **five-source** CSV if redistribution is permitted, or document how to obtain it through the respective data providers. For independent checks, also record the dataset checksum, package versions, OS/CPU/GPU and PyTorch settings.

## Data and scientific limitations

Satellite/geospatial aggregation was provisional and not a verified upstream catchment. Snow and soil data have substantial missingness; matched test dates are a filtered subset. Gauge-only LSTM A and full LSTM C use unequal training coverage. Results may change on a corrected watershed extraction, a uniform training sample, a new random seed, or a different PyTorch version. Dataset sharing remains subject to original data-source permissions.

