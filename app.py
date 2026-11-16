import streamlit as st

st.set_page_config(page_title="BiciDatos", layout="wide")

if "df_bici" not in st.session_state:
    st.session_state["df_bici"] = None
if "tipo_usuario" not in st.session_state:
    st.session_state["tipo_usuario"] = "Todos"
if "tipo_dia" not in st.session_state:
    st.session_state["tipo_dia"] = "Todos"
if "rango_horas" not in st.session_state:
    st.session_state["rango_horas"] = (0, 23)

st.sidebar.title("BiciDatos")

pag_explorar = st.Page("explorar.py", title="Explorar los datos", default=True)
pag_comparar = st.Page("comparar.py", title="Comparar horarios")

pg = st.navigation([pag_explorar, pag_comparar])

st.session_state["tipo_usuario"] = st.sidebar.selectbox(
    "Tipo de usuario",
    ["Todos", "Ocasionales", "Registrados"],
    index=["Todos", "Ocasionales", "Registrados"].index(st.session_state["tipo_usuario"])
)

st.session_state["tipo_dia"] = st.sidebar.radio(
    "Tipo de día",
    ["Todos", "Laborable", "No laborable"],
    index=["Todos", "Laborable", "No laborable"].index(st.session_state["tipo_dia"])
)

st.session_state["rango_horas"] = st.sidebar.slider(
    "Horas del día",
    min_value=0,
    max_value=23,
    value=st.session_state["rango_horas"]
)

pg.run()
