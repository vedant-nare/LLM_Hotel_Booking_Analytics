# LLM_Hotel_Booking_Analytics
Overview

This project is an LLM-powered booking analytics and QA system that leverages retrieval-augmented generation (RAG) to provide booking insights and answer queries using a vector database. It integrates FastAPI for API endpoints and ChromaDB or FAISS for efficient search.

Features

📊 Analytics API: Generates revenue trends, cancellation rates, and geographical distribution reports.

🧠 Question Answering API: Uses RAG to search hotel booking data and generate responses with an LLM.

⚡ FastAPI-based Backend: Provides a scalable and high-performance API.

🏎️ FAISS / ChromaDB for Vector Search: Enables fast similarity search on booking data.

🤖 LLM Integration: Uses SentenceTransformers for embeddings and a transformer-based LLM for query responses.

Installation

Prerequisites

Python 3.9+

Virtual Environment (recommended)

Setup

Clone the repository:
git clone https://github.com/your-username/llm-booking-analytics.git
cd llm-booking-analytics

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows

Install dependencies:

pip install -r requirements.txt

Usage

1️⃣ Start the API Server

Run the FastAPI server with Uvicorn:

uvicorn api:app --host 127.0.0.1 --port 8000 --reload

2️⃣ API Endpoints

Analytics API

Endpoint: POST /analytics

Description: Returns revenue trends, cancellation rates, and geographical distribution.

Example Request (PowerShell):

Invoke-RestMethod -Uri "http://127.0.0.1:8000/analytics" -Method POST

Question Answering API

Endpoint: POST /ask

Description: Answers queries based on booking data using RAG.

Example Request (PowerShell):

Invoke-RestMethod -Uri "http://127.0.0.1:8000/ask" -Method POST -Body (@{ query = "What is the cancellation rate?" } | ConvertTo-Json) -ContentType "application/json"
