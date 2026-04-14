import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="CO2 Adsorption Experiment Analyzer", layout="wide")

st.title("CO₂ Adsorption Experiment Analyzer")
st.write(
    "Upload adsorption experiment data to calculate adsorption capacity, "
    "removal efficiency, and generate plots."
)

with st.expander("Expected columns"):
    st.markdown(
        '''
        Required columns:
        - `sample`
        - `time_min`
        - `C0`
        - `Ct`
        - `volume_L`
        - `mass_g`
        '''
    )

uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

def validate_columns(df: pd.DataFrame):
    required = {"sample", "time_min", "C0", "Ct", "volume_L", "mass_g"}
    return sorted(list(required - set(df.columns)))

def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["removal_efficiency_percent"] = ((out["C0"] - out["Ct"]) / out["C0"]) * 100
    out["q_t"] = ((out["C0"] - out["Ct"]) * out["volume_L"]) / out["mass_g"]
    return out

def summarize(df: pd.DataFrame) -> pd.DataFrame:
    idx = df.groupby("sample")["time_min"].idxmax()
    final_rows = df.loc[idx].copy()
    final_rows = final_rows.rename(columns={"Ct": "final_Ct", "q_t": "final_qt"})
    summary = final_rows[
        ["sample", "time_min", "final_Ct", "final_qt", "removal_efficiency_percent"]
    ].sort_values("final_qt", ascending=False)
    summary = summary.rename(columns={
        "time_min": "final_time_min",
        "removal_efficiency_percent": "final_removal_efficiency_percent"
    })
    return summary.reset_index(drop=True)

if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    missing = validate_columns(df)
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()

    for col in ["time_min", "C0", "Ct", "volume_L", "mass_g"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["sample", "time_min", "C0", "Ct", "volume_L", "mass_g"]).copy()
    results = compute_metrics(df)
    summary = summarize(results)

    st.subheader("Calculated results")
    st.dataframe(results, use_container_width=True)

    st.subheader("Final sample summary")
    st.dataframe(summary, use_container_width=True)

    st.subheader("Concentration vs Time")
    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    for sample, grp in results.groupby("sample"):
        grp = grp.sort_values("time_min")
        ax1.plot(grp["time_min"], grp["Ct"], marker="o", label=sample)
    ax1.set_xlabel("Time (min)")
    ax1.set_ylabel("Ct")
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("Adsorption Capacity vs Time")
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    for sample, grp in results.groupby("sample"):
        grp = grp.sort_values("time_min")
        ax2.plot(grp["time_min"], grp["q_t"], marker="o", label=sample)
    ax2.set_xlabel("Time (min)")
    ax2.set_ylabel("q_t")
    ax2.legend()
    st.pyplot(fig2)

    st.subheader("Final Removal Efficiency by Sample")
    fig3, ax3 = plt.subplots(figsize=(8, 4.5))
    ax3.bar(summary["sample"], summary["final_removal_efficiency_percent"])
    ax3.set_xlabel("Sample")
    ax3.set_ylabel("Removal Efficiency (%)")
    plt.xticks(rotation=20)
    st.pyplot(fig3)

    st.download_button(
        "Download calculated results CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="co2_adsorption_calculated_results.csv",
        mime="text/csv",
    )

    st.download_button(
        "Download final summary CSV",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="co2_adsorption_summary.csv",
        mime="text/csv",
    )
else:
    st.info("Upload sample_data.csv from this package to test the app.")
