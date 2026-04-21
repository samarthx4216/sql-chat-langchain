import sqlite3
import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_groq import ChatGroq

from sqlalchemy import create_engine

# Auto-create student.db if not exists
db_path = Path(__file__).parent / "student.db"
if not db_path.exists():
    con = sqlite3.connect(db_path)
    con.execute("""CREATE TABLE IF NOT EXISTS STUDENT (
        NAME TEXT, CLASS TEXT, SECTION TEXT, MARKS INTEGER)""")
    con.executemany("INSERT INTO STUDENT VALUES (?,?,?,?)", [
        ('Krish','Data Science','A',90),
        ('Sudhanshu','Data Science','B',100),
        ('Darius','Data Science','A',86),
        ('Vikash','DEVOPS','A',50),
        ('Dipesh','DEVOPS','A',35),
    ])
    con.commit()
    con.close()

st.set_page_config(page_title="Langchain : Chat with SQL DB", page_icon="🦜")
st.title("🦜 Langchain : Chat with SQL DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["USE SQLlite 3 Database- Student.db","Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide My SQL Host", type="password")
    mysql_user=st.sidebar.text_input("MYsql user", type="password")
    mysql_password=st.sidebar.text_input("MYsql password", type="password")
    mysql_database=st.sidebar.text_input("MYsql database", type="password")
   
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="Enter your Groq API Key",type="password")

if not db_uri:
    st.info("Please select the database information and url")
    st.stop()

if not api_key:
    st.info("Please enter the API Key")
    st.stop()

## LLM Model

model_name = st.sidebar.selectbox(
    "Select Model:",
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "qwen/qwen3-32b"]
)

llm=ChatGroq(groq_api_key=api_key,model_name=model_name, streaming=True)


@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_database=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent / "student.db").absolute()
        creator=lambda: sqlite3.connect(f"{dbfilepath}")
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not(mysql_host and mysql_user and mysql_password and mysql_database):
            st.error("Please provide all the mysql database information")
            st.stop()
        return SQLDatabase.from_uri(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}")

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_database)
else:
    db=configure_db(db_uri)


## toolkit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="zero-shot-react-description",
    handle_parsing_errors=True
)


if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
