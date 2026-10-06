# MP1 Data Processing Pipeline

This project is a command-line data pipeline that loads, validates, cleans, and saves tabular data. The pipeline reads a CSV input file and a YAML configuration file that controls validation and processing behavior. The `pipeline.py` script coordinates the complete workflow and reports each major result through logging. The `src/data_loaders.py` module loads CSV, JSON, and YAML files, while `src/data_validator.py` checks required columns and removes invalid numeric values. The `src/data_processor.py` module removes duplicates, handles missing values, and filters outliers using either IQR or z-scores. The `src/data_output.py` module creates the output directory when needed and saves the cleaned DataFrame without an index, and `src/utils.py` provides shared logging and path validation. A cleaning report printed at the end summarizes the rows and columns removed during processing.

## Run the Pipeline

```bash
python pipeline.py \
  --input fixtures/sample_data.csv \
  --output output/clean.csv \
  --config config/config.yaml \
  --verbose
```

With the provided sample data, validation removes 2 rows containing invalid numeric ratings. Processing then removes 2 duplicate rows, 2 rows with missing values, and 2 rating outliers, producing `output/clean.csv` with 92 rows and 5 columns.
