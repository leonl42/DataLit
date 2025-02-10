## How to Use
### Manual
Run `python some_feature_extraction.py` with the following arguments:
   - `--math-path`: Path to the folder containing extracted math
   - `--metadata-json`: Path to the conference metadata JSON file
   - `--conference`: Either "iclr" or "neurips"
   - `--out`: Path for the output CSV file

### Script
1. Simply run `bash run_feature_extraction.sh` to process both ICLR and NeurIPS papers, making sure the paths are correct.