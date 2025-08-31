import os
import re
import shutil
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.tools import tool
from langchain.chains import LLMChain
load_dotenv()

from run_python_file import run_generated_file
from pdf_table_to_dataframe import pdf_extractor

from config.agents import discrepancy_identification,report_generator
from config.agents import duplicates_finder,summary_report

os.environ["GEMINI_API_KEY"]= input("Enter gemini api key: ")
#api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.environ["GEMINI_API_KEY"])

base_dir = os.getcwd()
root_dir = os.path.dirname(base_dir)
erp_data_excel_path = os.path.join(root_dir, "assets", "erp_data.xlsx")
file_path = os.path.join(root_dir, "src","all_output_file" ,"reconciliation_result.xlsx")
duplicate_file_path = os.path.join(root_dir, "src","all_output_file", "duplicates_result.xlsx")
summary_file_path = os.path.join(root_dir, "src","all_output_file", "Summary_Report.md")

for file in [file_path,duplicate_file_path,summary_file_path]:
    os.makedirs(os.path.dirname(file), exist_ok=True)

pdf_file_table,bank_data_pdf_path = pdf_extractor()


system_prompt = """
You are a highly experienced **Financial Data Reconciliation assistant** (20+ years expertise) in:
• Reconcile transactions between the ERP data and Bank Statement.
• Identify and classify discrepancies (e.g., missing in ERP, missing in Bank, duplicates, amount
 mismatches, rounding differences)

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}")
])

def generate_llm_response(input_prompt):
    chain = LLMChain(llm=llm,
        prompt=prompt,
        verbose=True
    )
    chat_response = chain.invoke({
        "input": input_prompt,
        "chat_history": []
    })
    final_output = chat_response["text"]
    return final_output

def excel_file_extractor() -> pd.DataFrame:
    if erp_data_excel_path.endswith(".xlsx"):
        return pd.read_excel(erp_data_excel_path)
    elif erp_data_excel_path.endswith(".csv"):
        return pd.read_csv(erp_data_excel_path)
    return pd.DataFrame()

def input_table_datas():
    erp_data = excel_file_extractor()
    bank_data = pdf_file_table
    return erp_data, bank_data

erp_df, bank_df = input_table_datas()

def get_the_reconciliation_prompt():
    if erp_df.empty or bank_df.empty:
        print("ERP or Bank DataFrame is empty. Cannot proceed.")
        return
    prompt = discrepancy_identification.financial_reconciliation_prompt(
        erp_df.head(6).to_string(),
        bank_df.head(6).to_string(),
        file_path,bank_data_pdf_path,erp_data_excel_path
    )
    return prompt


def generate_reconciliation_report():
    try:
        input_prompt = get_the_reconciliation_prompt()
        chat_response = generate_llm_response(input_prompt)
        filter_python_code = re.sub(r"```(?:python)?|```", "", chat_response).strip()
        with open("reconciliation.py", "w", encoding="utf-8") as f:
            f.write(filter_python_code)
        run_generated_file("reconciliation.py")
        return {"answer":"file_created"}
    except Exception as e:
        return str(e)

first_agent_answer = generate_reconciliation_report()

def generate_duplicate_values():
    if first_agent_answer["answer"] == "file_created":
        try:
            dataset = pd.read_excel(file_path)
            if dataset.empty:
                print("df1 is empty")
            else:
                df_ = dataset.head(6).to_string()
                input_prompt = duplicates_finder.financial_reconciliation_prompt(df_, file_path, duplicate_file_path)
                chat_response = generate_llm_response(input_prompt)
                filter_python_code = re.sub(r"```(?:python)?|```", "", chat_response).strip()
                with open("duplicates_data.py", "w", encoding="utf-8") as f:
                    f.write(filter_python_code)
                run_generated_file("duplicates_data.py")
            return {"answer":"duplicated_file_created","output":df_}
        except Exception as e:
            return (str(e))

second_agent_answer= generate_duplicate_values()
df_preview = second_agent_answer.get("output")

def create_summary_report_code():
    input_prompt = summary_report.financial_reconciliation_prompt(df_preview ,file_path)
    chat_response = generate_llm_response(input_prompt)
    filter_python_code = re.sub(r"```(?:python)?|```", "", chat_response).strip()
    with open("summary_data.py", "w", encoding="utf-8") as f:
        f.write(filter_python_code)
    output = run_generated_file("summary_data.py")
    return output

third_agent_output = create_summary_report_code()

fourth_agent_prompt = report_generator.final_report_generator(third_agent_output)
fourth_agent_output = report_generator.generate_llm_summary_response(fourth_agent_prompt,llm)

with open(summary_file_path,"w",encoding="utf-8") as f:
    f.write(fourth_agent_output)

if __name__ =="__main__":
    print("All Code Sucessfully Executed")