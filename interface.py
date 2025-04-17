# interface.py

import streamlit as st
import pandas as pd
from agent import create_agent, query_agent

st.set_page_config(page_title="Data-to-Insight Agent v2", layout="wide")
st.title("📊 Data-to-Insight Agent v2")
st.write("Upload a CSV, ask your question, and let the Agent show you insights or charts")
data = st.file_uploader("", type=["csv"])
if data is not None:
    query = st.text_input("Ask a question about your data:")

    if query:
        
        with st.spinner("Thinking..."):
            df = create_agent(data)
            response = query_agent(df, query)

        st.subheader("Insight:")

        if "answer" in response:
            st.success(response["answer"])

        elif "table" in response:
            st.subheader("📋 Table")
            table_data = pd.DataFrame(response["table"]["data"], columns=response["table"]["columns"])
            st.table(table_data)

        elif "bar" in response:
            st.subheader("📊 Bar Chart")
            columns = response["bar"]["columns"]
            data = response["bar"]["data"]
            bar_df = pd.DataFrame(data, columns=columns)
            bar_df.set_index(columns[0], inplace=True)
            st.bar_chart(bar_df)

        elif "line" in response:
            st.subheader("📈 Line Chart")
            columns = response["line"]["columns"]
            data = response["line"]["data"]
            line_df = pd.DataFrame(data, columns=columns)
            line_df.set_index(columns[0], inplace=True)
            st.line_chart(line_df)

        else:
            st.warning("⚠️ Couldn't understand the response format. Please rephrase your question.")

elif not data:
    st.info("Please upload a file")