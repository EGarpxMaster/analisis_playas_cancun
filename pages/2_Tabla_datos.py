import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # sube de /pages al root del proyecto
DATA = ROOT / "datos" / "ocupacion_playas_cancun.csv"  # ajusta el nombre real

if not DATA.exists():
    raise FileNotFoundError(f"No se encontró el archivo de datos en: {DATA}")


###################################
# Tabla de datos
##################################

st.subheader("Tabla de datos")
st.write("Los datos que exploraremos están disponibles en la siguiente tabla:")

df = pd.read_csv(DATA)
st.dataframe(df)
