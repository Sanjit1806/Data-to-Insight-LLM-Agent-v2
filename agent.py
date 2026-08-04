from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import environ
import json
import time

# Load API key
env = environ.Env()
environ.Env.read_env()
API_KEY = env("GEMINI_API_KEY")

# Set up Gemini model (free tier)
# Tested working models - uncomment your preferred one:
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=API_KEY)
# llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", google_api_key=API_KEY)
# llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=API_KEY)

def create_agent(filename):
    df = pd.read_csv(filename)
    return df

def query_agent(df, query):

    system_prompt = """You are a data assistant. A user has uploaded a CSV file as a dataframe. 
Your task is to respond to the query with one of the following formats ONLY:

1. If it's a simple answer:
{
    "answer": "The answer here"
}

2. If it's a table:
{
    "table": {
        "columns": ["col1", "col2"],
        "data": [["value1", "value2"], ["value3", "value4"]]
    }
}

3. If it's a bar chart:
{
    "bar": {
        "columns": ["label1", "label2"],
        "data": [["label1", 10], ["label2", 20]]
    }
}

4. If it's a line chart:
{
    "line": {
        "columns": ["label1", "label2"],
        "data": [["label1", 10], ["label2", 20]]
    }
}

Only return pure JSON. Do NOT include markdown formatting or code blocks.
"""

    # Limit rows to reduce token usage (helps stay within free-tier limits)
    if len(df) > 100:
        sample_df = df.head(100)
        data_note = f"\n(Showing first 100 of {len(df)} rows. Analyze ALL the data shown.)"
    else:
        sample_df = df
        data_note = ""

    # Use CSV format instead of JSON to save tokens
    csv_data = sample_df.to_csv(index=False)
    prompt = f"{system_prompt}\n\nQuery: {query}\n\nColumns: {list(df.columns)}\nTotal rows: {len(df)}{data_note}\n\nData:\n{csv_data}"

    # Retry logic for rate limits
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = llm.invoke(prompt)
            # Handle content being either a string or a list
            raw = response.content
            if isinstance(raw, list):
                raw = "".join([part if isinstance(part, str) else part.get("text", "") for part in raw])
            raw = raw.strip()

            # Remove markdown formatting
            if raw.startswith("```json"):
                raw = raw.replace("```json", "").strip()
            if raw.startswith("```"):
                raw = raw[3:].strip()
            if raw.endswith("```"):
                raw = raw[:-3].strip()

            return json.loads(raw)
        except json.JSONDecodeError as e:
            return {"answer": f"Failed to parse response. Error: {str(e)}\nRaw: {raw}"}
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg:
                if attempt < max_retries:
                    time.sleep(60)  # Wait 60 seconds before retry
                    continue
                return {"answer": "⚠️ API rate limit reached. The free tier has limited requests per minute/day. Please wait a minute and try again."}
            return {"answer": f"Error calling Gemini API: {error_msg}"}
