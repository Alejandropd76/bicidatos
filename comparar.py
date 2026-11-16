import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Comparar horarios")

if st.session_state.get("df_bici") is None:
    st.info("Instrucción: Ve primero a 'Explorar los datos' y carga el archivo 'bicicletas_listas.csv'.")
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

if len(df) == 0:
    st.warning("No hay registros disponibles con los filtros actuales.")
    st.stop()

color_barras = st.color_picker("Color de las barras", value="#197A8D")

df_horas = df.groupby("hora", as_index=False)["alquileres"].mean()
df_horas.rename(columns={"alquileres": "Promedio de alquileres"}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df_horas["hora"], df_horas["Promedio de alquileres"], color=color_barras, width=0.65)
ax.set_xlabel("Hora del día")
ax.set_ylabel("Alquileres por hora observada")
ax.set_xticks(range(0, 24, 2))
ax.grid(axis="y", linestyle="-", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

st.pyplot(fig)

if st.checkbox("Mostrar tabla de promedios"):
    df_tabla = df_horas.copy()
    df_tabla["Hora"] = df_tabla["hora"].apply(lambda h: f"{h:02d}:00")
    df_tabla["Promedio"] = df_tabla["Promedio de alquileres"].round(2)
    st.dataframe(df_tabla[["Hora", "Promedio"]], use_container_width=True, hide_index=True)

st.divider()

limite = st.number_input("Límite de alquileres por hora", min_value=0, value=250, step=10)

horas_superan = df_horas[df_horas["Promedio de alquileres"] > limite]["hora"].tolist()
total_horas_con_datos = len(df_horas)

st.metric(
    label="Horarios con promedio mayor que el límite",
    value=f"{len(horas_superan)}/{total_horas_con_datos}"
)

if len(horas_superan) > 0:
    lista_formateada = ", ".join([f"{h:02d}:00" for h in horas_superan])
    st.write(f"**Horarios:** {lista_formateada}.")
else:
    st.write("**Horarios:** Ninguno supera el límite establecido.")
