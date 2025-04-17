# 📊 Data-to-Insight AI Agent v2

An LLM app using Langchain and Gemini Language Model to answer user questions from dats files, returning smart insights, structured tables, and auto-generated visual charts through natural language queries.

---

## Project Structure

```bash
📂 cdata-to-insight-agent-v2
├── 📄 interface.py           # Streamlit app to chat with your CSV
├── 📄 agent.py               # Loads CSV, builds LLM prompt and parses structured response
├── 📄 .env                   # Stores API key
├── 📄 .gitignore
└── 📄 requirements.txt       # Required packages
```

---

## Key Features

- **CSV Upload**: Upload any CSV with product or order data.
- **Natural Language Querying**: Ask anything like “What are my delayed orders?” or “Top 5 products by quantity”.
- **Visual Responses**: Auto-generates response, tables, bar charts, or line charts using LLM-guided insights.
- **Structured JSON Prompting**: Agent uses JSON formating for clean parsing.
- **LLM Answering**: Uses Gemini to generate contextual answers.

---

## Requirements

  - `Python 3.10`
  - `streamlit`
  - `pandas`
  - `langchain`
  - `langchain-google-genai`
  - `python-environ`

---

## Interface

<img src="Output_Screenshots/DelayedOrdersTable.png" alt="Example Response" width="650"/>

---

## Setup & Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/chat-with-csv-gemini.git
   cd chat-with-csv-gemini
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Gemini API Key:
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

4. Run the Streamlit App:
   ```bash
   streamlit run interface.py
   ```

- Upload a CSV file
- Ask questions like:
  - "Show a table of delayed orders"
  - "Bar chart of quantities per product"
- Get:
  - 📋 Structured tables
  - 📈 Interactive bar/line charts
  - 💡 Direct insights from your data

---

## Technologies Used

- **Gemini 2.0 Flash**: Pre-trained LLM
- **Langchain**: LLM interface and prompt orchestration
- **Streamlit**: Web UI
- **Pandas**: Data handling and Visualization

---

## 👨‍💻 Developed By

[github.com/Sanjit1806](https://github.com/Sanjit1806)