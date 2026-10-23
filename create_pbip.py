import json
import os

base = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\powerbi"
rep_dir = os.path.join(base, "AURA_FinTech_Risk.Report")
sem_dir = os.path.join(base, "AURA_FinTech_Risk.SemanticModel")
os.makedirs(rep_dir, exist_ok=True)
os.makedirs(sem_dir, exist_ok=True)

# 1. pbip root
pbip = {
    "version": "1.0",
    "artifacts": [
        {"report": {"path": "AURA_FinTech_Risk.Report"}}
    ],
    "settings": {
        "enableAutoAuth": True
    }
}
with open(os.path.join(base, "AURA_FinTech_Risk.pbip"), "w", encoding="utf-8") as f:
    json.dump(pbip, f, indent=2)

# 2. definition.pbir
pbir = {
    "version": "4.0",
    "datasetReference": {
        "byPath": {"path": "../AURA_FinTech_Risk.SemanticModel"},
        "byConnection": None
    }
}
with open(os.path.join(rep_dir, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir, f, indent=2)

# 3. definition.pbism
pbism = {
    "version": "1.0"
}
with open(os.path.join(sem_dir, "definition.pbism"), "w", encoding="utf-8") as f:
    json.dump(pbism, f, indent=2)

# 4. model.bim
csv_credit = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_credit_portfolio.csv".replace("\\", "\\\\")
csv_txn = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_transactions_stream.csv".replace("\\", "\\\\")
csv_macro = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\dim_macro_stress_scenarios.csv".replace("\\", "\\\\")

bim = {
    "name": "AURA_FinTech_SemanticModel",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "tables": [
            {
                "name": "Fact_Credit_Portfolio",
                "columns": [
                    {"name": "loan_id", "dataType": "string", "sourceColumn": "loan_id"},
                    {"name": "customer_id", "dataType": "string", "sourceColumn": "customer_id"},
                    {"name": "credit_score", "dataType": "int64", "sourceColumn": "credit_score"},
                    {"name": "debt_to_income", "dataType": "double", "sourceColumn": "debt_to_income"},
                    {"name": "annual_income", "dataType": "double", "sourceColumn": "annual_income"},
                    {"name": "revolving_utilization", "dataType": "double", "sourceColumn": "revolving_utilization"},
                    {"name": "delinquency_history", "dataType": "int64", "sourceColumn": "delinquency_history"},
                    {"name": "loan_tenor_months", "dataType": "int64", "sourceColumn": "loan_tenor_months"},
                    {"name": "ead_exposure", "dataType": "double", "sourceColumn": "ead_exposure"},
                    {"name": "lgd_percentage", "dataType": "double", "sourceColumn": "lgd_percentage"},
                    {"name": "pd_calibrated", "dataType": "double", "sourceColumn": "pd_calibrated"},
                    {"name": "ifrs9_stage", "dataType": "string", "sourceColumn": "ifrs9_stage"},
                    {"name": "ifrs9_ecl_amount", "dataType": "double", "sourceColumn": "ifrs9_ecl_amount"},
                    {"name": "risk_weight", "dataType": "double", "sourceColumn": "risk_weight"},
                    {"name": "default_target_12m", "dataType": "int64", "sourceColumn": "default_target_12m"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Credit_Portfolio-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f"    Source = Csv.Document(File.Contents(\"{csv_credit}\"),[Delimiter=\",\", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])",
                                "in",
                                "    #\"Promoted Headers\""
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Fact_Transactions_Stream",
                "columns": [
                    {"name": "txn_id", "dataType": "string", "sourceColumn": "txn_id"},
                    {"name": "customer_id", "dataType": "string", "sourceColumn": "customer_id"},
                    {"name": "txn_amount", "dataType": "double", "sourceColumn": "txn_amount"},
                    {"name": "txn_channel", "dataType": "string", "sourceColumn": "txn_channel"},
                    {"name": "is_foreign_counterparty", "dataType": "int64", "sourceColumn": "is_foreign_counterparty"},
                    {"name": "is_high_risk_jurisdiction", "dataType": "int64", "sourceColumn": "is_high_risk_jurisdiction"},
                    {"name": "hourly_velocity_count", "dataType": "int64", "sourceColumn": "hourly_velocity_count"},
                    {"name": "structuring_flag", "dataType": "int64", "sourceColumn": "structuring_flag"},
                    {"name": "is_aml_flagged", "dataType": "int64", "sourceColumn": "is_aml_flagged"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Transactions_Stream-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f"    Source = Csv.Document(File.Contents(\"{csv_txn}\"),[Delimiter=\",\", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])",
                                "in",
                                "    #\"Promoted Headers\""
                            ]
                        }
                    }
                ]
            },
            {
                "name": "Dim_Macro_Stress",
                "columns": [
                    {"name": "scenario_name", "dataType": "string", "sourceColumn": "scenario_name"},
                    {"name": "gdp_shock_pct", "dataType": "double", "sourceColumn": "gdp_shock_pct"},
                    {"name": "inflation_rate_pct", "dataType": "double", "sourceColumn": "inflation_rate_pct"},
                    {"name": "central_bank_rate_pct", "dataType": "double", "sourceColumn": "central_bank_rate_pct"},
                    {"name": "unemployment_rate_pct", "dataType": "double", "sourceColumn": "unemployment_rate_pct"},
                    {"name": "ecl_stress_multiplier", "dataType": "double", "sourceColumn": "ecl_stress_multiplier"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Macro_Stress-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f"    Source = Csv.Document(File.Contents(\"{csv_macro}\"),[Delimiter=\",\", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])",
                                "in",
                                "    #\"Promoted Headers\""
                            ]
                        }
                    }
                ]
            }
        ]
    }
}
with open(os.path.join(sem_dir, "model.bim"), "w", encoding="utf-8") as f:
    json.dump(bim, f, indent=2)

print("PBIP successfully generated at:", os.path.join(base, "AURA_FinTech_Risk.pbip"))
