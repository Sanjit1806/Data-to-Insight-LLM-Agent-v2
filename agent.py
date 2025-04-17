from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import environ
import json

# Load API key
env = environ.Env()
environ.Env.read_env()
API_KEY = env("GEMINI_API_KEY")

# Set up Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY, temperature=0)

def create_agent(filename):
    df = pd.read_csv(filename)
    return df

def query_agent(df, query):

    system_prompt = f"""
    You are a data assistant. A user has uploaded a CSV file as a dataframe. 
    Your task is to respond to the query with one of the following formats ONLY:

    1. If it's a simple answer:
    {{
        "answer": "The answer here"
    }}

    2. If it's a table:
    {{
        "table": {{
            "columns": ["col1", "col2"],
            "data": [["value1", "value2"], ["value3", "value4"]]
        }}
    }}

    3. If it's a bar chart:
    {{
        "bar": {{
            "columns": ["label1", "label2"],
            "data": [["label1", 10], ["label2", 20]]
        }}
    }}

    4. If it's a line chart:
    {{
        "line": {{
            "columns": ["label1", "label2"],
            "data": [["label1", 10], ["label2", 20]]
        }}
    }}

    Only return pure JSON. Do NOT include markdown formatting or code blocks.
    """

    if len(df) > 200:
        df = df.head(200)
    # print(len(df))

    prompt = f"{system_prompt}\n\nQuery: {query}\n\nHere is the full CSV data:\n{df.to_json(orient='records')}"

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Remove markdown formatting
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").strip()
    if raw.endswith("```"):
        raw = raw[:-3].strip()

    try:
        return json.loads(raw)
    except Exception as e:
        return {"answer": f"Failed to parse response. Error: {str(e)}\nRaw: {raw}"}
