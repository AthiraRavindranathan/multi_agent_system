from fastapi import FastAPI

app = FastAPI()

class SupportQuery:
    def __init__(self, query: str):
        self.query = query

@app.post("/support-query/")
async def handle_query(query: SupportQuery):
    return {"response": f"Your query '{query.query}' has been received and is being processed."}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Customer Support API!"}