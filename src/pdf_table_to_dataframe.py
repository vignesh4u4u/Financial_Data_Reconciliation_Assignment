import os
import pandas as pd
import pdfplumber

base_dir = os.getcwd()
root_dir = os.path.dirname(base_dir)

bank_data_pdf_path = os.path.join(root_dir, "assets", "bank_statement.pdf")
def pdf_extractor() -> pd.DataFrame:
    tables = []
    headers = None
    with pdfplumber.open(bank_data_pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table)
                if headers is None:
                    headers = df.iloc[0]
                df = df.drop(0).reset_index(drop=True)
                df.columns = headers
                tables.append(df)
    if not tables:
        return pd.DataFrame()

    final_df = pd.concat(tables, ignore_index=True)

    output_path = os.path.splitext(bank_data_pdf_path)[0] + ".xlsx"
    final_df.to_excel(output_path, index=False)

    print(f"Excel file saved at: {output_path}")
    return final_df, output_path

