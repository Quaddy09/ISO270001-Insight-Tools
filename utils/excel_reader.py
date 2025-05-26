import pandas as pd

def read_gap_assessment(file):
    xls = pd.ExcelFile(file)
    print("Sheets found:", xls.sheet_names)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, header=None)
        print(f"Checking sheet: {sheet_name}")

        for i in range(min(20, len(df))):
            row = df.iloc[i].fillna('').astype(str).str.lower()
            if any("control" in cell for cell in row) and any("status" in cell for cell in row):
                print(f"Found header at row {i} in sheet '{sheet_name}'")

                header_row = i
                df.columns = df.iloc[header_row]
                df = df[header_row + 1:].reset_index(drop=True)

                col_map = {}
                for col in df.columns:
                    col_str = str(col).lower()
                    if "control" in col_str:
                        col_map[col] = "Control"
                    elif "status" in col_str:
                        col_map[col] = "Status"
                    elif "recommend" in col_str or "catatan" in col_str:
                        col_map[col] = "Recommendation"

                df.rename(columns=col_map, inplace=True)

                if 'Control' in df.columns and 'Status' in df.columns:
                    selected_cols = ['Control', 'Status']
                    if 'Recommendation' in df.columns:
                        selected_cols.append('Recommendation')
                    df_cleaned = df[selected_cols].dropna(subset=['Control', 'Status'])
                    return df_cleaned

    print("⚠️ Could not find the expected format in any sheet.")
    return pd.DataFrame()