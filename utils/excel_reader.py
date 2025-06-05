import pandas as pd
import difflib

def read_excel_sheets(file_path):
    """Return a list of sheet names from an Excel file."""
    try:
        xls = pd.ExcelFile(file_path)
        return xls.sheet_names
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel sheets: {e}")

def fuzzy_find_status_column(columns):
    """
    Attempt to find the most likely 'status' column using fuzzy matching.
    Returns the column name if found, else None.
    """
    possible_names = [
        "status", "implementation", "current status",
        "existing control", "gap", "state", "progress"
    ]
    columns_lower = [col.lower() for col in columns]
    for name in possible_names:
        match = difflib.get_close_matches(name.lower(), columns_lower, n=1, cutoff=0.7)
        if match:
            idx = columns_lower.index(match[0])
            return columns[idx]
    return None

def read_selected_sheet(file_path, sheet_name):
    """
    Read a specific sheet from an Excel file and attempt to identify the status column.
    Returns the DataFrame and the detected status column name (or None).
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        status_col = fuzzy_find_status_column(df.columns.tolist())
        return df, status_col
    except Exception as e:
        raise RuntimeError(f"Failed to read sheet '{sheet_name}': {e}")
