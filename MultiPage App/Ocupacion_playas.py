import streamlit as st

# Texto introductorio del dashboard (serio, claro y con apoyo visual mediante emojis)

st.title("🏖️ Ocupación de Playas en Cancún")

###################################
# Introducción
###################################
st.subheader("Introducción")
st.markdown("""
Este panel permite **concentrar, visualizar y explorar** la ocupación registrada en las playas de Cancún para comprender **patrones diarios, mensuales y anuales**.  
El monitoreo sistemático de afluencia es clave para la **planeación operativa**, la **asignación de recursos** (seguridad, limpieza, salvavidas), la **gestión turística** y la **sustentabilidad**.
  
**Propósito:** entregar **insights accionables** —claros y oportunos— que faciliten mejores decisiones.
""")

st.divider()

###################################
# ¿Qué es este dashboard?
###################################
st.subheader("🧭 ¿Qué es este dashboard?")
st.markdown("""
Es una herramienta interactiva que **agrega y compara** la ocupación a lo largo del tiempo. Ayuda a responder, entre otras, las siguientes preguntas:

- ¿Cómo evoluciona la afluencia **día a día** dentro de un mes?  
- ¿Qué **meses** concentran mayor afluencia en un año determinado?  
- ¿Cuál es la tendencia **histórica** de ocupación?  
- ¿Qué **playas** destacan por su ocupación acumulada en un periodo?  
- ¿Qué **días de la semana** muestran mayor demanda y con qué **variabilidad**?
""")

st.divider()

###################################
# Funcionalidades principales
###################################
st.subheader("🧩 Funcionalidades principales")

st.markdown("""
##### 1) 📈 Análisis Temporal (Global)
- **Vistas:** Diario (selección de **año + mes**), Mensual (**año**) y Anual (**toda la serie**).  
- **Gráficas:** líneas interactivas con métricas clave (total, promedio, máximos/mínimos y crecimiento).  
- **Uso:** detección de **picos**, **estacionalidad** y **tendencias** de largo plazo.

##### 2) 🏖️ Análisis por Playa
- **Vistas:** Diario, Mensual y Anual por **nombre de playa**.  
- **Comparaciones:** múltiples playas en una misma gráfica y **ranking** por ocupación acumulada.  
- **Extras:** **mapa de calor** mensual para identificar estacionalidad por playa de un vistazo.

##### 3) 📅 Análisis por Día de la Semana
- **Filtros opcionales:** **año** y **mes**.  
- **Salidas:** barras de **totales** y **promedios**, más **tabla de estadísticas** (suma, promedio, mediana, desviación estándar, mínimo, máximo y conteos) con expanders por día.

**Características técnicas destacadas**
- Interactividad **Plotly** (zoom, hover con valores, activar/ocultar series desde la leyenda).  
- **Caché de datos** para carga ágil (`@st.cache_data`).  
- **Calendario y etiquetas en español**; métricas presentadas de forma clara.

**Beneficios para el usuario**
- Comprensión rápida de la **situación actual** y de las **tendencias**.  
- Comparaciones entre **playas** y **periodos** sin salir del panel.  
- Identificación de **picos operativos** y oportunidades de mejora.
""")

st.divider()

###################################
# Guía de uso
###################################
st.subheader("🚀 Guía de uso")
st.markdown("""
1. **Elige la sección** en la barra lateral:  
   - *📈 Análisis Temporal* → visión agregada por periodo.  
   - *🏖️ Análisis por Playa* → comparación de playas.  
   - *📅 Día de la Semana* → hábitos semanales y variabilidad.
2. **Aplica los filtros** correspondientes (año, mes o fecha).  
3. **Interactúa con las gráficas:** usa el hover para valores exactos, zoom y la **leyenda** para mostrar/ocultar series.  
4. **Revisa las métricas** bajo cada gráfico para un resumen inmediato.  
5. **Explora el mapa de calor** (en *Por Playa > Mensual*) para detectar estacionalidad específica.

**Tip estratégico 🧠**  
Cruza los resultados de **📅 Día de la Semana** (promedios y variabilidad) con el **ranking por playa** del periodo seleccionado.  
Esto permite **priorizar recursos** (staff, limpieza, seguridad) en **días y playas críticas** con mayor impacto.
""")

st.divider()

###################################
# Elementos visuales y legibilidad
###################################
st.subheader("🎨 Elementos visuales")
st.markdown("""
- Uso moderado de **emojis** para orientar la navegación sin distraer.  
- Estructura con **encabezados**, **listas** y **separadores** para lectura escaneable.  
- Etiquetas, meses y días en **español** para coherencia con el contexto local.
""")
