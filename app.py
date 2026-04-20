from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import os

app = FastAPI(title="Customer Churn Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models properly
PROCESSOR_PATH = os.path.join("models", "processor.joblib")
MODEL_PATH = os.path.join("models", "svm_model.joblib")

processor = None
svm_model = None

@app.on_event("startup")
def load_models():
    global processor, svm_model
    if os.path.exists(PROCESSOR_PATH) and os.path.exists(MODEL_PATH):
        processor = joblib.load(PROCESSOR_PATH)
        svm_model = joblib.load(MODEL_PATH)
        print("Models loaded successfully.")
    else:
        print("WARNING: Models not found. Run train_and_save.py first.")

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join("static", "index.html"), "r") as f:
        return f.read()

@app.post("/predict")
async def predict_churn(customer: CustomerData):
    if not processor or not svm_model:
        return JSONResponse(status_code=500, content={"error": "Models are not loaded on server."})
    
    # Convert input to DataFrame
    input_dict = customer.dict()
    df = pd.DataFrame([input_dict])
    
    try:
        # Preprocess
        X_processed = processor.transform(df)
        
        # Predict
        prediction = svm_model.predict(X_processed)
        probabilities = svm_model.predict_proba(X_processed)[0]
        
        churn_class = int(prediction[0]) # 0 for No, 1 for Yes (based on SMOTE sorting, usually le)
        # Typically LabelEncoder alphabetical: "No" = 0, "Yes" = 1
        # SVM returns classes 0 or 1.
        
        is_churn = bool(churn_class == 1)
        confidence = probabilities[1] if is_churn else probabilities[0]
        
        return {
            "prediction": "Churn" if is_churn else "Stay",
            "confidence": round(float(confidence) * 100, 2)
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)