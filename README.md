# 🔮 Churn Oracle — AI-Powered Customer Retention Predictor

**Churn Oracle** is a high-performance machine learning web application designed to predict the likelihood of customer churn. Built with a focus on both technical rigor and premium user experience, it leverages a Support Vector Machine (SVC) engine to provide real-time retention insights through a sleek, glassmorphic interface.

![Project Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-05998b)

## ✨ Key Features

-   **Intelligent Prediction Engine**: Powered by a Support Vector Machine (SVC) model trained with **SMOTE** (Synthetic Minority Over-sampling Technique) to ensure high accuracy even with imbalanced datasets.
-   **Real-time Confidence Scoring**: Provides a percentage-based confidence level for every prediction, helping businesses gauge the reliability of each retention insight.
-   **Premium "Cyber-Oracle" UI**: A state-of-the-art frontend featuring:
    -   **Glassmorphism Design**: Frosted glass containers and vibrant background orbs.
    -   **Neon Aesthetics**: Sophisticated glow effects and interactive liquid-fill buttons.
    -   **Responsive Layout**: Optimized for both desktop and mobile viewing.
-   **Async Backend**: Built on **FastAPI** for ultra-low-latency inference and high concurrency handling.
-   **Robust Data Preprocessing**: Automatic handling of categorical encoding (One-Hot) and numerical scaling (StandardScaler) via a custom `ColumnTransformer` pipeline.

## 🛠️ Technology Stack

-   **Backend**: Python, FastAPI, Uvicorn, Pydantic.
-   **Machine Learning**: Scikit-learn (SVC), Imbalanced-learn (SMOTE), Pandas, Joblib.
-   **Frontend**: HTML5, Vanilla CSS3 (Modern Flexbox/Grid), JavaScript (ES6+ Fetch API).

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   `pip` (Python package manager)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/customer-churn-predict.git
    cd customer-churn-predict
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    python app.py
    ```

4.  **Access the Dashboard**:
    Open your browser and navigate to `http://localhost:8000`.

## 📂 Project Structure

```text
├── models/               # Pre-trained ML models and processors
├── static/               # Frontend assets (HTML, CSS, JS)
├── app.py                # FastAPI server and inference logic
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## 🧠 Machine Learning Pipeline

The underlying model was developed using a rigorous pipeline:
1.  **Data Cleaning**: Coercing `TotalCharges` to numeric and handling missing values.
2.  **Feature Engineering**: Transformation of categorical variables (Contract, Payment Method, etc.) and scaling of numerical metrics (Tenure, Charges).
3.  **Balancing**: Utilizing SMOTE to address the inherent class imbalance in churn data.
4.  **Optimization**: SVM kernel tuning for maximum separation between "Stay" and "Churn" classes.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with precision and style.*
