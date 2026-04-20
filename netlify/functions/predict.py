import json
import joblib
import pandas as pd
import os

# Load models globally so they state in memory between function calls
# Path is relative to this function file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSOR_PATH = os.path.join(BASE_DIR, "models", "processor.joblib")
MODEL_PATH = os.path.join(BASE_DIR, "models", "svm_model.joblib")

processor = None
svm_model = None

if os.path.exists(PROCESSOR_PATH) and os.path.exists(MODEL_PATH):
    processor = joblib.load(PROCESSOR_PATH)
    svm_model = joblib.load(MODEL_PATH)
    print("Models loaded successfully.")
else:
    print(f"ERROR: Models not found at {PROCESSOR_PATH}")

def handler(event, context):
    global processor, svm_model
    
    # Only allow POST
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

    try:
        if not processor or not svm_model:
            # Try reloading if not loaded
            if os.path.exists(PROCESSOR_PATH) and os.path.exists(MODEL_PATH):
                processor = joblib.load(PROCESSOR_PATH)
                svm_model = joblib.load(MODEL_PATH)
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'Prediction models not found on server.'})
                }

        # Parse input data
        data = json.loads(event['body'])
        
        # Convert input to DataFrame
        df = pd.DataFrame([data])
        
        # Preprocess
        X_processed = processor.transform(df)
        
        # Predict
        prediction = svm_model.predict(X_processed)
        probabilities = svm_model.predict_proba(X_processed)[0]
        
        churn_class = int(prediction[0])
        is_churn = bool(churn_class == 1)
        confidence = probabilities[1] if is_churn else probabilities[0]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "prediction": "Churn" if is_churn else "Stay",
                "confidence": round(float(confidence) * 100, 2)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
