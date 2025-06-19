import streamlit as st
#Report_Builder
import matplotlib.patches as patches
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import openpyxl
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML
import seaborn as sns
import pandas as pd
import numpy as np
import markdown2
import textwrap
import os
import sys

# === Define Dorectories
variable_directory = {
    "Final del Periodo":"Periodo",
    "Duración":"Duracion",
    "Ingresos": "Ingresos",
    "Costo de Ventas":"Costo_de_Ventas",
    "Margen Bruto": "Margen_Bruto",
    "Gastos Admin.": "Gastos_Admin",
    "Utilidad Operacional": "Utilidad_Operacional",
    "Intereses Pagados": "Intereses_Pagados",
    "Ingresos/Gastos Extraordinarios": "Ingresos_o_Gastos_Extraordinarios",
    "Utilidad Neta Antes de Impuestos": "Utilidad_Neta_Antes_de_Impuestos",
    "Impuestos Pagados": "Impuestos_Pagados",
    "Utilidad Neta": "Utilidad_Neta",
    "Distribuciones/Dividendos": "Distribuciones_Dividendos",
    "Utilidad Retenida": "Utilidad_Retenida",
    "Efectivo": "Efectivo",
    "Cuentas por Cobrar": "Cuentas_X_Cobrar",
    "Inventario": "Inventario",
    "Otros Activos Corrientes": "Otros_Activos_Corrientes",
    "Activos Corrientes": "Activos_Corrientes",
    "Activos Fijos": "Activos_Fijos",
    "Otros Activos No Corrientes": "Otros_Activos_No_Corrientes",
    "Otros Activos" : "Otros_Activos",
    "Activos No Corrientes" : "Activos_No_Corrientes",
    "Total Activos" : "Total_Activos",
    "Cuentas por Pagar": "Cuentas_X_Pagar",
    "Prestamos Bancarios - Corrientes": "Prestamos_Bancarios_CP",
    "Otros Pasivos de Corto Plazo": "Otros_Pasivos_CP",
    "Pasivos de Corto Plazo": "Pasivos_CP",
    "Prestamos Bancarios - No Corrientes" : "Prestamos_Bancarios_LP",
    "Otros Pasivos de Largo Plazo": "Otros_Pasivos_LP",
    "Pasivos de Largo Plazo": "Pasivos_LP",
    "Total Pasivos": "Total_Pasivos",
    "Ganancias del Periodo": "Ganancias_del_Periodo",
    "Ganancias Retenidas": "Ganancias_Retenidas",
    "Patrimonio": "Patrimonio", #Equity = Suma de todo el capital social
    "Depreciación & Amortización":"Depreciacion_Y_Amortizacion",
    "Utilidad Neta %": "Utilidad_Neta_Perc",
    "Gastos Admin. %": 'Gastos_Admin_Perc',
    "Utilidad Operacional %": 'Utilidad_Operacional_Perc',
    'Margen Bruto %': 'Margen_Bruto_Perc',
    'Cobertura de Intereses': 'Cobertura_de_Intereses',
    'Días de Cuentas por Cobrar': 'Dias_Cuentas_X_Cobrar',
    'Días de Inventario': 'Dias_Inventario',
    'Días de Cuentas por Pagar': 'Dias_Cuentas_X_Pagar',
    'Dias de Capital de trabajo': 'Dias_Capital_de_Trabajo',
    'Capital de Trabajo': 'Capital_de_Trabajo',
    'Capital de Trabajo.': 'Capital_de_Trabajo_por_100Dlls',
    'Cuentas X Pagar.': 'Cuentas_X_Pagar_por_100Dlls',
    'Inventario.': 'Inventario_por_100Dlls',
    'Cuentas X Cobrar.': 'Cuentas_X_Cobrar_por_100Dlls',
    'Margen Bruto.': 'Margen_Bruto_por_100Dlls',
    'Rotación del Capital de Trabajo': 'Rotacion_Capital_de_Trabajo',
    'Margen del Flujo de Efectivo': 'Margen_de_Flujo_de_Efectivo',
    'Razón Corriente': 'Razon_Corriente',
    'Otro Capital': 'Otro_Capital',
    'Otro Capital %': 'Otro_Capital_Perc',
    'Rotacion de Otro Capital': 'Rotacion_Otro_Capital',
    'Retorno sobre Otro Capital %': 'Retorno_Sobre_Otro_Capital_Perc',
    'Activos Oper. Netos': 'Activos_Operativos_Netos',
    'Activos Operativos Netos %': 'Activos_Operativos_Netos_Perc',
    'Rotación de Activos': 'Rotacion_Activos',
    'Retorno Sobre Capital %': 'Retorno_Sobre_Capital_Perc',
    'Retorno Sobre Total de Activos %': 'Retorno_Sobre_Total_de_Activos_Perc',
    'Retorno Sobre Patrimonio %': 'Retorno_Sobre_Patrimonio_Perc',
    'Deuda Neta': 'Deuda_Neta',
    'Deuda Neta/Capital Social': 'Deuda_Neta_a_Capital_Social',
    'Deuda/Capital': 'Deuda_a_Capital',
    'Repago de Deuda': 'Repago_de_Deuda',
    'Flujo de Efectivo Neto':'Flujo_Efectivo_Neto',
    'Flujo de Efectivo Operacional':'Flujo_Efectivo_Operacional',
    'Beneficio del Efectivo Operacional':'Beneficio_Efectivo_Operacional',
    'Crecimiento de Ingresos %':'Crecimiento_Ingresos_Perc',
    'Crecimiento Costos Ventas %':'Crecimiento_Costo_de_Ventas_Perc',
    'Crecimiento Gastos Admin. %' : 'Crecimiento_Gastos_Admin_Perc',
    'Deuda Total':'Deuda_Total',
    'Flujo de Efectivo Marginal':'Flujo_Efectivo_Marginal',
    'Financiamiento Total' : 'Financiamiento_Total',
    'Impacto en el Efectivo':'Impacto_Efectivo',
    'Inversion en Capital de Trabajo':'Inversion_Capital_de_Trabajo',
    'Inversion en Otro Capital':'Inversion_Otro_Capital',
    'Flujo de Efectivo Neto 2' : 'Flujo_Efe_Fin',
    'Efectivo de Clientes':'Efectivo_de_Clientes',
    'Efectivo a Proveedores':'Efectivo_a_Proveedores',
    'Beneficio Efectivo Bruto':'Beneficio_Efectivo_Bruto',
    'Gastos Admin. sin Depreciación':'Gastos_Admin_LessDA',
    'Beneficio Operativo del Efectivo':'Beneficio_Operativo_Efectivo',
    'Flujo de Efectivo Operativo':'Flujo_Efectivo_Operativo',
    'Inversion en Activos Fijos':'Inversion_Activos_Fijos',
    'Inversion Neta en Otros Activos':'Inversion_Otros_Activos_Netos',
    'Capital Inyectado':'Capital_Inyectado',
    'Flujo de Efectivo Fin':'Flujo_Efe_Fin',
    'Salidas de Otro Efectivo':'Salidas_Otro_Efectivo'}

graphs = {}
logo_path = "plots/logo.png"  # Ensure the correct file location
logoP = "plots/logopequeño.jpeg"  # Ensure the correct file location
brackets_path = "plots/brackets.jpeg"  # Ensure the correct file location




# ─── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Auto-Fin Dashboard", layout="wide")
st.title("Auto-Fin Dashboard")
st.image(
    logo_path,
    caption="Logo de Auto-Fin",
    use_container_width=True,
)
st.markdown("## 🔐 Secure Login System")

# ─── Session-State Defaults ────────────────────────────────────────────────────
for key, default in {
    "logged_in": False,
    "username":  None,
    "role":      None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Login Page ────────────────────────────────────────────────────────────────
def login_page():
    st.subheader("Login")

    # wrap inputs in a form so they don't vanish mid-click
    with st.form("login_form", clear_on_submit=False):
        user = st.text_input("Username")
        pwd  = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        users = st.secrets["users"]

        if user not in users:
            st.error("❌ Username not found")
            return

        if pwd != users[user]["password"]:
            st.error("❌ Incorrect password")
            return

        # ✅ Success path
        st.session_state.logged_in = True
        st.session_state.username  = user
        st.session_state.role      = users[user]["role"]
        st.success(f"Logged in as **{st.session_state.role}**")

        # NEW: explicit rerun if you want to jump straight to upload_page()
        st.rerun()

# ─── Upload Page ───────────────────────────────────────────────────────────────
def upload_page():
    import os

    st.subheader("📤 Upload Your Excel File")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file:
        try:
            # Step 1: Read the specific sheet with required options
            df_raw = pd.read_excel(uploaded_file, sheet_name="Inputs", skiprows=7, header=None)

            st.success("✅ File uploaded and read from 'Inputs' sheet successfully!")
            st.dataframe(df_raw)

            # Optional: store it in session_state if you need to use it on another page
            st.session_state["df_raw"] = df_raw

        except Exception as e:
            st.error(f"❌ Error reading 'Inputs' sheet from Excel file: {e}")

    # Logout button
    if st.button("Logout"):
        for key in ("logged_in", "username", "role", "df_raw"):
            st.session_state[key] = None
        st.rerun()
        
# ─── App Entry ────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    upload_page()
else:
    login_page()

#Report_Builder
import matplotlib.patches as patches
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import openpyxl
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML
import seaborn as sns
import pandas as pd
import numpy as np
import markdown2
import textwrap
import os
import sys
