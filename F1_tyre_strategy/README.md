# F1 Tyre Strategy Prediction Project

This project builds a full end to end pipeline for predicting Formula 1 race tyre strategies using FastF1 data. The workflow covers data extraction, feature engineering, target generation, model training, and an interactive Streamlit app that produces live predictions.

## 1. Project Overview

Tyre strategy is one of the most influential factors in race performance. The goal is to predict a driver’s most likely race strategy. The model predicts one of three categories:

- Aggressive
- Neutral
- Conservative

The final deployed model uses XGBoost, which outperforms the Random Forest baseline.

## 2. Project Structure

```
Capstone/
│
├── cache/                   # FastF1 downloaded session data
├── data/                    # Cleaned CSV outputs for features and targets
├── images/                  # Images for Streamlit UI
│
├── app.py                   # Streamlit prediction application
├── xgb_model.joblib         # Final trained XGBoost model
│
├── f1_practice_features.csv # Engineered features
├── f1_race_results.csv      # Raw race result data
│
├── feature_generation.ipynb # Feature engineering pipeline
├── target_generation.ipynb  # Generate strategy target labels
├── model.ipynb              # Model training and evaluation
└── Project_management/      # Notes and planning material
```

## 3. Data Pipeline

### 3.1 Data Extraction
FastF1 is used to download session data into the cache folder. After downloading once, the cache enables very fast loading without further internet use.

### 3.2 Feature Engineering
The notebook feature_generation.ipynb creates f1_practice_features.csv which includes:

- Lap times
- Tyre compound
- Stint data
- Track temperature
- Driver metadata
- Derived numerical features
- Aggregated practice session metrics

### 3.3 Target Generation
The notebook target_generation.ipynb produces the label dataset for supervised learning.

Drivers are grouped into one of three strategy types:

1. Aggressive
2. Neutral
3. Conservative

## 4. Models

Two supervised learning models were built:

### Random Forest
- Baseline model
- Reasonable results
- Lower performance on unseen races

### XGBoost
- Best performing model
- Handles imbalance and non linear behaviour
- Strong generalisation across races

The final trained model is saved as:

```
xgb_model.joblib
```

## 5. Streamlit Application

The file app.py contains the deployed user interface.

Key features:

- Detects or uploads the latest CSV
- Automatically performs feature engineering
- Loads the XGBoost model for inference
- Converts numeric model output back to labels:
  - 0 → Aggressive
  - 1 → Conservative
  - 2 → Neutral
- Displays an image representing the predicted strategy
- Includes custom CSS for an F1 themed UI

Run the app with:

```
streamlit run app.py
```

## 6. How to Reproduce

1. Install dependencies
2. Enable FastF1 cache
3. Run feature_generation.ipynb
4. Run target_generation.ipynb
5. Train using model.ipynb
6. Launch Streamlit UI

## 7. Requirements

Main packages:

- fastf1
- pandas
- numpy
- scikit learn
- xgboost
- joblib
- streamlit

Install all dependencies:

```
pip install -r requirements.txt
```

## 8. Future Improvements

- Add comparison against real race results
- Expand dataset to additional seasons
- Introduce grid position buckets
- Build a more detailed multi step strategy classifier
- Add SHAP explainability for model transparency
