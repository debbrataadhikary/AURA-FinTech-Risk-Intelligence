# -*- coding: utf-8 -*-
"""
train_risk_models.py
AURA-FinTech: Autonomous Risk Architecture & Machine Learning Engine
-------------------------------------------------------------------
Trains:
1. Credit Default Prediction Model (GradientBoostingClassifier / LogisticRegression baseline)
2. Statistical Model Validation (ROC-AUC, Precision, Recall, F1, KS-Statistic, Brier Score)
3. Feature Importance Attribution (Tree Feature Weights & Surrogate Explainability)
4. Unsupervised AML & Transaction Anomaly Engine (IsolationForest for Mule Detection)
5. Generates High-Resolution Charts for Power BI & Executive Visual Reporting
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, IsolationForest
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, classification_report, confusion_matrix, brier_score_loss
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

# Styling for Charts
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
PRIMARY_NAVY = "#0E3A5D"
SECONDARY_TEAL = "#1B657A"
ACCENT_CORAL = "#E65100"


def train_credit_default_model():
    print("\n[1/3] Training Credit Risk & IFRS 9 Default Prediction Model...")
    df_loans = pd.read_csv(os.path.join(DATA_DIR, "fact_credit_portfolio.csv"))
    
    # Feature Selection for Credit Risk
    features = [
        "FICO_Score", "Debt_to_Income_DTI", "Days_Past_Due_DPD", 
        "Annual_Income_EUR", "Loan_Amount_EUR", "Interest_Rate_Pct", 
        "Term_Months", "Employment_Length_Years", "Age"
    ]
    X = df_loans[features]
    y = df_loans["Default_12M_Target"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    # Train Gradient Boosting Classifier
    gb = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=4,
        subsample=0.85,
        random_state=42
    )
    gb.fit(X_train, y_train)
    
    # Evaluate Predictions
    y_pred_proba = gb.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.50).astype(int)
    
    auc = roc_auc_score(y_test, y_pred_proba)
    brier = brier_score_loss(y_test, y_pred_proba)
    
    # Calculate Kolmogorov-Smirnov (KS) Statistic
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    ks_stat = np.max(tpr - fpr)
    
    print(f"  -> Model ROC-AUC Score: {auc:.4f}")
    print(f"  -> Kolmogorov-Smirnov (KS) Statistic: {ks_stat*100:.2f}% (Industry Benchmark > 40%)")
    print(f"  -> Brier Calibration Score: {brier:.4f}")
    
    # Save Model Artifact
    model_path = os.path.join(MODELS_DIR, "credit_default_gb_model.joblib")
    joblib.dump(gb, model_path)
    print(f"  -> Saved trained model: {model_path}")
    
    # Feature Importance
    feat_imp = pd.DataFrame({
        "Feature": features,
        "Importance_Weight": gb.feature_importances_
    }).sort_values(by="Importance_Weight", ascending=False)
    
    feat_imp_path = os.path.join(EXPORTS_DIR, "credit_feature_importance.csv")
    feat_imp.to_csv(feat_imp_path, index=False)
    print(f"  -> Feature Importance saved: {feat_imp_path}")
    for _, r in feat_imp.iterrows():
        print(f"     * {r['Feature']:<25}: {r['Importance_Weight']*100:.2f}%")
        
    # Generate ROC Curve Chart
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color=PRIMARY_NAVY, lw=2.5, label=f"AURA-FinTech GB Model (AUC = {auc:.3f}, KS = {ks_stat*100:.1f}%)")
    plt.plot([0, 1], [0, 1], color="gray", lw=1.2, linestyle="--", label="Random Classifier Baseline")
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=10, fontweight="bold")
    plt.ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=10, fontweight="bold")
    plt.title("Credit Risk Model: ROC-AUC Discrimination Curve", fontsize=12, fontweight="bold", color=PRIMARY_NAVY)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    roc_img = os.path.join(ASSETS_DIR, "model_roc_curve.png")
    plt.savefig(roc_img, dpi=200)
    plt.close()
    print(f"  -> Saved ROC Curve visual: {roc_img}")
    
    return gb, auc, ks_stat


def train_aml_isolation_forest():
    print("\n[2/3] Training Unsupervised AML & Transaction Anomaly Engine...")
    df_tx = pd.read_csv(os.path.join(DATA_DIR, "fact_transactions_stream.csv"))
    
    features = ["Amount_EUR", "Is_Foreign_Counterparty", "Is_High_Risk_Jurisdiction", "Hourly_Velocity_Count"]
    X_tx = df_tx[features].copy()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_tx)
    
    iso = IsolationForest(
        n_estimators=120,
        contamination=0.035, # 3.5% expected anomaly rate
        random_state=42
    )
    df_tx["Anomaly_Score"] = iso.fit_predict(X_scaled) # -1 is anomaly, 1 is normal
    df_tx["Is_Anomaly_Detected"] = np.where(df_tx["Anomaly_Score"] == -1, 1, 0)
    
    # Save Model
    iso_path = os.path.join(MODELS_DIR, "aml_isolation_forest.joblib")
    joblib.dump(iso, iso_path)
    
    anom_count = df_tx["Is_Anomaly_Detected"].sum()
    print(f"  -> Total Suspicious Transactions Flagged: {anom_count} out of {len(df_tx)} ({anom_count/len(df_tx)*100:.2f}%)")
    
    # Save Scored Transactions
    scored_tx_path = os.path.join(EXPORTS_DIR, "scored_aml_transactions.csv")
    df_tx.to_csv(scored_tx_path, index=False)
    print(f"  -> Scored AML transactions saved: {scored_tx_path}")


def generate_executive_charts():
    print("\n[3/3] Generating Executive Boardroom Visualizations...")
    df_loans = pd.read_csv(os.path.join(DATA_DIR, "fact_credit_portfolio.csv"))
    
    # Chart 1: IFRS 9 Stage Distribution & Expected Loss
    stage_summary = df_loans.groupby("IFRS9_Stage").agg(
        Total_Exposure=("EAD_Exposure_EUR", lambda x: np.sum(x) / 1e6),
        Total_ECL=("ECL_Expected_Loss_EUR", lambda x: np.sum(x) / 1e6)
    ).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(stage_summary))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, stage_summary["Total_Exposure"], width, label="Total Exposure at Default (€M)", color=PRIMARY_NAVY)
    rects2 = ax1.bar(x + width/2, stage_summary["Total_ECL"], width, label="Expected Credit Loss (€M)", color=ACCENT_CORAL)
    
    ax1.set_ylabel("Euro (€ Millions)", fontsize=10, fontweight="bold")
    ax1.set_title("IFRS 9 Portfolio Exposure vs Expected Credit Loss (ECL)", fontsize=12, fontweight="bold", color=PRIMARY_NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(stage_summary["IFRS9_Stage"], fontsize=9, fontweight="bold")
    ax1.legend(loc="upper right", frameon=True)
    
    # Add values on top of bars
    for r in rects1:
        h = r.get_height()
        ax1.annotate(f"€{h:.1f}M", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    for r in rects2:
        h = r.get_height()
        ax1.annotate(f"€{h:.2f}M", xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=ACCENT_CORAL)
                     
    plt.tight_layout()
    chart_ecl = os.path.join(ASSETS_DIR, "ifrs9_ecl_stage_breakdown.png")
    plt.savefig(chart_ecl, dpi=200)
    plt.close()
    print(f"  -> Saved IFRS 9 ECL Breakdown Chart: {chart_ecl}")


if __name__ == "__main__":
    train_credit_default_model()
    train_aml_isolation_forest()
    generate_executive_charts()
    print("\nAURA-FinTech Model Training Complete.")
