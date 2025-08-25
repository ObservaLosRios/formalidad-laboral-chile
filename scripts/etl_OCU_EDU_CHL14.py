"""
ETL: Ocupados por nivel educativo x sexo (Región de Los Ríos - CHL14)

Entrada esperada: CSV con columnas similares a las de INE/DTI, por ejemplo:
 - 'DTI_CL_TRIMESTRE_MOVIL' y/o 'Trimestre Móvil'
 - 'DTI_CL_REGION' y/o 'Región'
 - 'DTI_CL_SEXO' y/o 'Sexo' con valores ('M','F','_T' o 'Hombres','Mujeres','Ambos sexos')
 - 'DTI_CL_NIVEL_EDUC' y/o 'Nivel educativo'
 - 'Value' (cantidad de ocupados)

Uso:
  python scripts/etl_OCU_EDU_CHL14.py [ruta_csv_entrada] [ruta_json_salida]

Genera JSON en docs/data/ocupados_nivel_educativo.json con estructura para la visualización:
{
  "titulo": str,
  "trimestres": [str,...],
  "niveles": [str,...],
  "series_por_nivel": { nivel: { "Hombres": [..], "Mujeres": [..] } },
  "tickvals": [str,...],
  "ticktext": [str,...]
}
"""

import json
import os
import sys
from typing import List, Dict

import pandas as pd


def find_col(df: pd.DataFrame, candidates: List[str]) -> str:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    # try partial contains
    for c in df.columns:
        l = c.lower()
        for cand in candidates:
            if cand.lower() in l:
                return c
    raise KeyError(f"No se encontró ninguna columna entre: {candidates}")


def normalize_sexo(val: str) -> str:
    v = str(val).strip().lower()
    if v in {"m", "h", "hombre", "hombres"}:
        return "Hombres"
    if v in {"f", "mujer", "mujeres"}:
        return "Mujeres"
    return "Ambos sexos"


def compute_ticks(trimestres: List[str]) -> Dict[str, List[str]]:
    # Espera formato 'YYYY xxx-yyy'
    years_seen = set()
    tickvals, ticktext = [], []
    for t in trimestres:
        parts = str(t).split()
        if not parts:
            continue
        year = parts[0]
        if year not in years_seen and ("abr" in t or "ago" in t or "dic" in t or "ene" in t):
            # toma el primer trimestre del año en los datos; si no hay abr- jun exacto, usa el primero que aparezca
            years_seen.add(year)
            tickvals.append(t)
            ticktext.append(year)
    return {"tickvals": tickvals, "ticktext": ticktext}


def main(input_csv: str, output_json: str):
    df = pd.read_csv(input_csv)

    # Detectar columnas
    col_trim = find_col(df, ["Trimestre Móvil", "DTI_CL_TRIMESTRE_MOVIL"])
    col_region = find_col(df, ["Región", "DTI_CL_REGION"]) 
    col_sexo = find_col(df, ["Sexo", "DTI_CL_SEXO"]) 
    col_nivel = find_col(df, ["Nivel educativo", "Nivel Educativo", "DTI_CL_NIVEL_EDUC", "Nivel"]) 
    col_value = find_col(df, ["Value", "Ocupados", "Cantidad"]) 

    # Filtrar región CHL14 / Región de Los Ríos
    mask_region = (df[col_region].astype(str).str.upper().str.contains("CHL14")) | \
                  (df[col_region].astype(str).str.contains("Ríos", case=False, na=False))
    dfr = df[mask_region].copy()
    if dfr.empty:
        raise ValueError("No se encontraron filas para la región CHL14 / Los Ríos en el archivo de entrada.")

    # Normalizar Sexo
    dfr["Sexo_norm"] = dfr[col_sexo].apply(normalize_sexo)

    # Orden temporal por 'Trimestre Móvil'
    # Intentar conservar el orden alfabético como en otras series (ya vienen ordenadas en los insumos originales)
    dfr.sort_values(by=[col_trim], inplace=True)

    # Seleccionar niveles y trimestres
    niveles = (
        dfr[col_nivel]
        .dropna()
        .astype(str)
        .str.strip()
        .replace({
            "Sin nivel educacional": "Sin educación",
            "Básica incompleta": "Básica",
            "Básica completa": "Básica",
            "Media incompleta": "Media",
            "Media completa": "Media",
            "Superior incompleta": "Superior",
            "Superior completa": "Superior",
        })
        .unique()
        .tolist()
    )
    # Orden sugerida
    prefer_order = ["Sin educación", "Básica", "Media", "Superior"]
    niveles = sorted(niveles, key=lambda x: (prefer_order.index(x) if x in prefer_order else 999, x))

    trimestres = dfr[col_trim].drop_duplicates().tolist()

    # Construir series por nivel y sexo
    series_por_nivel: Dict[str, Dict[str, List[float]]] = {}
    for nivel in niveles:
        series_por_nivel[nivel] = {"Hombres": [], "Mujeres": []}
        for t in trimestres:
            df_t = dfr[(dfr[col_trim] == t)]
            # mapear equivalencias de nivel a categoría consolidada
            df_t = df_t.copy()
            df_t["nivel_cat"] = (
                df_t[col_nivel]
                .astype(str).str.strip()
                .replace({
                    "Sin nivel educacional": "Sin educación",
                    "Básica incompleta": "Básica",
                    "Básica completa": "Básica",
                    "Media incompleta": "Media",
                    "Media completa": "Media",
                    "Superior incompleta": "Superior",
                    "Superior completa": "Superior",
                })
            )
            df_tn = df_t[df_t["nivel_cat"] == nivel]
            hombres = df_tn[df_tn["Sexo_norm"] == "Hombres"][col_value].sum()
            mujeres = df_tn[df_tn["Sexo_norm"] == "Mujeres"][col_value].sum()
            series_por_nivel[nivel]["Hombres"].append(float(hombres) if pd.notnull(hombres) else None)
            series_por_nivel[nivel]["Mujeres"].append(float(mujeres) if pd.notnull(mujeres) else None)

    ticks = compute_ticks(trimestres)

    payload = {
        "titulo": "Ocupados por nivel educativo y sexo — Región de Los Ríos",
        "trimestres": trimestres,
        "niveles": niveles,
        "series_por_nivel": series_por_nivel,
        "tickvals": ticks["tickvals"],
        "ticktext": ticks["ticktext"],
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

    print(f"JSON generado: {output_json}")


if __name__ == "__main__":
    input_csv = sys.argv[1] if len(sys.argv) > 1 else "data/OCU_EDU_CHL14.csv"
    output_json = sys.argv[2] if len(sys.argv) > 2 else "docs/data/ocupados_nivel_educativo.json"
    main(input_csv, output_json)
