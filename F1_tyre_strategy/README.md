# F1 Tyre Strategy Prediction Project

This project builds a complete end-to-end pipeline for predicting Formula 1 race tyre strategies using FastF1 telemetry. The workflow includes data extraction, feature engineering, supervised learning, target generation, and a Streamlit app that provides live strategy predictions.

## 1. Project Overview

Tyre strategy is one of the most influential factors in race performance. This project predicts a driver’s likely race strategy, classified into three categories:

- Aggressive
- Neutral
- Conservative

The final deployed model uses XGBoost, which outperforms the Random Forest baseline on accuracy and generalisation.

## 2. Project Structure

```
Capstone/
│
├── cache/                     # FastF1 session data (offline loading)
├── data/                      # Cleaned CSV outputs (features + targets)
├── images/                    # Strategy images for Streamlit UI
│
├── app.py                     # Streamlit prediction application
├── xgb_model.joblib           # Final trained XGBoost model
│
├── f1_practice_features.csv   # Engineered driver features
├── f1_race_results.csv        # Raw race result data
│
├── feature_generation.ipynb   # Feature engineering pipeline
├── target_generation.ipynb    # Strategy target creation
├── model.ipynb                # Model training and evaluation
└── Project_management/        # Notes, planning, documentation
```

## 3. Data Pipeline

### 3.1 Data Extraction
FastF1 is used to download weekend session data into a local cache. Once downloaded, all future loads are offline and fast.

### 3.2 Feature Engineering
`feature_generation.ipynb` produces `f1_practice_features.csv` containing:

- Lap times and stint windows
- Compound usage
- Track temperature metrics
- Driver and session identifiers
- Derived pace and degradation features
- Aggregated practice session performance indicators

### 3.3 Target Generation
`target_generation.ipynb` creates the supervised labels. Drivers are categorised into:

1. Aggressive  
2. Neutral  
3. Conservative  

These labels are used as targets for model training.

## 4. Models

Two models were developed and evaluated:

### Random Forest
- Baseline model  
- Reasonable predictive performance  
- Lower generalisation on unseen race weekends  

### XGBoost
- Best performing model  
- Handles imbalance and non-linear patterns effectively  
- Strong performance across multiple seasons and circuits  

The final model is saved as:

```
xgb_model.joblib
```

## 5. Streamlit Application

`app.py` contains the complete user interface and prediction logic.

Key features:

- Detects or uploads the latest feature CSV  
- Performs automated feature engineering  
- Loads and runs the XGBoost model  
- Converts numeric predictions to labels:
  - 0 → Conservative  
  - 1 → Neutral  
  - 2 → Aggressive  
- Displays a strategy image  
- Uses custom CSS for an F1-themed dark UI  

Run the app using:

```
open https://tehill1910-projects-f1-tyre-strategyapp-v9chya.streamlit.app
```

## 6. How to Reproduce

1. Install dependencies  
2. Enable FastF1 cache  
3. Run `feature_generation.ipynb`  
4. Run `target_generation.ipynb`  
5. Train using `model.ipynb`  
6. Launch the Streamlit app  

## 7. Requirements

Main packages:

- fastf1  
- pandas  
- numpy  
- scikit-learn  
- xgboost  
- joblib  
- streamlit  

Install all requirements:

```
pip install -r requirements.txt
```

## 8. Future Improvements

- Compare predictions with actual race outcomes  
- Extend dataset to more seasons  
- Add grid position buckets  
- Build multi-step sequence prediction  
- Introduce SHAP explainability for transparency  
