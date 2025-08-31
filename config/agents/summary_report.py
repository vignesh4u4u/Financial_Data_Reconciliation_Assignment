def financial_reconciliation_prompt(dataset, dataset_path) -> str:
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

**Step 4:Generate pandas,numpy (data manipulation) query**
    - 1. find the number of NAN values count.(merged_df.isna().sum())
    - 2. Find the unique values in all features make the ascending order.(merged_df.nunique().sort_values())
    - 3. Find the dataset shape.
    - 4. make the statistical summary report.
    - 5. Discrepancy columns summary report (eg. "discrepancy_summary = merged_df['Discrepancy'].value_counts()").
    - 6. Find duplicate values count.(merged_df.duplicated().sum())
    ** Note: above all query value print time use the proper header**
        eg. print(f" Total NAN Values : {{merged_df.isna().sum()}}    
  
### VERY IMPORTANT:
- When generating code, always read the DataFrame using the file path `{dataset_path}`.
    - ex: merged_df = pd.read_excel({dataset_path})    
- The **Financial Dataset** shown (top 6 rows) is provided only for reference and understanding of the structure.
- **\[IMPORTANT]**: Do **not** create or assume any synthetic datasets. Always use the data from the file located at `{dataset_path}`.

---

## OUTPUT REQUIREMENTS
  1. **Summary_Report**
  2. **Duplicate_Records**
  3. **Discrepancy_Summary** (only if column exists)
- **Strict Rule**: No print complete dataframe statements in the code.
- Excel or excelworkbook no need to save the output. only generate the code.
- Step 4 mention all questions corresponding answer will be print using print()
---

### OUTPUT FORMAT
Return only clean, production-ready code (no text, no comments, no prints):

```python
import pandas as pd
import numpy as np

{{clean_complete_code}}
"""