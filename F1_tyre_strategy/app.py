import pandas as pd
import numpy as np
import traceback
from sklearn.linear_model import LinearRegression
import pandas as pd
import os
import glob
import streamlit as st
import joblib

model = joblib.load("xgb_model.joblib")



def load_latest_csv(folder="data"):
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in /data")
    return max(csv_files, key=os.path.getmtime)

def feature_engineering(df):
    
    columns = [
        'Year',
        'Session',
        'Driver',
        'DriverNumber',
        'LapTime',
        'LapSeconds',
        'LapNumber',
        'Stint',
        'PitOutTime',
        'PitInTime',
        'Compound',
        'TyreLife',
        'TrackTemp'
    ]
    
    df = df[columns].copy()

    # Correct compound mapping
    df["Compound"] = df["Compound"].map({"HARD": 1, "MEDIUM": 2, "SOFT": 3})

    # Convert laptimes
    #df["LapSeconds"] = df["LapTime"].dt.total_seconds()

    # Remove pit laps
    df = df[df["PitInTime"].isna() & df["PitOutTime"].isna()].copy()

    # Per-stint median pace
    df["StintMedian"] = df.groupby(["Driver", "Stint", "Session"])["LapSeconds"].transform("median")

    # Drop slow laps
    df = df[df["LapSeconds"] <= df["StintMedian"] + 1.5]

    df = df.sort_values(["Driver", "Year", "Session", "LapNumber"]).reset_index(drop=True)

    # Remove short stints (<3 laps)
    df["StintLength"] = df.groupby(["Driver", "Session", "Stint"])["LapSeconds"].transform("size")
    df = df[df["StintLength"] >= 3].copy()

    df = df.drop(columns=["PitInTime", "PitOutTime", "LapTime"])

    # ---------- Build stint_df ----------
    stint_rows = []

    for (driver, session, stint), g in df.groupby(["Driver", "Session", "Stint"]):

        X = g["LapNumber"].values.reshape(-1, 1)
        y = g["LapSeconds"].values
        model = LinearRegression().fit(X, y)

        stint_rows.append({
            "Driver": driver,
            "Session": session,
            "Stint": stint,
            "Compound": g["Compound"].iloc[0],
            "TyreLifeStart": g["TyreLife"].min(),
            "TyreLifeEnd": g["TyreLife"].max(),
            "AvgLap": g["LapSeconds"].mean(),
            "DegSlope": model.coef_[0],
            "StintLength": len(g),
            "AvgTrackTemp": g["TrackTemp"].mean(),
            "Year": g["Year"].iloc[0]
        })

    stint_df = pd.DataFrame(stint_rows)

    # ---------- Build driver-level features ----------
    features = []

    for driver, g in stint_df.groupby("Driver"):

        row = {
            "Driver": driver,
            "Year": g["Year"].iloc[0],
            "NumStints": len(g),
            "NumCompoundsUsed": g["Compound"].nunique(),
            "LongestStint": g["StintLength"].max(),
            "AvgPaceSoft": g[g["Compound"] == 3]["AvgLap"].mean(),
            "AvgPaceMedium": g[g["Compound"] == 2]["AvgLap"].mean(),
            "AvgPaceHard": g[g["Compound"] == 1]["AvgLap"].mean(),
            "DegSoft": g[g["Compound"] == 3]["DegSlope"].mean(),
            "DegMed": g[g["Compound"] == 2]["DegSlope"].mean(),
            "AvgTrackTemp": g["AvgTrackTemp"].mean(),
            "MaxTrackTemp": g["AvgTrackTemp"].max(),
            "MinTrackTemp": g["AvgTrackTemp"].min(),
            "DegHard": g[g["Compound"] == 1]["DegSlope"].mean()
        }

        features.append(row)

    final_df = pd.DataFrame(features)

    return final_df


st.set_page_config(
    page_title="F1 Strategy",
    page_icon="🏎️",     # race car emoji works as favicon
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.set_page_config(
    page_title="F1 Strategy",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

    /* -------------------------------------- */
    /* F1 LOGO (scrolls, zooms, behaves clean) */
    /* -------------------------------------- */
    .f1-logo-wrapper {
        width: 100%;
        display: flex;
        justify-content: flex-end;   /* push to RIGHT */
        margin-bottom: -1.5rem;      /* pull it closer to top */
        padding-right: 2rem;         /* move away from the edge */
    }

    .f1-logo-wrapper img {
        height: 240px;               /* BIG LOGO — adjust to taste */
        opacity: 0.95;
    }


    /* -------------------------------------- */
    /* BACKGROUND + DARK OVERLAY              */
    /* -------------------------------------- */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://cdn.wallpapersafari.com/99/40/Fsd5YP.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }

    /* Darken background so text is ALWAYS readable */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.45);
        z-index: 0;
    }

    /* Lift all app content above overlay */
    [data-testid="stAppViewContainer"] > div {
        position: relative;
        z-index: 1;
    }


    /* -------------------------------------- */
    /* GLOBAL TEXT COLOR + SHADOW             */
    /* -------------------------------------- */
    html, body, [data-testid="stMarkdownContainer"] {
        color: #E6E6E6 !important;
        text-shadow: 0 0 4px rgba(0,0,0,0.85);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        text-shadow: 0 0 6px rgba(0,0,0,1);
    }


    /* -------------------------------------- */
    /* FILE UPLOADER (grey + black text)      */
    /* -------------------------------------- */
    div[data-testid="stFileUploader"] > section {
        background-color: #707070 !important;
        border: 1px solid #999;
        padding: 15px;
        border-radius: 8px;
    }

    /* Make all text inside uploader black */
    div[data-testid="stFileUploader"] * {
        color: black !important;
        fill: black !important;
    }

    /* Fix Browse Files button */
    div[data-testid="stFileUploader"] button[kind="secondary"] {
        background-color: #c0c0c0 !important;
        color: black !important;
        border: 1px solid #888 !important;
        border-radius: 6px !important;
    }

    div[data-testid="stFileUploader"] button[kind="secondary"]:hover {
        background-color: #b0b0b0 !important;
        border-color: #666 !important;
    }


    /* -------------------------------------- */
    /* NUMBER INPUT FIELD                     */
    /* -------------------------------------- */
    div[data-testid="stNumberInput"] > div > input {
        background-color: #707070 !important;
        color: black !important;
        border: 1px solid #999;
    }

    div[data-testid="stNumberInput"] button {
        background-color: #c0c0c0 !important;
        color: black !important;
        border: 1px solid #888 !important;
    }


    /* -------------------------------------- */
    /* ALL BUTTONS (Generate, Download, etc.) */
    /* -------------------------------------- */
    div.stButton > button,
    div[data-testid="stDownloadButton"] > button {
        background-color: #c0c0c0 !important;
        color: black !important;
        border: 1px solid #888 !important;
        border-radius: 6px !important;
        padding: 0.6em 1.2em !important;
        font-weight: bold !important;
    }

    div.stButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #b0b0b0 !important;
        border-color: #666 !important;
    }

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div class="f1-logo-wrapper">
        <img src="https://images.seeklogo.com/logo-png/33/2/formula-1-logo-png_seeklogo-330361.png" alt="F1 logo">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .fastf1-credit {
        position: fixed;
        bottom: 10px;
        right: 15px;
        background: rgba(255, 255, 255, 0.85);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        color: #000000;
        z-index: 9999;
        box-shadow: 0px 0px 6px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="fastf1-credit">
        FastF1 data provided under license by Formula One World Championship Limited.<br>
        Processed using the FastF1 Python library developed by the OpenF1 community.<br>
        <a href="https://theoehrly.github.io/Fast-F1/" target="_blank">FastF1 Documentation</a>
    </div>
    """,
    unsafe_allow_html=True
)


st.title("F1 Tyre Strategy")

st.write("Upload a CSV or use the newest CSV from /data.")



uploaded_file = st.file_uploader("Upload CSV", type=["csv"])



if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded from upload.")
else:
    try:
        latest = load_latest_csv("data")
        st.info(f"Using latest CSV file: {latest}")
        df = pd.read_csv(latest)
    except Exception:
        st.error("No CSV in /data. Upload one.")
        st.stop()

grid_position = st.number_input(
    "Enter your starting grid position after penalties:",
    min_value=1, max_value=20, value=10
)

if st.button("Generate Features"):
    result_df = feature_engineering(df)

    # GridGroup logic
    def grid_group(p):
        if p <= 4: return "Front"
        elif p <= 10: return "Mid"
        else: return "Back"


    cat_type = pd.CategoricalDtype(categories=["Front", "Mid", "Back"], ordered=False)

 

    result_df["GridPosition"] = int(grid_position)
    result_df["GridGroup"] = (
        result_df["GridPosition"]
        .apply(grid_group)
        .astype(cat_type)
        .cat.codes
    )

    result_df = result_df.drop(columns=["Driver", "Year"])

    st.subheader("Generated Driver Features")
    st.dataframe(result_df)

    csv_data = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_data, "engineered_output.csv")

    prediction = model.predict(result_df)

    label_map = {
        0: "Conservative",
        1: "Neutral",
        2: "Aggressive"
    }
    pred_int = int(prediction[0])
    pred_label = label_map[pred_int]

    st.subheader("Model Prediction")
    st.write(pred_label)

    image_map = {
        "Conservative": "images/conservative.png",
        "Neutral": "images/neutral.png",
        "Aggressive": "images/aggressive.png"
     }

    st.image(image_map[pred_label], use_container_width=True)


