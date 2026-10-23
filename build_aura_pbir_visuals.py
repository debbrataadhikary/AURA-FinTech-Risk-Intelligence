import json
import os
import shutil

base_report = r"d:\DW- Internship\AURA-FinTech-Risk-Intelligence\powerbi\AURA_FinTech_Risk.Report"
def_dir = os.path.join(base_report, "definition")
pages_dir = os.path.join(def_dir, "pages")

# Clean previous definitions if any
if os.path.exists(def_dir):
    shutil.rmtree(def_dir)
os.makedirs(pages_dir, exist_ok=True)

# 1. definition.pbir (version 4.0)
pbir = {
    "version": "4.0",
    "datasetReference": {
        "byPath": {
            "path": "../AURA_FinTech_Risk.SemanticModel"
        }
    }
}
with open(os.path.join(base_report, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir, f, indent=2)

# Remove legacy report.json if exists at root of report folder
legacy_rep = os.path.join(base_report, "report.json")
if os.path.exists(legacy_rep):
    os.remove(legacy_rep)

# 2. definition/report.json
report_def = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json",
    "themeCollection": {
        "baseTheme": {
            "name": "CY25SU11",
            "reportVersionAtImport": {
                "visual": "2.4.0",
                "report": "3.0.0",
                "page": "2.3.0"
            },
            "type": "SharedResources"
        }
    },
    "resourcePackages": [
        {
            "name": "SharedResources",
            "type": "SharedResources",
            "items": [
                {
                    "name": "CY25SU11",
                    "path": "BaseThemes/CY25SU11.json",
                    "type": "BaseTheme"
                }
            ]
        }
    ],
    "settings": {
        "useStylableVisualContainerHeader": True,
        "exportDataMode": "AllowSummarized",
        "defaultDrillFilterOtherVisuals": True,
        "allowChangeFilterTypes": True,
        "useEnhancedTooltips": True,
        "useDefaultAggregateDisplayName": True
    }
}
with open(os.path.join(def_dir, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_def, f, indent=2)

# 3. definition/version.json
with open(os.path.join(def_dir, "version.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0"
    }, f, indent=2)

# Helper to create styled visual containers
def make_header(text, bg_color="#002B5C", border_color="#FFF000", font_color="#FFF000"):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
        "name": "v0header",
        "position": {"x": 12, "y": 8, "z": 500, "height": 46, "width": 1256, "tabOrder": 500},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [{
                                "value": text,
                                "textStyle": {"fontWeight": "bold", "fontSize": "13pt", "color": font_color}
                            }],
                            "horizontalTextAlignment": "center"
                        }]
                    }
                }]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{bg_color}'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
                "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{border_color}'"}}}}}, "width": {"expr": {"Literal": {"Value": "2D"}}}}}],
                "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
            }
        }
    }

def make_page(name, display_name):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": name,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 720,
        "width": 1280,
        "objects": {
            "background": [{
                "properties": {
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0B2239'"}}}}},
                    "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                }
            }],
            "outspace": [{
                "properties": {
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#071726'"}}}}}
                }
            }]
        }
    }

# ==============================================================================
# PAGE 1: Executive Boardroom Cockpit
# ==============================================================================
p1_dir = os.path.join(pages_dir, "ReportSection1")
p1_vis = os.path.join(p1_dir, "visuals")
os.makedirs(p1_vis, exist_ok=True)

with open(os.path.join(p1_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump(make_page("ReportSection1", "1. Executive Boardroom Cockpit"), f, indent=2)

# P1 Visual 0: Header
h1_dir = os.path.join(p1_vis, "v0header")
os.makedirs(h1_dir, exist_ok=True)
with open(os.path.join(h1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(make_header("AURA: AUTONOMOUS RISK ARCHITECTURE & CREDIT INTELLIGENCE - EXECUTIVE BOARDROOM COCKPIT"), f, indent=2)

# P1 Visual 1: Multi-Row KPIs
kpi1_dir = os.path.join(p1_vis, "v0kpis")
os.makedirs(kpi1_dir, exist_ok=True)
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
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "AML_Suspicious_Flag"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Transactions_Stream.AML_Suspicious_Flag)",
                            "nativeQueryRef": "AML_Suspicious_Events"
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'PORTFOLIO SOLVENCY & CAPITAL METRICS (EAD • IFRS 9 ECL • AML ALERTS)'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#62B0E8'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "10D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(kpi1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(kpi1, f, indent=2)

# P1 Visual 2: Country Slicer
slic1_dir = os.path.join(p1_vis, "v0slicer")
os.makedirs(slic1_dir, exist_ok=True)
slic1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v0slicer",
    "position": {"x": 982, "y": 60, "z": 1500, "height": 110, "width": 286, "tabOrder": 1500},
    "visual": {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Country"}},
                            "queryRef": "Fact_Credit_Portfolio.Country",
                            "nativeQueryRef": "Country",
                            "active": True
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'SOVEREIGN MARKET FILTER'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#62B0E8'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "10D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(slic1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(slic1, f, indent=2)

# P1 Visual 3: Country Exposure (Clustered Bar Chart)
bar1_dir = os.path.join(p1_vis, "v1countryExposure")
os.makedirs(bar1_dir, exist_ok=True)
bar1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v1countryExposure",
    "position": {"x": 12, "y": 178, "z": 2000, "height": 266, "width": 680, "tabOrder": 2000},
    "visual": {
        "visualType": "clusteredBarChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [
                        {
                            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Country"}},
                            "queryRef": "Fact_Credit_Portfolio.Country",
                            "nativeQueryRef": "Country",
                            "active": True
                        }
                    ]
                },
                "Y": {
                    "projections": [
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.EAD_Exposure_EUR)",
                            "nativeQueryRef": "EAD_Exposure_EUR"
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'1. Sovereign Credit Exposure at Default (EAD EUR) by Country'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "11D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(bar1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(bar1, f, indent=2)

# P1 Visual 4: IFRS 9 Donut Chart
donut1_dir = os.path.join(p1_vis, "v2stagingDonut")
os.makedirs(donut1_dir, exist_ok=True)
donut1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v2stagingDonut",
    "position": {"x": 702, "y": 178, "z": 2500, "height": 266, "width": 566, "tabOrder": 2500},
    "visual": {
        "visualType": "donutChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [
                        {
                            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "IFRS9_Stage"}},
                            "queryRef": "Fact_Credit_Portfolio.IFRS9_Stage",
                            "nativeQueryRef": "IFRS9_Stage",
                            "active": True
                        }
                    ]
                },
                "Y": {
                    "projections": [
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "ECL_Expected_Loss_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.ECL_Expected_Loss_EUR)",
                            "nativeQueryRef": "ECL_Expected_Loss_EUR"
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'2. IFRS 9 Expected Credit Loss (ECL) by Regulatory Stage'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "11D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(donut1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(donut1, f, indent=2)

# P1 Visual 5: Loan Purpose / Facility Matrix (Clustered Column)
col1_dir = os.path.join(p1_vis, "v3loanPurpose")
os.makedirs(col1_dir, exist_ok=True)
col1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v3loanPurpose",
    "position": {"x": 12, "y": 452, "z": 3000, "height": 256, "width": 615, "tabOrder": 3000},
    "visual": {
        "visualType": "clusteredColumnChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [
                        {
                            "field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Loan_Purpose"}},
                            "queryRef": "Fact_Credit_Portfolio.Loan_Purpose",
                            "nativeQueryRef": "Loan_Purpose",
                            "active": True
                        }
                    ]
                },
                "Y": {
                    "projections": [
                        {
                            "field": {
                                "Aggregation": {
                                    "Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}},
                                    "Function": 0
                                }
                            },
                            "queryRef": "Sum(Fact_Credit_Portfolio.EAD_Exposure_EUR)",
                            "nativeQueryRef": "EAD_Exposure_EUR"
                        }
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'3. Total Exposure by Facility / Loan Purpose'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "11D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(col1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(col1, f, indent=2)

# P1 Visual 6: Detailed Portfolio Table
tab1_dir = os.path.join(p1_vis, "v4portfolioTable")
os.makedirs(tab1_dir, exist_ok=True)
tab1 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v4portfolioTable",
    "position": {"x": 639, "y": 452, "z": 3500, "height": 256, "width": 629, "tabOrder": 3500},
    "visual": {
        "visualType": "tableEx",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Loan_ID"}}, "queryRef": "Fact_Credit_Portfolio.Loan_ID"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Country"}}, "queryRef": "Fact_Credit_Portfolio.Country"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "FICO_Score"}}, "queryRef": "Fact_Credit_Portfolio.FICO_Score"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "IFRS9_Stage"}}, "queryRef": "Fact_Credit_Portfolio.IFRS9_Stage"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}}, "queryRef": "Fact_Credit_Portfolio.EAD_Exposure_EUR"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "ECL_Expected_Loss_EUR"}}, "queryRef": "Fact_Credit_Portfolio.ECL_Expected_Loss_EUR"}
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'4. Institutional Credit Facility Surveillance Table'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}, "fontSize": {"expr": {"Literal": {"Value": "11D"}}}}}],
            "dropShadow": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]
        }
    }
}
with open(os.path.join(tab1_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(tab1, f, indent=2)

# ==============================================================================
# PAGE 2: IFRS 9 Staging & ECL Stressed Allowances
# ==============================================================================
p2_dir = os.path.join(pages_dir, "ReportSection2")
p2_vis = os.path.join(p2_dir, "visuals")
os.makedirs(p2_vis, exist_ok=True)
with open(os.path.join(p2_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump(make_page("ReportSection2", "2. IFRS 9 Staging & ECL Migration"), f, indent=2)

h2_dir = os.path.join(p2_vis, "v0header")
os.makedirs(h2_dir, exist_ok=True)
with open(os.path.join(h2_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(make_header("PAGE 2: IFRS 9 EXPECTED CREDIT LOSS (ECL) STAGING & MIGRATION SURVEILLANCE"), f, indent=2)

# P2 Donut
d2_dir = os.path.join(p2_vis, "v1stageEAD")
os.makedirs(d2_dir, exist_ok=True)
d2 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v1stageEAD",
    "position": {"x": 12, "y": 64, "z": 1000, "height": 310, "width": 615, "tabOrder": 1000},
    "visual": {
        "visualType": "donutChart",
        "query": {
            "queryState": {
                "Category": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "IFRS9_Stage"}}, "queryRef": "Fact_Credit_Portfolio.IFRS9_Stage"}]},
                "Y": {"projections": [{"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}}, "Function": 0}}, "queryRef": "Sum(Fact_Credit_Portfolio.EAD_Exposure_EUR)"}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'IFRS 9 Exposure Distribution (Stage 1 vs Stage 2 vs Stage 3)'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(d2_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(d2, f, indent=2)

# P2 Bar: Delinquency DPD
dpd2_dir = os.path.join(p2_vis, "v2dpdLoss")
os.makedirs(dpd2_dir, exist_ok=True)
dpd2 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v2dpdLoss",
    "position": {"x": 639, "y": 64, "z": 1500, "height": 310, "width": 629, "tabOrder": 1500},
    "visual": {
        "visualType": "clusteredColumnChart",
        "query": {
            "queryState": {
                "Category": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Days_Past_Due_DPD"}}, "queryRef": "Fact_Credit_Portfolio.Days_Past_Due_DPD"}]},
                "Y": {"projections": [{"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "ECL_Expected_Loss_EUR"}}, "Function": 0}}, "queryRef": "Sum(Fact_Credit_Portfolio.ECL_Expected_Loss_EUR)"}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Expected Credit Loss (EUR) by Delinquency Days (DPD)'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(dpd2_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(dpd2, f, indent=2)

# P2 Table
tab2_dir = os.path.join(p2_vis, "v3loanDetail")
os.makedirs(tab2_dir, exist_ok=True)
tab2 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v3loanDetail",
    "position": {"x": 12, "y": 386, "z": 2000, "height": 320, "width": 1256, "tabOrder": 2000},
    "visual": {
        "visualType": "tableEx",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Customer_ID"}}, "queryRef": "Fact_Credit_Portfolio.Customer_ID"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Country"}}, "queryRef": "Fact_Credit_Portfolio.Country"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "FICO_Score"}}, "queryRef": "Fact_Credit_Portfolio.FICO_Score"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Debt_to_Income_DTI"}}, "queryRef": "Fact_Credit_Portfolio.Debt_to_Income_DTI"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "Days_Past_Due_DPD"}}, "queryRef": "Fact_Credit_Portfolio.Days_Past_Due_DPD"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "IFRS9_Stage"}}, "queryRef": "Fact_Credit_Portfolio.IFRS9_Stage"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "EAD_Exposure_EUR"}}, "queryRef": "Fact_Credit_Portfolio.EAD_Exposure_EUR"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Credit_Portfolio"}}, "Property": "ECL_Expected_Loss_EUR"}}, "queryRef": "Fact_Credit_Portfolio.ECL_Expected_Loss_EUR"}
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Detailed Obligor Impairment Ledger'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(tab2_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(tab2, f, indent=2)

# ==============================================================================
# PAGE 3: Basel III Capital Adequacy & Macro Stress
# ==============================================================================
p3_dir = os.path.join(pages_dir, "ReportSection3")
p3_vis = os.path.join(p3_dir, "visuals")
os.makedirs(p3_vis, exist_ok=True)
with open(os.path.join(p3_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump(make_page("ReportSection3", "3. Macro Stress Testing & Solvency"), f, indent=2)

h3_dir = os.path.join(p3_vis, "v0header")
os.makedirs(h3_dir, exist_ok=True)
with open(os.path.join(h3_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(make_header("PAGE 3: BASEL III CAPITAL ADEQUACY RATIO (CAR) & EBA MACRO STRESS RESILIENCE"), f, indent=2)

# P3 Slicer
slic3_dir = os.path.join(p3_vis, "v0slicer")
os.makedirs(slic3_dir, exist_ok=True)
slic3 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v0slicer",
    "position": {"x": 12, "y": 64, "z": 1000, "height": 110, "width": 400, "tabOrder": 1000},
    "visual": {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Scenario"}}, "queryRef": "Dim_Macro_Stress.Scenario", "active": True}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'MACRO STRESS SCENARIOS'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#62B0E8'"}}}}}}}]
        }
    }
}
with open(os.path.join(slic3_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(slic3, f, indent=2)

# P3 Bar: ECL Stress Multiplier
bar3_dir = os.path.join(p3_vis, "v1eclMultiplier")
os.makedirs(bar3_dir, exist_ok=True)
bar3 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v1eclMultiplier",
    "position": {"x": 424, "y": 64, "z": 1500, "height": 300, "width": 844, "tabOrder": 1500},
    "visual": {
        "visualType": "clusteredBarChart",
        "query": {
            "queryState": {
                "Category": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Scenario"}}, "queryRef": "Dim_Macro_Stress.Scenario", "active": True}]},
                "Y": {"projections": [{"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "ECL_Stress_Multiplier"}}, "Function": 0}}, "queryRef": "Sum(Dim_Macro_Stress.ECL_Stress_Multiplier)"}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'IFRS 9 Impairment Stress Multipliers by Economic Scenario'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(bar3_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(bar3, f, indent=2)

# P3 Table: Macro Parameters
tab3_dir = os.path.join(p3_vis, "v2macroGrid")
os.makedirs(tab3_dir, exist_ok=True)
tab3 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v2macroGrid",
    "position": {"x": 12, "y": 380, "z": 2000, "height": 326, "width": 1256, "tabOrder": 2000},
    "visual": {
        "visualType": "tableEx",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Scenario"}}, "queryRef": "Dim_Macro_Stress.Scenario"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "GDP_Growth_Pct"}}, "queryRef": "Dim_Macro_Stress.GDP_Growth_Pct"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Inflation_HICP_Pct"}}, "queryRef": "Dim_Macro_Stress.Inflation_HICP_Pct"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Central_Bank_Rate_Pct"}}, "queryRef": "Dim_Macro_Stress.Central_Bank_Rate_Pct"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "Unemployment_Pct"}}, "queryRef": "Dim_Macro_Stress.Unemployment_Pct"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Dim_Macro_Stress"}}, "Property": "ECL_Stress_Multiplier"}}, "queryRef": "Dim_Macro_Stress.ECL_Stress_Multiplier"}
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'EBA / ECB Macroeconomic Baseline & Severely Adverse Shock Parameters'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(tab3_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(tab3, f, indent=2)

# ==============================================================================
# PAGE 4: Real-Time AML & Forensic Matrix
# ==============================================================================
p4_dir = os.path.join(pages_dir, "ReportSection4")
p4_vis = os.path.join(p4_dir, "visuals")
os.makedirs(p4_vis, exist_ok=True)
with open(os.path.join(p4_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump(make_page("ReportSection4", "4. AML Transaction Surveillance Matrix"), f, indent=2)

h4_dir = os.path.join(p4_vis, "v0header")
os.makedirs(h4_dir, exist_ok=True)
with open(os.path.join(h4_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(make_header("PAGE 4: ANTI-MONEY LAUNDERING (AML) TRANSACTION FLOW & VELOCITY SURVEILLANCE"), f, indent=2)

# P4 Channel Donut
d4_dir = os.path.join(p4_vis, "v1channelDonut")
os.makedirs(d4_dir, exist_ok=True)
d4 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v1channelDonut",
    "position": {"x": 12, "y": 64, "z": 1000, "height": 310, "width": 615, "tabOrder": 1000},
    "visual": {
        "visualType": "donutChart",
        "query": {
            "queryState": {
                "Category": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Channel"}}, "queryRef": "Fact_Transactions_Stream.Channel"}]},
                "Y": {"projections": [{"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Amount_EUR"}}, "Function": 0}}, "queryRef": "Sum(Fact_Transactions_Stream.Amount_EUR)"}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Transactional Flow Volume (EUR) by Payment Channel'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(d4_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(d4, f, indent=2)

# P4 Velocity Bar
v4_dir = os.path.join(p4_vis, "v2velocityBar")
os.makedirs(v4_dir, exist_ok=True)
v4 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v2velocityBar",
    "position": {"x": 639, "y": 64, "z": 1500, "height": 310, "width": 629, "tabOrder": 1500},
    "visual": {
        "visualType": "clusteredColumnChart",
        "query": {
            "queryState": {
                "Category": {"projections": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Hourly_Velocity_Count"}}, "queryRef": "Fact_Transactions_Stream.Hourly_Velocity_Count"}]},
                "Y": {"projections": [{"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Amount_EUR"}}, "Function": 0}}, "queryRef": "Sum(Fact_Transactions_Stream.Amount_EUR)"}]}
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Payment Flow Exposure by Hourly Transaction Velocity Spikes'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(v4_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(v4, f, indent=2)

# P4 Table: Transaction Watchlist
tab4_dir = os.path.join(p4_vis, "v3amlTable")
os.makedirs(tab4_dir, exist_ok=True)
tab4 = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
    "name": "v3amlTable",
    "position": {"x": 12, "y": 386, "z": 2000, "height": 320, "width": 1256, "tabOrder": 2000},
    "visual": {
        "visualType": "tableEx",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Transaction_ID"}}, "queryRef": "Fact_Transactions_Stream.Transaction_ID"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Customer_ID"}}, "queryRef": "Fact_Transactions_Stream.Customer_ID"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Channel"}}, "queryRef": "Fact_Transactions_Stream.Channel"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Amount_EUR"}}, "queryRef": "Fact_Transactions_Stream.Amount_EUR"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Is_High_Risk_Jurisdiction"}}, "queryRef": "Fact_Transactions_Stream.Is_High_Risk_Jurisdiction"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "Hourly_Velocity_Count"}}, "queryRef": "Fact_Transactions_Stream.Hourly_Velocity_Count"},
                        {"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Fact_Transactions_Stream"}}, "Property": "AML_Suspicious_Flag"}}, "queryRef": "Fact_Transactions_Stream.AML_Suspicious_Flag"}
                    ]
                }
            }
        },
        "visualContainerObjects": {
            "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#102A43'"}}}}}, "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}],
            "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#334E68'"}}}}}, "width": {"expr": {"Literal": {"Value": "1D"}}}}}],
            "title": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "text": {"expr": {"Literal": {"Value": "'Real-Time AML High-Velocity Surveillance Audit Trail'"}}}, "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}}}]
        }
    }
}
with open(os.path.join(tab4_dir, "visual.json"), "w", encoding="utf-8") as f:
    json.dump(tab4, f, indent=2)

# 4. definition/pages/pages.json
pages_meta = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
    "pageOrder": [
        "ReportSection1",
        "ReportSection2",
        "ReportSection3",
        "ReportSection4"
    ],
    "activePageName": "ReportSection1"
}
with open(os.path.join(pages_dir, "pages.json"), "w", encoding="utf-8") as f:
    json.dump(pages_meta, f, indent=2)

print("AURA PBIR full visual architecture successfully generated!")
