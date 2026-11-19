import pandas as pd


def generate_insights(df: pd.DataFrame) -> dict:
    rows, columns = df.shape

    missing = {
        str(col): int(total)
        for col, total in df.isna().sum().items()
        if total > 0
    }

    duplicates = int(df.duplicated().sum())

    numeric = {}
    for col in df.select_dtypes(include="number").columns:
        values = df[col].dropna()

        if not values.empty:
            numeric[str(col)] = {
                "minimum": float(values.min()),
                "average": round(float(values.mean()), 2),
                "maximum": float(values.max())
            }

    findings = [
        f"A planilha possui {rows} linhas e {columns} colunas.",
        f"Foram encontradas {duplicates} linhas duplicadas.",
        f"Existem {sum(missing.values())} células vazias."
    ]

    return {
        "status": "success",
        "rows": rows,
        "columns": columns,
        "missing_cells_by_column": missing,
        "duplicate_rows": duplicates,
        "numeric_summary": numeric,
        "findings": findings,
        "original_modified": False
    }
