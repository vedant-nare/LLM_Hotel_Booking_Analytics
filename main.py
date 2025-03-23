from fastapi import FastAPI, Query
import pandas as pd
from services.analytics import generate_analytics
from services.preprocessing import load_and_clean_data
from services.qa import search_booking
from request import QuestionRequest


app = FastAPI()

# Load and preprocess data once on startup
df = load_and_clean_data()

@app.get("/analytics")
def get_analytics():
    #"""Returns analytics reports as structured JSON, including base64-encoded images."""
    return generate_analytics(df)

@app.get("/ask")
def ask_question(request: QuestionRequest):
    
    if df is None or df.empty:
        return {"error": "No booking data available."}

    response = search_booking(request.question, df)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
