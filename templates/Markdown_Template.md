<style>
  body {
      font-family: sans-serif;
      font-size: 0.9rem;
      color: #333;
      margin: 0px;
      padding: 0.5px;  }
  /* H1 styling */
  h1 {
      font-size: 27px;
      font-weight: normal;
      color: #91abbe;
      text-align: left;
      margin-top: 2px;
      margin-bottom: 7px;  }
  /* H2 styling */
  h2 {
      font-size: 20px;
      font-weight: normal;
      color: #284a5f;
      text-align: left;
      margin-top: 5px;
      margin-bottom: 5px;  }
  /* General Table Styling */
  table {
      width: 100%;
      border-collapse: collapse;
      font-family:sans-serif;
      font-size: 9pt;
      margin: 0px 0;}
  /* Header Styling */
  h3 {
      margin-bottom: 0;
      font-family: sans-serif;
      font-weight: 600;
      font-size: 11px;
      color: #333;
      text-align: left;  }
  /* Separator Line Below Header */
  hr {
      border: none;
      height: 2px;
      background-color: #adbec9;
      margin-top: 3px;
      margin-bottom: 3px;  }
  /* Table Header Styling */
  table th {
      border-top: none !important;
      font-size: 8pt;
      border-bottom: 2px solid #adbec9;
      padding: 5px 7px;
      font-weight: bold;
      text-align: center; /* ✅ Soft separator */}
  /* Table Body Styling */
  table td {
      font-size: 8pt;
      padding: 5px 7px;
      text-align: right;
      border-bottom: 0.5px solid #e3ecf3; /* ✅ Adds bottom border only */
      min-width: 80px;}
  /* Removes Extra Borders */
  table, th, td {
      white-space: nowrap;
      border-top: none !important;
      border-left: none !important;
      border-right: none !important;}
  
  @page:first {
  margin: 0; /* o personalizado para portada */
  @top-left-corner {
    content: none;
  }
  @top-right {
    content: none;
  }
  @bottom-left {
    content: none;
  }
  @bottom-right {
    content: none;
  }}
  @page {
    margin: 110px 80px 60px 80px;
    @top-left-corner{      
      content: url("{{ logo_url }}");
      width: 30px;}
    @top-right {
      content: "{{ company }}\A{{ company }} {{ YEAR }}";
      font-size: 10pt;
      font-family: sans-serif;
      color: #343337;}
      white-space: pre;  
    @bottom-left {
      content: "Preparado por {{Usuario}} usando Finanzas en Automático";
      font-size: 9pt;
      color: #343337;
      font-family: sans-serif;}
    @bottom-right {
      content: "Página " counter(page) " de " counter(pages);
      font-size: 9pt;
      color: #343337;
      font-family: sans-serif;}}
</style>

<br>
<br>


<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; font-weight: 600;">
  <img src="{{ logo_path }}" alt="Company Logo" style="width:400px;"/>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
  {{ company }} {{ YEAR }}
  <br>
  Preparado para {{ company }}
  <p> {{ date }}</p>
  <div style="page-break-after: always;"></div>

</div>

# Datos
<br><br>

{{ tables['Periodo de Reportes'] | safe }}

{{ tables['Estado de Resultados'] | safe }}

{{ tables['Otra Información'] | safe }}

{{ tables['Activos'] | safe }}

{{ tables['Pasivos'] | safe }}

{{ tables['Financiamiento'] | safe }}

<div style="page-break-after: always;"></div>


# Resumen

## La Historia de tus Ganancias 
<div style="text-align: center;">
  <img src="{{ graphs['Profit_Story'] }}" alt="Profit Story" style="max-width: 100%; height: auto;" />
</div>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Rendimiento'] | safe }}
</div>

<br>

## La Historia de tu Balance General
<div style="text-align: center;">
  <img src="{{ graphs['BalanceSheet_Story'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Balance'] | safe }}
</div>

<br>
<div style="page-break-after: always;"></div>

## La Historia de tu Flujo de Efectivo
<div style="text-align: center;">
  <img src="{{ graphs['CashFlow_Story'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['FlujodeEfectivo'] | safe }}
</div>

<div style="page-break-after: always;"></div>

# Capítulo 1
<br>

## Rentabilidad

{{ tables['Ch1_Profitability'] | safe }}
<br>
<br>

## Tendencias de Rentabilidad
<div style="text-align: center;">
  <img src="{{ graphs['Profitability_Trends'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<br>
<br>
<br>
## Crecimiento de Ingresos vs Crecimiento de Costo de Ventas
<div style="text-align: center;">
  <img src="{{ graphs['RevenueVScogs'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<div style="page-break-after: always;"></div>


## Crecimiento de Ingresos vs Crecimiento de Gastos Administrativos
<div style="text-align: center;">
  <img src="{{ graphs['RevenueVSoverhead'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<br>
<br>

## Razones de Rentabilidad
<br>


<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Chap1'] | safe }}
</div>


<div style="page-break-after: always;"></div>

# Capítulo 2
<br>

## Capital de Trabajo
<br>

{{ tables['Ch2_WC'] | safe }}
<br>
<br>
<br>

## Tendencias de Capital de Trabajo
<div style="text-align: center;">
  <img src="{{ graphs['Working_Capital_Trends'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<div style="page-break-after: always;"></div>

## Linea del Tiempo del Capital de Trabajo
<br>
<div style="text-align: center;">
  <img src="{{ graphs['working_capital_timeline'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>

<br>
<br>

## Capital de Trabajo por $100
<div style="display: flex; justify-content: center; align-items: flex-start; gap: 10px;">
  <img src="{{ graphs['Working_Capital_Blocks'] }}" alt="Working Capital Blocks" style="max-width: 100%; height: auto;" />
  <img src="{{ graphs['ResumenCapTrabajo'] }}" alt="Working Capital Summary" style="max-width: 100%; height: auto;" />
</div>
<br>
<div style="page-break-after: always;"></div>



## Inversion en Capital de Trabajo por $100
<div style="text-align: center;">
  <img src="{{ graphs['Investment_WC_per100DLLS'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<br>

## Margen Bruto vs Captital de Trabajo por $100
<div style="text-align: center;">
  <img src="{{ graphs['GrossMarginVSwc'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<br>
<br>

## Razones del Capital de Trabajo
<br>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Chap2'] | safe }}
</div>

<br>
<div style="page-break-after: always;"></div>

# Capítulo 3
<br>

## Otro Capital
<br>


<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Ch3_OtherCap'] | safe }}
</div>

<br>

## Tendencias de Retorno sobre Capital
<br>
<div style="text-align: center;">
  <img src="{{ graphs['Return_on_Capital_Trends'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
<br>

## Retorno sobre Capital %
<br>

<div style="text-align: center;">
  <img src="{{ graphs['Return_on_Capital'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>

<div style="page-break-after: always;"></div>

## Otras Razones de Capital
<br>
<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Chap3'] | safe }}
</div>



<div style="page-break-after: always;"></div>

# Capítulo 4
<br>

## Financiamiento

<div style="max-width: 85%; margin: 0; auto; text-align: center;">
  {{ tables['Ch4_Fund'] | safe }}
</div>
<br>

## Tendencias de Financiamiento
<div style="text-align: center; margin: 8px auto 20px auto;">
  <img src="{{ graphs['Funding_Trends'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>


## Tu Financiamiento

{{ tables["Cashflow_Summary"] | safe }}

<br>
<div style="text-align: center;">
  <img src="{{ graphs['shortfall_legend'] }}" alt="Balance Sheet Story" style="max-width: 100%; height: auto;" />
</div>
 
<br>

## Tu Ecuación
<div style="text-align: center;">
  <img src="{{ graphs['Funding_Story'] }}" alt="Funding Story" style="max-width: 100%; height: auto;" />
  <img src="{{ brackets_path }}" alt="" style="width:650px;"/>
</div>

<div style="display: flex; font-weight: bold; color: #99a5ad;">
  <div style="width: 50%; text-align: center;">Financiamiento</div>
  <div style="width: 50%; text-align: center;">Activos Operativos Netos</div>
</div>
<div style="page-break-after: always;"></div>


## Rentabilidad vs Flujo de Efectivo 
<br>

{{ tables["Cash_vs_Profit"] | safe }}

<br>
<br>

## Beneficio del Efectivo Operacional vs Flujo de Efectivo Operacional
<div style="text-align: center;">
  <img src="{{ graphs['OperatingCash'] }}" alt="Funding Story" style="max-width: 100%; height: auto;" />
</div>
<br>

<div style="page-break-after: always;"></div>

## Razones de Financiamiento
<br>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['Chap4'] | safe }}
</div>


<div style="page-break-after: always;"></div>

# Poder del Uno
<br>

## Tu Poder del Uno

{{ tables["Poder_UNO"] | safe }}
<br>
<br>

## Impacto de Tu Poder del Uno
<br>

<div style="text-align: center;">
  <img src="{{ graphs['ImpactoUNO'] }}" alt="Funding Story" style="max-width: 100%; height: auto;" />
</div>

<div style="page-break-after: always;"></div>


# Indicador del Valor del Negocio
<br>

## Valor de tu Negocio
<br>
{{ tables["Valuation_Params"] | safe }}

<br>
{{ tables["1Val"] | safe }}
<br>

{{ tables["2Val"] | safe }}
<br>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables["3Val"] | safe }}
</div>
<br>
<div style="text-align: center;">
  <img src="{{ graphs['Valuation_StackedBar'] }}" alt="Funding Story" style="max-width: 100%; height: auto;" />
</div>

<br>
<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables['4Val'] | safe }}
</div>
<br>

<div style="max-width: 85%; margin: 0 auto; text-align: center;">
  {{ tables["5Val"] | safe }}
</div>

<br>



<div style="page-break-after: always;"></div>

# Crecimiento sostenido
<br>

## Tu Crecimiento sostenido
<br>

<div style="text-align: center;">
  <img src="{{ graphs['sustainable_growth'] }}" alt="Funding Story" style="max-width: 100%; height: auto;" />
</div>

<br>


<div style="page-break-after: always;"></div>


# Resultados & Proyecciones

<br>
{{ tables["Results_Statement"] | safe }}
<br>
{{ tables["Balance_Sheet"] | safe }}
<div style="page-break-after: always;"></div>

{{ tables["ResultsChap1"] | safe }}
<br>
{{ tables["ResultsChap2"] | safe }}
<div style="page-break-after: always;"></div>

{{ tables["ResultsChap3"] | safe }}
<br>
{{ tables["ResultsChap4"] | safe }}
