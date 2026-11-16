import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("Explorar los datos")


archivo = st.file_uploader("Selecciona bicicletas_listas.csv", type=["csv"])

if st.button("Cargar datos"):
    if archivo is not None:
        # Lectura con coma, UTF-8 con BOM y parseo de fecha según especificaciones
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig", parse_dates=["fecha"])
        st.session_state["df_bici"] = df
        st.success(f"{len(df):,} registros cargados.")
    else:
        st.warning("Por favor, selecciona el archivo bicicletas_listas.csv antes de presionar Cargar datos.")

if st.session_state["df_bici"] is None:
    st.info("Instrucción: Sube el archivo 'bicicletas_listas.csv' arriba y haz clic en 'Cargar datos' para comenzar.")
    st.stop()

df = st.session_state["df_bici"].copy()

usuario = st.session_state["tipo_usuario"]
if usuario == "Todos":
    col_conteo = "alquileres_total"
elif usuario == "Ocasionales":
    col_conteo = "alquileres_ocasionales"
else:
    col_conteo = "alquileres_registrados"

df["alquileres"] = df[col_conteo]

dia = st.session_state["tipo_dia"]
if dia != "Todos":
    df = df[df["tipo_dia"] == dia]

h_min, h_max = st.session_state["rango_horas"]
df = df[(df["hora"] >= h_min) & (df["hora"] <= h_max)]

total_alquileres = int(df["alquileres"].sum())
promedio_hora = df["alquileres"].mean() if len(df) > 0 else 0.0

col1, col2 = st.columns(2)

col1.metric("Total de alquileres", f"{total_alquileres:,}".replace(",", "."))
col2.metric("Promedio por hora observada", f"{promedio_hora:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."))


tab_grafico, tab_datos = st.tabs(["Gráfico diario", "Datos"])

with tab_grafico:
    if len(df) > 0:
        
        df_diario = df.groupby("fecha", as_index=False)["alquileres"].sum()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_diario["fecha"], df_diario["alquileres"], color="#197A8D", linewidth=1.2)
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Alquileres por día")
        ax.grid(axis="y", linestyle="-", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        
        st.pyplot(fig)
    else:
        st.warning("No hay registros que coincidan con los filtros seleccionados.")

with tab_datos:
    df_mostrar = df.copy()
    df_mostrar["fecha"] = df_mostrar["fecha"].dt.strftime("%Y-%m-%d")
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
    
    csv_bytes = df_mostrar.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="Descargar datos filtrados",
        data=csv_bytes,
        file_name="bicicletas_filtradas.csv",
        mime="text/csv"
    )
    
    st.write("Fanaee-T, H. (2013). Bike Sharing [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Licencia CC BY 4.0.")
    st.link_button("Consultar la fuente en UCI", "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset")
