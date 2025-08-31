def financial_reconciliation_prompt(dataset, dataset_path ,output_path) -> str:
    return f"""
# You are a **Senior Data Scientist** with 15+ years of expertise in **Pandas, NumPy**.  
Your task is to generate **production-ready Pandas code** to identify duplicate records in the dataset and save them into an Excel file.

---

### **Financial Dataset**
{dataset}  
(Only the top 5 rows are shown; more rows are available)

---

## Instructions

**Step 1: Understand the dataset**
- Analyze the provided dataset structure (columns, datatypes, unique values).
- Do not create any new datasets. The full dataset is already preloaded in memory; only the first 6 rows are shown here as a preview, but more rows are available
- Strictly use read DataFrame variable name: `merged_df`.

**Step 2: Standardize Column Names**
- Clean all column names in both datasets:
  - Strip leading/trailing spaces.
  - Replace spaces, dashes, or special characters with underscores (`_`).
  - Convert all column names to lowercase.
- Example: `"Invoice ID"` → `"invoice_id"`

**Step 3: Detect potential unique identifier column(s)**
- Automatically detect column(s) that are most likely unique identifiers (e.g., *Invoice ID*, *Transaction ID*, etc.).
- If multiple potential identifier columns exist, check combinations as needed.
- Strictly use **Financial Dataset** present columns.

**Step 4: Find duplicate records**
- Use Pandas `duplicated()` to detect duplicate rows based on the identified unique column(s).
- Extract **all duplicate rows** (not just the first occurrence).

**Step 4: Save duplicates**
- Save the duplicate rows into an Excel file at the location: {output_path}.
- Use the variable name `duplicates_df` for the DataFrame containing duplicates.

### VERY IMPORTANT:
- When generating code, always read the DataFrame using the file path `{dataset_path}`.
    - ex: merged_df = pd.read_excel({dataset_path})    
- The **Financial Dataset** shown (top 6 rows) is provided only for reference and understanding of the structure.
- **\[IMPORTANT]**: Do **not** create or assume any synthetic datasets. Always use the data from the file located at `{dataset_path}`.


### Expected Output Code Format:
- Provide clean code without text, notes, or explanations within the code.
```python
import pandas as pd
import numpy as np

unique_cols = "automatically find more unique columns name like ID"
if unique_cols:
    # Find duplicates based on detected columns
    duplicates_df = merged_df[merged_df.duplicated(subset=unique_cols, keep=False)]
else:
    # Fallback: check for full row duplicates
    duplicates_df = merged_df[merged_df.duplicated(keep=False)]

# Save duplicate records
duplicates_df.to_excel({output_path}, index=False)
"""