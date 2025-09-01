import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import numpy as np

st.set_page_config(page_title="Análisis de Ocupación de Playas", page_icon="🏖️", layout="wide")
st.title("🏖️ Dashboard de Análisis de Ocupación de Playas")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("../Datos/ocupacion_playas_cancun_clean.csv")
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['fecha'])
        
        # Mapeo de días
        dias_semana_es = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes', 
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        df['dia_semana'] = df['fecha'].dt.day_name().map(dias_semana_es)
        df['año'] = df['fecha'].dt.year
        df['mes'] = df['fecha'].dt.month
        df['mes_nombre'] = df['fecha'].dt.month_name()
        
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

# Cargar datos
df = load_data()

if df is not None:
    # Sidebar para navegación
    st.sidebar.title("📊 Navegación")
    seccion = st.sidebar.selectbox(
        "Selecciona el análisis:",
        ["📈 Análisis Temporal", "🏖️ Análisis por Playa", "📅 Análisis por Día de la Semana"]
    )
    
    # ======================
    # SECCIÓN 1: ANÁLISIS TEMPORAL
    # ======================
    if seccion == "📈 Análisis Temporal":
        st.header("📈 Análisis Temporal Global")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            tipo_vista = st.selectbox(
                "Tipo de visualización:",
                ["Diario", "Mensual", "Anual"]
            )
        
        if tipo_vista == "Diario":
            with col2:
                año_sel = st.selectbox("Año:", sorted(df['año'].unique()))
            with col3:
                mes_sel = st.selectbox(
                    "Mes:", 
                    range(1, 13),
                    format_func=lambda x: calendar.month_name[x]
                )
            
            # Filtrar datos
            df_filtrado = df[(df['año'] == año_sel) & (df['mes'] == mes_sel)]
            serie = df_filtrado.groupby('fecha', as_index=False)['ocupacion'].sum()
            
            if not serie.empty:
                fig = px.line(
                    serie,
                    x='fecha',
                    y='ocupacion',
                    markers=True,
                    title=f'📊 Ocupación Diaria - {calendar.month_name[mes_sel]} {año_sel}',
                    labels={'fecha': 'Fecha', 'ocupacion': 'Ocupación Total (personas)'}
                )
                fig.update_layout(
                    xaxis_title="Fecha",
                    yaxis_title="Ocupación (personas)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas del período
                st.subheader("📊 Estadísticas del Período")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", f"{serie['ocupacion'].sum():,}")
                with col2:
                    st.metric("Promedio Diario", f"{serie['ocupacion'].mean():.0f}")
                with col3:
                    st.metric("Máximo", f"{serie['ocupacion'].max():,}")
                with col4:
                    st.metric("Mínimo", f"{serie['ocupacion'].min():,}")
            else:
                st.warning("No hay datos disponibles para el período seleccionado.")
        
        elif tipo_vista == "Mensual":
            with col2:
                año_sel = st.selectbox("Año:", sorted(df['año'].unique()))
            
            # Filtrar por año y agrupar por mes
            df_año = df[df['año'] == año_sel]
            serie = (df_año.groupby('mes', as_index=False)['ocupacion']
                    .sum()
                    .sort_values('mes'))
            serie['mes_nombre'] = serie['mes'].apply(lambda x: calendar.month_name[x])
            
            if not serie.empty:
                fig = px.line(
                    serie,
                    x='mes_nombre',
                    y='ocupacion',
                    markers=True,
                    title=f'📊 Ocupación Mensual - {año_sel}',
                    labels={'mes_nombre': 'Mes', 'ocupacion': 'Ocupación Total (personas)'}
                )
                fig.update_layout(
                    xaxis_title="Mes",
                    yaxis_title="Ocupación (personas)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas del año
                st.subheader("📊 Estadísticas del Año")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Anual", f"{serie['ocupacion'].sum():,}")
                with col2:
                    st.metric("Promedio Mensual", f"{serie['ocupacion'].mean():.0f}")
                with col3:
                    st.metric("Mejor Mes", f"{serie.loc[serie['ocupacion'].idxmax(), 'mes_nombre']}")
                with col4:
                    st.metric("Menor Mes", f"{serie.loc[serie['ocupacion'].idxmin(), 'mes_nombre']}")
            else:
                st.warning("No hay datos disponibles para el año seleccionado.")
        
        else:  # Anual
            serie = df.groupby('año', as_index=False)['ocupacion'].sum()
            
            fig = px.line(
                serie,
                x='año',
                y='ocupacion',
                markers=True,
                title='📊 Ocupación Anual - Serie Histórica',
                labels={'año': 'Año', 'ocupacion': 'Ocupación Total (personas)'}
            )
            fig.update_layout(
                xaxis_title="Año",
                yaxis_title="Ocupación (personas)",
                hovermode='x unified'
            )
            fig.update_xaxes(dtick=1)
            st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas históricas
            st.subheader("📊 Estadísticas Históricas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Histórico", f"{serie['ocupacion'].sum():,}")
            with col2:
                st.metric("Promedio Anual", f"{serie['ocupacion'].mean():.0f}")
            with col3:
                st.metric("Mejor Año", f"{serie.loc[serie['ocupacion'].idxmax(), 'año']}")
            with col4:
                st.metric("Crecimiento", f"{((serie['ocupacion'].iloc[-1] / serie['ocupacion'].iloc[0] - 1) * 100):.1f}%")
    
    # ======================
    # SECCIÓN 2: ANÁLISIS POR PLAYA
    # ======================
    elif seccion == "🏖️ Análisis por Playa":
        st.header("🏖️ Análisis de Ocupación por Playa")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            tipo_vista = st.selectbox(
                "Temporalidad:",
                ["Diario", "Mensual", "Anual"],
                key="playa_temporal"
            )
        
        # Obtener lista de playas disponibles
        playas_disponibles = sorted(df['nombre_playa'].unique()) if 'nombre_playa' in df.columns else ['Todas las playas']

        if tipo_vista == "Diario":
            with col2:
                año_sel = st.selectbox("Año:", sorted(df['año'].unique()), key="playa_año")
            with col3:
                mes_sel = st.selectbox(
                    "Mes:", 
                    range(1, 13),
                    format_func=lambda x: calendar.month_name[x],
                    key="playa_mes"
                )
            
            # Filtrar datos por período
            df_filtrado = df[(df['año'] == año_sel) & (df['mes'] == mes_sel)]
            
            if 'nombre_playa' in df.columns:
                serie = df_filtrado.groupby(['fecha', 'nombre_playa'], as_index=False)['ocupacion'].sum()
                
                if not serie.empty:
                    fig = px.line(
                        serie,
                        x='fecha',
                        y='ocupacion',
                        color='nombre_playa',
                        markers=True,
                        title=f'🏖️ Ocupación por Playa - {calendar.month_name[mes_sel]} {año_sel}',
                        labels={'fecha': 'Fecha', 'ocupacion': 'Ocupación (personas)', 'playa': 'Playa'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Ranking de playas
                    ranking = df_filtrado.groupby('nombre_playa')['ocupacion'].sum().sort_values(ascending=False)
                    st.subheader("🏆 Ranking de Playas")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.bar_chart(ranking.head(10))
                    with col2:
                        for i, (nombre_playa, ocupacion) in enumerate(ranking.head(5).items()):
                            st.metric(f"{i+1}. {nombre_playa}", f"{ocupacion:,} personas")
                else:
                    st.warning("No hay datos disponibles para el período seleccionado.")
            else:
                st.info("La columna 'nombre_playa' no está disponible en los datos.")

        elif tipo_vista == "Mensual":
            with col2:
                año_sel = st.selectbox("Año:", sorted(df['año'].unique()), key="playa_año_m")
            
            df_año = df[df['año'] == año_sel]

            if 'nombre_playa' in df.columns:
                serie = df_año.groupby(['mes', 'nombre_playa'], as_index=False)['ocupacion'].sum()
                serie['mes_nombre'] = serie['mes'].apply(lambda x: calendar.month_name[x])
                
                if not serie.empty:
                    fig = px.line(
                        serie,
                        x='mes_nombre',
                        y='ocupacion',
                        color='nombre_playa',
                        markers=True,
                        title=f'🏖️ Ocupación Mensual por Playa - {año_sel}',
                        labels={'mes_nombre': 'Mes', 'ocupacion': 'Ocupación (personas)', 'nombre_playa': 'Playa'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Heatmap de ocupación
                    pivot_data = serie.pivot(index='nombre_playa', columns='mes_nombre', values='ocupacion').fillna(0)
                    
                    fig_heatmap = px.imshow(
                        pivot_data,
                        aspect="auto",
                        title="🔥 Mapa de Calor - Ocupación por Playa y Mes",
                        labels=dict(x="Mes", y="Playa", color="Ocupación")
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.warning("No hay datos disponibles para el año seleccionado.")
            else:
                st.info("La columna 'playa' no está disponible en los datos.")
        
        else:  # Anual
            if 'nombre_playa' in df.columns:
                serie = df.groupby(['año', 'nombre_playa'], as_index=False)['ocupacion'].sum()
                
                fig = px.line(
                    serie,
                    x='año',
                    y='ocupacion',
                    color='nombre_playa',
                    markers=True,
                    title='🏖️ Ocupación Anual por Playa - Serie Histórica',
                    labels={'año': 'Año', 'ocupacion': 'Ocupación (personas)', 'nombre_playa': 'Playa'}
                )
                fig.update_xaxes(dtick=1)
                st.plotly_chart(fig, use_container_width=True)
                
                # Totales históricos por playa
                totales = df.groupby('nombre_playa')['ocupacion'].sum().sort_values(ascending=False)
                st.subheader("🏆 Totales Históricos por Playa")
                st.bar_chart(totales)
            else:
                st.info("La columna 'nombre_playa' no está disponible en los datos.")

    # ======================
    # SECCIÓN 3: ANÁLISIS POR DÍA DE LA SEMANA
    # ======================
    else:  # Análisis por Día de la Semana
        st.header("📅 Análisis por Día de la Semana")
        
        # Filtros opcionales
        col1, col2 = st.columns(2)
        with col1:
            años_disponibles = sorted(df['año'].unique())
            año_filtro = st.selectbox("Filtrar por año (opcional):", ['Todos'] + años_disponibles)
        
        with col2:
            if año_filtro != 'Todos':
                meses_disponibles = sorted(df[df['año'] == año_filtro]['mes'].unique())
                mes_filtro = st.selectbox(
                    "Filtrar por mes (opcional):", 
                    ['Todos'] + [calendar.month_name[m] for m in meses_disponibles],
                    key="dia_semana_mes"
                )
            else:
                mes_filtro = 'Todos'
        
        # Aplicar filtros
        df_filtrado = df.copy()
        if año_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['año'] == año_filtro]
        if mes_filtro != 'Todos':
            mes_num = list(calendar.month_name).index(mes_filtro)
            df_filtrado = df_filtrado[df_filtrado['mes'] == mes_num]
        
        # Agrupar por día de la semana
        ocupacion_por_dia = df_filtrado.groupby('dia_semana')['ocupacion'].agg([
            'sum', 'mean', 'median', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        # Ordenar días de la semana
        orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        ocupacion_por_dia = ocupacion_por_dia.reindex(orden_dias)
        
        # Gráfico principal
        fig = px.bar(
            x=ocupacion_por_dia.index,
            y=ocupacion_por_dia['sum'],
            title='📊 Ocupación Total por Día de la Semana',
            labels={'x': 'Día de la Semana', 'y': 'Ocupación Total (personas)'},
            color=ocupacion_por_dia['sum'],
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, xaxis_title="Día de la Semana", yaxis_title="Ocupación Total")
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de promedio
        fig_promedio = px.bar(
            x=ocupacion_por_dia.index,
            y=ocupacion_por_dia['mean'],
            title='📈 Ocupación Promedio por Día de la Semana',
            labels={'x': 'Día de la Semana', 'y': 'Ocupación Promedio (personas)'},
            color=ocupacion_por_dia['mean'],
            color_continuous_scale='Greens'
        )
        fig_promedio.update_layout(showlegend=False, xaxis_title="Día de la Semana", yaxis_title="Ocupación Promedio")
        st.plotly_chart(fig_promedio, use_container_width=True)
        
        # Estadísticas detalladas
        st.subheader("📊 Estadísticas Detalladas por Día")
        
        # Crear métricas por día
        for dia in orden_dias:
            if dia in ocupacion_por_dia.index:
                with st.expander(f"📅 {dia}"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total", f"{ocupacion_por_dia.loc[dia, 'sum']:,.0f}")
                        st.metric("Registros", f"{ocupacion_por_dia.loc[dia, 'count']:.0f}")
                    with col2:
                        st.metric("Promedio", f"{ocupacion_por_dia.loc[dia, 'mean']:.0f}")
                        st.metric("Mediana", f"{ocupacion_por_dia.loc[dia, 'median']:.0f}")
                    with col3:
                        st.metric("Máximo", f"{ocupacion_por_dia.loc[dia, 'max']:.0f}")
                        st.metric("Mínimo", f"{ocupacion_por_dia.loc[dia, 'min']:.0f}")
                    with col4:
                        st.metric("Desv. Estándar", f"{ocupacion_por_dia.loc[dia, 'std']:.0f}")
                        variabilidad = (ocupacion_por_dia.loc[dia, 'std'] / ocupacion_por_dia.loc[dia, 'mean']) * 100
                        st.metric("Variabilidad (%)", f"{variabilidad:.1f}%")
        
        # Tabla resumen
        st.subheader("📋 Tabla Resumen")
        df_display = ocupacion_por_dia.copy()
        df_display.columns = ['Total', 'Promedio', 'Mediana', 'Desv. Std', 'Mínimo', 'Máximo', 'Registros']
        df_display = df_display.round(0).astype(int)
        st.dataframe(df_display, use_container_width=True)
        
        # Insights automáticos
        st.subheader("💡 Insights Automáticos")
        dia_mas_ocupado = ocupacion_por_dia['sum'].idxmax()
        dia_menos_ocupado = ocupacion_por_dia['sum'].idxmin()
        dia_mas_variable = ocupacion_por_dia['std'].idxmax()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"📈 **Día más ocupado:** {dia_mas_ocupado}\n\nTotal: {ocupacion_por_dia.loc[dia_mas_ocupado, 'sum']:,.0f} personas")
        with col2:
            st.info(f"📉 **Día menos ocupado:** {dia_menos_ocupado}\n\nTotal: {ocupacion_por_dia.loc[dia_menos_ocupado, 'sum']:,.0f} personas")
        with col3:
            st.info(f"📊 **Día más variable:** {dia_mas_variable}\n\nDesv. Std: {ocupacion_por_dia.loc[dia_mas_variable, 'std']:.0f}")

else:
    st.error("No se pudieron cargar los datos. Verifica que el archivo CSV esté en la ruta correcta.")