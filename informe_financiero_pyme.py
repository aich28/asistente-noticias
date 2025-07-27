import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import base64
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from streamlit_option_menu import option_menu
import locale

# Configuración de la página
st.set_page_config(
    page_title="Informe Financiero PYME España",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de idioma español
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    except:
        pass

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .financial-section {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e40af 0%, #3730a3 100%);
    }
    .stSelectbox > div > div > select {
        background-color: #e0e7ff;
    }
    .summary-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }
    .alert-box {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class FinancialReportGenerator:
    def __init__(self):
        self.current_year = datetime.now().year
        self.company_data = self.generate_sample_data()
    
    def generate_sample_data(self):
        """Genera datos financieros de muestra realistas para una PYME española"""
        np.random.seed(42)  # Para reproducibilidad
        
        # Datos base de la empresa
        company_info = {
            'nombre': 'TechSolutions Innovación S.L.',
            'cif': 'B12345678',
            'sector': 'Tecnología y Servicios Digitales',
            'ubicacion': 'Madrid, España',
            'empleados': 45,
            'año_constitucion': 2018,
            'forma_juridica': 'Sociedad de Responsabilidad Limitada'
        }
        
        # Generar datos históricos de 5 años
        years = list(range(self.current_year - 4, self.current_year + 1))
        
        # Datos financieros principales
        base_revenue = 850000  # Facturación base
        growth_rates = [0.15, 0.22, 0.18, 0.25, 0.20]  # Tasas de crecimiento
        
        financial_data = {}
        
        for i, year in enumerate(years):
            revenue = base_revenue * (1 + sum(growth_rates[:i+1]))
            
            financial_data[year] = {
                # Cuenta de Resultados
                'ingresos_explotacion': revenue,
                'ventas': revenue * 0.85,
                'prestacion_servicios': revenue * 0.15,
                'gastos_explotacion': revenue * 0.72,
                'gastos_personal': revenue * 0.38,
                'gastos_externos': revenue * 0.22,
                'amortizaciones': revenue * 0.08,
                'otros_gastos': revenue * 0.04,
                'resultado_explotacion': revenue * 0.28,
                'gastos_financieros': revenue * 0.02,
                'resultado_antes_impuestos': revenue * 0.26,
                'impuesto_sociedades': revenue * 0.26 * 0.25,
                'resultado_neto': revenue * 0.26 * 0.75,
                
                # Balance de Situación
                'activo_no_corriente': revenue * 0.45,
                'inmovilizado_material': revenue * 0.35,
                'inmovilizado_intangible': revenue * 0.08,
                'inversiones_financieras': revenue * 0.02,
                'activo_corriente': revenue * 0.55,
                'existencias': revenue * 0.12,
                'deudores': revenue * 0.25,
                'tesoreria': revenue * 0.18,
                'total_activo': revenue,
                'patrimonio_neto': revenue * 0.42,
                'capital_social': 50000,
                'reservas': revenue * 0.42 - 50000,
                'pasivo_no_corriente': revenue * 0.28,
                'deudas_largo_plazo': revenue * 0.28,
                'pasivo_corriente': revenue * 0.30,
                'proveedores': revenue * 0.15,
                'deudas_corto_plazo': revenue * 0.12,
                'otras_deudas': revenue * 0.03,
                
                # Ratios financieros
                'liquidez': (revenue * 0.55) / (revenue * 0.30),
                'solvencia': revenue / (revenue * 0.58),
                'endeudamiento': (revenue * 0.58) / revenue,
                'rentabilidad_economica': (revenue * 0.28) / revenue,
                'rentabilidad_financiera': (revenue * 0.26 * 0.75) / (revenue * 0.42),
                
                # Datos mensuales para el año actual
                'datos_mensuales': self.generate_monthly_data(revenue) if year == self.current_year else None
            }
        
        return {
            'info': company_info,
            'financials': financial_data,
            'years': years
        }
    
    def generate_monthly_data(self, annual_revenue):
        """Genera datos mensuales para análisis detallado"""
        monthly_data = {}
        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Distribución estacional (algunos meses mejores que otros)
        seasonal_factors = [0.08, 0.07, 0.09, 0.08, 0.085, 0.09, 
                           0.075, 0.07, 0.095, 0.10, 0.09, 0.11]
        
        for i, month in enumerate(months):
            monthly_revenue = annual_revenue * seasonal_factors[i]
            monthly_data[month] = {
                'ingresos': monthly_revenue,
                'gastos': monthly_revenue * 0.72,
                'beneficio': monthly_revenue * 0.28,
                'liquidez': np.random.uniform(15000, 45000),
                'clientes_nuevos': np.random.randint(8, 25),
                'proyectos_activos': np.random.randint(12, 28)
            }
        
        return monthly_data

# Inicializar el generador de informes
@st.cache_data
def load_financial_data():
    return FinancialReportGenerator()

def main():
    st.markdown('<h1 class="main-header">📊 INFORME FINANCIERO EJECUTIVO</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #64748b;">Análisis Integral PYME España</h2>', unsafe_allow_html=True)
    
    # Cargar datos
    report_gen = load_financial_data()
    company_data = report_gen.company_data
    
    # Menú de navegación
    with st.sidebar:
        st.markdown("### 🏢 Información de la Empresa")
        st.markdown(f"**{company_data['info']['nombre']}**")
        st.markdown(f"CIF: {company_data['info']['cif']}")
        st.markdown(f"Sector: {company_data['info']['sector']}")
        st.markdown(f"Empleados: {company_data['info']['empleados']}")
        
        st.markdown("---")
        
        selected = option_menu(
            "Secciones del Informe",
            ["Resumen Ejecutivo", "Análisis Financiero", "Cuenta de Resultados", 
             "Balance de Situación", "Ratios y KPIs", "Análisis Temporal", 
             "Proyecciones", "Conclusiones"],
            icons=["speedometer2", "graph-up", "calculator", "bank", 
                   "pie-chart", "clock-history", "crystal-ball", "check-circle"],
            menu_icon="briefcase",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#3b82f6", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#3b82f6"}
            }
        )
    
    # Contenido principal basado en la selección
    if selected == "Resumen Ejecutivo":
        show_executive_summary(company_data)
    elif selected == "Análisis Financiero":
        show_financial_analysis(company_data)
    elif selected == "Cuenta de Resultados":
        show_income_statement(company_data)
    elif selected == "Balance de Situación":
        show_balance_sheet(company_data)
    elif selected == "Ratios y KPIs":
        show_ratios_kpis(company_data)
    elif selected == "Análisis Temporal":
        show_temporal_analysis(company_data)
    elif selected == "Proyecciones":
        show_projections(company_data)
    elif selected == "Conclusiones":
        show_conclusions(company_data)

def show_executive_summary(company_data):
    st.markdown("## 🎯 Resumen Ejecutivo")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    previous_data = company_data['financials'][current_year - 1]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue_growth = ((current_data['ingresos_explotacion'] - previous_data['ingresos_explotacion']) 
                         / previous_data['ingresos_explotacion'] * 100)
        st.metric(
            "Facturación Anual",
            f"€{current_data['ingresos_explotacion']:,.0f}",
            f"{revenue_growth:+.1f}%"
        )
    
    with col2:
        profit_margin = (current_data['resultado_neto'] / current_data['ingresos_explotacion'] * 100)
        st.metric(
            "Beneficio Neto",
            f"€{current_data['resultado_neto']:,.0f}",
            f"{profit_margin:.1f}% margen"
        )
    
    with col3:
        st.metric(
            "Patrimonio Neto",
            f"€{current_data['patrimonio_neto']:,.0f}",
            f"{current_data['rentabilidad_financiera']*100:.1f}% ROE"
        )
    
    with col4:
        st.metric(
            "Ratio de Liquidez",
            f"{current_data['liquidez']:.2f}",
            "Excelente" if current_data['liquidez'] > 1.5 else "Bueno"
        )
    
    # Gráfico de evolución de ingresos
    st.markdown("### 📈 Evolución de Ingresos")
    
    years = company_data['years']
    revenues = [company_data['financials'][year]['ingresos_explotacion'] for year in years]
    profits = [company_data['financials'][year]['resultado_neto'] for year in years]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=years, y=revenues, name="Ingresos", 
                  line=dict(color='#3b82f6', width=3)),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=profits, name="Beneficio Neto", 
                  line=dict(color='#10b981', width=3)),
        secondary_y=True,
    )
    
    fig.update_layout(
        title="Evolución Financiera (5 años)",
        xaxis_title="Año",
        height=400
    )
    
    fig.update_yaxis(title_text="Ingresos (€)", secondary_y=False)
    fig.update_yaxis(title_text="Beneficio Neto (€)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Puntos clave del resumen
    st.markdown('<div class="summary-box">', unsafe_allow_html=True)
    st.markdown("### 🔑 Puntos Clave del Ejercicio")
    st.markdown(f"""
    - **Crecimiento sostenido**: La empresa ha experimentado un crecimiento del {revenue_growth:.1f}% en facturación
    - **Rentabilidad sólida**: Margen de beneficio neto del {profit_margin:.1f}%
    - **Posición financiera estable**: Ratio de liquidez de {current_data['liquidez']:.2f}
    - **Solvencia adecuada**: Nivel de endeudamiento del {current_data['endeudamiento']*100:.1f}%
    - **Perspectivas positivas**: Tendencia alcista en todos los indicadores principales
    """)
    st.markdown('</div>', unsafe_allow_html=True)

def show_financial_analysis(company_data):
    st.markdown("## 💰 Análisis Financiero Detallado")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    
    # Análisis de rentabilidad
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Estructura de Ingresos")
        
        # Gráfico de estructura de ingresos
        labels = ['Ventas', 'Servicios']
        values = [current_data['ventas'], current_data['prestacion_servicios']]
        
        fig = px.pie(values=values, names=labels, 
                     title="Distribución de Ingresos por Tipo",
                     color_discrete_sequence=['#3b82f6', '#10b981'])
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💸 Estructura de Gastos")
        
        # Gráfico de estructura de gastos
        gastos_labels = ['Gastos Personal', 'Gastos Externos', 'Amortizaciones', 'Otros']
        gastos_values = [
            current_data['gastos_personal'],
            current_data['gastos_externos'],
            current_data['amortizaciones'],
            current_data['otros_gastos']
        ]
        
        fig = px.pie(values=gastos_values, names=gastos_labels,
                     title="Distribución de Gastos de Explotación",
                     color_discrete_sequence=['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4'])
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis mensual (si disponible)
    if current_data.get('datos_mensuales'):
        st.markdown("### 📅 Evolución Mensual del Año Actual")
        
        monthly_data = current_data['datos_mensuales']
        months = list(monthly_data.keys())
        monthly_revenues = [monthly_data[month]['ingresos'] for month in months]
        monthly_profits = [monthly_data[month]['beneficio'] for month in months]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=months,
            y=monthly_revenues,
            name='Ingresos Mensuales',
            marker_color='#3b82f6',
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=months,
            y=monthly_profits,
            mode='lines+markers',
            name='Beneficio Mensual',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Evolución Mensual - Ingresos vs Beneficios",
            xaxis_title="Mes",
            yaxis_title="Importe (€)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de datos mensuales
        st.markdown("### 📋 Detalle Mensual")
        
        monthly_df = pd.DataFrame({
            'Mes': months,
            'Ingresos (€)': [f"{monthly_data[month]['ingresos']:,.0f}" for month in months],
            'Gastos (€)': [f"{monthly_data[month]['gastos']:,.0f}" for month in months],
            'Beneficio (€)': [f"{monthly_data[month]['beneficio']:,.0f}" for month in months],
            'Liquidez (€)': [f"{monthly_data[month]['liquidez']:,.0f}" for month in months],
            'Clientes Nuevos': [monthly_data[month]['clientes_nuevos'] for month in months],
            'Proyectos Activos': [monthly_data[month]['proyectos_activos'] for month in months]
        })
        
        st.dataframe(monthly_df, use_container_width=True)

def show_income_statement(company_data):
    st.markdown("## 🧮 Cuenta de Resultados")
    
    # Crear tabla comparativa de varios años
    years = company_data['years'][-3:]  # Últimos 3 años
    
    income_data = []
    for year in years:
        data = company_data['financials'][year]
        income_data.append({
            'Concepto': 'Ingresos de Explotación',
            str(year): f"€{data['ingresos_explotacion']:,.0f}"
        })
    
    # Construir DataFrame para la cuenta de resultados
    concepts = [
        ('Ingresos de Explotación', 'ingresos_explotacion'),
        ('  - Ventas', 'ventas'),
        ('  - Prestación de Servicios', 'prestacion_servicios'),
        ('Gastos de Explotación', 'gastos_explotacion'),
        ('  - Gastos de Personal', 'gastos_personal'),
        ('  - Gastos Externos', 'gastos_externos'),
        ('  - Amortizaciones', 'amortizaciones'),
        ('  - Otros Gastos', 'otros_gastos'),
        ('RESULTADO DE EXPLOTACIÓN', 'resultado_explotacion'),
        ('Gastos Financieros', 'gastos_financieros'),
        ('RESULTADO ANTES DE IMPUESTOS', 'resultado_antes_impuestos'),
        ('Impuesto sobre Sociedades', 'impuesto_sociedades'),
        ('RESULTADO NETO', 'resultado_neto')
    ]
    
    # Crear DataFrame
    df_data = {'Concepto': [concept[0] for concept in concepts]}
    
    for year in years:
        year_data = []
        for concept in concepts:
            value = company_data['financials'][year][concept[1]]
            if concept[0] in ['Gastos de Explotación', 'Gastos de Personal', 'Gastos Externos', 
                             'Amortizaciones', 'Otros Gastos', 'Gastos Financieros', 'Impuesto sobre Sociedades']:
                year_data.append(f"-€{abs(value):,.0f}")
            else:
                year_data.append(f"€{value:,.0f}")
        df_data[str(year)] = year_data
    
    df_income = pd.DataFrame(df_data)
    
    # Aplicar formato condicional
    st.markdown("### 📊 Estado de Resultados Comparativo")
    
    # Mostrar tabla con estilo
    st.dataframe(
        df_income,
        use_container_width=True,
        hide_index=True
    )
    
    # Gráfico de cascada para el año actual
    current_year = max(years)
    current_data = company_data['financials'][current_year]
    
    st.markdown("### 🌊 Análisis de Cascada - Formación del Resultado")
    
    # Datos para el gráfico de cascada
    waterfall_data = [
        ('Ingresos', current_data['ingresos_explotacion'], 'increasing'),
        ('Gastos Personal', -current_data['gastos_personal'], 'decreasing'),
        ('Gastos Externos', -current_data['gastos_externos'], 'decreasing'),
        ('Amortizaciones', -current_data['amortizaciones'], 'decreasing'),
        ('Otros Gastos', -current_data['otros_gastos'], 'decreasing'),
        ('Gastos Financieros', -current_data['gastos_financieros'], 'decreasing'),
        ('Impuestos', -current_data['impuesto_sociedades'], 'decreasing'),
        ('Resultado Final', current_data['resultado_neto'], 'total')
    ]
    
    fig = go.Figure(go.Waterfall(
        name="Formación del Resultado",
        orientation="v",
        measure=[item[2] for item in waterfall_data],
        x=[item[0] for item in waterfall_data],
        y=[item[1] for item in waterfall_data],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#3b82f6"}}
    ))
    
    fig.update_layout(
        title=f"Formación del Resultado Neto {current_year}",
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de márgenes
    st.markdown("### 📈 Análisis de Márgenes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        margen_bruto = (current_data['ingresos_explotacion'] - current_data['gastos_externos']) / current_data['ingresos_explotacion'] * 100
        st.metric("Margen Bruto", f"{margen_bruto:.1f}%")
    
    with col2:
        margen_operativo = current_data['resultado_explotacion'] / current_data['ingresos_explotacion'] * 100
        st.metric("Margen Operativo", f"{margen_operativo:.1f}%")
    
    with col3:
        margen_neto = current_data['resultado_neto'] / current_data['ingresos_explotacion'] * 100
        st.metric("Margen Neto", f"{margen_neto:.1f}%")

def show_balance_sheet(company_data):
    st.markdown("## 🏦 Balance de Situación")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 ACTIVO")
        
        # Estructura del activo
        activo_data = {
            'Concepto': [
                'ACTIVO NO CORRIENTE',
                '  - Inmovilizado Material',
                '  - Inmovilizado Intangible',
                '  - Inversiones Financieras',
                'ACTIVO CORRIENTE',
                '  - Existencias',
                '  - Deudores',
                '  - Tesorería',
                'TOTAL ACTIVO'
            ],
            'Importe (€)': [
                f"{current_data['activo_no_corriente']:,.0f}",
                f"{current_data['inmovilizado_material']:,.0f}",
                f"{current_data['inmovilizado_intangible']:,.0f}",
                f"{current_data['inversiones_financieras']:,.0f}",
                f"{current_data['activo_corriente']:,.0f}",
                f"{current_data['existencias']:,.0f}",
                f"{current_data['deudores']:,.0f}",
                f"{current_data['tesoreria']:,.0f}",
                f"{current_data['total_activo']:,.0f}"
            ],
            '% s/Total': [
                f"{current_data['activo_no_corriente']/current_data['total_activo']*100:.1f}%",
                f"{current_data['inmovilizado_material']/current_data['total_activo']*100:.1f}%",
                f"{current_data['inmovilizado_intangible']/current_data['total_activo']*100:.1f}%",
                f"{current_data['inversiones_financieras']/current_data['total_activo']*100:.1f}%",
                f"{current_data['activo_corriente']/current_data['total_activo']*100:.1f}%",
                f"{current_data['existencias']/current_data['total_activo']*100:.1f}%",
                f"{current_data['deudores']/current_data['total_activo']*100:.1f}%",
                f"{current_data['tesoreria']/current_data['total_activo']*100:.1f}%",
                "100.0%"
            ]
        }
        
        df_activo = pd.DataFrame(activo_data)
        st.dataframe(df_activo, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📉 PASIVO Y PATRIMONIO NETO")
        
        # Estructura del pasivo
        pasivo_data = {
            'Concepto': [
                'PATRIMONIO NETO',
                '  - Capital Social',
                '  - Reservas',
                'PASIVO NO CORRIENTE',
                '  - Deudas a Largo Plazo',
                'PASIVO CORRIENTE',
                '  - Proveedores',
                '  - Deudas a Corto Plazo',
                '  - Otras Deudas',
                'TOTAL PASIVO + PN'
            ],
            'Importe (€)': [
                f"{current_data['patrimonio_neto']:,.0f}",
                f"{current_data['capital_social']:,.0f}",
                f"{current_data['reservas']:,.0f}",
                f"{current_data['pasivo_no_corriente']:,.0f}",
                f"{current_data['deudas_largo_plazo']:,.0f}",
                f"{current_data['pasivo_corriente']:,.0f}",
                f"{current_data['proveedores']:,.0f}",
                f"{current_data['deudas_corto_plazo']:,.0f}",
                f"{current_data['otras_deudas']:,.0f}",
                f"{current_data['total_activo']:,.0f}"
            ],
            '% s/Total': [
                f"{current_data['patrimonio_neto']/current_data['total_activo']*100:.1f}%",
                f"{current_data['capital_social']/current_data['total_activo']*100:.1f}%",
                f"{current_data['reservas']/current_data['total_activo']*100:.1f}%",
                f"{current_data['pasivo_no_corriente']/current_data['total_activo']*100:.1f}%",
                f"{current_data['deudas_largo_plazo']/current_data['total_activo']*100:.1f}%",
                f"{current_data['pasivo_corriente']/current_data['total_activo']*100:.1f}%",
                f"{current_data['proveedores']/current_data['total_activo']*100:.1f}%",
                f"{current_data['deudas_corto_plazo']/current_data['total_activo']*100:.1f}%",
                f"{current_data['otras_deudas']/current_data['total_activo']*100:.1f}%",
                "100.0%"
            ]
        }
        
        df_pasivo = pd.DataFrame(pasivo_data)
        st.dataframe(df_pasivo, use_container_width=True, hide_index=True)
    
    # Gráficos de estructura patrimonial
    st.markdown("### 🎯 Estructura Patrimonial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de estructura del activo
        labels_activo = ['Activo No Corriente', 'Activo Corriente']
        values_activo = [current_data['activo_no_corriente'], current_data['activo_corriente']]
        
        fig1 = px.pie(values=values_activo, names=labels_activo,
                     title="Estructura del Activo",
                     color_discrete_sequence=['#3b82f6', '#10b981'])
        
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Gráfico de estructura de financiación
        labels_financiacion = ['Patrimonio Neto', 'Pasivo No Corriente', 'Pasivo Corriente']
        values_financiacion = [
            current_data['patrimonio_neto'],
            current_data['pasivo_no_corriente'],
            current_data['pasivo_corriente']
        ]
        
        fig2 = px.pie(values=values_financiacion, names=labels_financiacion,
                     title="Estructura de Financiación",
                     color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'])
        
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Análisis de equilibrio patrimonial
    st.markdown("### ⚖️ Análisis de Equilibrio Patrimonial")
    
    fondo_maniobra = current_data['activo_corriente'] - current_data['pasivo_corriente']
    capital_trabajo = current_data['patrimonio_neto'] + current_data['pasivo_no_corriente'] - current_data['activo_no_corriente']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fondo de Maniobra", f"€{fondo_maniobra:,.0f}")
        
    with col2:
        st.metric("Capital de Trabajo", f"€{capital_trabajo:,.0f}")
        
    with col3:
        autonomia_financiera = current_data['patrimonio_neto'] / current_data['total_activo'] * 100
        st.metric("Autonomía Financiera", f"{autonomia_financiera:.1f}%")

def show_ratios_kpis(company_data):
    st.markdown("## 📊 Ratios Financieros y KPIs")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    
    # Ratios de liquidez
    st.markdown("### 💧 Ratios de Liquidez")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        liquidez_corriente = current_data['liquidez']
        st.metric("Liquidez Corriente", f"{liquidez_corriente:.2f}")
        st.caption("Activo Corriente / Pasivo Corriente")
        
    with col2:
        liquidez_acida = (current_data['activo_corriente'] - current_data['existencias']) / current_data['pasivo_corriente']
        st.metric("Liquidez Ácida", f"{liquidez_acida:.2f}")
        st.caption("(Activo Corriente - Existencias) / Pasivo Corriente")
        
    with col3:
        liquidez_inmediata = current_data['tesoreria'] / current_data['pasivo_corriente']
        st.metric("Liquidez Inmediata", f"{liquidez_inmediata:.2f}")
        st.caption("Tesorería / Pasivo Corriente")
    
    # Ratios de endeudamiento
    st.markdown("### 🏦 Ratios de Endeudamiento")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        endeudamiento_total = current_data['endeudamiento']
        st.metric("Endeudamiento Total", f"{endeudamiento_total*100:.1f}%")
        st.caption("Pasivo Total / Activo Total")
        
    with col2:
        autonomia_financiera = current_data['patrimonio_neto'] / current_data['total_activo']
        st.metric("Autonomía Financiera", f"{autonomia_financiera*100:.1f}%")
        st.caption("Patrimonio Neto / Activo Total")
        
    with col3:
        garantia = current_data['total_activo'] / (current_data['pasivo_no_corriente'] + current_data['pasivo_corriente'])
        st.metric("Ratio de Garantía", f"{garantia:.2f}")
        st.caption("Activo Total / Pasivo Total")
    
    # Ratios de rentabilidad
    st.markdown("### 💰 Ratios de Rentabilidad")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        roe = current_data['rentabilidad_financiera']
        st.metric("ROE", f"{roe*100:.1f}%")
        st.caption("Resultado Neto / Patrimonio Neto")
        
    with col2:
        roa = current_data['rentabilidad_economica']
        st.metric("ROA", f"{roa*100:.1f}%")
        st.caption("Resultado Explotación / Activo Total")
        
    with col3:
        margen_ventas = current_data['resultado_neto'] / current_data['ingresos_explotacion']
        st.metric("Margen sobre Ventas", f"{margen_ventas*100:.1f}%")
        st.caption("Resultado Neto / Ingresos")
    
    # Gráfico comparativo de ratios
    st.markdown("### 📈 Evolución de Ratios Clave")
    
    years = company_data['years']
    roe_evolution = [company_data['financials'][year]['rentabilidad_financiera']*100 for year in years]
    roa_evolution = [company_data['financials'][year]['rentabilidad_economica']*100 for year in years]
    liquidez_evolution = [company_data['financials'][year]['liquidez'] for year in years]
    endeudamiento_evolution = [company_data['financials'][year]['endeudamiento']*100 for year in years]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Rentabilidad Financiera (ROE)', 'Rentabilidad Económica (ROA)', 
                       'Ratio de Liquidez', 'Ratio de Endeudamiento'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # ROE
    fig.add_trace(
        go.Scatter(x=years, y=roe_evolution, name="ROE (%)", 
                  line=dict(color='#10b981', width=3)),
        row=1, col=1
    )
    
    # ROA
    fig.add_trace(
        go.Scatter(x=years, y=roa_evolution, name="ROA (%)", 
                  line=dict(color='#3b82f6', width=3)),
        row=1, col=2
    )
    
    # Liquidez
    fig.add_trace(
        go.Scatter(x=years, y=liquidez_evolution, name="Liquidez", 
                  line=dict(color='#f59e0b', width=3)),
        row=2, col=1
    )
    
    # Endeudamiento
    fig.add_trace(
        go.Scatter(x=years, y=endeudamiento_evolution, name="Endeudamiento (%)", 
                  line=dict(color='#ef4444', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Evolución de Ratios Financieros")
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis del sector (benchmarking)
    st.markdown("### 🎯 Benchmarking Sectorial")
    
    # Datos de referencia del sector tecnológico
    sector_benchmarks = {
        'ROE': {'Excelente': '>15%', 'Bueno': '10-15%', 'Aceptable': '5-10%', 'Deficiente': '<5%'},
        'ROA': {'Excelente': '>10%', 'Bueno': '7-10%', 'Aceptable': '3-7%', 'Deficiente': '<3%'},
        'Liquidez': {'Excelente': '>2.0', 'Bueno': '1.5-2.0', 'Aceptable': '1.0-1.5', 'Deficiente': '<1.0'},
        'Endeudamiento': {'Excelente': '<30%', 'Bueno': '30-50%', 'Aceptable': '50-70%', 'Deficiente': '>70%'}
    }
    
    def evaluate_ratio(ratio_name, value):
        if ratio_name == 'ROE':
            if value > 15: return 'Excelente', '#10b981'
            elif value > 10: return 'Bueno', '#3b82f6'
            elif value > 5: return 'Aceptable', '#f59e0b'
            else: return 'Deficiente', '#ef4444'
        elif ratio_name == 'ROA':
            if value > 10: return 'Excelente', '#10b981'
            elif value > 7: return 'Bueno', '#3b82f6'
            elif value > 3: return 'Aceptable', '#f59e0b'
            else: return 'Deficiente', '#ef4444'
        elif ratio_name == 'Liquidez':
            if value > 2.0: return 'Excelente', '#10b981'
            elif value > 1.5: return 'Bueno', '#3b82f6'
            elif value > 1.0: return 'Aceptable', '#f59e0b'
            else: return 'Deficiente', '#ef4444'
        elif ratio_name == 'Endeudamiento':
            if value < 30: return 'Excelente', '#10b981'
            elif value < 50: return 'Bueno', '#3b82f6'
            elif value < 70: return 'Aceptable', '#f59e0b'
            else: return 'Deficiente', '#ef4444'
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        roe_eval, roe_color = evaluate_ratio('ROE', roe*100)
        st.markdown(f"""
        <div style="background: {roe_color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h4>ROE: {roe*100:.1f}%</h4>
            <p>{roe_eval}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        roa_eval, roa_color = evaluate_ratio('ROA', roa*100)
        st.markdown(f"""
        <div style="background: {roa_color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h4>ROA: {roa*100:.1f}%</h4>
            <p>{roa_eval}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        liquidez_eval, liquidez_color = evaluate_ratio('Liquidez', liquidez_corriente)
        st.markdown(f"""
        <div style="background: {liquidez_color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h4>Liquidez: {liquidez_corriente:.2f}</h4>
            <p>{liquidez_eval}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        endeud_eval, endeud_color = evaluate_ratio('Endeudamiento', endeudamiento_total*100)
        st.markdown(f"""
        <div style="background: {endeud_color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h4>Endeudamiento: {endeudamiento_total*100:.1f}%</h4>
            <p>{endeud_eval}</p>
        </div>
        """, unsafe_allow_html=True)

def show_temporal_analysis(company_data):
    st.markdown("## ⏰ Análisis Temporal y Tendencias")
    
    years = company_data['years']
    
    # Evolución de indicadores principales
    st.markdown("### 📈 Evolución de Indicadores Clave")
    
    # Preparar datos para gráficos
    revenues = [company_data['financials'][year]['ingresos_explotacion'] for year in years]
    profits = [company_data['financials'][year]['resultado_neto'] for year in years]
    assets = [company_data['financials'][year]['total_activo'] for year in years]
    equity = [company_data['financials'][year]['patrimonio_neto'] for year in years]
    
    # Gráfico de evolución principal
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Evolución de Ingresos', 'Evolución del Beneficio Neto', 
                       'Evolución del Activo Total', 'Evolución del Patrimonio Neto'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Ingresos
    fig.add_trace(
        go.Scatter(x=years, y=revenues, name="Ingresos", 
                  line=dict(color='#3b82f6', width=3), mode='lines+markers'),
        row=1, col=1
    )
    
    # Beneficios
    fig.add_trace(
        go.Scatter(x=years, y=profits, name="Beneficio Neto", 
                  line=dict(color='#10b981', width=3), mode='lines+markers'),
        row=1, col=2
    )
    
    # Activos
    fig.add_trace(
        go.Scatter(x=years, y=assets, name="Activo Total", 
                  line=dict(color='#f59e0b', width=3), mode='lines+markers'),
        row=2, col=1
    )
    
    # Patrimonio
    fig.add_trace(
        go.Scatter(x=years, y=equity, name="Patrimonio Neto", 
                  line=dict(color='#8b5cf6', width=3), mode='lines+markers'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Evolución Temporal de Magnitudes Principales")
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de crecimiento
    st.markdown("### 📊 Análisis de Tasas de Crecimiento")
    
    # Calcular tasas de crecimiento anuales
    growth_data = []
    for i in range(1, len(years)):
        year = years[i]
        prev_year = years[i-1]
        
        revenue_growth = (revenues[i] - revenues[i-1]) / revenues[i-1] * 100
        profit_growth = (profits[i] - profits[i-1]) / profits[i-1] * 100
        asset_growth = (assets[i] - assets[i-1]) / assets[i-1] * 100
        equity_growth = (equity[i] - equity[i-1]) / equity[i-1] * 100
        
        growth_data.append({
            'Año': f"{prev_year}-{year}",
            'Crecimiento Ingresos (%)': revenue_growth,
            'Crecimiento Beneficio (%)': profit_growth,
            'Crecimiento Activo (%)': asset_growth,
            'Crecimiento Patrimonio (%)': equity_growth
        })
    
    df_growth = pd.DataFrame(growth_data)
    
    # Gráfico de barras de crecimiento
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_growth['Año'],
        y=df_growth['Crecimiento Ingresos (%)'],
        name='Ingresos',
        marker_color='#3b82f6'
    ))
    
    fig.add_trace(go.Bar(
        x=df_growth['Año'],
        y=df_growth['Crecimiento Beneficio (%)'],
        name='Beneficio',
        marker_color='#10b981'
    ))
    
    fig.add_trace(go.Bar(
        x=df_growth['Año'],
        y=df_growth['Crecimiento Activo (%)'],
        name='Activo',
        marker_color='#f59e0b'
    ))
    
    fig.add_trace(go.Bar(
        x=df_growth['Año'],
        y=df_growth['Crecimiento Patrimonio (%)'],
        name='Patrimonio',
        marker_color='#8b5cf6'
    ))
    
    fig.update_layout(
        title="Tasas de Crecimiento Anuales",
        xaxis_title="Período",
        yaxis_title="Crecimiento (%)",
        height=400,
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de crecimiento
    st.dataframe(df_growth.round(2), use_container_width=True, hide_index=True)
    
    # Análisis de tendencias
    st.markdown("### 🎯 Análisis de Tendencias")
    
    # Calcular tendencias (regresión lineal simple)
    from scipy import stats
    
    # Tendencia de ingresos
    slope_revenue, _, r_value_revenue, _, _ = stats.linregress(range(len(years)), revenues)
    # Tendencia de beneficios
    slope_profit, _, r_value_profit, _, _ = stats.linregress(range(len(years)), profits)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Tendencia de Ingresos")
        trend_revenue = "Creciente" if slope_revenue > 0 else "Decreciente"
        strength_revenue = "Fuerte" if abs(r_value_revenue) > 0.8 else "Moderada" if abs(r_value_revenue) > 0.5 else "Débil"
        
        st.metric(
            "Tendencia",
            trend_revenue,
            f"Correlación: {r_value_revenue:.3f} ({strength_revenue})"
        )
        
        # Crecimiento medio anual
        cagr_revenue = (revenues[-1] / revenues[0]) ** (1/(len(years)-1)) - 1
        st.metric("CAGR Ingresos", f"{cagr_revenue*100:.1f}%")
    
    with col2:
        st.markdown("#### 💰 Tendencia de Beneficios")
        trend_profit = "Creciente" if slope_profit > 0 else "Decreciente"
        strength_profit = "Fuerte" if abs(r_value_profit) > 0.8 else "Moderada" if abs(r_value_profit) > 0.5 else "Débil"
        
        st.metric(
            "Tendencia",
            trend_profit,
            f"Correlación: {r_value_profit:.3f} ({strength_profit})"
        )
        
        # Crecimiento medio anual
        cagr_profit = (profits[-1] / profits[0]) ** (1/(len(years)-1)) - 1
        st.metric("CAGR Beneficio", f"{cagr_profit*100:.1f}%")
    
    # Volatilidad
    st.markdown("### 📊 Análisis de Volatilidad")
    
    # Calcular coeficientes de variación
    cv_revenue = np.std(revenues) / np.mean(revenues) * 100
    cv_profit = np.std(profits) / np.mean(profits) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Volatilidad Ingresos", f"{cv_revenue:.1f}%")
        st.caption("Coeficiente de Variación")
        
    with col2:
        st.metric("Volatilidad Beneficios", f"{cv_profit:.1f}%")
        st.caption("Coeficiente de Variación")
    
    # Interpretación de volatilidad
    if cv_revenue < 10:
        volatility_revenue = "Baja"
    elif cv_revenue < 20:
        volatility_revenue = "Moderada"
    else:
        volatility_revenue = "Alta"
    
    if cv_profit < 15:
        volatility_profit = "Baja"
    elif cv_profit < 30:
        volatility_profit = "Moderada"
    else:
        volatility_profit = "Alta"
    
    st.markdown(f"""
    **Interpretación de Volatilidad:**
    - **Ingresos**: Volatilidad {volatility_revenue.lower()} ({cv_revenue:.1f}%)
    - **Beneficios**: Volatilidad {volatility_profit.lower()} ({cv_profit:.1f}%)
    
    *Una menor volatilidad indica mayor estabilidad y previsibilidad del negocio.*
    """)

def show_projections(company_data):
    st.markdown("## 🔮 Proyecciones y Escenarios")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    
    # Parámetros de proyección
    st.markdown("### ⚙️ Configuración de Escenarios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🐻 Escenario Pesimista")
        growth_pessimistic = st.slider("Crecimiento Anual (%)", -10, 30, 5, key="pessimistic")
        margin_pessimistic = st.slider("Margen Beneficio (%)", 5, 30, 15, key="margin_pess")
        
    with col2:
        st.markdown("#### 🎯 Escenario Base")
        growth_base = st.slider("Crecimiento Anual (%)", -10, 30, 15, key="base")
        margin_base = st.slider("Margen Beneficio (%)", 5, 30, 20, key="margin_base")
        
    with col3:
        st.markdown("#### 🚀 Escenario Optimista")
        growth_optimistic = st.slider("Crecimiento Anual (%)", -10, 30, 25, key="optimistic")
        margin_optimistic = st.slider("Margen Beneficio (%)", 5, 30, 25, key="margin_opt")
    
    # Generar proyecciones
    projection_years = list(range(current_year + 1, current_year + 6))  # 5 años
    
    def generate_projections(base_revenue, growth_rate, margin_rate):
        projections = []
        revenue = base_revenue
        
        for year in projection_years:
            revenue *= (1 + growth_rate / 100)
            profit = revenue * (margin_rate / 100)
            
            projections.append({
                'year': year,
                'revenue': revenue,
                'profit': profit,
                'assets': revenue * 1.2,  # Asumiendo ratio activo/ventas de 1.2
                'equity': revenue * 0.45   # Asumiendo ratio patrimonio/ventas de 0.45
            })
        
        return projections
    
    # Generar los tres escenarios
    base_revenue = current_data['ingresos_explotacion']
    
    projections_pessimistic = generate_projections(base_revenue, growth_pessimistic, margin_pessimistic)
    projections_base = generate_projections(base_revenue, growth_base, margin_base)
    projections_optimistic = generate_projections(base_revenue, growth_optimistic, margin_optimistic)
    
    # Gráfico de proyecciones
    st.markdown("### 📈 Proyecciones de Ingresos")
    
    # Datos históricos + proyecciones
    historical_years = company_data['years']
    historical_revenues = [company_data['financials'][year]['ingresos_explotacion'] for year in historical_years]
    
    all_years = historical_years + projection_years
    
    fig = go.Figure()
    
    # Datos históricos
    fig.add_trace(go.Scatter(
        x=historical_years,
        y=historical_revenues,
        mode='lines+markers',
        name='Histórico',
        line=dict(color='#1f2937', width=4),
        marker=dict(size=8)
    ))
    
    # Proyecciones
    revenue_pessimistic = [p['revenue'] for p in projections_pessimistic]
    revenue_base = [p['revenue'] for p in projections_base]
    revenue_optimistic = [p['revenue'] for p in projections_optimistic]
    
    # Conectar último año histórico con proyecciones
    connection_years = [current_year] + projection_years
    
    fig.add_trace(go.Scatter(
        x=connection_years,
        y=[historical_revenues[-1]] + revenue_pessimistic,
        mode='lines+markers',
        name='Escenario Pesimista',
        line=dict(color='#ef4444', width=3, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=connection_years,
        y=[historical_revenues[-1]] + revenue_base,
        mode='lines+markers',
        name='Escenario Base',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=connection_years,
        y=[historical_revenues[-1]] + revenue_optimistic,
        mode='lines+markers',
        name='Escenario Optimista',
        line=dict(color='#10b981', width=3, dash='dot'),
        marker=dict(size=6)
    ))
    
    # Línea vertical separando histórico de proyecciones
    fig.add_vline(x=current_year + 0.5, line_dash="solid", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Proyección de Ingresos: Escenarios Comparativos",
        xaxis_title="Año",
        yaxis_title="Ingresos (€)",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de proyecciones
    st.markdown("### 📊 Tabla de Proyecciones Detallada")
    
    # Crear DataFrame combinado
    projection_data = []
    
    for i, year in enumerate(projection_years):
        projection_data.append({
            'Año': year,
            'Ingresos Pesimista (€)': f"{projections_pessimistic[i]['revenue']:,.0f}",
            'Ingresos Base (€)': f"{projections_base[i]['revenue']:,.0f}",
            'Ingresos Optimista (€)': f"{projections_optimistic[i]['revenue']:,.0f}",
            'Beneficio Pesimista (€)': f"{projections_pessimistic[i]['profit']:,.0f}",
            'Beneficio Base (€)': f"{projections_base[i]['profit']:,.0f}",
            'Beneficio Optimista (€)': f"{projections_optimistic[i]['profit']:,.0f}"
        })
    
    df_projections = pd.DataFrame(projection_data)
    st.dataframe(df_projections, use_container_width=True, hide_index=True)
    
    # Análisis de sensibilidad
    st.markdown("### 🎛️ Análisis de Sensibilidad")
    
    # Calcular impacto de cambios en variables clave
    base_final_revenue = projections_base[-1]['revenue']
    pessimistic_final_revenue = projections_pessimistic[-1]['revenue']
    optimistic_final_revenue = projections_optimistic[-1]['revenue']
    
    impact_pessimistic = (pessimistic_final_revenue - base_final_revenue) / base_final_revenue * 100
    impact_optimistic = (optimistic_final_revenue - base_final_revenue) / base_final_revenue * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Impacto Escenario Pesimista",
            f"{impact_pessimistic:+.1f}%",
            f"€{pessimistic_final_revenue - base_final_revenue:,.0f}"
        )
    
    with col2:
        st.metric(
            "Escenario Base (Año 5)",
            f"€{base_final_revenue:,.0f}",
            "Referencia"
        )
    
    with col3:
        st.metric(
            "Impacto Escenario Optimista",
            f"{impact_optimistic:+.1f}%",
            f"€{optimistic_final_revenue - base_final_revenue:,.0f}"
        )
    
    # Probabilidades y recomendaciones
    st.markdown("### 🎯 Evaluación de Escenarios")
    
    st.markdown("""
    <div class="summary-box">
    <h4>📋 Análisis de Probabilidades</h4>
    <ul>
        <li><strong>Escenario Pesimista (25% probabilidad):</strong> Considera factores como recesión económica, pérdida de clientes principales o crisis sectoriales</li>
        <li><strong>Escenario Base (50% probabilidad):</strong> Mantiene las tendencias actuales con un crecimiento moderado y sostenible</li>
        <li><strong>Escenario Optimista (25% probabilidad):</strong> Aprovecha oportunidades de expansión, nuevos mercados o innovaciones disruptivas</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="alert-box">
    <h4>⚠️ Recomendaciones Estratégicas</h4>
    <ul>
        <li><strong>Diversificación:</strong> Reducir dependencia de clientes/sectores específicos</li>
        <li><strong>Eficiencia Operativa:</strong> Optimizar costes para mantener márgenes en escenarios adversos</li>
        <li><strong>Liquidez:</strong> Mantener reservas suficientes para capear períodos difíciles</li>
        <li><strong>Inversión en I+D:</strong> Prepararse para aprovechar oportunidades de crecimiento</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

def show_conclusions(company_data):
    st.markdown("## 📝 Conclusiones y Recomendaciones")
    
    current_year = max(company_data['years'])
    current_data = company_data['financials'][current_year]
    previous_data = company_data['financials'][current_year - 1]
    
    # Resumen de fortalezas y debilidades
    st.markdown("### 💪 Análisis DAFO Financiero")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0;">
        <h4>🟢 FORTALEZAS</h4>
        <ul>
            <li><strong>Crecimiento sostenido:</strong> Ingresos en constante aumento</li>
            <li><strong>Rentabilidad sólida:</strong> Márgenes superiores a la media sectorial</li>
            <li><strong>Liquidez excelente:</strong> Capacidad de hacer frente a obligaciones</li>
            <li><strong>Estructura financiera equilibrada:</strong> Nivel de endeudamiento adecuado</li>
            <li><strong>Generación de caja:</strong> Flujos positivos consistentes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0;">
        <h4>🟦 OPORTUNIDADES</h4>
        <ul>
            <li><strong>Expansión digital:</strong> Mercado tecnológico en crecimiento</li>
            <li><strong>Internacionalización:</strong> Acceso a nuevos mercados</li>
            <li><strong>Innovación:</strong> Desarrollo de nuevos productos/servicios</li>
            <li><strong>Alianzas estratégicas:</strong> Colaboraciones para acelerar crecimiento</li>
            <li><strong>Transformación digital:</strong> Automatización de procesos</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0;">
        <h4>🟡 DEBILIDADES</h4>
        <ul>
            <li><strong>Dependencia sectorial:</strong> Concentración en tecnología</li>
            <li><strong>Tamaño limitado:</strong> Recursos humanos y financieros acotados</li>
            <li><strong>Capacidad de inversión:</strong> Limitaciones para grandes proyectos</li>
            <li><strong>Diversificación geográfica:</strong> Mercado principalmente nacional</li>
            <li><strong>Marca empresarial:</strong> Reconocimiento limitado vs. grandes corporaciones</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0;">
        <h4>🔴 AMENAZAS</h4>
        <ul>
            <li><strong>Competencia:</strong> Entrada de nuevos competidores</li>
            <li><strong>Crisis económicas:</strong> Vulnerabilidad a recesiones</li>
            <li><strong>Cambios tecnológicos:</strong> Obsolescencia de productos/servicios</li>
            <li><strong>Regulación:</strong> Nuevas normativas del sector</li>
            <li><strong>Dependencia de clientes:</strong> Riesgo de concentración</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Indicadores clave de rendimiento
    st.markdown("### 🎯 Resumen de KPIs Críticos")
    
    # Calcular métricas de rendimiento
    revenue_growth = (current_data['ingresos_explotacion'] - previous_data['ingresos_explotacion']) / previous_data['ingresos_explotacion'] * 100
    profit_margin = current_data['resultado_neto'] / current_data['ingresos_explotacion'] * 100
    roe = current_data['rentabilidad_financiera'] * 100
    debt_ratio = current_data['endeudamiento'] * 100
    liquidity = current_data['liquidez']
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        color = "#10b981" if revenue_growth > 10 else "#f59e0b" if revenue_growth > 0 else "#ef4444"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h3>{revenue_growth:.1f}%</h3>
            <p>Crecimiento<br>Ingresos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "#10b981" if profit_margin > 15 else "#f59e0b" if profit_margin > 10 else "#ef4444"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h3>{profit_margin:.1f}%</h3>
            <p>Margen<br>Beneficio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "#10b981" if roe > 15 else "#f59e0b" if roe > 10 else "#ef4444"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h3>{roe:.1f}%</h3>
            <p>Rentabilidad<br>Financiera</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = "#10b981" if debt_ratio < 50 else "#f59e0b" if debt_ratio < 70 else "#ef4444"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h3>{debt_ratio:.1f}%</h3>
            <p>Ratio<br>Endeudamiento</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        color = "#10b981" if liquidity > 1.5 else "#f59e0b" if liquidity > 1.0 else "#ef4444"
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
            <h3>{liquidity:.2f}</h3>
            <p>Ratio<br>Liquidez</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recomendaciones estratégicas
    st.markdown("### 🎯 Recomendaciones Estratégicas")
    
    st.markdown("#### 🚀 Recomendaciones a Corto Plazo (6-12 meses)")
    
    recommendations_short = [
        "**Optimización de costes operativos:** Revisar gastos externos y identificar ahorros del 3-5%",
        "**Mejora del ciclo de caja:** Reducir días de cobro y optimizar pagos a proveedores",
        "**Diversificación de clientes:** Reducir dependencia de los 3 clientes principales",
        "**Inversión en marketing digital:** Aumentar visibilidad online y captación de leads",
        "**Automatización de procesos:** Implementar herramientas para mejorar eficiencia"
    ]
    
    for rec in recommendations_short:
        st.markdown(f"• {rec}")
    
    st.markdown("#### 🎯 Recomendaciones a Medio Plazo (1-3 años)")
    
    recommendations_medium = [
        "**Expansión geográfica:** Entrada en mercados internacionales (Portugal, Francia)",
        "**Desarrollo de nuevos productos:** Invertir en I+D para innovación tecnológica",
        "**Alianzas estratégicas:** Partnerships con empresas complementarias",
        "**Digitalización completa:** Transformación digital de todos los procesos",
        "**Formación del equipo:** Plan de desarrollo profesional continuo"
    ]
    
    for rec in recommendations_medium:
        st.markdown(f"• {rec}")
    
    st.markdown("#### 🌟 Recomendaciones a Largo Plazo (3-5 años)")
    
    recommendations_long = [
        "**Consolidación sectorial:** Evaluar adquisiciones de competidores más pequeños",
        "**Diversificación sectorial:** Expandir a sectores relacionados (fintech, e-commerce)",
        "**Sostenibilidad:** Implementar prácticas ESG para atraer inversión responsable",
        "**Escalabilidad tecnológica:** Desarrollar plataformas escalables y productos SaaS",
        "**Salida estratégica:** Preparar la empresa para posible venta o IPO"
    ]
    
    for rec in recommendations_long:
        st.markdown(f"• {rec}")
    
    # Plan de acción prioritario
    st.markdown("### 📋 Plan de Acción Prioritario")
    
    action_plan = [
        {
            "Prioridad": "ALTA",
            "Acción": "Optimización de costes operativos",
            "Plazo": "3 meses",
            "Responsable": "CFO",
            "Impacto": "Mejora margen 2-3%",
            "Inversión": "€5,000"
        },
        {
            "Prioridad": "ALTA",
            "Acción": "Diversificación cartera clientes",
            "Plazo": "6 meses",
            "Responsable": "Director Comercial",
            "Impacto": "Reducir riesgo concentración",
            "Inversión": "€15,000"
        },
        {
            "Prioridad": "MEDIA",
            "Acción": "Automatización procesos",
            "Plazo": "9 meses",
            "Responsable": "CTO",
            "Impacto": "Eficiencia +20%",
            "Inversión": "€25,000"
        },
        {
            "Prioridad": "MEDIA",
            "Acción": "Expansión internacional",
            "Plazo": "18 meses",
            "Responsable": "CEO",
            "Impacto": "Crecimiento +30%",
            "Inversión": "€50,000"
        }
    ]
    
    df_action = pd.DataFrame(action_plan)
    st.dataframe(df_action, use_container_width=True, hide_index=True)
    
    # Evaluación final
    st.markdown("### 🏆 Evaluación Final de la Empresa")
    
    # Puntuación global
    score_growth = min(100, max(0, revenue_growth * 5))  # Máx 100 para 20% crecimiento
    score_profitability = min(100, profit_margin * 4)    # Máx 100 para 25% margen
    score_liquidity = min(100, liquidity * 50)           # Máx 100 para ratio 2.0
    score_leverage = max(0, 100 - debt_ratio)            # Mejor cuanto menor endeudamiento
    score_roe = min(100, roe * 4)                        # Máx 100 para 25% ROE
    
    overall_score = (score_growth + score_profitability + score_liquidity + score_leverage + score_roe) / 5
    
    # Determinar calificación
    if overall_score >= 80:
        grade = "EXCELENTE"
        grade_color = "#10b981"
        grade_description = "La empresa muestra un rendimiento excepcional en todas las áreas clave"
    elif overall_score >= 65:
        grade = "BUENO"
        grade_color = "#3b82f6"
        grade_description = "Rendimiento sólido con algunas áreas de mejora identificadas"
    elif overall_score >= 50:
        grade = "ACEPTABLE"
        grade_color = "#f59e0b"
        grade_description = "Rendimiento moderado que requiere atención en varias áreas"
    else:
        grade = "NECESITA MEJORAS"
        grade_color = "#ef4444"
        grade_description = "Requiere intervención inmediata para mejorar la situación financiera"
    
    st.markdown(f"""
    <div style="background: {grade_color}; padding: 2rem; border-radius: 15px; color: white; text-align: center; margin: 2rem 0;">
        <h2>🏆 CALIFICACIÓN GLOBAL: {grade}</h2>
        <h3>Puntuación: {overall_score:.0f}/100</h3>
        <p style="font-size: 1.2em; margin-top: 1rem;">{grade_description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Desglose de puntuaciones
    st.markdown("#### 📊 Desglose de Puntuaciones")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("Crecimiento", score_growth),
        ("Rentabilidad", score_profitability),
        ("Liquidez", score_liquidity),
        ("Solvencia", score_leverage),
        ("ROE", score_roe)
    ]
    
    for i, (metric, score) in enumerate(metrics):
        with [col1, col2, col3, col4, col5][i]:
            color = "#10b981" if score >= 80 else "#3b82f6" if score >= 65 else "#f59e0b" if score >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; text-align: center;">
                <h4>{score:.0f}/100</h4>
                <p>{metric}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Mensaje final
    st.markdown("""
    ---
    
    ### 📄 Declaración de Responsabilidad
    
    *Este informe ha sido elaborado con datos simulados para fines demostrativos. 
    En un análisis real, se requeriría acceso a los estados financieros auditados 
    y información adicional de la empresa para garantizar la precisión de las conclusiones.*
    
    **Fecha del informe:** {}
    
    **Elaborado por:** Sistema de Análisis Financiero Automatizado
    """.format(datetime.now().strftime("%d de %B de %Y")))

if __name__ == "__main__":
    main()