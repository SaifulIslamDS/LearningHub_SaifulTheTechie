#!/usr/bin/env python3
"""
Rebuild the Excel practice workbooks from the CSV files in content/downloads.

    pip install openpyxl pandas
    python tools/make_practice_files.py

Creates / overwrites:
    content/downloads/orders.xlsx           starting workbook for the Excel & Pivot lessons
    content/downloads/sales_model.xlsx      5 Excel Tables for Power Pivot / Power BI
    content/downloads/excel-solutions.xlsx  worked answers for the Excel & Pivot lessons
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.formatting.rule import DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

DL = Path(__file__).resolve().parent.parent / "content" / "downloads"
HEAD_FONT = Font(bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="3F7D6A")
NOTE_FONT = Font(italic=True, color="5F6D66")


def style_header(ws, row=1):
    for c in ws[row]:
        if c.value is not None:
            c.font, c.fill, c.alignment = HEAD_FONT, HEAD_FILL, Alignment(horizontal="center")


def autosize(ws, min_w=10, max_w=40):
    for col in range(1, ws.max_column + 1):
        width = max((len(str(ws.cell(r, col).value or "")) for r in range(1, ws.max_row + 1)), default=8)
        ws.column_dimensions[get_column_letter(col)].width = max(min_w, min(width + 3, max_w))


def load():
    orders = pd.read_csv(DL / "orders.csv")
    customers = pd.read_csv(DL / "customers.csv")
    products = pd.read_csv(DL / "products.csv")
    regions = pd.read_csv(DL / "regions.csv")
    targets = pd.read_csv(DL / "targets_long.csv")
    return orders, customers, products, regions, targets


def add_orders_sheet(wb, orders, title="Orders"):
    ws = wb.create_sheet(title)
    ws.append(list(orders.columns) + ["value"])
    for i, r in enumerate(orders.itertuples(index=False), start=2):
        ws.append([int(r.order_id), dt.date.fromisoformat(r.order_date), r.customer, r.region, r.category,
                   r.product, int(r.quantity), float(r.unit_price), r.status, f"=G{i}*H{i}"])
        ws.cell(i, 2).number_format = "yyyy-mm-dd"
        ws.cell(i, 8).number_format = "0.00"
        ws.cell(i, 10).number_format = "#,##0.00"
    style_header(ws)
    ws.freeze_panes = "A2"
    return ws


def add_plain_sheet(wb, title, df, money_cols=()):
    ws = wb.create_sheet(title)
    ws.append(list(df.columns))
    for r in df.itertuples(index=False):
        ws.append([v.item() if hasattr(v, "item") else v for v in r])
    for col in money_cols:
        idx = list(df.columns).index(col) + 1
        for i in range(2, ws.max_row + 1):
            ws.cell(i, idx).number_format = "0.00"
    style_header(ws)
    ws.freeze_panes = "A2"
    autosize(ws)
    return ws


# ---------------------------------------------------------------- orders.xlsx
def make_orders_workbook(orders, customers, products):
    wb = Workbook()
    wb.remove(wb.active)
    ws = add_orders_sheet(wb, orders)
    autosize(ws)
    add_plain_sheet(wb, "Products", products, money_cols=["list_price"])
    add_plain_sheet(wb, "Customers", customers)
    wb.save(DL / "orders.xlsx")


# ---------------------------------------------------------------- sales_model.xlsx
def make_model_workbook(orders, customers, products, regions, targets):
    o = orders.copy()
    o["value"] = (o.quantity * o.unit_price).round(2)
    o["order_date"] = pd.to_datetime(o.order_date).dt.date
    t = targets.copy()
    t["month"] = pd.to_datetime(t.month).dt.date
    wb = Workbook()
    wb.remove(wb.active)
    style = TableStyleInfo(name="TableStyleMedium7", showRowStripes=True)
    for name, df in [("Orders", o), ("Customers", customers), ("Products", products), ("Regions", regions), ("Targets", t)]:
        ws = wb.create_sheet(name)
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append([v.item() if hasattr(v, "item") else v for v in row])
        ref = f"A1:{get_column_letter(df.shape[1])}{df.shape[0] + 1}"
        tbl = Table(displayName=name, ref=ref)
        tbl.tableStyleInfo = style
        ws.add_table(tbl)
        for i, col in enumerate(df.columns, 1):
            if "date" in col or col == "month":
                for r in range(2, df.shape[0] + 2):
                    ws.cell(r, i).number_format = "yyyy-mm-dd"
        ws.freeze_panes = "A2"
        autosize(ws, max_w=34)
    wb.save(DL / "sales_model.xlsx")


# ---------------------------------------------------------------- excel-solutions.xlsx
def make_solutions_workbook(orders, customers, products):
    wb = Workbook()
    wb.remove(wb.active)
    ws = add_orders_sheet(wb, orders, "Orders (solved)")
    extra = ["counts_as_sale", "size", "size_ifs", "priority", "follow_up", "key_delivery",
             "list_price_xlookup", "list_price_index_match", "discount", "segment", "supplier"]
    for j, h in enumerate(extra, start=11):
        ws.cell(1, j, h)
    for r in range(2, 14):
        ws[f"K{r}"] = f'=IF(I{r}="Cancelled","No","Yes")'
        ws[f"L{r}"] = f'=IF(J{r}>=1000,"Large",IF(J{r}>=500,"Medium","Small"))'
        ws[f"M{r}"] = f'=_xlfn.IFS(J{r}>=1000,"Large",J{r}>=500,"Medium",TRUE,"Small")'
        ws[f"N{r}"] = f'=IF(AND(D{r}="Dhaka",J{r}>=1000),"Priority","Normal")'
        ws[f"O{r}"] = f'=IF(OR(I{r}="Shipped",I{r}="Pending"),"Follow up","")'
        ws[f"P{r}"] = f'=IF(AND(I{r}="Delivered",J{r}>=1000),"Key delivery","-")'
        ws[f"Q{r}"] = f'=_xlfn.XLOOKUP(F{r},Products!$A$2:$A$7,Products!$C$2:$C$7,"Not found")'
        ws[f"R{r}"] = f'=INDEX(Products!$C$2:$C$7,MATCH(F{r},Products!$A$2:$A$7,0))'
        ws[f"S{r}"] = f'=1-H{r}/R{r}'
        ws[f"S{r}"].number_format = "0.0%"
        ws[f"T{r}"] = f'=INDEX(Customers!$C$2:$C$7,MATCH(C{r},Customers!$B$2:$B$7,0))'
        ws[f"U{r}"] = f'=INDEX(Products!$D$2:$D$7,MATCH(F{r},Products!$A$2:$A$7,0))'
    style_header(ws)
    # conditional formatting (lesson: Conditional formatting)
    red = PatternFill("solid", fgColor="F4D3C9")
    amber = PatternFill("solid", fgColor="F6E7C8")
    ws.conditional_formatting.add("A2:J13", FormulaRule(formula=['$I2="Cancelled"'], fill=red))
    ws.conditional_formatting.add("A2:J13", FormulaRule(formula=['OR($I2="Shipped",$I2="Pending")'], fill=amber))
    ws.conditional_formatting.add("J2:J13", DataBarRule(start_type="min", end_type="max", color="5F83A6"))
    autosize(ws, max_w=26)

    add_plain_sheet(wb, "Products", products, money_cols=["list_price"])
    add_plain_sheet(wb, "Customers", customers)

    # Summary sheet (SUMIFS / COUNTIFS lesson)
    s = wb.create_sheet("Summary")
    O = "'Orders (solved)'!"
    s["A1"], s["B1"], s["C1"] = "region", "net_revenue", "net_orders"
    for i, reg in enumerate(["Dhaka", "Gazipur", "Chattogram", "Narayanganj"], start=2):
        s[f"A{i}"] = reg
        s[f"B{i}"] = f'=SUMIFS({O}$J$2:$J$13,{O}$D$2:$D$13,A{i},{O}$I$2:$I$13,"<>Cancelled")'
        s[f"C{i}"] = f'=COUNTIFS({O}$D$2:$D$13,A{i},{O}$I$2:$I$13,"<>Cancelled")'
    s["A6"], s["B6"], s["C6"] = "Total", "=SUM(B2:B5)", "=SUM(C2:C5)"
    s["E1"], s["F1"], s["G1"] = "category", "net_revenue", "net_orders"
    for i, cat in enumerate(["Fabric", "Yarn", "Trims"], start=2):
        s[f"E{i}"] = cat
        s[f"F{i}"] = f'=SUMIFS({O}$J$2:$J$13,{O}$E$2:$E$13,E{i},{O}$I$2:$I$13,"<>Cancelled")'
        s[f"G{i}"] = f'=COUNTIFS({O}$E$2:$E$13,E{i},{O}$I$2:$I$13,"<>Cancelled")'
    checks = [
        ("February 2026 net revenue", f'=SUMIFS({O}$J$2:$J$13,{O}$B$2:$B$13,">="&DATE(2026,2,1),{O}$B$2:$B$13,"<"&DATE(2026,3,1),{O}$I$2:$I$13,"<>Cancelled")'),
        ("Average Fabric order (net)", f'=AVERAGEIFS({O}$J$2:$J$13,{O}$E$2:$E$13,"Fabric",{O}$I$2:$I$13,"<>Cancelled")'),
        ("Orders for Cotton* products", f'=COUNTIFS({O}$F$2:$F$13,"Cotton*")'),
        ("Orders counted as sales", f'=COUNTIF({O}$K$2:$K$13,"Yes")'),
        ("Orders for Star Trims products", f'=COUNTIF({O}$U$2:$U$13,"Star Trims")'),
        ("Average order value (net)", f'=SUMIFS({O}$J$2:$J$13,{O}$I$2:$I$13,"<>Cancelled")/COUNTIFS({O}$I$2:$I$13,"<>Cancelled")'),
        ("Average of all 12 values (incl. cancelled)", f"=AVERAGE({O}$J$2:$J$13)"),
        ("CHECK: region total = all net revenue", f'=IF(B6=SUMIFS({O}$J$2:$J$13,{O}$I$2:$I$13,"<>Cancelled"),"OK","MISMATCH")'),
    ]
    s["A9"] = "check"
    s["B9"] = "result"
    for i, (label, f) in enumerate(checks, start=10):
        s[f"A{i}"], s[f"B{i}"] = label, f
    for row in (1, 9):
        style_header(s, row)
    autosize(s, max_w=44)

    # Dynamic-array formulas (FILTER / SORT / LET) — given as text to type in Microsoft 365
    d = wb.create_sheet("FILTER & LET")
    d.append(["Type these formulas into cell L2 of the Orders sheet (Microsoft 365 / Excel 2021+).", "", ""])
    d["A1"].font = NOTE_FONT
    d.append(["Task", "Formula (type it, don't paste as text)", "Expected result"])
    rows = [
        ("Non-cancelled Dhaka orders", '=FILTER(A2:J13,(D2:D13="Dhaka")*(I2:I13<>"Cancelled"),"No orders")', "Orders 1, 3, 7, 10"),
        ("Shipped or Pending", '=FILTER(A2:J13,(I2:I13="Shipped")+(I2:I13="Pending"),"None")', "Orders 7, 9, 12"),
        ("Dhaka, sorted by value", '=SORT(FILTER(A2:J13,(D2:D13="Dhaka")*(I2:I13<>"Cancelled"),"No orders"),10,-1)', "Orders 3, 10, 1, 7"),
        ("Exercise: Fabric > 700, not cancelled", '=SORT(FILTER(A2:J13,(E2:E13="Fabric")*(J2:J13>700)*(I2:I13<>"Cancelled"),"None"),10,-1)', "Orders 3, 12, 9"),
        ("Average order value with LET", '=LET(revenue,SUMIFS(J2:J13,I2:I13,"<>Cancelled"),orders,COUNTIFS(I2:I13,"<>Cancelled"),revenue/orders)', "825"),
    ]
    for r in rows:
        d.append(list(r))
    style_header(d, 2)
    autosize(d, max_w=90)

    # What-If model (What-If Analysis & Goal Seek lesson)
    m = wb.create_sheet("Model")
    m["A1"], m["B1"] = "Base revenue (non-cancelled)", f'=SUMIFS({O}$J$2:$J$13,{O}$I$2:$I$13,"<>Cancelled")'
    m["A2"], m["B2"] = "Price change (input)", 0
    m["A3"], m["B3"] = "Volume change (input)", 0
    m["A4"], m["B4"] = "Projected revenue", "=B1*(1+B2)*(1+B3)"
    input_fill = PatternFill("solid", fgColor="FFF6D5")
    for c in ("B2", "B3"):
        m[c].fill = input_fill
        m[c].number_format = "0.0%"
    m["D1"] = "Scenario grid — same result as Data → What-If Analysis → Data Table (rows: volume, columns: price)"
    m["D1"].font = NOTE_FONT
    m["D2"] = "volume ↓ / price →"
    for j, p in enumerate([0, 0.05, 0.10]):
        cell = m.cell(2, 5 + j, p)
        cell.number_format = "0%"
    for i, v in enumerate([0, -0.05, -0.10]):
        cell = m.cell(3 + i, 4, v)
        cell.number_format = "0%"
        for j in range(3):
            col = get_column_letter(5 + j)
            c = m.cell(3 + i, 5 + j, f"=$B$1*(1+{col}$2)*(1+$D{3 + i})")
            c.number_format = "#,##0.00"
    m["A7"] = "Goal Seek answers"
    m["A7"].font = Font(bold=True)
    m["A8"] = "Price change for 10,000 revenue at −5% volume"
    m["B8"] = "=10000/(B1*0.95)-1"
    m["B8"].number_format = "0.00%"
    m["A9"] = "Volume change that keeps 9,075 after +10% price"
    m["B9"] = "=1/1.1-1"
    m["B9"].number_format = "0.00%"
    m["A10"] = "Denim units for a 1,000 order at 5.40 (round up in practice)"
    m["B10"] = "=1000/5.4"
    m["B10"].number_format = "0.00"
    m["B1"].number_format = "#,##0.00"
    m["B4"].number_format = "#,##0.00"
    autosize(m, max_w=48)

    # Notes
    n = wb.create_sheet("README", 0)
    lines = [
        "Excel & Pivot lessons — worked solutions",
        "Try each exercise in orders.xlsx first. Then compare with this workbook.",
        "Sheets: Orders (solved) = IF, IFS, AND/OR, XLOOKUP, INDEX/MATCH, discount, conditional formatting.",
        "Summary = SUMIFS / COUNTIFS / AVERAGEIFS tables and checks.",
        "FILTER & LET = dynamic-array formulas to type (Microsoft 365 / Excel 2021+).",
        "Model = What-If model, scenario grid and Goal Seek answers.",
        "PivotTables and slicers are not included: build them yourself by following the Pivot lessons.",
        "XLOOKUP and IFS need Excel 2019+/365; INDEX/MATCH columns work in every version.",
    ]
    for i, t in enumerate(lines, 1):
        n.cell(i, 1, t)
    n["A1"].font = Font(bold=True, size=14)
    n.column_dimensions["A"].width = 100
    wb.save(DL / "excel-solutions.xlsx")


def main():
    orders, customers, products, regions, targets = load()
    make_orders_workbook(orders, customers, products)
    make_model_workbook(orders, customers, products, regions, targets)
    make_solutions_workbook(orders, customers, products)
    print("Workbooks written to", DL)


if __name__ == "__main__":
    main()
