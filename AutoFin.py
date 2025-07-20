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
import textwrap
import os
import sys
import locale
from fpdf import FPDF

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
logoP_path = "plots/logopequeño.jpeg"  # Ensure the correct file location
brackets_path = "plots/brackets.jpeg"  # Ensure the correct file location
Ajuste = 0
df_transposed = {}
df_trans_latest_two = {}
EBITDA_Ajustada = 0
ValorObjetivo = 0
Usuario = ""
Company_Name = ""
df_raw = {}
# Initialize dictionary to store generated tables
tables = {} 

# ─── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Auto-Fin Dashboard", layout="wide")
st.title("Auto-Fin Dashboard")
st.image(
    logo_path,
    caption="Logo de Auto-Fin",
    use_container_width=True)
st.markdown("## 🔐 Secure Login System")

# ─── Session-State Defaults ────────────────────────────────────────────────────
for key, default in {
    "logged_in": False,
    "username":  None,
    "role":      None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =============== Crear dfs ===================#
def build_power_of_one(df_raw):
    """    Generate the 'Poder del UNO' impact table based on latest financial period.
    Parameters:    - df_raw (pd.DataFrame): Financial data (variables as index, periods as columns)
    Returns:    - Power_of_ONE_df (pd.DataFrame): Table with impact from pricing, volume, cost, and WC levers"""
    latest_col = df_raw.columns[-1]
    Power_of_ONE_df = pd.DataFrame(columns=["Flujo de efectivo neto", "Utilidad Operacional"], index=[
        "Posición_Actual", "Incre_Precio_Perc", "Incre_Volumen_Perc",
        "Reduc_Costo_de_Ventas_Perc", "Reduc_Gastos_Admin_Perc",
        "Reduc_Cuentas_X_Cobrar_Dias", "Reduc_Inventario_Dias",
        "Incre_Cuentas_X_Pagar_Dias", "Impacto_Poder_UNO", "Pósicion_Ajustada"])
    # Define movement assumptions
    movimientos = {
        "Incre_Precio_Perc": 0.01,
        "Incre_Volumen_Perc": 0.01,
        "Reduc_Costo_de_Ventas_Perc": 0.01,
        "Reduc_Gastos_Admin_Perc": 0.01,
        "Reduc_Cuentas_X_Cobrar_Dias": 1,
        "Reduc_Inventario_Dias": 1,
        "Incre_Cuentas_X_Pagar_Dias": 1    }
    Power_of_ONE_df["Movimiento"] = Power_of_ONE_df.index.map(movimientos)
    # Extract needed base values from latest column
    ingresos = df_raw.at["Ingresos", latest_col]
    costos = df_raw.at["Costo_de_Ventas", latest_col]
    utilidad_op = df_raw.at["Utilidad_Operacional", latest_col]
    gastos_admin = df_raw.at["Gastos_Admin", latest_col]
    flujo_efectivo = df_raw.at["Flujo_Efectivo_Neto", latest_col]
    dias_cxc = df_raw.at["Dias_Cuentas_X_Cobrar", latest_col]
    dias_inv = df_raw.at["Dias_Inventario", latest_col]
    dias_cxp = df_raw.at["Dias_Cuentas_X_Pagar", latest_col]
    # Posición actual
    Power_of_ONE_df.at["Posicion_Actual", "Utilidad Operacional"] = utilidad_op
    Power_of_ONE_df.at["Posicion_Actual", "Flujo de efectivo neto"] = flujo_efectivo
    # Incremento Precio
    incr_precio = ingresos * movimientos["Incre_Precio_Perc"]
    Power_of_ONE_df.at["Incre_Precio_Perc", "Utilidad Operacional"] = incr_precio
    Power_of_ONE_df.at["Incre_Precio_Perc", "Flujo de efectivo neto"] = (1 - dias_cxc / 365) * incr_precio
    # Incremento Volumen
    utilidad_vol = (ingresos - costos) * movimientos["Incre_Volumen_Perc"]
    flujo_vol = ((1 - dias_cxc / 365) * ingresos - (1 + dias_inv / 365 - dias_cxp / 365) * costos) * movimientos["Incre_Volumen_Perc"]
    Power_of_ONE_df.at["Incre_Volumen_Perc", "Utilidad Operacional"] = utilidad_vol
    Power_of_ONE_df.at["Incre_Volumen_Perc", "Flujo de efectivo neto"] = flujo_vol
    # Reducción Costo Ventas
    ahorro_costos = costos * movimientos["Reduc_Costo_de_Ventas_Perc"]
    flujo_costos = ahorro_costos * (1 + dias_inv / 365 - dias_cxp / 365)
    Power_of_ONE_df.at["Reduc_Costo_de_Ventas_Perc", "Utilidad Operacional"] = ahorro_costos
    Power_of_ONE_df.at["Reduc_Costo_de_Ventas_Perc", "Flujo de efectivo neto"] = flujo_costos
    # Reducción Gastos Admin
    ahorro_admin = gastos_admin * movimientos["Reduc_Gastos_Admin_Perc"]
    Power_of_ONE_df.at["Reduc_Gastos_Admin_Perc", "Utilidad Operacional"] = ahorro_admin
    Power_of_ONE_df.at["Reduc_Gastos_Admin_Perc", "Flujo de efectivo neto"] = ahorro_admin
    # Mejora WC
    Power_of_ONE_df.at["Reduc_Cuentas_X_Cobrar_Dias", "Flujo de efectivo neto"] = \
        ingresos / 365 * movimientos["Reduc_Cuentas_X_Cobrar_Dias"]
    Power_of_ONE_df.at["Reduc_Inventario_Dias", "Flujo de efectivo neto"] = \
        costos / 365 * movimientos["Reduc_Inventario_Dias"]
    Power_of_ONE_df.at["Incre_Cuentas_X_Pagar_Dias", "Flujo de efectivo neto"] = \
        costos / 365 * movimientos["Incre_Cuentas_X_Pagar_Dias"]
    # Totales intermedios
    rows = [
        "Incre_Precio_Perc", "Incre_Volumen_Perc", "Reduc_Costo_de_Ventas_Perc",
        "Reduc_Gastos_Admin_Perc", "Reduc_Cuentas_X_Cobrar_Dias",
        "Reduc_Inventario_Dias", "Incre_Cuentas_X_Pagar_Dias"]
    Power_of_ONE_df.at["Impacto_Poder_UNO", "Flujo de efectivo neto"] = Power_of_ONE_df.loc[rows, "Flujo de efectivo neto"].sum()
    Power_of_ONE_df.at["Impacto_Poder_UNO", "Utilidad Operacional"] = Power_of_ONE_df.loc[rows, "Utilidad Operacional"].sum()
    # Posición ajustada
    Power_of_ONE_df.at["Posicion_Ajustada", "Flujo de efectivo neto"] = \
        Power_of_ONE_df.at["Impacto_Poder_UNO", "Flujo de efectivo neto"] + flujo_efectivo
    Power_of_ONE_df.at["Posicion_Ajustada", "Utilidad Operacional"] = \
        Power_of_ONE_df.at["Impacto_Poder_UNO", "Utilidad Operacional"] + utilidad_op
    return Power_of_ONE_df
def build_Valuation(df_raw, df_power):
    """    Generar las 'Valuaciones' based on latest financial period.
    Parameters:    - df_raw (pd.DataFrame): Financial data (variables as index, periods as columns)
    Parameters:    - df_power (pd.DataFrame): Financial data (variables as index, type of outcome (profit, Cash flow) as columns)
        Returns:    - Power_of_ONE_df (pd.DataFrame): Table with impact from pricing, volume, cost, and WC levers"""
    latest_col = df_raw.columns[-1]
    
    Valuacion = pd.DataFrame(columns=[4,3,5], index = [
        "Valor Bruto del Negocio",
        "Deuda Total",
        "Valor Actual de tu Negocio",
        "Incremento de Precio %",
        "Incremento de Volumen %",
        "Reducción del Costo de Ventas %",
        "Reducción de Gastos Admin %",
        "Impacto de la Ganancia en la Valoración",
        "Reducción en Días de Cuentas por Cobrar",
        "Reducción en Días de Inventario",
        "Aumento en Días de Cuentas por Pagar",
        "Impacto del Efectivo en la Valoración",
        "Impacto de tu Poder del Uno",
        "Valor Objetivo del Negocio",
        "Brecha de Valor Actual",
        "Valor del Negocio Mejorado",
        "Brecha de Valor Mejorada"])
    # Extract needed base values from latest column
    deudas = df_raw.at["Deuda_Total", latest_col]
    pxIncre = df_power.at["Incre_Precio_Perc", "Utilidad Operacional"]
    volIncre = df_power.at["Incre_Volumen_Perc", "Utilidad Operacional"]
    COGSRedu = df_power.at["Reduc_Costo_de_Ventas_Perc", "Utilidad Operacional"]
    GtosAdminRedu = df_power.at["Reduc_Gastos_Admin_Perc", "Utilidad Operacional"]
    ReduAR = df_power.at["Reduc_Cuentas_X_Cobrar_Dias", "Flujo de efectivo neto"]
    IncrAP = df_power.at["Incre_Cuentas_X_Pagar_Dias", "Flujo de efectivo neto"]
    ReduInv = df_power.at["Reduc_Inventario_Dias", "Flujo de efectivo neto"]
    # Posición actual
    Valuacion.loc["Deuda Total"] = deudas
    Valuacion.loc["Múltiplo de Ganancias"] = np.array([
    float(col) if (isinstance(col, int) or (isinstance(col, str) and col.isdigit())) else np.nan
    for col in Valuacion.columns])
    Valuacion.loc["Valor Bruto del Negocio"] = EBITDA_Ajustada * np.array(
    [col if isinstance(col, int) else int(col) for col in Valuacion.columns 
     if (isinstance(col, str) and col.isdigit()) or isinstance(col, int)])
    Valuacion.loc["Valor Actual de tu Negocio"] = Valuacion.loc["Valor Bruto del Negocio"] - Valuacion.loc["Deuda Total"]
    Valuacion.loc["Incremento de Precio %"] = pxIncre * np.array(
    [col if isinstance(col, int) else int(col) for col in Valuacion.columns 
     if (isinstance(col, str) and col.isdigit()) or isinstance(col, int)])
    Valuacion.loc["Incremento de Volumen %"] = volIncre * np.array(
    [col if isinstance(col, int) else int(col) for col in Valuacion.columns 
     if (isinstance(col, str) and col.isdigit()) or isinstance(col, int)])
    Valuacion.loc["Reducción del Costo de Ventas %"] = COGSRedu * np.array(
    [col if isinstance(col, int) else int(col) for col in Valuacion.columns 
     if (isinstance(col, str) and col.isdigit()) or isinstance(col, int)])
    Valuacion.loc["Reducción de Gastos Admin %"] = GtosAdminRedu * np.array(
    [col if isinstance(col, int) else int(col) for col in Valuacion.columns 
     if (isinstance(col, str) and col.isdigit()) or isinstance(col, int)])
    Impactorows = ["Incremento de Precio %", "Incremento de Volumen %", "Reducción del Costo de Ventas %","Reducción de Gastos Admin %",]
    Valuacion.loc["Impacto de la Ganancia en la Valoración"] = Valuacion.loc[Impactorows,:].sum()
    Valuacion.loc["Reducción en Días de Cuentas por Cobrar"] = ReduAR
    Valuacion.loc["Aumento en Días de Cuentas por Pagar"] = IncrAP
    Valuacion.loc["Reducción en Días de Inventario"] = ReduInv
    CashRows = ["Reducción en Días de Cuentas por Cobrar","Reducción en Días de Inventario", "Aumento en Días de Cuentas por Pagar"]
    Valuacion.loc["Impacto del Efectivo en la Valoración"] = Valuacion.loc[CashRows,:].sum()
    Valuacion.loc["Impacto de tu Poder del Uno"] = Valuacion.loc["Impacto del Efectivo en la Valoración",:]+Valuacion.loc["Impacto de la Ganancia en la Valoración",:]
    Valuacion.loc["Valor del Negocio Mejorado"] = Valuacion.loc["Impacto de tu Poder del Uno",:]+Valuacion.loc["Valor Actual de tu Negocio",:]
    Valuacion.loc["Valor Objetivo del Negocio"] = ValorObjetivo
    Valuacion.loc["Brecha de Valor Actual"] = Valuacion.loc["Valor Actual de tu Negocio",:] - Valuacion.loc["Valor Objetivo del Negocio",:]
    Valuacion.loc["Brecha de Valor Mejorada"] = Valuacion.loc["Valor del Negocio Mejorado",:] - Valuacion.loc["Valor Objetivo del Negocio",:]
    return Valuacion
# =============== Crear graficas ===================#
def plot_business_valuation_stacked(df_Valuacion, output_dir="plots"):
    current = df_Valuacion.at["Valor Actual de tu Negocio", df_Valuacion.columns[-1]]
    impact = df_Valuacion.at["Impacto de tu Poder del Uno", df_Valuacion.columns[-1]]
    target = df_Valuacion.at["Valor Objetivo del Negocio", df_Valuacion.columns[-1]]
    labels = ['Valor Objetivo', 'Valor Mejorado']
    values_target = [target, 0]
    values_current = [0, current]
    values_impact = [0, impact]
    x = np.arange(len(labels))
    width = 0.6
    fig, ax = plt.subplots(figsize=(4.5, 2))
    # Bars
    ax.bar(x, values_target, width, color='#f3a24f', label='Valor Objetivo')
    ax.bar(x, values_current, width, color='#14457b', label='Valor Actual del Negocio')
    ax.bar(x, values_impact, width, bottom=values_current, color='#3fa9f5', label='Impacto del Poder del Uno')
    # Labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels,fontsize=7, color='gray')
    ax.set_ylim(0, max(target, current + impact) * 1.15)
    ax.tick_params(axis='y', labelsize=8, color='gray')
    ax.tick_params(axis='x', labelsize=8, color='gray')
    ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax.grid(axis='y', linestyle='-', alpha=0.2)
    ax.legend(
        title_fontsize=6,
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        ncol=1,
        fontsize=6,
        frameon=False,
        fancybox=True,
        columnspacing=0.8,
        handletextpad=0.4,
        labelcolor='gray'    )
    # Prevent y-axis scaling and scientific notation
    ax.ticklabel_format(style='plain', axis='y')  # disable 1e6
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))  # format with comma
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "Valuation_StackedBar.svg")
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    print ('Generating graph: Valuation_StackedBar...')
    return {"Valuation_StackedBar": path}
def Blocks_Plot(graph_data, df_transposed, output_dir="plots"):
    """ Creates a box-style financial diagram with values for a set of variables.
    Parameters:
    - graph_data: dict with:
        - GraphName: filename
        - variables: list of variable keys to extract from df
        - colors: list of corresponding box colors
    - df_transposed: DataFrame with variables as index and periods as columns
    - output_dir: where to save the image
    Returns: dict with {GraphName: file_path}"""
    variables = graph_data["variables"]
    colors = graph_data["colors"]
    graph_name = graph_data["GraphName"]
    # Get latest period and values
    latest_period = df_transposed.index[-1]
    values = [df_transposed.at[latest_period, var] if var in df_transposed.columns else None for var in variables]
    # Position layout — you can customize this further
    positions = {
        0: (100, 200),  # First variable (e.g. Inventario)
        1: (260, 200),  # Second (e.g. CxC)
        2: (410, 200),  # Third (e.g. CxP)
        3: (260, 90)}    # Final denominator (e.g. Ingresos)
    # Setup plot
    fig, ax = plt.subplots(figsize=(4, 3.))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 300)
    ax.axis('off')
    # Draw boxes
    for i, (x, y) in positions.items():
        val = values[i]
        var = variables[i]
        label = " " if pd.notna(val) else " \nN/A"
        ax.text(
            x, y, label,
            fontsize=5, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle="square", facecolor=colors[i], edgecolor=colors[i], pad=5.7),
            color='white')
    for i, (x, y) in positions.items():
        val = values[i]
        var = variables[i]
        label = f"\n\n{var.replace('_', ' ')}\n\n\n\n" if pd.notna(var) else f"{val}"
        ax.text(
            x, y, label,
            fontsize=5.2, fontweight='bold',
            ha='center', va='center',
            color='white')
    for i, (x, y) in positions.items():
        val = values[i]
        var = variables[i]
        label = f"${val:,.0f}" if pd.notna(val) else f"{var}\nN/A"
        ax.text(
            x, y-6, label,
            fontsize=7, fontweight='normal',
            ha='center', va='center',
            color='white')
    # Symbols
    ax.text(180, 200, "+", fontweight='bold', fontsize=15, ha='center', va='center', color='gray')
    ax.text(330, 200, "-", fontweight='bold', fontsize=15, ha='center', va='center', color='gray')
    ax.text(520, 150, "=", fontweight='bold', fontsize=15, ha='center', va='center', color='gray')
    # Divider
    ax.hlines(145, 43, 470, colors='lightgray', linestyles='-', linewidth=1.2)
    # Save
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    global graphs
    if 'graphs' not in globals():
        graphs = {}
    graphs[graph_name] = path
    return {graph_name: path}
#== Grouped Bar Graphs
def Period_Grouped_bars(graph_data, output_dir="plots"):
    df = graph_data.get("df", df_transposed)
    variables = graph_data["variables"]
    colors = graph_data["colors"]
    graph_name = graph_data["GraphName"]
    df = df.dropna(subset=variables, how='any')
    periods = graph_data.get("periodos", df.index)
    num_vars = len(variables)
    bar_width = 0.2
    x = np.arange(len(periods))
    fig, ax = plt.subplots(figsize=(6, 1.5))
    VariableNames = [next((k for k, v in variable_directory.items() if v == var), var) for var in variables]
    for i, var in enumerate(variables):
        label = VariableNames[i]
        offset = (i - (num_vars - 1) / 2) * bar_width
        ax.bar(x + offset + 0.08 * offset, df.loc[periods, var].values, width=bar_width, color=colors[i], label=label, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=7, color='gray')
    ax.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.15, zorder=1)
    ax.tick_params(axis='y', labelsize=6, colors='gray', width=0.8, length=0)
    ax.tick_params(axis='x', bottom=False)
    ax.axhline(0, color= 'lightgray' , linewidth=2.5, zorder=4)
    ax.legend(
        title="Periodo", title_fontsize=6, loc='center left',
        bbox_to_anchor=(1.02, 0.5), ncol=1, fontsize=6, frameon=False,
        fancybox=True, columnspacing=0.8, handletextpad=0.4, labelcolor='gray')
    def format_k_m(val, pos=None):
        if abs(val) >= 1_000_000:
            return f"{val/1_000_000:.1f}M"
        elif abs(val) >= 1_000:
            return f"{val/1_000:.1f}k"
        elif abs(val) <= 1:
            return f"{val*100:.1f}"
        else:
            return f"{val:.1f}"
    for i, period in enumerate(periods):
        values = df.loc[period, variables].values
        for j, val in enumerate(values):
            if pd.notna(val):
                xpos = x[i] + (j - (num_vars - 1) / 2) * bar_width
                ypos = val * 1.1 
                ax.text(xpos, ypos, format_k_m(val), ha='center', va='bottom' if val >= 0 else 'top', fontsize=5.5, color='gray', zorder=5)
    ax.yaxis.set_major_formatter(FuncFormatter(format_k_m))
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    graphs[graph_name] = path
    return {graph_name: path}
#== Equation Bar Graphs
def Eq_Bar_graphs(graph_data, output_dir="plots"):
    """    Generates a financial equation-style bar chart.
    Parameters:
    - graph_data (dict): Contains keys:
        - GraphName (str)
        - variables (list of str)
        - colors (list of str)
        - symbols (list of str)    """
    df = df_transposed
    variables = graph_data["variables"]
    colors = graph_data.get("colors", ['gray'] * len(variables))
    symbols = graph_data.get("symbols", [])
    graph_name = graph_data["GraphName"]
    # Resolve variable display names
    VariableNames = [next((k for k, v in variable_directory.items() if v == var), var) for var in variables]
    # Extract values from latest period
    last_period_values = df.iloc[-1]
    values = [last_period_values.get(var, 0) for var in variables]
    positions = range(len(variables))
    fig, ax = plt.subplots(figsize=(7, 1.5))
    # Plot bars
    ax.bar(positions, values, color=colors[:len(variables)], width=0.4, zorder=3)
    # Add labels below bars
    for pos, val, label in zip(positions, values, VariableNames):
        ax.text(pos, -max(values)*0.07, label, ha='center', va='top', fontsize=6, color='gray', fontweight='bold')
        ax.text(pos, -max(values)*0.2, f"${val:,.0f}", ha='center', va='top', fontsize=6, color='gray')
    # Insert math symbols between bars
    for i, symbol in enumerate(symbols):
        ax.text(i + 0.5, -max(values)*0.02, symbol, fontsize=16, ha='center', va='top', fontweight='bold', color='gray')
        if symbol == "=":
            ax.plot([i+0.35, i+0.65], [0, 0], color="white", linewidth=3, zorder=5)
    # Grid and formatting
    ax.grid(which='major', linestyle='-', linewidth=0.4, color='lightgray', alpha=0.2, zorder=1)
    ax.axhline(0, color='lightgray', linewidth=3, zorder=2.5)
    ax.set_yticks([])  # Remove y ticks
    ax.set_xticks([])  # Remove x ticks
    ax.tick_params(left=False, bottom=False)
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    global graphs
    if 'graphs' not in globals():
        graphs = {}
    graphs[graph_name] = path
    return {graph_name: path}
#== Stacked Variables X Periods Bar Graphs
def Stacked_graph(graph_data, output_dir="plots"):
    """   Create a stacked bar chart from financial data.
    Parameters:
    - graph_data (dict): {
        "GraphName": str,  # File name (without extension)
        "df": pd.DataFrame (optional),  # DataFrame indexed by period
        "variables": list of str,  # Internal variable names to stack
        "colors": list of str      # Colors corresponding to variables}
    Returns:
    - dict: {GraphName: saved_file_path} """
    # === Extract inputs
    df = graph_data.get("df", df_transposed)
    variables = graph_data["variables"]
    colors = graph_data["colors"]
    graph_name = graph_data["GraphName"]
    # === Map internal variable names to readable labels
    VariableNames = [k for var in variables for k, v in variable_directory.items() if v == var]
    VariableNames = [
        VariableNames[i] if i < len(VariableNames) else var
        for i, var in enumerate(variables)]
    # === Setup plot
    fig, ax = plt.subplots(figsize=(6, 1.5))
    bottom = None
    # === Plot stacked bars
    bars = []
    for i, var in enumerate(variables):
        label = VariableNames[i]
        values = df[var].values
        bar = ax.bar(df.index, values, color=colors[i], label=label, bottom=bottom, width=0.4, zorder=3)
        bars.append(bar)
        bottom = values if bottom is None else bottom + values
    # Add data labels on bars
    for bar_group in bars:
        for bar in bar_group:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{height:,.0f}",
                    ha='center', va='center',
                    fontsize=6,
                    color='white' if bar.get_facecolor()[:3] < (0.7, 0.7, 0.7) else 'black',
                    fontweight='normal',
                    zorder=5)
    # === Calculate max y to scale annotations
    max_total = df[variables].sum(axis=1).max()
    # === Hide axes & grid formatting
    ax.grid(which='major', linestyle='-', linewidth=0.4, color='lightgray', alpha=0.2, zorder=2)
    ax.set_xticks([])
    ax.tick_params(axis='y', labelsize=6, colors='#888888', width=0.8, length=4 )
    # Optional: Style gridlines (for reference)
    ax.grid(axis='y', color='lightgray', linestyle='--', linewidth=0.4,alpha=0.2)
    ax.axhline(0, color='lightgray', linewidth=2.5, zorder=4,alpha=0.2)
    
    ax.tick_params(axis='x', bottom=False)
    y_max = df[variables].sum(axis=1).max()
    step = max(int(round(y_max / 4, -2)), 100)  # asegura mínimo de 100
    ax.set_yticks(range(0, int(y_max) + step, step))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
    # Format grid and axes
    ax.grid(which='major', linestyle='-', linewidth=0.4, color='lightgray', alpha=0.2, zorder=2)
    ax.axhline(0, color='lightgray', linewidth=2.5, zorder=4)
    ax.set_xticks([])
    # Legend (only keep custom labels)
    ax.legend(
    loc='center left',         # Puts legend at the top center
    bbox_to_anchor=(1.02, 0.5), # Moves legend up, centered above plot
    ncol=1,        # One column per variable (horizontal layout) len(variables)
    fontsize=6,                 # Smaller font
    frameon=False,               # ✅ Draw a border box
#    framealpha=0.9,             # Slight transparency
    fancybox=True,              # Rounded corners
#    edgecolor='lightgray',      # Subtle border
    columnspacing=0.8,          # Reduce space between entries
    handletextpad=0.4,      # Tighten spacing between color and text
    labelcolor = 'gray')          
    # === Remove spines
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    # === Add period annotations below each bar
    for x in df.index:
        if hasattr(x, 'strftime'):
            date_str = x.strftime('%Y-%m-%d')
        else:
            date_str = str(x)
        ax.text(x, -0.1 * max_total, "Deuda Total",
                ha='center', va='top', fontsize=6, color='gray', fontweight='normal')
        ax.text(x, -0.2 * max_total, date_str,
                ha='center', va='top', fontsize=6, color='gray', fontweight='normal')
    # Disable scientific notation and force regular comma-separated formatting
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
    # === Save plot
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)
    # === Update and return global graph path registry
    global graphs
    if 'graphs' not in globals():
        graphs = {}
    graphs[graph_name] = path
    return {graph_name: path}
def Grouped_Bar_Graph(graph_data, output_dir="plots"):
    """Create a grouped bar chart from financial data."""
    df = graph_data.get("df", df_raw)  # Use provided df or fallback
    variables = graph_data["variables"]
    colors = graph_data["colors"]
    graph_name = graph_data["GraphName"]
    periods = df.columns.tolist()
    x = np.arange(len(variables))
    width = 0.2
    n = len(periods)
    # Map internal to display names
    VariableNames = [k for var in variables for k, v in variable_directory.items() if v == var]
    VariableNames = [
        VariableNames[i] if i < len(VariableNames) else var
        for i, var in enumerate(variables)    ]
    fig, ax = plt.subplots(figsize=(6, 1.5))
    # === Plot bars
    for i, period in enumerate(periods):
        values = df.loc[variables, period].values
        ax.bar(x + i * width + 0.06 * width * i, values, width=width, color=colors[i], label=str(period), zorder=3)
    ax.set_xticks(x + width * (n - 1) / 2)
    ax.set_xticklabels(VariableNames, rotation=0, fontsize=7, color='gray')
    ax.grid(axis='y', linestyle='-', linewidth=0.5, alpha=0.15, zorder=2)
    ax.tick_params(axis='y', labelsize=6, colors= 'gray', width=0.8, length=0)
    ax.tick_params(axis='x', bottom=False)
    ax.axhline(0, color='lightgray', linewidth=2.5, zorder=4)
    # === Format y-axis
    def format_k_m_label(val):
        if abs(val) >= 1_000_000:
            return f"{val/1_000_000:.1f}M"
        elif abs(val) >= 1_000:
            return f"{val/1_000:.1f}k"
        elif abs(val) <= 1:
            return f"{val*100:.1f}"
        else:
            return f"{val:.1f}"

    def format_k_m_tick(val, _):
        return format_k_m_label(val)
    ax.yaxis.set_major_formatter(FuncFormatter(format_k_m_tick))
    # === Add labels on bars
    for i, period in enumerate(periods):
        values = df.loc[variables, period].values
        for j, val in enumerate(values):
            if np.isnan(val): continue
            xpos = x[j] + i * width + 0.06 * width * i
            ypos = val * 1.1 if val >= 0 else val *-1.1
            ha = 'center'
            va = 'bottom' if val >= 0 else 'top'
            ax.text(xpos, ypos, format_k_m_label(val), ha=ha, va=va, fontsize=5.5, color='gray', zorder=5)
    # === Legend
    ax.legend(
        title="Periodo",
        title_fontsize=6,
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        ncol=1,
        fontsize=6,
        frameon=False,
        fancybox=True,
        columnspacing=0.8,
        handletextpad=0.4,
        labelcolor='gray'    )
    # === Hide spines
    for side in ['top', 'right', 'left', 'bottom']:
        ax.spines[side].set_visible(False)
    # === Save
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    global graphs
    if 'graphs' not in globals():
        graphs = {}
    graphs[graph_name] = path
    return {graph_name: path}
def create_shortfall_legend(amount, output_path="plots/shortfall_legend.svg"):
    """
    Crea una imagen con la leyenda de financiamiento requerido o superávit.
    El color se ajusta según si el valor es positivo (superávit) o negativo (shortfall).

    Parámetros:
    - amount (float): cantidad a mostrar (puede ser negativa)
    - output_path (str): ruta de guardado de la imagen
    """
    # Estilos según valor
    if amount >= 0:
        bg_color = '#d3f6d1'     # verde claro
        text_color = '#256029'   # verde oscuro
        msg_prefix = "Tu negocio tiene "
        amount_text = f"${amount:,.0f}"
        msg_suffix = " de superavit de efectivo para fondear las necesidades de capital"
    else:
        bg_color = '#f3b7ac'     # rojo suave
        text_color = '#4b2374'   # morado
        msg_prefix = "Tu negocio requiere "
        amount_text = f"${abs(amount):,.0f}"
        msg_suffix = " de financiamiento para fondear las necesidades de capital"
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 0.5))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')
    xOffset=0.01
    # Renderizar texto en partes
    ax.text(xOffset, 0.5, msg_prefix, ha='left', va='center',
            fontsize=10, color=text_color, transform=ax.transAxes)
    ax.text(xOffset+0.16, 0.5, amount_text, ha='left', va='center',
            fontsize=10, color=text_color, fontweight='bold', transform=ax.transAxes)
    ax.text(xOffset+0.28, 0.5, msg_suffix, ha='left', va='center',
            fontsize=10, color=text_color, transform=ax.transAxes)
    # Guardar
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format="svg", bbox_inches="tight")
    plt.close()
    return output_path
def calcular_resumen_financiero(df_raw):
    latest_period = df_raw.columns[-1]

    # === IZQUIERDA ===
    incremento_ingresos = 100
    margen_bruto = round(df_raw.at["Margen_Bruto_Perc", latest_period] * 100, 2)
    costo_ventas = round(incremento_ingresos - margen_bruto, 2)
    utilidad_operativa = round(df_raw.at["Utilidad_Operacional_Perc", latest_period] * 100, 2)
    gastos_admin = round(incremento_ingresos - utilidad_operativa, 2)
    ingresos = df_raw.at["Ingresos", latest_period]
    extraordinarios = (
        round(df_raw.at["Ingresos_o_Gastos_Extraordinarios", latest_period] / ingresos * 100, 2)
        if ingresos else 0)
    intereses = round(df_raw.at["Intereses_Pagados", latest_period] / ingresos * 100, 2)
    impuestos = round(df_raw.at["Impuestos_Pagados", latest_period] / ingresos * 100, 2)
    dividendos = round(df_raw.at["Distribuciones_Dividendos", latest_period] / ingresos * 100, 2)

    utilidad_retenida = round(utilidad_operativa - extraordinarios - intereses - impuestos - dividendos, 2)

    # === DERECHA ===
    cxc = round(df_raw.at["Cuentas_X_Cobrar_por_100Dlls", latest_period], 2)
    inventario = round(df_raw.at["Inventario_por_100Dlls", latest_period], 2)
    cxp = round(df_raw.at["Cuentas_X_Pagar_por_100Dlls", latest_period], 2)
    capital_trabajo = round(df_raw.at["Capital_de_Trabajo_por_100Dlls", latest_period], 2)

    deuda_capital = round(df_raw.at["Deuda_Neta_a_Capital_Social", latest_period], 2)
    capacidad_fondeo = round(utilidad_retenida * deuda_capital, 2)

    # === BOTTOM (shortfall)
    shortfall = round(capital_trabajo - utilidad_retenida - capacidad_fondeo, 2)

    return {
        "incremento_ingresos": incremento_ingresos, "costo_ventas": costo_ventas, "margen_bruto": margen_bruto, "gastos_admin": gastos_admin, "utilidad_operativa": utilidad_operativa, "extraordinarios": extraordinarios,
        "intereses": intereses, "impuestos": impuestos, "dividendos": dividendos, "utilidad_retenida": utilidad_retenida, "cxc": cxc, "inventario": inventario, "cxp": cxp,
        "capital_trabajo": capital_trabajo, "deuda_capital": deuda_capital, "capacidad_fondeo": capacidad_fondeo, "shortfall": shortfall,}
def create_sustainable_growth_graph(data_dict, output_path="plots/sustainable_growth.svg", wrap_width=33):
    """    Genera un gráfico tipo Sustainable Growth.
    - Formato 0: normal
    - Formato 1: texto gris y pequeño
    - Formato 2: línea completa en caja gris
    - wrap_width: número máximo de caracteres por línea para auto-wrap"""
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.axis('off')
    ax.set_xlim(.5, 1.4)
    padder=0.6
    import textwrap
    def draw_block(items, formats, x_text, x_symbol, x_value, align):
        for i, ((text, symbol, value), fmt) in enumerate(zip(items, formats)):
            y = 1.2 - i * 0.12
            wrapped_text = textwrap.fill(text, width=wrap_width)
            if fmt == 2:
                if symbol is not None and value is not None:
                    full_text = f"{text} {symbol}    $ {value:,.2f}"
                else:
                    full_text = text  # solo texto si no hay valores
                ax.text(x_text, y-.35, full_text, ha='left', va='center',
                        fontsize=17, fontweight='normal',
                        bbox=dict(boxstyle="square", facecolor="#dddddd", edgecolor="#dddddd",pad=padder),
                        color='#333333') 
                ax.text(x_symbol-.04, y-.35, "----------", ha='left', va='center',
                        fontsize=17, fontweight='normal',
                        bbox=dict(boxstyle="square", facecolor="#9f9b9b", edgecolor="#9f9b9b",pad=padder),
                        color='#9f9b9b')  
                ax.text(x_text, y-.35, full_text, ha='left', va='center',
                        fontsize=17, fontweight='normal')                              
            elif fmt == 1:
                if symbol is not None:
                    ax.text(x_symbol, 0.75-(0.7*y), symbol, ha='center', va='center', fontsize=18, color='#777777')
                if value is not None:
                    ax.text(x_value, 0.75-(0.7*y), f"$ {value:,.2f}", ha='right', va='center', fontsize=15, color='#777777')
                ax.text(x_text+.1, 0.75-(0.7*y), text, ha='left', va='center', fontsize=15, color='#777777')
            else:
                if value is not None:
                    facecolor = "#ffeb99" if align == 'left' else "#a9dce3"
                    text_color = "#b36b00" if align == 'left' else "#00506b"
                    ax.text(x_text, y, "------------------------------------------------------------------------\n------------------------------------------------------------------------", ha='left', va='center',
                            fontsize=15, fontweight='bold',
                            bbox=dict(boxstyle="square", facecolor=facecolor, edgecolor=facecolor, pad=padder),
                            color=facecolor)
                    ax.text(x_value, y, f"$ {value:,.2f}", ha='right', va='center',
                            fontsize=15, fontweight='bold',
                            bbox=dict(boxstyle="square", facecolor=text_color, edgecolor=facecolor, pad=padder),
                            color='white')
                    ax.text(x_text, y, wrapped_text, ha='left', va='center', fontsize=18, color='#333333',)
                if symbol is not None:
                    ax.text(x_symbol, y, symbol, ha='center', va='center', fontsize=16, color='#333333',fontweight='bold',)
                
    # Columnas izquierda y derecha
    draw_block(data_dict['left']['Variables'], data_dict['left']['format'], -.5, 0.2, 0.41, 'left')
    draw_block(data_dict['right']['Variables'], data_dict['right']['format'], 0.64, 1.3,1.5 , 'right')

    # Parte inferior
    if data_dict.get('bottom'):
        import textwrap
        label, symbol, amount = data_dict['bottom']
        ax.text(-00.1, 0, "----------------------------------------------------------------------------------\n----------------------------------------------------------------------------------", ha='left', va='center',
                            fontsize=16, fontweight='bold',
                            bbox=dict(boxstyle="square", facecolor= '#f3b7ac', edgecolor='#f3b7ac', pad=padder),
                            color= '#f3b7ac')
        ax.text(-0.10, 0.0, label, ha='left', va='center', fontsize=16, color="#620369")
        ax.text(0.78, 0, f"$ {abs(amount):,.2f}", ha='left', va='center',
                fontsize=17, fontweight='bold',
                bbox=dict(boxstyle="square", facecolor="#620369", edgecolor="#620369",pad=padder),
                color='white')
        ax.text(0.73, 0, symbol, ha='center', va='center', fontsize=16, color='#620369', bbox=dict(boxstyle="square", facecolor="#f3b7ac", edgecolor="#f3b7ac", pad=padder))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, format="svg", bbox_inches="tight")
    plt.close()
    print('Generating Sustainable Growth graph...')
    return output_path
def ReturnOnCapital_Plot(graph_data, df_transposed, output_dir="plots"):
    """    Generates a Return on Capital layout with stacked blocks for visual storytelling."""
    variables = graph_data["variables"]
    colors = graph_data["colors"]
    graph_name = graph_data["GraphName"]
    # Get latest period
    latest_period = df_transposed.columns[-1]
    values = [df_transposed.at[var, latest_period] if var in df_transposed.index else None for var in variables]
    # Setup plot
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 300)
    ax.axis('off')
    # Position config

    y1=110
    y2=250
    positions = {
        # Chapter 1: Operating Profit %
        0: (100, y2),  # Operating Profit
        1: (100, y1),  # Revenue (denominator)
        # Chapter 2: Asset Turnover
        2: (420, y2),  # Revenue
        3: (350, y1),  # Working Capital
        4: (500, y1),  # Other Capital
        # Chapter 3: Return on Capital %
        5: (700, y2),  # Operating Profit
        6: (700, y1),}  # Net Operating Assets
    # Block labels
    VariableNames = [k for var in variables for k, v in variable_directory.items() if v == var]
    VariableNames = [VariableNames[i] if i < len(VariableNames) else var
        for i, var in enumerate(variables)]
    # Draw all boxes
    for i, (x, y) in positions.items():
        val = values[i]
        label = VariableNames[i]
        label = "\n".join(textwrap.wrap(label, width=13))
        value_txt = f"${val:,.0f}" if pd.notna(val) else "N/A"
        ax.text(
            x, y, "-",
            fontsize=8, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle="square", facecolor=colors[i], edgecolor=colors[i], pad=4.8),
            color=colors[i])
        ax.text(
            x, y+5, f"{label}",
            fontsize=9, fontweight='bold',
            ha='center', va='center',
            color='white')
        ax.text(
            x, y-10, f"{value_txt}",
            fontsize=9, fontweight='normal',
            ha='center', va='top',
            color='white')
    # Draw symbols
    ax.text(225, 180, "×", fontsize=20, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(420, y1, "+", fontsize=20, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(620, 180, "=", fontsize=20, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(810, 180, "=", fontsize=20, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(100, y1-80, "Capítulo 1", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(350, y1-80, "Capítulo 1", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(500, y1-80, "Capítulo 3", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(100, y2+80, "Utilidad Operacional %", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(420, y2+80, "Rotación de Activos", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')
    ax.text(700, y2+80, "Retorno sobre Capital %", fontsize=9, ha='center', va='center', color='gray', fontweight='bold')

    # Draw division lines
    ax.hlines(180, 50, 150, colors='gray', linewidth=1.2)
    ax.hlines(180, 310, 540, colors='gray', linewidth=1.2)
    ax.hlines(180, 650, 750, colors='gray', linewidth=1.2)
    # Final return on capital %
    if pd.notna(values[5]) and pd.notna(values[6]) and values[6] != 0:
        roc = values[5] / values[6]*100
        roc_txt = f"{roc :.2f}%"
    else:
        roc_txt = "N/A"
    ax.text(900, 180, roc_txt,
        fontsize=18, fontweight='bold', ha='center', va='center', color= 'gray')
    ax.text(900, 160, "Retorno / Capital", fontsize=12, ha='center', va='top', color="gray")
    # Save
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{graph_name}.svg")
    plt.tight_layout()
    plt.savefig(path, format="svg", bbox_inches="tight")
    plt.close()
    global graphs
    if 'graphs' not in globals():
        graphs = {}
    graphs[graph_name] = path
    return {graph_name: path}
def plot_working_capital_timeline(df,period_labels, Store_name, output_dir="plots"):
    """    Plots a working capital timeline for two periods using WC cycle metrics.
    Parameters:
    - data_dict: dict like:
        {"Este": {"Inventory": 121, "Payables": 46, "Receivables": 80},
        "Last": {"Inventory": 110, "Payables": 44, "Receivables": 76}}
    - period_labels: tuple like ("This Period", "Last Period")    """
    # Setup figure
    fig, ax = plt.subplots(figsize=(7, 3))
    colors = ['#1f77b4', '#e377c2', '#ff7f0e', '#2ca02c']
    events = ["Recibo \n Inventario", "Pago a \nAcreedores", "Vendo \nInventario", "Recibo \nEfectivo"]
    # Extraer como diccionario limpio
    data_dict = {
        "Este": {
            "Inventory": round(df.iloc[-1]["Dias_Inventario"]),
            "Payables": round(df.iloc[-1]["Dias_Cuentas_X_Pagar"]),
            "Receivables": round(df.iloc[-1]["Dias_Cuentas_X_Cobrar"])},
        "Anterior": {
            "Inventory": round(df.iloc[-2]["Dias_Inventario"]),
            "Payables": round(df.iloc[-2]["Dias_Cuentas_X_Pagar"]),
            "Receivables": round(df.iloc[-2]["Dias_Cuentas_X_Cobrar"])},
        "Suma":{
            "Impacto en el Efectivo": round(df.iloc[-1]["Impacto_Efectivo"])}}
    # === Extract values
    def get_days(period_data):
        inv = 0
        pay = period_data["Payables"]
        sold = period_data["Inventory"]
        cash = sold + period_data["Receivables"]
        return [0, pay, sold, cash]
    y_start = 0.8
    spacing = 10
    # Plot timelines
    for i, label in enumerate(["Este", "Anterior"]):
        y = y_start - i * spacing
        days = get_days(data_dict[label])
        wc_days = days[-1] - days[1]-1
        label_text = f"{period_labels[i]}"        
        # Plot line
        ax.hlines(y, -1, 270, color='lightgray', linewidth=1)
        # Flecha hacia la derecha encima de la línea
        ax.annotate(
            '',                      # Sin texto
            xy=(280, y),             # Punto final de la flecha
            xytext=(240, y),          # Punto inicial de la flecha
            arrowprops=dict(
                arrowstyle='->',     # Flecha simple
                color='lightgray',
                lw=1,                # Grosor de la flecha
                shrinkA=0, shrinkB=0 # Sin espacio en los extremos
            )        )
        for j, day in enumerate(days):
            ax.vlines(day, y-.4, y+.4, color=colors[j], linewidth=1.5)
            wrapped_label = "\n".join(textwrap.wrap(events[j], width=12))
            ax.text(day, y+.6, f"Día {day}", ha='center', fontsize=6, color='gray')
            ax.text(day, y-1.3, wrapped_label, ha='center', fontsize=6, color='gray')
        # Add WC summary
        ax.text(340, y, f".", fontsize=16, fontweight='bold',
                ha='center', va='center', bbox=dict(boxstyle="square", facecolor="#007b8f", edgecolor= "#007b8f", pad=2.15), color= "#007b8f")
        ax.text(340, y, f"{wc_days}", fontsize=16, fontweight='bold',
                ha='center', va='bottom', color='white')
        ax.text(340, y-0.3, "Días de \n Capital de Trabajo", fontsize=6, fontweight='normal',
                ha='center', va='center', color="white", zorder = 4)
        ax.text(-40, y+1.35, label_text, ha='left', fontsize=8, fontweight='bold', color = 'gray') #Label del periodo
    # Compute impact
    impact = data_dict["Suma"]["Impacto en el Efectivo"]
    if impact > 0:
        ax.text(338, -3.8,  f" +{abs(impact):,.0f}", fontsize=12, color="#48983F", ha='center', va='center', fontweight='bold' )
    else :
        ax.text(338, -3.8, f"-{abs(impact):,.0f}", fontsize=12, color="#d62728", ha='center', va='center', fontweight='bold')
    
    ax.text(340, -4.6, "Impacto en \nel Efectivo", fontsize=6, ha='center', va='center', color='gray')
    # Flecha superior (apunta hacia abajo, desde arriba hacia el texto)
    ax.annotate(
        '',
        xy=(340, -2.2),         # Punta de la flecha (donde termina)
        xytext=(340, -3.2),     # Inicio (más arriba)
        arrowprops=dict(
            arrowstyle='->',
            color='lightgray',
            lw=1,
            shrinkA=0, shrinkB=0        )    )
    # Flecha inferior (apunta hacia arriba, desde abajo hacia el texto)
    ax.annotate(
        '',
        xy=(340, -6.2),         # Punta de la flecha (donde termina)
        xytext=(340, -5.2),     # Inicio (más abajo)
        arrowprops=dict(
            arrowstyle='->',
            color='lightgray',
            lw=1,
            shrinkA=0, shrinkB=0))
    ax.axis('off')  # O coméntalo para depurar
    ax.set_xlim(-50, 370)
    ax.set_ylim(-10, 1)
    # Save
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "Working_Capital_Timeline.svg")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return {Store_name: path}
# =============== Crear Tablas ===================#
# #== Generar Tablas
def generate_jinja_table(df, table_title, variables):
    """
    Generates a fully rendered HTML table using real values.
    """
    display_names = [k for v in variables for k, val in variable_directory.items() if val == v]
    Columns = df.columns.tolist()
    markdown_table = f'<h3 >{table_title}</h3>\n'
    markdown_table += '<hr />\n'
    markdown_table += '<table>\n  <thead>\n    <tr >\n'
    markdown_table += '    </tr>\n  </thead>\n  <tbody>\n'
    
    for row, display_label in zip(variables, display_names):
        markdown_table += f'    <tr>\n      <td style="width: 550px; text-align: left">{display_label}</td>\n'
        for col in Columns:
            try:
                val = df.at[row, col]
                val_fmt = (
                    val.strftime("%d-%m-%Y") if isinstance(val, (pd.Timestamp, datetime))
                    else f"{val:,.0f}" if pd.notna(val)
                    else "")
            except KeyError:
                val_fmt = ""
            markdown_table += f'      <td style="text-align: right;">{val_fmt}</td>\n'
        markdown_table += '    </tr>\n'

    markdown_table += '  </tbody>\n</table>\n'
    return markdown_table
def generate_bi_period_table(df_transposed, graph_data):
    """  Generate an HTML table comparing the last two periods and showing the movement.
    - df_transposed: DataFrame with period rows and variable columns
    - table_title: Title of the table
    - variables: list of internal variable names (keys of variable_directory)    """
    # --- Identify last two periods (sorted by date)
    recent_periods = df_transposed.index[-2:]  # [older, latest]
    p1, p2 = recent_periods
    variables = graph_data["variables"]
    diff_logic = graph_data["diff_logic"]
    table_title = graph_data["title"][0]
    # --- Header
    markdown_table = '<table style="width: 100%; border-collapse: collapse;">\n  <thead>\n    <tr>\n'
    markdown_table += f'      <th style="text-align: left;">{table_title}</th>\n'
    markdown_table += f'      <th style="text-align: right;">{p1}</th>\n'
    markdown_table += f'      <th style="text-align: right;">{p2}</th>\n'
    markdown_table += '      <th style="text-align: right;">Movimiento</th>\n'
    markdown_table += '    </tr>\n  </thead>\n  <tbody>\n'
    for var, logic in zip(variables, diff_logic):
        label = next((k for k, v in variable_directory.items() if v == var), var)
        try:
            v1 = df_transposed.loc[p1, var]
            v2 = df_transposed.loc[p2, var]
        except KeyError:
            v1 = v2 = movement = ""
        else:
            # Movement calculation
            if pd.notna(v1) and pd.notna(v2):
                movement = v2 - v1
                abs_movement = abs(movement)
            def format_val(val):
                if pd.isna(val):
                    return ""
                elif abs(val) >= 10_000:
                    return f"{val:,.0f}"
                elif abs(val) >= 1:
                    return f"{val:,.1f}"
                else:
                    return f"{val * 100:,.1f}%"


            if pd.notna(v1) and pd.notna(v2):
                movement = v2 - v1
                abs_movement = abs(movement)

                if abs_movement < 0.0009 and abs(v2) <1 :
                    movement_fmt = "-"
                    color = "gray"
                elif abs_movement < 0.009 and abs(v2) >1 :
                    movement_fmt = "-"
                    color = "gray"
                else:
                    sign = "+" if movement > 0 else "-"  # zero is handled above
                    if abs_movement < 1 and abs(v1) <= 1:
                        movement_fmt = f"{sign}{abs_movement * 100:,.1f}%"
                    elif abs_movement > 100_000_000:
                        movement_fmt = f"{sign}{abs_movement / 1_000_000:,.0f}M"
                    elif abs_movement < 10_000:
                        movement_fmt = f"{sign}{abs_movement:.1f}"
                    else:
                        movement_fmt = f"{sign}{abs_movement:,.0f}"

                    # Define dynamic threshold based on value magnitude
                    threshold = 0.0009 if abs(v2) < 1 else 0.009

                    # Apply inverse color logic if needed
                    if logic == 0:
                        color = (
                            "green" if movement > threshold else
                            "red" if movement < -threshold else
                            "gray")
                    else:
                        color = (
                            "green" if movement < -threshold else
                            "red" if movement > threshold else
                            "gray"    )
                movement_html = f'<span style="color: {color}; font-weight: normal;">{movement_fmt}</span>'
            else:
                movement_html = ""

            v1_fmt = format_val(v1)
            v2_fmt = format_val(v2)
        # Row
        markdown_table += f'    <tr>\n'
        markdown_table += f'      <td style="text-align: left; width: 350px;">{label}</td>\n'
        markdown_table += f'      <td style="text-align: right;">{v1_fmt}</td>\n'
        markdown_table += f'      <td style="text-align: right;">{v2_fmt}</td>\n'
        markdown_table += f'      <td style="text-align: right;">{movement_html}</td>\n'
        markdown_table += f'    </tr>\n'
    markdown_table += '  </tbody>\n</table>\n'
    return markdown_table
def generate_single_var_table(df_transposed, table_title, variable_dict):
    """    Generate a 3-column summary table with current period and movement from previous.
    Parameters:
    - df_transposed: DataFrame (periods as rows, variables as columns)
    - table_title: str, section title
    - variable_dict: dict with:
        - "variables": list of internal variable names
        - "diff_logic": list (0 = direct, 1 = inverse for movement color)
    Returns:    - HTML string of the table    """
    periods = df_transposed.index[-2:]
    prev, curr = periods
    variables = variable_dict["variables"]
    diff_logic = variable_dict["diff_logic"]

    markdown_table = '<table style="width: 100%; border-collapse: collapse;">\n'
    markdown_table += '  <thead>\n    <tr>\n'
    markdown_table += '      <th style="text-align: left;"> </th>\n'
    markdown_table += '      <th style="text-align: right;">Periodo Actual</th>\n'
    markdown_table += '      <th style="text-align: right;">Movimiento</th>\n'
    markdown_table += '    </tr>\n  </thead>\n  <tbody>\n'
    for var, logic in zip(variables, diff_logic):
        label = next((k for k, v in variable_directory.items() if v == var), var)
        try:
            val_prev = df_transposed.loc[prev, var]
            val_curr = df_transposed.loc[curr, var]
        except KeyError:
            val_curr_fmt = ""
            movement_html = ""
        else:
            # Value formatting
            if abs(val_curr) < 1 and abs(val_curr) >0 :
                val_curr_fmt = f"{val_curr * 100:,.1f}%"
            elif abs(val_curr) > 100_000_000:
                val_curr_fmt = f"{val_curr / 1_000_000:,.0f}M"
            elif abs(val_curr) < 1000:
                val_curr_fmt = f"{val_curr:.1f}"
            elif abs(val_curr) < 0.009:
                val_curr_fmt = "-"
            else:
                val_curr_fmt = f"{val_curr:,.0f}"
            # Movement formatting
            if pd.notna(val_prev) and pd.notna(val_curr):
                diff = val_curr - val_prev
                abs_diff = abs(diff)
                sign = "+" if diff > 0 else "-" if diff < 0 else "-"

                threshold_large = 0.009
                threshold_small = 0.0009

                # Default color
                color = "gray"

                if pd.notna(diff) and pd.notna(val_curr):
                    if logic == 0:
                        if abs(val_curr) > 1:
                            if diff > threshold_large:
                                color = "green"
                            elif diff < -threshold_large:
                                color = "red"
                        else:
                            if diff > threshold_small:
                                color = "green"
                            elif diff < -threshold_small:
                                color = "red"
                    else:
                        if abs(val_curr) > 1:
                            if diff < -threshold_large:
                                color = "green"
                            elif diff > threshold_large:
                                color = "red"
                        else:
                            if diff < -threshold_small:
                                color = "green"
                            elif diff > threshold_small:
                                color = "red"
                # Format movement
                if abs_diff < 0.009 and val_curr >1:
                    movement_fmt = "-"
                elif abs_diff < 0.0009 and val_curr <1:
                    movement_fmt = "-"
                elif abs_diff < 1 and abs(val_curr) < 1 and abs(val_curr) > 0:
                    movement_fmt = f"{sign}{abs_diff * 100:,.1f}%"
                elif abs_diff > 100_000_000:
                    movement_fmt = f"{sign}{abs_diff / 1_000_000:,.0f}M"
                elif abs_diff < 1000:
                    movement_fmt = f"{sign}{abs_diff:.1f}"
                else:
                    movement_fmt = f"{sign}{abs_diff:,.0f}"

                movement_html = f'<span style="color:{color}; font-weight:normal;">{movement_fmt}</span>'

            else:
                movement_html = ""
        markdown_table += f'    <tr>\n'
        markdown_table += f'      <td style="text-align: left; font-weight: bold;">{label}</td>\n'
        markdown_table += f'      <td style="text-align: right;">{val_curr_fmt}</td>\n'
        markdown_table += f'      <td style="text-align: right;">{movement_html}</td>\n'
        markdown_table += f'    </tr>\n'
    markdown_table += '  </tbody>\n</table>\n'
    return markdown_table
def generate_Summary_table(df, table_title, variables):
    """
    Generates a 1-row summary HTML table with:
    - Variable name
    - Current value (latest period)
    - Movement from previous period
    """
    latest_col, prev_col = df.columns[-1], df.columns[-2]
    display_names = [k for v in variables for k, val in variable_directory.items() if val == v]
    html = '<table style="width:100%;">\n<tr>\n'
    for i, var in enumerate(variables):
        current_val = df.at[var,latest_col]
        prev_val = df.at[var, prev_col]
        diff = current_val - prev_val
        change_text = (f"arriba por {abs(diff):,.0f}" if diff > 0   else "-" if diff == 0 else f"abajo por {abs(diff):,.0f}")
        display_label = display_names[i] if i < len(display_names) else var.replace("_", " ")
        html += f'''
        <td style="padding: 12px;">
            <div style="font-size: 12px;font-weight: bold ; color: #284a5f; text-align: center;">{display_label}</div>
            <br>
            <div style="font-size: 16px; font-weight: bold;text-align: center">{current_val:,.0f}</div>
            <br>
            <div style="font-size: 11px; color: gray;text-align: center">{change_text}</div>
        </td>
        '''
    html += "\n</tr>\n</table>\n"
    return html
def generate_power_of_one_blocks(df, label_map, title="Tu Poder del Uno"):
    """    Genera 3 bloques de tabla HTML con formato Power of One:
    1. Posición Actual
    2. Impactos del Poder del Uno
    3. Posición Ajustada
    Parameters:
    - df: Power_of_ONE_df (con columnas 'Movimiento', 'Flujo de efectivo neto', 'Utilidad Operacional')
    - label_map: dict de {variable: etiqueta}
    - title: título opcional para el bloque medio
    Returns:    - str: HTML string listo para usar con Jinja2"""
    def fmt(val, digits=0):
        if pd.isna(val): return ""
        if isinstance(val, (float, int)): return f"{val:,.{digits}f}"
        return str(val)
    html = ""
    # -------------------- Tabla 1: Posición Actual --------------------
    html += '<table style="width: 100%;">'
    html += "<thead><tr><th></th><th></th><th style='text-align: right;'>Flujo de Efectivo Neto</th><th style='text-align: right;'>Utilidad Operacional</th></tr></thead><tbody>"
    row = "Posicion_Actual"
    html += f"<tr><td style='text-align: left;'>{label_map.get(row, row)}</td><td></td>"
    html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Flujo de efectivo neto'])}</td>"
    html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Utilidad Operacional'])}</td></tr>"
    html += "</tbody></table><br>"
    # -------------------- Tabla 2: Movimiento --------------------
    html += '<table style="width: 100%; border-collapse: collapse;">'
    html += f"<thead><tr><th style='text-align: left;'>{title}</th><th style='text-align: center;'>Movimiento</th><th style='text-align: right;white-space: normal!important'>Impacto en<br>Flujo de Efectivo Neto</th><th style='text-align: right;white-space:normal'>Impacto en<br>Utilidad Operacional</th></tr></thead><tbody>"
    for row in df.index:
        if pd.notna(df.at[row, "Movimiento"]) or row == "Impacto_Poder_UNO":
            label = label_map.get(row, row)
            move = df.at[row, "Movimiento"]
            move_fmt = f"{move:.0%}" if abs(move) < 1 else f"{int(move)} días" if pd.notna(move) else ""
            html += f"<tr><td style='text-align: left;'>{label}</td><td style='text-align: center; color: gray;'>{move_fmt}</td>"
            html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Flujo de efectivo neto'])}</td>"
            html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Utilidad Operacional'])}</td></tr>"
    html += "</tbody></table><br>"
    # -------------------- Tabla 3: Posición Ajustada --------------------
    html += '<table style="width: 100%;">'
    html += "<thead><tr><th></th><th></th><th style='text-align: right;'>Flujo de Efectivo Neto</th><th style='text-align: right;'>Utilidad Operacional</th></tr></thead><tbody>"
    row = "Posicion_Ajustada"
    html += f"<tr><td style='text-align: left;'>{label_map.get(row, row)}</td><td></td>"
    html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Flujo de efectivo neto'])}</td>"
    html += f"<td style='text-align: right;'>{fmt(df.at[row, 'Utilidad Operacional'])}</td></tr>"
    html += "</tbody></table>"
    return html
def generate_cashflow_chapter_table_from_df(df, chapters_dict, current_period, title=""):
    """ Crea tabla HTML estilo "Cash Flow Chapter Table" usando variables del DataFrame.
    Parameters:
    - df: DataFrame (transpuesto, con fechas como índice y variables como columnas).
    - chapters_dict: dict como {chapter: [var1, var2]} donde cada capítulo suma esas variables.
    - current_period: str → período actual (última fecha en df).
    - title: str opcional para el título.
    Returns:    - str (HTML table)"""
    def fmt(val):
        if val == 0: return "0"
        return f"{abs(val):,.0f}" if pd.notna(val) else ""
    total_pos, total_neg = 0, 0
    html = f"<h4>{title}</h4>" if title else ""
    html += ""
    html += '<table style="width: 100%; border-collapse: collapse;"><thead><tr><th style="text-align: left;">&nbsp;</th><th style="text-align: left;">&nbsp;</th><th style="text-align: right;">+ Flujo de Efectivo</th><th style="text-align: right;">- Flujo de Efectivo</th></tr></thead><tbody>'
    for chapter, variables in chapters_dict.items():
        value = sum(df.at[current_period, var] for var in variables if var in df.columns)
        label = [k for v in variables for k, val in variable_directory.items() if val == v]
        label = label[0] if label else variables[0]  # fallback si no hay mapeo
        pos = fmt(value) if value >= 0 else ""
        neg = fmt(value) if value < 0 else ""
        if value > 0: total_pos += value
        if value < 0: total_neg += abs(value)
        html += f"""
        <tr>
          <td style="font-weight: bold;text-align: left; color: #284a5f; width:700ppx;">{chapter}</td>
          <td style="font-weight: normal;text-align: left;">{label}</td>
          <td >{pos}</td>
          <td >{neg}</td>
        </tr>        """
    html += f"""
        <tr>
          <td colspan="2" style="font-weight: bold;text-align: center; color: #284a5f">Total</td>
          <td style="font-weight: bold; color: #284a5f;width:500ppx;">{fmt(total_pos)}</td>
          <td style="font-weight: bold; color: #284a5f;width:500ppx;">{fmt(total_neg)}</td>
        </tr>
    </tbody></table>    """
    return html
def generate_financial_statements_table_from_df(df, section_dict, title=""):
    """
    Generates a financial statement table from a DataFrame.

    Parameters:
    - df: DataFrame (index = variables, columns = periods)
    - section_dict: {'title': str, 'variables': [...], 'format': [...]}
    - title: Optional global title for the block
    Returns:
    - str: HTML table
    """
    def fmt(val):
        if pd.isna(val): return "N/A"
        if isinstance(val, (int, float)):
            if abs(val) < 1 and abs(val) > 0:
                return f"{val * 100:,.1f}%"
            elif abs(val) > 100_000_000:
                return f"{val / 1_000_000:,.0f}M"
            elif abs(val) < 1000:
                return f"{val:.1f}"
            else:
                return f"{val:,.0f}"
        return str(val)

    html = f"<h4>{title}</h4>" if title else ""
    html += '<table style="width: 100%; border-collapse: collapse; font-size: 10px;">'

    section_title = section_dict.get("title", "")
    variables = section_dict.get("variables", [])
    formats = section_dict.get("format", [0] * len(variables))
    periods = df.columns.tolist()

    # 👇 Column header row
    html += f"<tr><th style='text-align:left;'>{section_title}</th>"
    for p in periods:
        html += f"<th style='text-align:right;'>{p}</th>"
    html += "</tr></thead><tbody>"

    # Data rows
    for i, var in enumerate(variables):
        row_format = formats[i] if i < len(formats) else 0
        label = next((k for k, v in variable_directory.items() if v == var), var)
        label_style = "color: #284a5f; font-weight: bold; border-bottom: 1px solid #ccc;" if row_format == 1 else "color: #000;"
        val_style = "color: #284a5f; font-weight: bold; border-bottom: 1px solid #ccc;" if row_format == 1 else "color: #000;"
        html += f"<tr><td style='text-align:left; {label_style}'>{label}</td>"
        for p in periods:
            val = df.at[var, p]
            html += f"<td style='text-align:right; {val_style}'>{fmt(val)}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html
def generate_valuation_table(df, table_dict):
    html = ""

    for section, details in table_dict.items():
        variables = list(details.values())[0]  # List of row labels (index names in df)
        bold_flags = details.get("bold", [0] * len(variables))
        title = list(details.keys())[0] if list(details.keys())[0] != "" else ""

        # Start table
        html += "<table style='width: 100%; border-collapse: collapse; margin-bottom: 10px;'>"

        # Add title if present
        if title:
            html += f"<thead><tr><th style='text-align: left;'>{title}</th>"
        else:
            html += "<thead><tr><th></th>"

        html += "<th style='text-align: right;'> </th><th style='text-align: right;'>-1</th> <th style='text-align: right;'>+1</th>"
        html += "</tr></thead><tbody>"

        # Add data rows
        for i, label in enumerate(variables):
            # Apply bold styling conditionally
            if bold_flags and i < len(bold_flags) and bold_flags[i] == 1:
                style = "font-weight: bold; color: #284a5f; padding-top: 6px; padding-bottom: 13px;"
            else:
                style = ""

            html += f"<tr><td style='text-align: left; {style}'>{label}</td>"

            for col in df.columns:
                val = df.at[label, col] if label in df.index and col in df.columns else ""
                val_fmt =(f"{val:,.0f}" if pd.notna(val) and abs(val) >= 100 
                            else f"{val:,.2f}" if pd.notna(val) 
                            else "")
                html += f"<td style='text-align: right; {style}'>{val_fmt}</td>"

            html += "</tr>"

        html += "</tbody></table>\n"

    return html
def generate_cash_vs_profit_table(df, structure_dict, title=""):
    current_period = df.columns[-1]
    html = '<table style="width: 100%; border-collapse: collapse;">'
    html += (
        '<thead><tr>'
        '<th style="text-align: left;">Utilidad</th>'
        '<th style="text-align: right;">&nbsp;</th>'
        '<th style="text-align: left;">Flujo de Efectivo</th>'
        '<th style="text-align: right;">&nbsp;</th>'
        '<th style="text-align: right;">Variación</th>'
        '</tr></thead><tbody>')

    def fmt(val):
        if pd.isna(val):
            return ""
        elif round(abs(val), 0) == 0:
            return "-"
        else:
            return f"{val:,.0f}"

    for key, valmap in structure_dict.items():
        profit_vars = valmap["Profit"]
        cash_vars = valmap["cash"]
        inverse_logic = valmap.get("Inverse_logic", ["0"] * max(len(profit_vars), len(cash_vars)))
        max_len = max(len(profit_vars), len(cash_vars))

        for i in range(max_len):
            p_var = profit_vars[i] if i < len(profit_vars) else None
            c_var = cash_vars[i] if i < len(cash_vars) else None
            logic = int(inverse_logic[i]) if i < len(inverse_logic) else 0

            # Labels
            label1 = next((k for k, v in variable_directory.items() if v == p_var), "") if p_var else ""
            label2 = next((k for k, v in variable_directory.items() if v == c_var), "") if c_var else ""

            # Values
            profit_val = df.at[p_var, current_period] if p_var in df.index else None
            cash_val = df.at[c_var, current_period] if c_var in df.index else None
            profit_fmt = fmt(profit_val)
            cash_fmt = fmt(cash_val)

            # Difference
            # Difference with inverse logic controlling subtraction direction
            if pd.notna(profit_val) and pd.notna(cash_val):
                diff = (cash_val - profit_val) if logic == 0 else (profit_val - cash_val)
            else:
                diff = None


            # Format difference and assign color
            if diff is None:
                diff_fmt = ""
            elif abs(diff) < 0.009:
                diff_fmt = '<span style="color:gray; font-weight:normal;">-</span>'
            else:
                sign = "+" if diff > 0 else "-"
                color = ( "green" if (diff > 0) else "red" if (diff < 0) else "gray" )
                diff_fmt = f'<span style="color:{color}; font-weight:normal;">{sign}{abs(diff):,.0f}</span>'

            # Blue & bold final row of section
            is_final = (i == max_len - 1)
            font_style = "color: #284a5f; font-weight:bold;" if is_final else "font-weight:normal;"

            html += f"""
                <tr>
                    <td style="text-align: left; max-width: 160px; {font_style}">{label1}</td>
                    <td style="text-align: right; {font_style}">{profit_fmt}</td>
                    <td style="text-align: left; max-width: 160px; {font_style}">{label2}</td>
                    <td style="text-align: right; {font_style}">{cash_fmt}</td>
                    <td style="text-align: right; max-width: 50px; {font_style}">{diff_fmt}</td>
                </tr>
            """

    html += "</tbody></table>"
    return html
def generate_valuation_parameters_table(df_Valuacion, EBITDA_Promedio_Ponderada, Ajuste, EBITDA_Ajustada, current_period=None, title=""):
    if current_period is None:
        current_period = df_Valuacion.columns[-1]

    def fmt(val):
        if pd.isna(val) or val == "":
            return ""
        return f"{val:,.0f}" if isinstance(val, (int, float)) else str(val)

    rows = [
        ("Valor Objetivo del Negocio", "Valor Objetivo del Negocio", None),
        ("Multiplo de Rentabilidad", None, "4 +/- 1"),  # Custom text
        ("EBITDA Promedio Ponderada", None, EBITDA_Promedio_Ponderada),  # from variable
        ("Ajuste", None, Ajuste),  # static value
        ("EBITDA Ajustada", None, EBITDA_Ajustada),  # from variable   
         ]

    html = f"<h4>{title}</h4>"
    html += '<table style="width: 60%; border-collapse: collapse;">'
    html += '<thead><tr><th style="text-align: left;">Parametros</th><th style="text-align: right;"> </th></tr></thead><tbody>'

    for label, variable, override in rows:
        if override is not None:
            value = fmt(override)
        elif variable and variable in df_Valuacion.index:
            value = fmt(df_Valuacion.at[variable, current_period])
        else:
            value = ""
        html += f"<tr><td style='text-align: left;'>{label}</td><td style='text-align: right;'>{value}</td></tr>"

    html += "</tbody></table>"
    return html
#----------------------------------------------


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
    st.subheader("📤 Upload Your Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            # Step 1: Read the specific sheet
            df_raw = pd.read_excel(uploaded_file, sheet_name="Inputs", skiprows=7, header=None)
            # Drop first and third columns
            df_raw.drop([df_raw.columns[0], df_raw.columns[2]], axis=1, inplace=True)
            # Extract company name
            Company_Name = df_raw.iloc[0, 1]
            Usuario= df_raw.iloc[1, 1]

            st.success(f"✅ Informacion de {Company_Name} cargada exitosamente por {Usuario}")
            # Layout with two buttons in a row
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Generar Reporte"):
                    st.session_state["show_sections"] = True

            with col2:
                if st.button("Calculadora Poder del 1"):
                    st.session_state["go_to_poder_uno"] = True

            # If Calculadora Poder del 1 button is clicked
            if st.session_state.get("go_to_poder_uno"):
                st.markdown("## 🧮 Calculadora - Poder del Uno")
                st.write("Aquí podrías mostrar la herramienta de cálculo para Poder del Uno.")
                # 👉 Llama aquí a tu función específica, por ejemplo:
                # show_poder_del_uno_calculator(df_raw)

            # If Generar Reporte was clicked
            if st.session_state.get("show_sections"):
                all_sections = [
                    "Resumen",
                    "Capítulo 1 - Rentabilidad",
                    "Capítulo 2 - Capital de Trabajo",
                    "Capítulo 3 - Otro Capital",
                    "Capítulo 4 - Financiamiento",
                    "Poder del Uno",
                    "Valuación",
                    "Crecimiento Sostenible",
                    "Resultados & Proyecciones"]
                select_all = st.checkbox("Todas", value=True)
                selected_sections = st.multiselect(
                    "Selecciona las secciones del reporte:",
                    all_sections,
                    default=all_sections if select_all else [])

                st.session_state["selected_sections"] = selected_sections
                if st.button("Confirmar Secciones y Generar"):
                    if selected_sections:
                        st.success("✅ Generando el reporte con las secciones seleccionadas...")
                        st.write("Secciones incluidas:", selected_sections)
                        if df_raw is None or df_raw.empty:
                            st.error("❌ El archivo no fue leído correctamente.")
                            return
                        generate_report(df_raw, selected_sections)
                    else:
                        st.warning("⚠️ Debes seleccionar al menos una sección para generar el reporte.")
            st.dataframe(df_raw)
        except Exception as e:
            st.error(f"❌ Error leyendo el archivo: {e}")

    # Logout button
    if st.button("Logout"):
        for key in ("logged_in", "username", "role", "df_raw"):
            st.session_state[key] = None
        st.rerun()

def df_raw_SETUP(df_raw):
    ValorObjetivo = df_raw.iloc[2, 1]
    Ajuste= df_raw.iloc[3, 1]
    # Drop first 5 rows
    df_raw.drop(index=[0, 1, 2, 3 ,4], inplace=True)
    # Assign first row as column headers safely
    df_raw.columns = df_raw.iloc[0].values
    df_raw.drop(index=df_raw.index[0], inplace=True)
    # 🏗️ Set "Final del Periodo" as Index
    df_raw.set_index("Final del Periodo", inplace=True)
    # 🔎 Identify period columns dynamically
    potential_periods = df_raw.columns
    # 🛠 Convert period columns to datetime & filter valid ones
    period_columns = [col for col in potential_periods if pd.to_datetime([col], errors='coerce').strftime('%d-%m-%Y').notna().all()]
    # 🛠 Remove rows where all period values are empty
    df_raw.dropna(subset=potential_periods, how="all", inplace=True)
    # 🔄 Convert period values to numeric format
    df_raw[period_columns] = df_raw[period_columns].apply(pd.to_numeric, errors="coerce")
    # ✅ Rename index safely based on `variable_directory`
    df_raw.rename(index=variable_directory, inplace=True)
    calculations = [
        ("Periodo", lambda df: pd.Series(df.columns, index=df.columns)),
        # 🏆 Profit & Loss Calculations
        ("Utilidad_Neta", lambda df: df.loc["Utilidad_Retenida", period_columns] + df.loc["Distribuciones_Dividendos", period_columns]),
        ("Utilidad_Neta_Antes_de_Impuestos", lambda df: df.loc["Utilidad_Neta", period_columns] + df.loc["Impuestos_Pagados", period_columns]),
        ("Utilidad_Operacional", lambda df: df.loc["Utilidad_Neta_Antes_de_Impuestos", period_columns] + df.loc["Intereses_Pagados", period_columns] + df.loc["Ingresos_o_Gastos_Extraordinarios", period_columns]),
        ("Gastos_Admin", lambda df: df.loc["Margen_Bruto", period_columns] - df.loc["Utilidad_Operacional", period_columns]),
        ("Costo_de_Ventas", lambda df: df.loc["Ingresos", period_columns] - df.loc["Margen_Bruto", period_columns]),
        # 📄 Balance sheet concepts
        ("Otros_Activos_Corrientes", lambda df: df.loc["Activos_Corrientes", period_columns] - df.loc["Inventario", period_columns] - df.loc["Cuentas_X_Cobrar", period_columns] - df.loc["Efectivo", period_columns] ),
        ("Activos_No_Corrientes", lambda df: df.loc["Total_Activos", period_columns] - df.loc["Activos_Corrientes", period_columns]) ,
        ("Otros_Activos_No_Corrientes", lambda df: df.loc["Activos_No_Corrientes", period_columns] - df.loc["Activos_Fijos", period_columns]),
        ("Otros_Pasivos_CP", lambda df: df.loc["Pasivos_CP", period_columns] - df.loc["Cuentas_X_Pagar", period_columns] - df.loc["Prestamos_Bancarios_CP", period_columns]),
        ("Otros_Activos", lambda df: df.loc["Otros_Activos_No_Corrientes", period_columns] + df.loc["Otros_Activos_Corrientes", period_columns]),
        ("Pasivos_LP", lambda df: df.loc["Total_Pasivos", period_columns] - df.loc["Pasivos_CP", period_columns]),
        ("Otros_Pasivos_LP", lambda df: df.loc["Pasivos_LP", period_columns] - df.loc["Prestamos_Bancarios_LP", period_columns]),
        ("Otros_Pasivos", lambda df: df.loc["Otros_Pasivos_CP", period_columns] + df.loc["Otros_Pasivos_LP", period_columns]),
        ("Patrimonio", lambda df: df.loc["Total_Activos", period_columns] - df.loc["Total_Pasivos", period_columns]),
        # 📊 Profitability Ratios
        ("Margen_Bruto_Perc", lambda df: (df.loc["Margen_Bruto", period_columns] / df.loc["Ingresos", period_columns]) ),
        ("Gastos_Admin_Perc", lambda df: (df.loc["Gastos_Admin", period_columns] / df.loc["Ingresos", period_columns]) ),
        ("Utilidad_Operacional_Perc", lambda df: (df.loc["Utilidad_Operacional", period_columns] / df.loc["Ingresos", period_columns]) ),
        ("Utilidad_Neta_Perc", lambda df: (df.loc["Utilidad_Neta", period_columns] / df.loc["Ingresos", period_columns]) ),
        # 💰 EBITDA & Interest Cover
        ("EBITDA", lambda df: df.loc["Utilidad_Operacional", period_columns] + df.loc["Depreciacion_Y_Amortizacion", period_columns]),
        ("Cobertura_de_Intereses", lambda df: df.loc["Utilidad_Operacional", period_columns] / df.loc["Intereses_Pagados", period_columns]),
        # 🔄 Working Capital Metrics
        ("Dias_Cuentas_X_Cobrar", lambda df: (df.loc["Cuentas_X_Cobrar", period_columns] / df.loc["Ingresos", period_columns]) * 365),
        ("Dias_Inventario", lambda df: (df.loc["Inventario", period_columns] / df.loc["Costo_de_Ventas", period_columns]) * 365),
        ("Dias_Cuentas_X_Pagar", lambda df: (df.loc["Cuentas_X_Pagar", period_columns] / df.loc["Costo_de_Ventas", period_columns]) * 365),
        ("Dias_Capital_de_Trabajo", lambda df: df.loc["Dias_Cuentas_X_Cobrar", period_columns] + df.loc["Dias_Inventario", period_columns] - df.loc["Dias_Cuentas_X_Pagar", period_columns]),
        ("Capital_de_Trabajo", lambda df: df.loc["Cuentas_X_Cobrar", period_columns] + df.loc["Inventario", period_columns] - df.loc["Cuentas_X_Pagar", period_columns]),
        ("Cuentas_X_Pagar_por_100Dlls", lambda df: (df.loc["Cuentas_X_Pagar", period_columns] / df.loc["Ingresos", period_columns]) *100),
        ("Cuentas_X_Cobrar_por_100Dlls", lambda df: (df.loc["Cuentas_X_Cobrar", period_columns] / df.loc["Ingresos", period_columns]) *100),
        ("Inventario_por_100Dlls", lambda df: (df.loc["Inventario", period_columns] / df.loc["Ingresos", period_columns]) *100),
        ("Capital_de_Trabajo_por_100Dlls", lambda df: (df.loc["Capital_de_Trabajo", period_columns] / df.loc["Ingresos", period_columns]) *100),
        ("Margen_Bruto_por_100Dlls", lambda df: (df.loc["Margen_Bruto", period_columns] / df.loc["Ingresos", period_columns])*100 ),
        ("Rotacion_Capital_de_Trabajo", lambda df: df.loc["Ingresos", period_columns] / df.loc["Capital_de_Trabajo", period_columns]),
        # 📊 Asset & Capital Efficiency Metrics
        ("Margen_de_Flujo_de_Efectivo", lambda df: ((df.loc["Margen_Bruto", period_columns] / df.loc["Ingresos", period_columns])
                                            - ((df.loc["Cuentas_X_Cobrar", period_columns] + df.loc["Inventario", period_columns] 
                                            - df.loc["Cuentas_X_Pagar", period_columns]) / df.loc["Ingresos", period_columns])) ),
        ("Razon_Corriente", lambda df: df.loc["Activos_Corrientes", period_columns] / df.loc["Pasivos_CP", period_columns]),
        ("Otro_Capital", lambda df: df.loc["Activos_Fijos", period_columns] + df.loc["Otros_Activos_Corrientes", period_columns] 
                                    + df.loc["Otros_Activos_No_Corrientes", period_columns] - df.loc["Otros_Pasivos_CP", period_columns] 
                                    - df.loc["Otros_Pasivos_LP", period_columns]),
        ("Otro_Capital_Perc", lambda df: df.loc["Otro_Capital", period_columns] / df.loc["Ingresos", period_columns]),
        ("Retorno_Sobre_Otro_Capital_Perc", lambda df: df.loc["Utilidad_Operacional", period_columns] / df.loc["Otro_Capital", period_columns]),
        ("Rotacion_Otro_Capital", lambda df: df.loc["Ingresos", period_columns] / df.loc["Otro_Capital", period_columns]),
        # 🏗️ Net Operating Assets & Performance Metrics
        ("Activos_Operativos_Netos", lambda df: df.loc["Prestamos_Bancarios_CP", period_columns] + df.loc["Prestamos_Bancarios_LP", period_columns] 
                                        - df.loc["Efectivo", period_columns] + df.loc["Patrimonio", period_columns]),
        ("Activos_Operativos_Netos_Perc", lambda df: df.loc["Activos_Operativos_Netos", period_columns] / df.loc["Ingresos", period_columns]),
        ("Rotacion_Activos", lambda df: df.loc["Ingresos", period_columns] / df.loc["Activos_Operativos_Netos", period_columns]),
        ("Retorno_Sobre_Capital_Perc", lambda df: df.loc["Utilidad_Operacional", period_columns] / df.loc["Activos_Operativos_Netos", period_columns]),
        ("Retorno_Sobre_Total_de_Activos_Perc", lambda df: df.loc["Utilidad_Operacional", period_columns] / df.loc["Total_Activos", period_columns]),
        ("Retorno_Sobre_Patrimonio_Perc", lambda df: df.loc["Utilidad_Neta", period_columns] / df.loc["Patrimonio", period_columns]),
        # 🏗️ Debt & Cash Flow Metrics
        ("Deuda_Neta", lambda df: df.loc["Prestamos_Bancarios_CP", period_columns] 
                            + df.loc["Prestamos_Bancarios_LP", period_columns] 
                            - df.loc["Efectivo", period_columns]),
        ("Deuda_Neta_a_Capital_Social", lambda df: df.loc["Deuda_Neta", period_columns] / df.loc["Patrimonio", period_columns]),
        ("Deuda_a_Capital", lambda df: (df.loc["Prestamos_Bancarios_CP", period_columns]
                                        + df.loc["Prestamos_Bancarios_LP", period_columns]) 
                                        / (df.loc["Prestamos_Bancarios_CP", period_columns] 
                                        + df.loc["Prestamos_Bancarios_LP", period_columns] 
                                        + df.loc["Patrimonio", period_columns])),
        ("Repago_de_Deuda", lambda df: df.loc["Deuda_Neta", period_columns] / df.loc["EBITDA", period_columns]),
        ("Deuda_Total", lambda df: df.loc["Prestamos_Bancarios_CP", period_columns] + df.loc["Prestamos_Bancarios_LP", period_columns]),
        ("Flujo_Efectivo_Marginal", lambda df: ((df.loc["Margen_Bruto", period_columns] / df.loc["Ingresos", period_columns])-((df.loc["Cuentas_X_Cobrar", period_columns]+df.loc["Inventario", period_columns]-df.loc["Cuentas_X_Pagar", period_columns])/df.loc["Ingresos", period_columns]))),
        ("Financiamiento_Total", lambda df: df.loc["Efectivo", period_columns] + df.loc["Deuda_Total", period_columns]+ df.loc["Patrimonio", period_columns]),] 

    # 🛠️ Apply calculations dynamically
    for var, formula in calculations:
        try:
            df_raw.loc[var, period_columns] = formula(df_raw)
        except ZeroDivisionError:
            print(f"⚠️ ZeroDivisionError in calculation for: {var}")
            df_raw.loc[var, period_columns] = np.nan  # Or 0 or any fallback
        except KeyError as e:
            print(f"⚠️ KeyError in calculation for {var}: missing {e}")
            df_raw.loc[var, period_columns] = np.nan
        except Exception as e:
            print(f"⚠️ Error in calculation for {var}: {e}")
            df_raw.loc[var, period_columns] = np.nan
    for i in range(1, len(period_columns)):  # Start from second period (index 1)
        prev_period = period_columns[i - 1]
        curr_period = period_columns[i]
        try:
            # Growth Percentages
            df_raw.loc["Crecimiento_Ingresos_Perc", curr_period] = (
                (df_raw.loc["Ingresos", curr_period] - df_raw.loc["Ingresos", prev_period]) /
                df_raw.loc["Ingresos", prev_period] if df_raw.loc["Ingresos", prev_period] != 0 else np.nan)
            df_raw.loc["Crecimiento_Costo_de_Ventas_Perc", curr_period] = (
                (df_raw.loc["Costo_de_Ventas", curr_period] - df_raw.loc["Costo_de_Ventas", prev_period]) /
                df_raw.loc["Costo_de_Ventas", prev_period] if df_raw.loc["Costo_de_Ventas", prev_period] != 0 else np.nan)
            df_raw.loc["Crecimiento_Gastos_Admin_Perc", curr_period] = (
                (df_raw.loc["Gastos_Admin", curr_period] - df_raw.loc["Gastos_Admin", prev_period]) /
                df_raw.loc["Gastos_Admin", prev_period] if df_raw.loc["Gastos_Admin", prev_period] != 0 else np.nan)
            # Operating Cash Flow
            change_wcap = (
                (df_raw.loc["Cuentas_X_Cobrar", curr_period] + df_raw.loc["Inventario", curr_period] - df_raw.loc["Cuentas_X_Pagar", curr_period]) -
                (df_raw.loc["Cuentas_X_Cobrar", prev_period] + df_raw.loc["Inventario", prev_period] - df_raw.loc["Cuentas_X_Pagar", prev_period]))
            df_raw.loc["Flujo_Efectivo_Operacional", curr_period] = df_raw.loc["EBITDA", curr_period] - change_wcap
            # Operating Cash Profit
            df_raw.loc["Beneficio_Efectivo_Operacional", curr_period] = (
                df_raw.loc["Margen_Bruto", curr_period] -
                (df_raw.loc["Gastos_Admin", curr_period] - df_raw.loc["Depreciacion_Y_Amortizacion", curr_period])      )
            # Net Cash Flow
            df_raw.loc["Flujo_Efectivo_Neto", curr_period] = (
                (df_raw.loc["Ingresos", curr_period] - (df_raw.loc["Cuentas_X_Cobrar", curr_period] - df_raw.loc["Cuentas_X_Cobrar", prev_period])) -
                (df_raw.loc["Costo_de_Ventas", curr_period] +
                (df_raw.loc["Inventario", curr_period] - df_raw.loc["Inventario", prev_period]) -
                (df_raw.loc["Cuentas_X_Pagar", curr_period] - df_raw.loc["Cuentas_X_Pagar", prev_period])) -
                df_raw.loc["Gastos_Admin", curr_period] -
                df_raw.loc["Depreciacion_Y_Amortizacion", curr_period] -
                df_raw.loc["Intereses_Pagados", curr_period] -
                df_raw.loc["Impuestos_Pagados", curr_period] -
                df_raw.loc["Distribuciones_Dividendos", curr_period] -
                (df_raw.loc["Activos_Fijos", curr_period] - df_raw.loc["Activos_Fijos", prev_period] - df_raw.loc["Depreciacion_Y_Amortizacion", curr_period]))

            # Capital de Trabajo and Effective Impact
            df_raw.loc["delta_cxc", curr_period] = df_raw.loc["Dias_Cuentas_X_Cobrar", curr_period] - df_raw.loc["Dias_Cuentas_X_Cobrar", prev_period]
            df_raw.loc["delta_cxp", curr_period] = df_raw.loc["Dias_Cuentas_X_Pagar", curr_period] - df_raw.loc["Dias_Cuentas_X_Pagar", prev_period]
            df_raw.loc["delta_inv", curr_period] = df_raw.loc["Dias_Inventario", curr_period] - df_raw.loc["Dias_Inventario", prev_period]
            df_raw.loc["Impacto_Efectivo", curr_period] = (
                -((df_raw.loc["delta_cxc", curr_period] / 365) * df_raw.loc["Ingresos", curr_period]) +
                ((df_raw.loc["delta_cxp", curr_period] / 365) * df_raw.loc["Costo_de_Ventas", curr_period]) -
                ((df_raw.loc["delta_inv", curr_period] / 365) * df_raw.loc["Costo_de_Ventas", curr_period]))
            # Additional Components
            df_raw.loc["Inversion_Capital_de_Trabajo", curr_period] = df_raw.loc["Capital_de_Trabajo", prev_period] - df_raw.loc["Capital_de_Trabajo", curr_period]
            df_raw.loc["Inversion_Otro_Capital", curr_period] = df_raw.loc["Otro_Capital", prev_period] - df_raw.loc["Otro_Capital", curr_period]
            df_raw.loc["Efectivo_de_Clientes", curr_period] = df_raw.loc["Ingresos", curr_period] - (df_raw.loc["Cuentas_X_Cobrar", curr_period] - df_raw.loc["Cuentas_X_Cobrar", prev_period])
            df_raw.loc["Efectivo_a_Proveedores", curr_period] = df_raw.loc["Costo_de_Ventas", curr_period] + (df_raw.loc["Inventario", curr_period] - df_raw.loc["Inventario", prev_period]) - (df_raw.loc["Cuentas_X_Pagar", curr_period] - df_raw.loc["Cuentas_X_Pagar", prev_period])
            df_raw.loc["Beneficio_Efectivo_Bruto", curr_period] = df_raw.loc["Efectivo_de_Clientes", curr_period] - df_raw.loc["Efectivo_a_Proveedores", curr_period]
            df_raw.loc["Gastos_Admin_LessDA", curr_period] = df_raw.loc["Gastos_Admin", curr_period] - df_raw.loc["Depreciacion_Y_Amortizacion", curr_period]
            df_raw.loc["Flujo_Efectivo_Operativo", curr_period] = df_raw.loc["Beneficio_Efectivo_Bruto", curr_period] - df_raw.loc["Gastos_Admin_LessDA", curr_period]
            df_raw.loc["Beneficio_Operativo_Efectivo", curr_period] = df_raw.loc["Margen_Bruto", curr_period] - df_raw.loc["Gastos_Admin_LessDA", curr_period]
            df_raw.loc["Inversion_Activos_Fijos", curr_period] = df_raw.loc["Activos_Fijos", curr_period] - df_raw.loc["Activos_Fijos", prev_period] + df_raw.loc["Depreciacion_Y_Amortizacion", curr_period]
            df_raw.loc["Inversion_Otros_Activos_Netos", curr_period] = -(
                (df_raw.loc["Otros_Activos_Corrientes", curr_period] - df_raw.loc["Otros_Activos_Corrientes", prev_period]) +
                (df_raw.loc["Otros_Activos_No_Corrientes", curr_period] - df_raw.loc["Otros_Activos_No_Corrientes", prev_period]) -
                (df_raw.loc["Otros_Pasivos_CP", curr_period] - df_raw.loc["Otros_Pasivos_CP", prev_period]) -
                (df_raw.loc["Otros_Pasivos_LP", curr_period] - df_raw.loc["Otros_Pasivos_LP", prev_period])        )
            df_raw.loc["Capital_Inyectado", curr_period] = -(
                (df_raw.loc["Patrimonio", curr_period] - df_raw.loc["Patrimonio", prev_period]) -
                df_raw.loc["Utilidad_Retenida", curr_period]        )
            df_raw.loc["Flujo_Efe_Fin", curr_period] = df_raw.loc["Flujo_Efectivo_Operativo", curr_period] - (
                df_raw.loc["Intereses_Pagados", curr_period] +
                df_raw.loc["Impuestos_Pagados", curr_period] +
                df_raw.loc["Ingresos_o_Gastos_Extraordinarios", curr_period] +
                df_raw.loc["Distribuciones_Dividendos", curr_period] +
                df_raw.loc["Inversion_Activos_Fijos", curr_period] +
                df_raw.loc["Inversion_Otros_Activos_Netos", curr_period] +
                df_raw.loc["Capital_Inyectado", curr_period]        )

        except Exception as e:
            print(f"❌ Error processing period {curr_period}: {e}")

    # 📜 Sort results properly
    df_raw.sort_index(inplace=True)
    df_transposed = df_raw.T
    df_transposed.index = pd.to_datetime(df_transposed.index, errors="coerce").strftime('%d-%m-%Y')
    df_raw.columns = pd.to_datetime(df_raw.columns, errors="coerce").strftime('%d-%m-%Y')
    # ✅ Display cleaned and calculated data
    # Get last two periods (assumes index is datetime-like or sorted strings)
    df_trans_latest_two = df_transposed.tail(2)
    # Ensure column names are properly formatted for Jinja2
    df_raw.columns = df_raw.columns.astype(str)
    df_raw.index = df_raw.index.astype(str)  # Convert index to strings

# ========= SECCIONES =============
### RESUMEN
def Resumen (df_raw):
    #-----------------------------------------------------------
    table_configs = {                                            #========= RESUMEN
        "Periodo de Reportes": ["Periodo", "Duracion"],
        "Estado de Resultados": ["Ingresos", "Margen_Bruto", "Utilidad_Operacional", "Utilidad_Neta"],
        "Otra Información": ["Depreciacion_Y_Amortizacion", "Intereses_Pagados", "Ingresos_o_Gastos_Extraordinarios","Distribuciones_Dividendos"],
        "Activos": ["Total_Activos", "Efectivo", "Cuentas_X_Cobrar", "Inventario", "Activos_Corrientes","Activos_No_Corrientes"],
        "Pasivos": ["Total_Pasivos", "Cuentas_X_Pagar", "Pasivos_CP"],
        "Financiamiento": ["Prestamos_Bancarios_CP", "Prestamos_Bancarios_LP"]}
    for table_name, variables in table_configs.items():
        tables[table_name] = generate_jinja_table(df_raw, table_name, variables)
    Single_Var_Table_Data =  {
        "Rendimiento": {
            "variables":["Ingresos", "Margen_Bruto_Perc", "Utilidad_Operacional_Perc", "Utilidad_Neta_Perc"],
            "diff_logic":[0,0,0,0]},
        "Balance": {
            "variables":["Dias_Cuentas_X_Cobrar", "Dias_Inventario", "Dias_Cuentas_X_Pagar", "Dias_Capital_de_Trabajo"],
            "diff_logic":[1,1,0,1]},
        "FlujodeEfectivo": {
            "variables": ["Efectivo", "Prestamos_Bancarios_CP", "Prestamos_Bancarios_LP", "Flujo_Efectivo_Neto"],
            "diff_logic":[0,1,1,0]}}
    for section, varinfo in Single_Var_Table_Data.items():
        tables[section] = generate_single_var_table(df_transposed, section, varinfo)
    Stacked_graphs_data = {
        "CashFlow_Story": {
            "GraphName": "CashFlow_Story",  # This will generate a file named "total_debt.png"
            "variables": ["Prestamos_Bancarios_LP","Prestamos_Bancarios_CP"],
            "colors": ["#2c5b9c", "#44acd3"],}}
    for graph_name, graph_data in Stacked_graphs_data.items():
        print(f"Generando Gráficas Apliladas: {graph_name}...")
        graph_paths = Stacked_graph(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
### CHAP 1
def Cap1 (df_raw):
    Bi_Per_Table_Data1 = {                                   #========== CAP 1
        "Chap1": {
            "title":["Capítulo 1 - Rentabilidad"],
            "variables":["Ingresos","Crecimiento_Ingresos_Perc", "Margen_Bruto","Margen_Bruto_Perc","Gastos_Admin","Gastos_Admin_Perc", "Utilidad_Operacional", "Utilidad_Operacional_Perc", "EBITDA", "Utilidad_Neta", "Utilidad_Neta_Perc","Ganancias_Retenidas","Cobertura_de_Intereses"],
            "diff_logic":[0,0,0,0,1,1,0,0,0,0,0,0,0]}}
    for chapter, variable_list in Bi_Per_Table_Data1.items():
        tables[chapter] = generate_bi_period_table(df_transposed, variable_list)
    Grouped_Bar_data1 = {
        "Profitability_Trends": { #1
            "GraphName": 'Profitability_Trends',
            "variables": ["Margen_Bruto_Perc", "Utilidad_Operacional_Perc", "Utilidad_Neta_Perc"],  # 3 variables
            "colors": ["#84cbcc", "#44acd3", "#3b84b4", "#2c5b9c"]}}  # Color mapping  # Equation structure
    for graph_name, graph_data in Grouped_Bar_data1.items():
        print(f"Generando Gráficas Apliladas: {graph_name}...")
        graph_paths = Grouped_Bar_Graph(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
    Eq_Bar_graphs_directory = {
        "Profit_Story": {
            "GraphName": 'Profit_Story',
            "variables": ["Ingresos", "Costo_de_Ventas", "Margen_Bruto", "Gastos_Admin", "Utilidad_Operacional"],  # 5 variables
            "colors": ["#E9989E", "#EA638C", "#C4448C", "#8F3192", "#7F2E90"],  # Color mapping
            "symbols": ["-", "=", "-", "="],},  # Equation structure
        "BalanceSheet_Story": {
            "GraphName": 'BalanceSheet_Story',
            "variables": ['Patrimonio', 'Activos_Corrientes', 'Activos_Fijos', 'Pasivos_CP','Pasivos_LP'],  # 3 variables
            "colors": ['#fad36c','#f2b154','#ec8f43','#e66c33','#d35028'],  # Color mapping
            "symbols": ["=", "+","-","-"],},
        "Funding_Story": {
            "GraphName": 'Funding_Story',
            "variables": ['Patrimonio', 'Deuda_Neta', 'Capital_de_Trabajo', 'Otro_Capital'],  # 3 variables
            "colors": ['#EC9BA3', '#E54771', '#9B3E97', '#6E2C91'],  # Color mapping
            "symbols": ["+", "=","+"],}}  # Equation structure
    for graph_name, graph_data in Eq_Bar_graphs_directory.items():
        print(f"Generating graph: {graph_name}...")
        graph_paths = Eq_Bar_graphs(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
    Period_Grouped_Bar_data1 = {
        "RevenueVScogs": { #1
            "GraphName": 'RevenueVScogs',
            "variables": ["Crecimiento_Ingresos_Perc", "Crecimiento_Costo_de_Ventas_Perc"],  # 2 variables
            "colors": ["#e8e265", "#f7b750"]},
        "RevenueVSoverhead": { #1
            "GraphName": 'RevenueVSoverhead',
            "variables": ['Crecimiento_Ingresos_Perc', 'Crecimiento_Gastos_Admin_Perc'],  # 2 variables
            "colors": ['#fad36c',"#e69333"]}}
    for graph_name, graph_data in Period_Grouped_Bar_data1.items():
        print(f"Generating graph: {graph_name}...")
        graph_paths = Period_Grouped_bars(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
    Summary_Tables1 = { 
        "Ch1_Profitability": ["Ingresos", "Margen_Bruto", "Utilidad_Operacional", "Utilidad_Neta"]}
    for section, varlist in Summary_Tables1.items(): 
        tables[section] = generate_Summary_table(df_raw, section, varlist)
### CAP 2
def Cap2 (df_raw):
    #== Blocks Plots
    # Get the latest column (i.e., the latest period)
    latest_period = df_raw.columns[-1]              #============== CAP 2
    inventory_days = df_raw.at["Inventario_por_100Dlls", latest_period]
    receivables_days =df_raw.at["Cuentas_X_Cobrar_por_100Dlls", latest_period]
    payables_days = df_raw.at["Cuentas_X_Pagar_por_100Dlls", latest_period]
    wc_days = df_raw.at["Capital_de_Trabajo_por_100Dlls", latest_period]
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    ax.axis('off')
    ax.text(0.0, 0.90, "Capital de Trabajo", fontsize=8, fontweight='bold', color="#3b4a58", ha='left')
    ax.text(1.0, 0.90, f"{wc_days:.0f}", fontsize=10, fontweight='bold', color="#3b4a58", ha='right')
    ax.text(0.0, 0.70, "Inventario", fontsize=9, color="gray", ha='left')
    ax.text(1.0, 0.70, f"{inventory_days:.0f}", fontsize=9, color="gray", ha='right')
    ax.text(0.0, 0.60, "Ctas. por Cobrar", fontsize=9, color="gray", ha='left')
    ax.text(1.0, 0.60, f"{receivables_days:.0f}", fontsize=9, color="gray", ha='right')
    ax.text(0.0, 0.50, "Ctas. por Pagar", fontsize=9, color="gray", ha='left')
    ax.text(1.0, 0.50, f"{payables_days:.0f}", fontsize=9, color="gray", ha='right')
    ax.text(0.0, 0.20,
            f"Por cada $100 adicionales de Ingreso,\nInviertes ${wc_days:.0f} en Capital de Trabajo",
            fontsize=8, color="gray", ha='left')
    os.makedirs("plots", exist_ok=True)
    camino = os.path.join("plots", f"ResumenCapTrabajo.svg")
    plt.tight_layout()
    plt.savefig(camino, format="svg", bbox_inches="tight")
    plt.close()
    graphs.update({"ResumenCapTrabajo": camino})  # Merge all generated paths into `graphs`
    Blocks_Plot_data = {
        "Working_Capital_Blocks": {
            "GraphName": 'Working_Capital_Blocks',
            "variables": ['Inventario', 'Cuentas_X_Cobrar', 'Cuentas_X_Pagar', 'Ingresos'],
            "colors": ["#f5989d", "#ea4c89", "#9b2fae", "#4c0070"]}}
    for name, graph_data in Blocks_Plot_data.items():
        print(f"Generating: {name}")
        blockspath = Blocks_Plot(graph_data, df_transposed)
        graphs.update(blockspath)  # Merge all generated paths into `graphs`

    Bi_Per_Table_Data2 = { #Cols:Last_Period, Current_Period , 'Movement' 
        "Chap2": {
            "title":["Capítulo 2 - Capital de Trabajo"],
            "variables":["Dias_Cuentas_X_Cobrar", "Dias_Inventario", "Dias_Cuentas_X_Pagar", "Dias_Capital_de_Trabajo","Capital_de_Trabajo", "Capital_de_Trabajo_por_100Dlls","Rotacion_Capital_de_Trabajo","Flujo_Efectivo_Marginal","Razon_Corriente"],
            "diff_logic":[1,1,0,1,1,1,0,0,0]}}
    for chapter, variable_list in Bi_Per_Table_Data2.items():
        tables[chapter] = generate_bi_period_table(df_transposed, variable_list)

    Grouped_Bar_data2 = {
        "Working_Capital_Trends": {
            "GraphName": 'Working_Capital_Trends',
            "variables": ['Dias_Cuentas_X_Pagar', 'Dias_Inventario', 'Dias_Cuentas_X_Cobrar'],  # 3 variables
            "colors": ["#84cbcc", "#44acd3", "#3b84b4", "#2c5b9c"]},  # Color mapping
        "Investment_WC_per100DLLS": {
            "GraphName": "Investment_WC_per100DLLS",  # This will generate a file named "total_debt.png"
            "variables": ["Cuentas_X_Pagar_por_100Dlls","Inventario_por_100Dlls","Cuentas_X_Cobrar_por_100Dlls"],
            "colors": ["#84cbcc", "#44acd3", "#3b84b4", "#2c5b9c"]}}
    for graph_name, graph_data in Grouped_Bar_data2.items():
        print(f"Generando Gráficas Apliladas: {graph_name}...")
        graph_paths = Grouped_Bar_Graph(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
    Period_Grouped_Bar_data2 = {
        "GrossMarginVSwc":  { #2
            "GraphName": 'GrossMarginVSwc',
            "variables": ['Margen_Bruto_por_100Dlls', 'Capital_de_Trabajo_por_100Dlls'],  # 2 variables
            "colors": ["#d7a42e","#e18216"]}}  # Color mapping
    for graph_name, graph_data in Period_Grouped_Bar_data2.items():
        print(f"Generating graph: {graph_name}...")
        graph_paths = Period_Grouped_bars(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`

    Summary_Tables2 = { 
        "Ch2_WC": ["Cuentas_X_Cobrar", "Inventario", "Cuentas_X_Pagar", "Capital_de_Trabajo"]}
    for section, varlist in Summary_Tables2.items(): 
        tables[section] = generate_Summary_table(df_raw, section, varlist)
    #== WC Time Line
    nombre_linea= 'working_capital_timeline'
    Line_Path = plot_working_capital_timeline(df_trans_latest_two, ("Este Periodo", "Periodo Anterior"),nombre_linea)
    print(f"Generating Timeline: {nombre_linea}...")
    graphs.update(Line_Path)  # Merge all generated paths into `graphs`
### CAP 3
def Cap3 (df_raw):
    Bi_Per_Table_Data3 = {                                       #========== CAP 3
        "Chap3": {
            "title":["Capítulo 3 - Otro Capital"],
            "variables":["Otro_Capital", "Otro_Capital_Perc", "Retorno_Sobre_Otro_Capital", "Activos_Operativos_Netos", "Activos_Operativos_Netos_Perc", "Rotacion_Activos",  'Retorno_Sobre_Capital_Perc','Retorno_Sobre_Total_de_Activos_Perc','Retorno_Sobre_Patrimonio_Perc'],
            "diff_logic":[1,1,0,0,1,0,0,0,0]}}
    for chapter, variable_list in Bi_Per_Table_Data3.items():
        tables[chapter] = generate_bi_period_table(df_transposed, variable_list)
    Grouped_Bar_data3 = {
        "Return_on_Capital_Trends": {
            "GraphName": 'Return_on_Capital_Trends',
            "variables": ['Utilidad_Operacional_Perc', 'Rotacion_Activos', 'Retorno_Sobre_Capital_Perc'],  # 3 variables
            "colors": ["#84cbcc", "#44acd3", "#3b84b4", "#2c5b9c"]}} # Color mapping
    for graph_name, graph_data in Grouped_Bar_data3.items():
        print(f"Generando Gráficas Apliladas: {graph_name}...")
        graph_paths = Grouped_Bar_Graph(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`
    #== 2 Blocks Plots
    ReturnOnCapital_data = {
        "Return_on_Capital": {
            "GraphName": "Return_on_Capital",
            "variables": [
                "Utilidad_Operacional",  # 0
                "Ingresos",              # 1
                "Ingresos",              # 2
                "Capital_de_Trabajo",    # 3
                "Otro_Capital",          # 4
                "Utilidad_Operacional",  # 5
                "Activos_Operativos_Netos"  # 6
            ],
            "colors": [
                "#f5989d", "#f5989d", "#f5989d",
                "#ea4c89", "#9b2fae", "#4c0070", "#6c3483"
            ]
        }
    }
    for name, graph_data in ReturnOnCapital_data.items():
        print(f"Generating: {name}")
        pathdict = ReturnOnCapital_Plot(graph_data, df_raw)
        graphs.update(pathdict)
    Summary_Tables3 = { 
        "Ch3_OtherCap": ["Activos_Fijos", "Otros_Activos", "Otros_Pasivos", "Otro_Capital"]}
    for section, varlist in Summary_Tables3.items(): 
        tables[section] = generate_Summary_table(df_raw, section, varlist)
### CAP 4
def Cap4 (df_raw):
    latest_period = df_raw.columns[-1]
    Cash_vs_Profit_Dict = {                                     #===========CAP 4
        "1": {
            "Profit":["Ingresos","Costo_de_Ventas","Margen_Bruto"],
            "cash": ["Efectivo_de_Clientes","Efectivo_a_Proveedores","Beneficio_Efectivo_Bruto"],
            "Inverse_logic": ['0','1','0']},
        "2": {
            "Profit":["Gastos_Admin_LessDA","Beneficio_Operativo_Efectivo"],
            "cash": ["Gastos_Admin_LessDA","Flujo_Efectivo_Operativo"]},
        "3": {
            "Profit":[None],
            "cash": ["Salidas_Otro_Efectivo"]},
        "4": {
            "Profit":["Intereses_Pagados","Impuestos_Pagados","Ingresos_o_Gastos_Extraordinarios","Distribuciones_Dividendos","Depreciacion_Y_Amortizacion",None,None,"Utilidad_Retenida"],
            "cash": ["Intereses_Pagados","Impuestos_Pagados","Ingresos_o_Gastos_Extraordinarios","Distribuciones_Dividendos","Inversion_Activos_Fijos","Inversion_Otros_Activos_Netos","Capital_Inyectado","Flujo_Efe_Fin"]}}
    tables["Cash_vs_Profit"] = generate_cash_vs_profit_table(df_raw, Cash_vs_Profit_Dict, title="Utilidad vs Flujo de Efectivo")
    Cashflow_Chapters = {
        "Capítulo 1": ["Utilidad_Retenida"],
        "Capítulo 2": ["Inversion_Capital_de_Trabajo"],
        "Capítulo 3": ["Inversion_Otro_Capital",]}
    tables["Cashflow_Summary"] = generate_cashflow_chapter_table_from_df(
        df_transposed,
        Cashflow_Chapters,
        current_period=latest_period,
        title="")
    Bi_Per_Table_Data4 = {  
        "Chap4": {
            "title":["Capítulo 4 - Financiamiento"],
            "variables":["Flujo_Efectivo_Marginal", "Flujo_Efectivo_Operacional", "Beneficio_Efectivo_Operacional", "Flujo_Efectivo_Neto", "Deuda_Neta", "Deuda_Neta_a_Capital_Social", "Deuda_a_Capital","Cobertura_de_Intereses","Repago_de_Deuda"],
            "diff_logic":[0,0,0,1,1,1,1,0,1]}}
    for chapter, variable_list in Bi_Per_Table_Data4.items():
        tables[chapter] = generate_bi_period_table(df_transposed, variable_list)
    Grouped_Bar_data4= {
        "Funding_Trends": {
            "GraphName": "Funding_Trends",  # This will generate a file named "total_debt.png"
            "variables": ["Efectivo","Deuda_Total","Patrimonio"],
            "colors": ["#84cbcc", "#44acd3", "#3b84b4", "#2c5b9c"]}}  # Color mapping
    for graph_name, graph_data in Grouped_Bar_data4.items():
        print(f"Generando Gráficas Apliladas: {graph_name}...")
        graph_paths = Grouped_Bar_Graph(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`

    Period_Grouped_Bar_data4 = {
        "OperatingCash": { #4
            "GraphName": 'OperatingCash',
            "variables": ['Beneficio_Efectivo_Operacional', 'Flujo_Efectivo_Operacional'],  # 2 variables
            "colors": ["#ecb944","#e0642a"]}}
    for graph_name, graph_data in Period_Grouped_Bar_data4.items():
        print(f"Generating graph: {graph_name}...")
        graph_paths = Period_Grouped_bars(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`

    Summary_Tables4 = { 
        "Ch4_Fund": ["Efectivo", "Deuda_Total", "Patrimonio", "Financiamiento_Total"],}
    for section, varlist in Summary_Tables4.items(): 
        tables[section] = generate_Summary_table(df_raw, section, varlist)
### VALUACION y Poder del UNO
def Valuacion_y_Poder_del_Uno(df_raw):
    #============= Poder del UNO==========#
    df_power = build_power_of_one(df_raw)
    df_power_transposed = df_power.T
    weights = [4, 3, 2, 1]
    available_columns = df_raw.columns[-len(weights):]  # Toma solo las últimas N columnas disponibles
    used_weights = weights[-len(available_columns):]    # Ajusta los pesos si hay menos columnas
    ebitda_values = df_raw.loc["EBITDA", available_columns]
    EBITDA_Promedio_Ponderada = (ebitda_values * used_weights).sum() / sum(used_weights)
    EBITDA_Ajustada = (EBITDA_Promedio_Ponderada+Ajuste)
    #============== Valuacion ============#
    df_Valuacion= build_Valuation(df_raw, df_power)
    label_map = { # Diccionario de etiquetas Poder UNO
        "Posicion_Actual": "Tu Posicion Actual",
        "Incre_Precio_Perc": "Incremento en el Precio  %",
        "Incre_Volumen_Perc": "Incremento en el Volumen %",
        "Reduc_Costo_de_Ventas_Perc": "Reduccion del Costo de Ventas %",
        "Reduc_Gastos_Admin_Perc": "Reduccion de Gastos Administrativos %",
        "Reduc_Cuentas_X_Cobrar_Dias": "Reduccion en Dias de Cuentas X Cobrar",
        "Reduc_Inventario_Dias": "Reduccion en Dias de Inventario",
        "Incre_Cuentas_X_Pagar_Dias": "Reduccion en Dias de Cuentas X Pagar",
        "Impacto_Poder_UNO": "Impacto de Tu Poder del Uno",
        "Posicion_Ajustada": "Tu Posicion Ajustada"}
    tables["Poder_UNO"] = generate_power_of_one_blocks(df_power, label_map)
    Period_Grouped_Bar_dataUNO = {
        "ImpactoUNO": {
            "df": df_power_transposed,
            "periodos":['Flujo de efectivo neto','Utilidad Operacional'],
            "GraphName": 'ImpactoUNO',
            "variables": ['Posicion_Actual', 'Posicion_Ajustada'],  # 2 variables
            "colors": ["#ecb944","#e0642a"]}} 
    for graph_name, graph_data in Period_Grouped_Bar_dataUNO.items():
        print(f"Generating graph: {graph_name}...")
        graph_paths = Period_Grouped_bars(graph_data)  # Generate graphs
        graphs.update(graph_paths)  # Merge all generated paths into `graphs`

    weights = [4, 3, 2, 1]
    available_columns = df_raw.columns[-len(weights):]  # Toma solo las últimas N columnas disponibles
    used_weights = weights[-len(available_columns):]    # Ajusta los pesos si hay menos columnas
    ebitda_values = df_raw.loc["EBITDA", available_columns]
    EBITDA_Promedio_Ponderada = (ebitda_values * used_weights).sum() / sum(used_weights)
    EBITDA_Ajustada = (EBITDA_Promedio_Ponderada+Ajuste)
    Valuation_table = {                                         #============VALUACION
        "1Val":{"Tu Valor del Negocio Actual": ["Múltiplo de Ganancias", "Valor Bruto del Negocio", "Deuda Total", "Valor Actual de tu Negocio"],
                "bold":[0,0,0,1]},
        "2Val":{"Tu Valor con el Poder del Uno": ["Múltiplo de Ganancias", "Incremento de Precio %","Incremento de Volumen %","Reducción del Costo de Ventas %","Reducción de Gastos Admin %","Impacto de la Ganancia en la Valoración","Reducción en Días de Cuentas por Cobrar","Reducción en Días de Inventario","Aumento en Días de Cuentas por Pagar","Impacto del Efectivo en la Valoración","Impacto de tu Poder del Uno", "Valor del Negocio Mejorado"],
                "bold":[0,0,0,0,0,1,0,0,0,1,1,1]},
        "3Val":{"Tu Indicador de Valor Mejorado":["Múltiplo de Ganancias","Valor Actual de tu Negocio", "Impacto de tu Poder del Uno", "Valor del Negocio Mejorado"],
                "bold":[0,0,0,1]}, 
        "4Val":{"Tu Valor Objetivo del Negocio":["Múltiplo de Ganancias", "Valor Objetivo del Negocio", "Valor Actual de tu Negocio", "Brecha de Valor Actual"],
                "bold":[0,0,0,1]}, 
        "5Val":{"Tu Valor del Negocio Mejorado":["Múltiplo de Ganancias", "Valor Objetivo del Negocio", "Valor del Negocio Mejorado","Brecha de Valor Mejorada"],
                "bold":[0,0,0,1]}}
    for section, details in Valuation_table.items():
        tables[section] = generate_valuation_table(df_Valuacion, {section: details})
    graphs.update(plot_business_valuation_stacked(df_Valuacion))
    tables["Valuation_Params"] = generate_valuation_parameters_table(
        df_Valuacion,
        EBITDA_Promedio_Ponderada=EBITDA_Promedio_Ponderada,
        Ajuste=Ajuste,
        EBITDA_Ajustada=EBITDA_Ajustada)
### Crecimiento Sostenible
def Crecimiento_Sostenible(df_raw):
    latest_period = df_raw.columns[-1]    
    #== Shortfall legend
    legend_path = create_shortfall_legend(round(df_raw.at["Flujo_Efe_Fin", latest_period],0))  # genera la versión en rojo
    graphs["shortfall_legend"] = legend_path
    #== Shorfall Sheet
    resultados = calcular_resumen_financiero(df_raw)
    sustainable_data = {
        "left": {
            'Variables':[
                ("Si incrementas tus Ingresos por", "+", resultados["incremento_ingresos"]),
                ("Menos Costo de ventas de", "-", resultados["costo_ventas"]),
                ("Tu margen Bruto será", "=", resultados["margen_bruto"]),
                ("Menos Costos Administrativos", "-", resultados["gastos_admin"]),
                ("Tu Utilidad Operativa será", "=", resultados["utilidad_operativa"]),
                ("Menos Ingresos/Gastos Extraordinarios", "-", resultados["extraordinarios"]),
                ("Menos Intereses Pagados", "-", resultados["intereses"]),
                ("Menos Impuestos", "-", resultados["impuestos"]),
                ("Menos Dividendos", "-", resultados["dividendos"]),
                ("Tu Utilidad Retenida será", "=", resultados["utilidad_retenida"])],
            'format':[0,0,0,0,0,1,1,1,1,0]},
        "right": {
            'Variables':[
                ("Tu inversión en Cuentas por Cobrar será", "+", resultados["cxc"]),
                ("Tu inversión en Inventario será", "+", resultados["inventario"]),
                ("Provisto por Cuentas por Pagar", "-", resultados["cxp"]),
                ("Requerirás Capital de Trabajo de", "=", resultados["capital_trabajo"]),
                (f"Tu razon Deuda/Capital es {resultados['deuda_capital']}", None, None),
                (f"Puedes pedir \${resultados['deuda_capital']} por cada \$1 de Utilidad Retenida", None, None),
                ("Tu capacidad de fondearte será", "=", resultados["capacidad_fondeo"])],
            'format':[0,0,0,0,1,1,2]},
        "bottom": ("Tendrás una necesidad de financiamiento de", "=", resultados["shortfall"])}
    sustainable_growth_path = create_sustainable_growth_graph(sustainable_data, output_path="plots/sustainable_growth.svg")
    graphs["sustainable_growth"] = sustainable_growth_path
    #---------------------------------------------------------#
### PROYECCIONES
def Proyecciones (df_raw):
    Fin_Statements = {                                         #============PROYECCIONES
        'Results_Statement': { 'title': 'Estado de Resultados',
            'variables': [
                "Ingresos", "Costo_de_Ventas", "Margen_Bruto", "Gastos_Admin",
                "Utilidad_Operacional", "Intereses_Pagados", "Ingresos_o_Gastos_Extraordinarios",
                "Utilidad_Neta_Antes_de_Impuestos", "Impuestos_Pagados",
                "Utilidad_Neta", "Distribuciones_Dividendos", "Utilidad_Retenida"],
            'format': [0,0,1,0,1,0,0,1,0,1,0,1]},
        'Balance_Sheet': { 'title': 'Balance General',
            'variables': [
                "Efectivo", "Cuentas_X_Cobrar", "Inventario", "Otros_Activos_Corrientes",
                "Activos_Corrientes", "Activos_Fijos", "Otros_Activos_No_Corrientes",
                "Activos_No_Corrientes", "Total_Activos", "Cuentas_X_Pagar",
                "Prestamos_Bancarios_CP", "Otros_Pasivos_CP", "Pasivos_CP",
                "Prestamos_Bancarios_LP", "Otros_Pasivos_LP", "Pasivos_LP",
                "Total_Pasivos", "Patrimonio"],
            'format': [0,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,1,1]},
        'ResultsChap1': { 'title': 'Capítulo 1 - Rentabilidad',
            'variables': [
                "Ingresos", "Crecimiento_Ingresos_Perc", "Margen_Bruto", "Margen_Bruto_Perc",
                "Gastos_Admin", "Gastos_Admin_Perc", "Utilidad_Operacional",
                "Utilidad_Operacional_Perc", "EBITDA", "Utilidad_Neta",
                "Utilidad_Neta_Perc", "Utilidad_Retenida", "Cobertura_de_Intereses"],
            'format': [0,0,0,0,0,0,0,0,0,0,0,0,0]},        
        'ResultsChap2': { 'title': 'Capítulo 2 - Capital de Trabajo',
            'variables': [
                "Dias_Cuentas_X_Cobrar", "Dias_Inventario", "Dias_Cuentas_X_Pagar", "Dias_Capital_de_Trabajo",
                "Capital_de_Trabajo", "Capital_de_Trabajo_por_100Dlls", "Rotacion_Capital_de_Trabajo",
                "Flujo_Efectivo_Marginal", "Razon_Corriente"],
            'format': [0,0,0,0,0,0,0,0,0]},
        'ResultsChap3': { 'title': 'Capítulo 3 - Otro Capital',
            'variables': [
                "Otro_Capital", "Otro_Capital_Perc", "Rotacion_Otro_Capital", "Activos_Operativos_Netos",
                "Activos_Operativos_Netos_Perc", "Rotacion_Activos", "Retorno_Sobre_Capital_Perc",
                "Retorno_Sobre_Total_de_Activos_Perc", "Retorno_Sobre_Patrimonio_Perc"],
            'format': [0,0,0,0,0,0,0,0,0]},   
        'ResultsChap4': { 'title': 'Capítulo 4 - Financiamiento',
            'variables': [
                "Flujo_Efectivo_Marginal", "Flujo_Efectivo_Operacional", "Beneficio_Efectivo_Operacional", "Flujo_Efectivo_Neto",
                "Deuda_Neta", "Deuda_a_Capital", "Deuda_Neta_a_Capital_Social",
                "Cobertura_de_Intereses", "Repago_de_Deuda"],
            'format': [0,0,0,0,0,0,0,0,0]},   
            }
    for section, cfg in Fin_Statements.items():
        tables[section] = generate_financial_statements_table_from_df(df_raw, cfg)
#---------------------------------------------------

def generate_report(df_raw, selected_sections):
    if "Resumen" in selected_sections:
        Resumen(df_raw)
    if "Capítulo 1 - Rentabilidad" in selected_sections:
        Cap1(df_raw)
    if "Capítulo 2 - Capital de Trabajo" in selected_sections:
        Cap2(df_raw)
    if "Capítulo 3 - Otro Capital" in selected_sections:
        Cap3(df_raw)
    if "Capítulo 4 - Financiamiento" in selected_sections:
        Cap4(df_raw)
    if "Poder del Uno" in selected_sections or "Valuación" in selected_sections:
        Valuacion_y_Poder_del_Uno(df_raw)
    if "Crecimiento Sostenible" in selected_sections:
        Crecimiento_Sostenible(df_raw)
    if "Resultados & Proyecciones" in selected_sections:
        Proyecciones(df_raw)

    #### ============  EXPORTACION DEL REPORTE ============##
    #--------------------------------------------------------#
    from base64 import b64encode
    import mimetypes
    mime = mimetypes.guess_type(logoP_path)[0]
    with open(logoP_path, "rb") as img_file:
        encoded_logo = b64encode(img_file.read()).decode("utf-8")
    logo_url = f"data:{mime};base64,{encoded_logo}"
    #=============== Generate Report =============#
    # Set locale for Spanish (Mexico)
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # fallback
    # 1. Load your HTML template (instead of .md)
    with open("templates/HTML_Template.html", encoding="utf-8") as f:
        html_template = f.read()
    template = Template(html_template)
    # 2. Render the template with your data
    rendered_html = template.render(
        date=pd.Timestamp.now().strftime("%d de %B de %Y"),
        YEAR=pd.Timestamp.now().strftime("%Y"),
        graphs=graphs,
        tables=tables,
        # (drop generate_jinja_table & df_transposed if not used in pure-HTML)
        logo_path=logo_path,
        logoP_path=logoP_path,
        logo_url=logo_url,
        brackets_path=brackets_path,
        Usuario=Usuario,
        df_raw=df_raw,
        company=Company_Name)
    # 3. Make sure the output directory exists
    os.makedirs("output", exist_ok=True)
    pdf_path = "output/reportST.pdf"
    # 4. Convert the rendered HTML straight to PDF
    HTML(string=rendered_html, base_url=".").write_pdf(pdf_path)
    print(f"✅ PDF generated at {pdf_path}")
    # Streamlit Interface
    st.success("✅ Report successfully generated!")
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="AutoFin_Report.pdf")


# ─── App Entry ────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    upload_page()
else:
    login_page()

