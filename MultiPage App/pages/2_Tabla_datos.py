import streamlit as st
import pandas as pd

###################################
# Tabla de datos
##################################

st.subheader("Tabla de datos")
st.write("Los datos que exploraremos están disponibles en la siguiente tabla:")

df = pd.read_csv("../Datos/ocupacion_playas_cancun_clean.csv")
st.dataframe(df)

