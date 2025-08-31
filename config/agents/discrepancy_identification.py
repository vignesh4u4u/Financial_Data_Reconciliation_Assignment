def financial_reconciliation_prompt(erp_df, bank_df, output_file_path,
                                   bank_data_pdf_path, erp_data_excel_path) -> str:
    return f"""
# You are a **Senior Data Scientist** with 15+ years of experience in **Pandas, NumPy, SciPy, Seaborn, Matplotlib**. Generate a production-ready Pandas query based on the following instructions.

----
### **ERP DATASET**
{erp_df}  (only the top 5 rows are shown; note that more rows are available)

---
### **BANK DATASET**
{bank_df}  (only the top 5 rows are shown; note that more rows are available)

----

## Your Task:

**Step 1: Standardize Column Names**
- Clean all column names in both datasets:
  - Strip leading/trailing spaces.
  - Replace spaces, dashes, or special characters with underscores (`_`).
  - Convert all column names to lowercase.
- Example: `"Invoice ID"` → `"invoice_id"`

**Step 2: Understand the Input Datasets**
    - Carefully analyze the provided **ERP DATASET** and **BANK DATASET**.
    - These datasets are preloaded to help you generate the Pandas and NumPy query.
    - Do not create any new datasets.
    - Note that **BANK DATASET** columns are of type `object`, not `int` or `float`.
    - Understand the data types, column names, unique values, etc.
    - Do not include extra code or commented lines in the output.    

**Step 3: Data Preprocessing**
    - Detect all date-like columns and convert them to `datetime`.
    - Detect all numeric columns and convert them to `float` or `int`.
    - Handle conversion errors using `errors='coerce'`.
    - Format all dates consistently as `YYYY-MM-DD`.
    - Columns name inside present space or gap remove and make proper format.

**Step 4: Merge Datasets Dynamically**
    - Identify common identifier column(s) automatically.
    - Perform an outer join to retain all records from both datasets.
    - Add suffixes `_ERP` and `_Bank` to overlapping columns.
    - Use the dataset variable names `erp_df` and `bank_df`.

**Step 5: Compute Differences**
    - Automatically detect ERP and Bank amount columns.
    - Create an `Amount_Diff` column = ERP amount − Bank amount (rounded to 2 decimal places).

**Step 6: Classify Discrepancies Dynamically**
    - For each row, classify discrepancies as:
        - 'Transaction Missing in ERP' (Bank has a record, ERP is missing)
        - 'Transaction Missing in Bank' (ERP has a record, Bank is missing)
        - 'Amounts Match Exactly' (difference = 0)
        - 'Minor Rounding Difference' (difference ≤ 1)
        - 'Amount Mismatch' (difference > 1 and ≤ 5)
        - 'Significant Amount Discrepancy' (difference > 5)
    - Handle negative or NaN differences gracefully.
    - Include duplicates and overlapping Invoice IDs.

### VERY IMPORTANT:
- Use the file path `{erp_data_excel_path}` for the `erp_df` DataFrame.
- Use the file path `{bank_data_pdf_path}` for the `bank_df` DataFrame.
- Save the output to the file path `{output_file_path}`.

**Expected Output Table Format in Saved Excel File:**

| Invoice_ID | Date_ERP  | Date_Bank | Amount_ERP | Amount_Bank | Amount_Diff | Discrepancy                   |
|------------|-----------|-----------|------------|-------------|-------------|-------------------------------|
| INV0200    | 2025-01-04| NaT       | 353.38     | NaN         | NaN         | Transaction Missing in Bank   |
| NaN        | NaT       | 2025-01-06| NaN        | -37.76      | NaN         | Transaction Missing in ERP    |
| NaN        | NaT       | 2025-01-28| NaN        | -28.15      | NaN         | Transaction Missing in ERP    |
| INV0001    | 2025-02-10| 2025-02-09| 267.10     | 267.10      | 0.00        | Amounts Match Exactly         |
| INV0002    | 2025-02-17| 2025-02-15| 1789.75    | 1788.62     | 1.13        | Moderate Amount Difference    |

**OUTPUT FORMAT**
- Provide clean code without text, notes, or explanations within the code.
```python
import pandas as pd
import numpy as np
import re, os

{{clean_complete_code}}
```

**IMPORTANT NOTE:**
- Save the final output as an Excel file: `reconciliation_result.to_excel({output_file_path}, index=False)`
- Include only the provided packages; do not add advanced packages.
- Ensure all columns in the expected output table are present, even if not found in the input datasets (ignore missing columns).
- Strictly use the variable names mentioned in the instructions for backend compatibility. 
- 100% prodution ready code. with zero present error.
"""


