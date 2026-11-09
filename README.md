# Five-source results — export required

The **original full-precision files are not included in this ZIP**, because they were not present in the submitted GitHub archive. No invented or partially reconstructed prediction rows have been added. Do not confuse the rounded result summary in `docs/FIVE_SOURCE_EXPERIMENT.md` with a complete CSV export.

The executed local notebook reported saving these five files in a `results_5sources/` folder in its local working directory:

- `model_comparison.csv`
- `test_predictions.csv`
- `ablation_results.csv`
- `statistical_tests.csv`
- `run_config.json`

**How to finish**: from the computer where the notebook was run, locate that folder or `ulba_5sources_results.zip`. Copy or extract those five actual files into *this* directory, then commit them to GitHub. You do not need to retrain if the saved full result exports still exist.

For a permanent reproducibility package, verify the outputs against the notebook, record the exact dataset version/hash and software environment, and review whether the input dataset can legally be shared.
