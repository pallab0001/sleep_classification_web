# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import numpy as np
import re

# Initialize FastAPI app
app = FastAPI()

# Mount the "static" directory to serve CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Load the vectorizer and SVM model from disk
vectorizer = joblib.load("vectorizer.pkl")
svm_model = joblib.load("svm_model.pkl")

# Define sleep-related keywords
sleep_keywords = [
    'ঘুম', 'নিদ্রা', 'উঘাত', 'ঘুমাচ্ছে', 'নিশি',
    'ঘুমিয়েছিলাম', 'নিদ্রাহীন', 'তন্দ্রা', 'তন্দ্রাচ্ছন্ন', 'অনিদ্রা'
]

# Utility function to check if text is sleep-related
def is_sleep_related(text):
    return any(re.search(keyword, text) for keyword in sleep_keywords)

# Pydantic model for the request payload
class Story(BaseModel):
    text: str

# Serve the main page (index.html) at the root URL
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the prediction endpoint
@app.post("/predict")
async def predict(story: Story):
    text = story.text

    # First, check if the text is sleep-related
    if not is_sleep_related(text):
        return {
            "label": "no sleep",
            "score": 0.0,
            "message": "এই লেখাটি ঘুম সম্পর্কিত কোনো গল্প নয়।"
        }

    # Transform the text and predict the class
    X_vec = vectorizer.transform([text])
    pred_label = svm_model.predict(X_vec)[0]

    # Compute prediction confidence
    if hasattr(svm_model, "predict_proba"):
        prob = svm_model.predict_proba(X_vec)[0]
        confidence = float(prob.max())
    else:
        confidence = 0.0  # If predict_proba not available

    return {
        "label": pred_label,
        "score": confidence
    }
