#directly run in terminal
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

db_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    return_direct=True, 
    verbose=False
)

print("Ask your Employee DB questions (type 'exit' to quit):")
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    try:
        result = db_chain.invoke(query)
        if isinstance(result, list) and isinstance(result[0], tuple):
            values = ', '.join(str(item) for item in result[0])
            print(f"Bot: {values}")
        else:
            print(f"Bot: {result}")
    except Exception as e:
        print("Error:", str(e))
