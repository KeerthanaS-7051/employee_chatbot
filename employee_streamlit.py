#run in streamlit
import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_together import Together

db = SQLDatabase.from_uri("sqlite:///employee.db")

llm = Together(
    model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    temperature=0.7,
    max_tokens=512,
    top_p=0.7
)

db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, return_direct=True, verbose=False)

st.title("💼 Employee Database Chatbot")
st.write("Ask questions about your employee database.")

if "history" not in st.session_state:
    st.session_state.history = []

user_question = st.text_input("Ask a question:")

if user_question:
    try:
        sql_result = db_chain.invoke({"query": user_question})

        if isinstance(sql_result, list) and isinstance(sql_result[0], tuple):
            formatted_result = ', '.join(str(item) for item in sql_result[0])
        else:
            formatted_result = str(sql_result)

        prompt = f"""
You are a helpful assistant. Given a user's question from a database, explain the answer clearly.

User question: "{user_question}"
SQL result: "{formatted_result}"

Respond with a helpful sentence.
"""
        final_answer = llm.invoke(prompt).strip()

        st.session_state.history.append(
            {"question": user_question, "sql_result": formatted_result, "answer": final_answer}
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.session_state.history:
    st.markdown("## 🧾 Query History")
    for i, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"### {item['question']}")
        st.markdown(f"**Answer:** {item['answer']}")
