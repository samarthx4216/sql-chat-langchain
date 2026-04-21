# 🦜 LangChain : Chat with SQL DB

An AI-powered chatbot that lets you query SQL databases using plain English. Built with **LangChain**, **Groq LLMs**, and **Streamlit** — supports both local SQLite and remote MySQL databases.

---

## ✨ Features

- 💬 Natural language to SQL — ask questions, get answers
- 🗄️ Supports **SQLite** (local `student.db`) and **MySQL** (remote)
- ⚡ Powered by **Groq** ultra-fast inference (LLaMA 3.3 70B, LLaMA 3.1 8B, Qwen3 32B)
- 🔁 Persistent chat history within session
- 🔍 Verbose agent reasoning with Streamlit callback handler
- 🔒 Secure — API keys and DB credentials entered at runtime, never hardcoded

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| LLM | Groq (`langchain-groq`) |
| Agent | LangChain SQL Agent |
| DB Interface | SQLAlchemy + LangChain SQLDatabase |
| Local DB | SQLite 3 |
| Remote DB | MySQL via PyMySQL |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/sql-chat-langchain.git
cd sql-chat-langchain
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the SQLite database (optional)

Place your `student.db` file in the root of the project directory. A sample schema:

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    marks INTEGER,
    grade TEXT,
    section TEXT
);
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## ⚙️ Configuration (Sidebar)

| Setting | Description |
|---|---|
| **Database** | Choose SQLite (local) or MySQL (remote) |
| **Groq API Key** | Get yours at [console.groq.com](https://console.groq.com) |
| **Model** | Select from LLaMA 3.3 70B, LLaMA 3.1 8B, or Qwen3 32B |
| **MySQL Credentials** | Host, user, password, database name (only for MySQL mode) |

---

## 📦 Requirements

```
streamlit
langchain
langchain-community
langchain-groq
sqlalchemy
pymysql
```

> Install all at once: `pip install -r requirements.txt`

---

## 💡 Example Queries

- *"How many students are in section A?"*
- *"Show me the top 5 students by marks."*
- *"What is the average grade of all students?"*
- *"List students who scored more than 90."*

---

## 🔐 Security Notes

- All credentials (API key, DB passwords) are entered via sidebar inputs with `type="password"` — they are never stored or logged.
- The SQLite database is opened in **read-only mode** to prevent accidental writes.

---

## 📄 License

MIT License. Feel free to use, modify, and distribute.
