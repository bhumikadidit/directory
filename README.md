
# District Data Cleaner

A simple Python tool that fixes spelling mistakes in district names and merges CSV files automatically.

## What This Does

- **Fixes Spelling**: Corrects district name typos like "Dhanusa" → "Dhanusha"
- **Merges Data**: Combines multiple CSV files into one dataset
- **Saves Time**: No more manual data cleaning

## Setup

```bash
# Install required package
pip install pandas
```

## How to Use

1. **Add your files** to `data/raw/` folder:
   - `kpi_1.csv` - First dataset
   - `kpi_2.csv` - Second dataset  
   - `correct_districts.txt` - List of correct district names

2. **Run the cleaner**:
```bash
python merge/main.py
```

3. **Check results** in:
   - `data/temp/` - Cleaned individual files
   - `data/processed/` - Final merged file

## Example

**Before (different spellings):**
- Dataset 1: "Kavre palanchowk"
- Dataset 2: "Kavrepalanchowk"

**After (automatically fixed):**
- Both become: "kavrepalanchowk"
- Data merges correctly

## Test It Works

```bash
python -m tests.test_main
```

## File Structure

```
data/
├── raw/           # Put your CSV files here
├── temp/          # Cleaned files (auto-generated)
└── processed/     # Final merged data (auto-generated)
```

Perfect for cleaning messy district data before analysis!
```
