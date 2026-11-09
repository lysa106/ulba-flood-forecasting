## Five-source extension (new experiment)

An additional Ulba flood-forecasting experiment includes **five** data sources: Kazhydromet discharge (`discharge_m3_s`), GPM IMERG precipitation (`precipitation_mm`), MODIS snow cover (`snow_cover_mean`), ERA5-Land temperature (`temperature_c`), and ESA CCI soil moisture (`soil_moisture`). The inputs are combined into one daily CSV.

**LSTM C (five-source model)** was evaluated on **343 matched test dates** from 2022–2023 and obtained **RMSE = 22.3964 m³/s, NSE = 0.9614** in the saved VS Code notebook run. The original manuscript values **RMSE = 24.08 m³/s, NSE = 0.955** are preserved as historical results from a separate experimental setup; they were not exactly reproduced by this new run.

See [five-source methodology and caveats](docs/FIVE_SOURCE_EXPERIMENT.md) and [five-source VS Code notebook](notebooks/Ulba_Flood_Forecasting_5sources_VSCode.ipynb). Dataset extraction is provisional and its licensing must be checked before posting the merged CSV. There are important limitations involving nonuniform missingness, differing training data coverage and uncertain statistical significance.
