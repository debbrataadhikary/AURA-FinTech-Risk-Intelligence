import os
import json

base_pbi = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\powerbi"
sem_dir = os.path.join(base_pbi, "AURA_FinTech_Risk.SemanticModel")
tables_dir = os.path.join(sem_dir, "definition", "tables")
rep_dir = os.path.join(base_pbi, "AURA_FinTech_Risk.Report")

csv_credit = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_credit_portfolio.csv".replace("\\", "\\\\")
csv_txn = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\fact_transactions_stream.csv".replace("\\", "\\\\")
csv_macro = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\data\dim_macro_stress_scenarios.csv".replace("\\", "\\\\")

# 1. Fact_Credit_Portfolio.tmdl
tmdl_credit = """table Fact_Credit_Portfolio
\tlineageTag: 5be31a46-b17b-437f-85c7-bbec180ea2af

\tcolumn Loan_ID
\t\tdataType: string
\t\tlineageTag: 0ed84613-e10c-41eb-b380-b06faf73996f
\t\tsummarizeBy: none
\t\tsourceColumn: Loan_ID

\tcolumn Customer_ID
\t\tdataType: string
\t\tlineageTag: acf62202-59b0-491b-ade4-3b8a3b92c1ad
\t\tsummarizeBy: none
\t\tsourceColumn: Customer_ID

\tcolumn Age
\t\tdataType: int64
\t\tlineageTag: 5e931219-2f80-4b10-bc7f-8bba7c030119
\t\tsummarizeBy: average
\t\tsourceColumn: Age

\tcolumn Annual_Income_EUR
\t\tdataType: double
\t\tlineageTag: 5b816731-d746-4480-b3d8-382a04558034
\t\tsummarizeBy: sum
\t\tsourceColumn: Annual_Income_EUR
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn FICO_Score
\t\tdataType: int64
\t\tlineageTag: 65435e45-e2fc-4507-a14a-6646637a193e
\t\tsummarizeBy: average
\t\tsourceColumn: FICO_Score

\tcolumn Debt_to_Income_DTI
\t\tdataType: double
\t\tlineageTag: f910d6ce-829c-46bf-b2d7-a7eafcb9fa57
\t\tsummarizeBy: average
\t\tsourceColumn: Debt_to_Income_DTI
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Employment_Length_Years
\t\tdataType: int64
\t\tlineageTag: 13af849d-2190-4069-b36a-9f226262e178
\t\tsummarizeBy: average
\t\tsourceColumn: Employment_Length_Years

\tcolumn Loan_Amount_EUR
\t\tdataType: double
\t\tlineageTag: 15dc3ccc-0407-4686-888a-a21290e037ab
\t\tsummarizeBy: sum
\t\tsourceColumn: Loan_Amount_EUR
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Loan_Purpose
\t\tdataType: string
\t\tlineageTag: 8852e690-32df-4c28-97c7-0eeadbbcf03c
\t\tsummarizeBy: none
\t\tsourceColumn: Loan_Purpose

\tcolumn Term_Months
\t\tdataType: int64
\t\tlineageTag: 66a3aa8f-2877-43f1-b851-ca6cfa50c4ad
\t\tsummarizeBy: average
\t\tsourceColumn: Term_Months

\tcolumn Interest_Rate_Pct
\t\tdataType: double
\t\tlineageTag: f4c3f59e-14f7-41a4-9ecb-e7b398dfaa04
\t\tsummarizeBy: average
\t\tsourceColumn: Interest_Rate_Pct
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Days_Past_Due_DPD
\t\tdataType: int64
\t\tlineageTag: ad071279-d10d-45f8-a006-21820684cf05
\t\tsummarizeBy: sum
\t\tsourceColumn: Days_Past_Due_DPD

\tcolumn IFRS9_Stage
\t\tdataType: string
\t\tlineageTag: b699f485-6126-444a-953e-32b509bc050e
\t\tsummarizeBy: none
\t\tsourceColumn: IFRS9_Stage

\tcolumn EAD_Exposure_EUR
\t\tdataType: double
\t\tlineageTag: 8eb512c0-7cf1-4ec4-9df2-5ec24b330364
\t\tsummarizeBy: sum
\t\tsourceColumn: EAD_Exposure_EUR
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn LGD_Loss_Given_Default
\t\tdataType: double
\t\tlineageTag: a0391d4e-b73a-4ef3-be5b-86ba6bf4f620
\t\tsummarizeBy: average
\t\tsourceColumn: LGD_Loss_Given_Default
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn PD_Probability_of_Default
\t\tdataType: double
\t\tlineageTag: 489437ff-99d9-4fa2-bcda-3adfb3763f35
\t\tsummarizeBy: average
\t\tsourceColumn: PD_Probability_of_Default
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn ECL_Expected_Loss_EUR
\t\tdataType: double
\t\tlineageTag: 1c55d3e1-3193-499a-8b5e-49a840d09d82
\t\tsummarizeBy: sum
\t\tsourceColumn: ECL_Expected_Loss_EUR
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Default_12M_Target
\t\tdataType: int64
\t\tlineageTag: 29f19652-f44e-46db-8621-d36b21e15e99
\t\tsummarizeBy: sum
\t\tsourceColumn: Default_12M_Target

\tcolumn Origination_Date
\t\tdataType: dateTime
\t\tformatString: General Date
\t\tlineageTag: f035bc25-3446-4a33-9b51-922706e5a80b
\t\tsummarizeBy: none
\t\tsourceColumn: Origination_Date

\tcolumn Country
\t\tdataType: string
\t\tlineageTag: de4570e3-a06f-4940-8232-e6a220528406
\t\tsummarizeBy: none
\t\tsourceColumn: Country

\tpartition Fact_Credit_Portfolio-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("__CSV_CREDIT__"),[Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    ChangedType = Table.TransformColumnTypes(PromotedHeaders,{{"Loan_ID", type text}, {"Customer_ID", type text}, {"Age", Int64.Type}, {"Annual_Income_EUR", type number}, {"FICO_Score", Int64.Type}, {"Debt_to_Income_DTI", type number}, {"Employment_Length_Years", Int64.Type}, {"Loan_Amount_EUR", type number}, {"Loan_Purpose", type text}, {"Term_Months", Int64.Type}, {"Interest_Rate_Pct", type number}, {"Days_Past_Due_DPD", Int64.Type}, {"IFRS9_Stage", type text}, {"EAD_Exposure_EUR", type number}, {"LGD_Loss_Given_Default", type number}, {"PD_Probability_of_Default", type number}, {"ECL_Expected_Loss_EUR", type number}, {"Default_12M_Target", Int64.Type}, {"Origination_Date", type datetime}, {"Country", type text}})
\t\t\t\tin
\t\t\t\t    ChangedType
""".replace("__CSV_CREDIT__", csv_credit)

with open(os.path.join(tables_dir, "Fact_Credit_Portfolio.tmdl"), "w", encoding="utf-8") as f:
    f.write(tmdl_credit)

# 2. Fact_Transactions_Stream.tmdl
tmdl_txn = """table Fact_Transactions_Stream
\tlineageTag: c219de19-21df-41ef-bf74-27ee389e87af

\tcolumn Transaction_ID
\t\tdataType: string
\t\tlineageTag: 247183e8-8a9d-4c3e-812d-0b73138b5551
\t\tsummarizeBy: none
\t\tsourceColumn: Transaction_ID

\tcolumn Customer_ID
\t\tdataType: string
\t\tlineageTag: a3f3e1a0-6c9f-4318-9ef4-c154316715f2
\t\tsummarizeBy: none
\t\tsourceColumn: Customer_ID

\tcolumn Channel
\t\tdataType: string
\t\tlineageTag: e4857418-5a2a-4420-bfef-c7db11b421a1
\t\tsummarizeBy: none
\t\tsourceColumn: Channel

\tcolumn Amount_EUR
\t\tdataType: double
\t\tlineageTag: db341851-38e9-41fa-8fbc-61327173e1c2
\t\tsummarizeBy: sum
\t\tsourceColumn: Amount_EUR
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Is_Foreign_Counterparty
\t\tdataType: int64
\t\tlineageTag: e983058a-36ee-4890-84a1-8d07e600579e
\t\tsummarizeBy: sum
\t\tsourceColumn: Is_Foreign_Counterparty

\tcolumn Is_High_Risk_Jurisdiction
\t\tdataType: int64
\t\tlineageTag: 3ea416d8-80f2-45e0-99e1-e630d7aa5267
\t\tsummarizeBy: sum
\t\tsourceColumn: Is_High_Risk_Jurisdiction

\tcolumn Hourly_Velocity_Count
\t\tdataType: int64
\t\tlineageTag: 3676c666-4c4f-40e8-8687-73ee9707e38a
\t\tsummarizeBy: sum
\t\tsourceColumn: Hourly_Velocity_Count

\tcolumn AML_Suspicious_Flag
\t\tdataType: int64
\t\tlineageTag: e9aa123b-55cf-4df5-bd84-c89bdfd257a0
\t\tsummarizeBy: sum
\t\tsourceColumn: AML_Suspicious_Flag

\tcolumn Timestamp
\t\tdataType: dateTime
\t\tformatString: General Date
\t\tlineageTag: 18ee8755-9ee8-4ec2-9e80-d6e2776c9ef5
\t\tsummarizeBy: none
\t\tsourceColumn: Timestamp

\tpartition Fact_Transactions_Stream-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("__CSV_TXN__"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    ChangedType = Table.TransformColumnTypes(PromotedHeaders,{{"Transaction_ID", type text}, {"Customer_ID", type text}, {"Channel", type text}, {"Amount_EUR", type number}, {"Is_Foreign_Counterparty", Int64.Type}, {"Is_High_Risk_Jurisdiction", Int64.Type}, {"Hourly_Velocity_Count", Int64.Type}, {"AML_Suspicious_Flag", Int64.Type}, {"Timestamp", type datetime}})
\t\t\t\tin
\t\t\t\t    ChangedType
""".replace("__CSV_TXN__", csv_txn)

with open(os.path.join(tables_dir, "Fact_Transactions_Stream.tmdl"), "w", encoding="utf-8") as f:
    f.write(tmdl_txn)

# 3. Dim_Macro_Stress.tmdl
tmdl_macro = """table Dim_Macro_Stress
\tlineageTag: 928374a1-b8ef-41fa-8a9d-5364718a9ef1

\tcolumn Scenario
\t\tdataType: string
\t\tlineageTag: e372b849-0fa1-447a-8efb-665518b06c01
\t\tsummarizeBy: none
\t\tsourceColumn: Scenario

\tcolumn GDP_Growth_Pct
\t\tdataType: double
\t\tlineageTag: f4728d11-e1ef-40bc-9e11-137bfa0057aa
\t\tsummarizeBy: average
\t\tsourceColumn: GDP_Growth_Pct
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Inflation_HICP_Pct
\t\tdataType: double
\t\tlineageTag: 48937bca-9efa-4e90-8e10-dbcfb1806a09
\t\tsummarizeBy: average
\t\tsourceColumn: Inflation_HICP_Pct
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Central_Bank_Rate_Pct
\t\tdataType: double
\t\tlineageTag: a1847cbb-18ef-4cfa-93e1-87bbca0038aa
\t\tsummarizeBy: average
\t\tsourceColumn: Central_Bank_Rate_Pct
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn Unemployment_Pct
\t\tdataType: double
\t\tlineageTag: b3847acc-28fa-4efa-84e1-27ee810029aa
\t\tsummarizeBy: average
\t\tsourceColumn: Unemployment_Pct
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tcolumn ECL_Stress_Multiplier
\t\tdataType: double
\t\tlineageTag: c4847add-38fa-4ffa-75e1-38ff910018aa
\t\tsummarizeBy: average
\t\tsourceColumn: ECL_Stress_Multiplier
\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}

\tpartition Dim_Macro_Stress-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("__CSV_MACRO__"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    ChangedType = Table.TransformColumnTypes(PromotedHeaders,{{"Scenario", type text}, {"GDP_Growth_Pct", type number}, {"Inflation_HICP_Pct", type number}, {"Central_Bank_Rate_Pct", type number}, {"Unemployment_Pct", type number}, {"ECL_Stress_Multiplier", type number}})
\t\t\t\tin
\t\t\t\t    ChangedType
""".replace("__CSV_MACRO__", csv_macro)

with open(os.path.join(tables_dir, "Dim_Macro_Stress.tmdl"), "w", encoding="utf-8") as f:
    f.write(tmdl_macro)

# 4. Update v0kpis to strictly use Fact_Credit_Portfolio
kpi_json_path = os.path.join(rep_dir, "definition", "pages", "ReportSection1", "visuals", "v0kpis", "visual.json")
kpi1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v0kpis",
    "position": {"x": 12, "y": 60, "z": 1000, "height": 110, "width": 960, "tabOrder": 1000},
    "visual": {
        "visualType": "multiRowCard",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.EAD_Exposure_EUR)",
                            "nativeQueryRef": "Total_EAD_Exposure_EUR"
                        },
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "ECL_Expected_Loss_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.ECL_Expected_Loss_EUR)",
                            "nativeQueryRef": "Total_IFRS9_ECL_EUR"
                        },
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Loan_Amount_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.Loan_Amount_EUR)",
                            "nativeQueryRef": "Total_Loan_Amount_EUR"
                        },
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Default_12M_Target"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.Default_12M_Target)",
                            "nativeQueryRef": "Default_Accounts_12M"
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'PORTFOLIO SOLVENCY & CAPITAL METRICS (EAD • IFRS 9 ECL • TOTAL VOLUME • DEFAULTS)'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#62B0E8'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "10D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(kpi_json_path, "w", encoding="utf-8") as f:
    json.dump(kpi1, f, indent=2)

# 5. Delete cache so Power BI recalculates clean typed VertiPaq
cache_path = os.path.join(sem_dir, ".pbi", "cache.abf")
if os.path.exists(cache_path):
    os.remove(cache_path)

print("TMDL and visuals successfully corrected with proper numeric types!")
