import json
import os

base = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\powerbi"
rep_dir = os.path.join(base, "AURA_FinTech_Risk.Report")
sem_dir = os.path.join(base, "AURA_FinTech_Risk.SemanticModel")
os.makedirs(rep_dir, exist_ok=True)
os.makedirs(sem_dir, exist_ok=True)

# 1. pbip root (standard strict schema without extra settings)
pbip = {
    "version": "1.0",
    "artifacts": [
        {"report": {"path": "AURA_FinTech_Risk.Report"}}
    ]
}
with open(os.path.join(base, "AURA_FinTech_Risk.pbip"), "w", encoding="utf-8") as f:
    json.dump(pbip, f, indent=2)

# 2. definition.pbir
pbir = {
    "version": "1.0",
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

# 4. report.json
report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json",
    "config": "{\"name\":\"AURA_FinTech_Risk_Report\",\"layouts\":[{\"id\":0,\"name\":\"Landscape\",\"reportWidth\":1280,\"reportHeight\":720}],\"activeSectionIndex\":0}",
    "layoutOptimization": 0,
    "resourcePackages": [],
    "sections": [
        {
            "name": "ReportSection_Boardroom",
            "displayName": "Executive Boardroom Cockpit",
            "displayOption": 1,
            "config": "{}",
            "visualContainers": [],
            "filters": []
        },
        {
            "name": "ReportSection_IFRS9",
            "displayName": "IFRS 9 Staging & ECL",
            "displayOption": 1,
            "config": "{}",
            "visualContainers": [],
            "filters": []
        },
        {
            "name": "ReportSection_Stress",
            "displayName": "Macro Stress Testing",
            "displayOption": 1,
            "config": "{}",
            "visualContainers": [],
            "filters": []
        },
        {
            "name": "ReportSection_AML",
            "displayName": "AML Surveillance Matrix",
            "displayOption": 1,
            "config": "{}",
            "visualContainers": [],
            "filters": []
        }
    ]
}
with open(os.path.join(rep_dir, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

# 5. model.bim with exact column names and types matching CSVs
csv_credit = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_credit_portfolio.csv".replace("\\", "\\\\")
csv_txn = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_transactions_stream.csv".replace("\\", "\\\\")
csv_macro = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\dim_macro_stress_scenarios.csv".replace("\\", "\\\\")

credit_cols = [
    ("Loan_ID", "string"),
    ("Customer_ID", "string"),
    ("Age", "int64"),
    ("Annual_Income_EUR", "double"),
    ("FICO_Score", "int64"),
    ("Debt_to_Income_DTI", "double"),
    ("Employment_Length_Years", "int64"),
    ("Loan_Amount_EUR", "double"),
    ("Loan_Purpose", "string"),
    ("Term_Months", "int64"),
    ("Interest_Rate_Pct", "double"),
    ("Days_Past_Due_DPD", "int64"),
    ("IFRS9_Stage", "string"),
    ("EAD_Exposure_EUR", "double"),
    ("LGD_Loss_Given_Default", "double"),
    ("PD_Probability_of_Default", "double"),
    ("ECL_Expected_Loss_EUR", "double"),
    ("Default_12M_Target", "int64"),
    ("Origination_Date", "dateTime"),
    ("Country", "string")
]

txn_cols = [
    ("Transaction_ID", "string"),
    ("Customer_ID", "string"),
    ("Channel", "string"),
    ("Amount_EUR", "double"),
    ("Is_Foreign_Counterparty", "int64"),
    ("Is_High_Risk_Jurisdiction", "int64"),
    ("Hourly_Velocity_Count", "int64"),
    ("AML_Suspicious_Flag", "int64"),
    ("Timestamp", "dateTime")
]

macro_cols = [
    ("Scenario", "string"),
    ("GDP_Growth_Pct", "double"),
    ("Inflation_HICP_Pct", "double"),
    ("Central_Bank_Rate_Pct", "double"),
    ("Unemployment_Pct", "double"),
    ("ECL_Stress_Multiplier", "double")
]

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
                "columns": [{"name": col, "dataType": dtype, "sourceColumn": col} for col, dtype in credit_cols],
                "partitions": [
                    {
                        "name": "Fact_Credit_Portfolio-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f"    Source = Csv.Document(File.Contents(\"{csv_credit}\"),[Delimiter=\",\", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
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
                "columns": [{"name": col, "dataType": dtype, "sourceColumn": col} for col, dtype in txn_cols],
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
                "columns": [{"name": col, "dataType": dtype, "sourceColumn": col} for col, dtype in macro_cols],
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

print("model.bim and PBIP successfully updated and synced!")
