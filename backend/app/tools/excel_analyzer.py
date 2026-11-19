from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/excel", tags=["Excel"])

MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    extension = Path(filename).suffix.lower()

    if extension not in [".xlsx", ".csv"]:
        raise HTTPException(
            status_code=400,
            detail="Envie somente arquivos XLSX ou CSV."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Arquivo maior que o limite de 10 MB."
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="O arquivo está vazio."
        )

    try:
        if extension == ".xlsx":
            workbook = pd.ExcelFile(BytesIO(content), engine="openpyxl")
            sheets = {}

            for sheet_name in workbook.sheet_names:
                df = pd.read_excel(
                    workbook,
                    sheet_name=sheet_name,
                    engine="openpyxl"
                )

                sheets[sheet_name] = {
                    "rows": int(len(df)),
                    "columns": int(len(df.columns)),
                    "column_names": [str(c) for c in df.columns],
                    "empty_cells": int(df.isna().sum().sum()),
                    "duplicate_rows": int(df.duplicated().sum()),
                    "data_types": {
                        str(c): str(t)
                        for c, t in df.dtypes.items()
                    }
                }

            return {
                "status": "success",
                "filename": filename,
                "sheets": sheets,
                "original_modified": False
            }

        df = pd.read_csv(BytesIO(content), encoding="utf-8-sig")

        return {
            "status": "success",
            "filename": filename,
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "column_names": [str(c) for c in df.columns],
            "empty_cells": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "data_types": {
                str(c): str(t)
                for c, t in df.dtypes.items()
            },
            "original_modified": False
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível analisar o arquivo. Verifique se ele é válido."
        )
