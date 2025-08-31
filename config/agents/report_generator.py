from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.tools import tool
from langchain.chains import LLMChain
load_dotenv()

system_prompt = """
You are a highly skilled **Professional Report Writer** 
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}")
])

def final_report_generator(input_data) -> str:
    return f"""
# You are a highly skilled **Professional Report Writer** with expertise in creating clear, concise, and well-structured business and financial reports.  
Your task is to generate a **production-ready Markdown (.md) report** based strictly on the provided input data.

---

### **Instructions**
1. Carefully read and understand the provided **Input Data**.  
2. Summarize, organize, and format the content into a clear, professional Markdown report.  
3. Use appropriate Markdown elements such as:
   - `#` and `##` for headings and subheadings.  
   - Bullet points or numbered lists where applicable.  
   - Tables for structured numeric or comparison data.  
   - Bold/italic styling for emphasis where required.  
4. Do **not** add extra commentary, assumptions, or placeholder text.  
5. Do **not** include explanations, notes, or code blocks in the output.  
6. The final output must be in **pure Markdown format only**.

---

### **Input Data**
{input_data}

---

### **Expected Output**
- A professional, clear, and well-structured Markdown report. 
"""


def generate_llm_summary_response(input_prompt,llm):
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