#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Informes Financieros para PYMEs Españolas
Generador de informes ejecutivos de alta calidad con visualizaciones profesionales
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import locale
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuración para español de manera robusta
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES')
    except locale.Error:
        # Si no está disponible el locale español, usar el predeterminado
        locale.setlocale(locale.LC_ALL, '')

class InformeFinancieroPYME:
    """
    Clase principal para generar informes financieros profesionales
    para PYMEs españolas
    """
    
    def __init__(self, nombre_empresa: str, año_actual: int = 2024):
        self.nombre_empresa = nombre_empresa
        self.año_actual = año_actual
        self.año_anterior = año_actual - 1
        self.setup_estilos()
        
    def setup_estilos(self):
        """Configurar estilos profesionales para las visualizaciones"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configurar colores corporativos
        self.colores = {
            'primario': '#1f77b4',
            'secundario': '#ff7f0e',
            'terciario': '#2ca02c',
            'cuaternario': '#d62728',
            'quintenario': '#9467bd',
            'gris': '#7f7f7f'
        }
        
    def generar_datos_ejemplo(self) -> Dict:
        """
        Generar datos financieros de ejemplo para demostración
        En un caso real, estos datos vendrían de la contabilidad de la empresa
        """
        # Datos del Balance de Situación
        balance = {
            'activo_corriente': {
                'caja_bancos': 125000,
                'clientes': 180000,
                'existencias': 95000,
                'otros_activos_corrientes': 15000
            },
            'activo_no_corriente': {
                'inmovilizado_material': 320000,
                'inmovilizado_inmaterial': 45000,
                'inversiones_financieras': 25000
            },
            'pasivo_corriente': {
                'proveedores': 85000,
                'acreedores': 25000,
                'impuestos_pendientes': 15000,
                'otros_pasivos_corrientes': 10000
            },
            'pasivo_no_corriente': {
                'prestamos_largo_plazo': 150000,
                'otros_pasivos_no_corrientes': 20000
            },
            'patrimonio_neto': {
                'capital_social': 200000,
                'reservas': 45000,
                'beneficios_no_distribuidos': 35000
            }
        }
        
        # Datos de la Cuenta de Resultados
        cuenta_resultados = {
            'ventas_netas': 850000,
            'coste_ventas': 510000,
            'gastos_operativos': {
                'gastos_personal': 120000,
                'gastos_administrativos': 45000,
                'gastos_comerciales': 35000,
                'amortizaciones': 25000
            },
            'otros_ingresos': 8000,
            'otros_gastos': 5000,
            'intereses': 12000,
            'impuestos': 28000
        }
        
        # Datos de Flujo de Caja
        flujo_caja = {
            'actividades_operativas': 85000,
            'actividades_inversoras': -45000,
            'actividades_financieras': -25000
        }
        
        # Datos históricos para comparación
        datos_historicos = {
            'ventas': [720000, 780000, 820000, 850000],
            'beneficio_neto': [45000, 52000, 58000, 65000],
            'margen_beneficio': [6.25, 6.67, 7.07, 7.65],
            'roa': [8.5, 9.2, 10.1, 11.2],
            'roe': [12.5, 13.8, 15.2, 16.8]
        }
        
        return {
            'balance': balance,
            'cuenta_resultados': cuenta_resultados,
            'flujo_caja': flujo_caja,
            'datos_historicos': datos_historicos
        }
    
    def calcular_ratios_financieros(self, datos: Dict) -> Dict:
        """Calcular ratios financieros clave"""
        balance = datos['balance']
        cuenta_resultados = datos['cuenta_resultados']
        
        # Cálculos del balance
        activo_total = (sum(balance['activo_corriente'].values()) + 
                       sum(balance['activo_no_corriente'].values()))
        pasivo_total = (sum(balance['pasivo_corriente'].values()) + 
                       sum(balance['pasivo_no_corriente'].values()))
        patrimonio_neto = sum(balance['patrimonio_neto'].values())
        
        # Cálculos de la cuenta de resultados
        ventas = cuenta_resultados['ventas_netas']
        coste_ventas = cuenta_resultados['coste_ventas']
        gastos_operativos = sum(cuenta_resultados['gastos_operativos'].values())
        beneficio_bruto = ventas - coste_ventas
        beneficio_operativo = beneficio_bruto - gastos_operativos
        beneficio_neto = (beneficio_operativo + cuenta_resultados['otros_ingresos'] - 
                         cuenta_resultados['otros_gastos'] - cuenta_resultados['intereses'] - 
                         cuenta_resultados['impuestos'])
        
        ratios = {
            # Ratios de Liquidez
            'liquidez_corriente': sum(balance['activo_corriente'].values()) / 
                                 sum(balance['pasivo_corriente'].values()),
            'liquidez_inmediata': (balance['activo_corriente']['caja_bancos'] + 
                                  balance['activo_corriente']['clientes']) / 
                                 sum(balance['pasivo_corriente'].values()),
            
            # Ratios de Solvencia
            'solvencia': activo_total / pasivo_total,
            'endeudamiento': pasivo_total / activo_total,
            
            # Ratios de Rentabilidad
            'margen_bruto': beneficio_bruto / ventas * 100,
            'margen_operativo': beneficio_operativo / ventas * 100,
            'margen_neto': beneficio_neto / ventas * 100,
            'roa': beneficio_neto / activo_total * 100,
            'roe': beneficio_neto / patrimonio_neto * 100,
            
            # Ratios de Actividad
            'rotacion_activos': ventas / activo_total,
            'rotacion_existencias': coste_ventas / balance['activo_corriente']['existencias'],
            
            # Ratios de Endeudamiento
            'ratio_deuda_patrimonio': pasivo_total / patrimonio_neto,
            'cobertura_intereses': beneficio_operativo / cuenta_resultados['intereses']
        }
        
        return ratios
    
    def crear_balance_situacion(self, datos: Dict) -> go.Figure:
        """Crear visualización del Balance de Situación"""
        balance = datos['balance']
        
        # Preparar datos para el gráfico
        activo_corriente = sum(balance['activo_corriente'].values())
        activo_no_corriente = sum(balance['activo_no_corriente'].values())
        pasivo_corriente = sum(balance['pasivo_corriente'].values())
        pasivo_no_corriente = sum(balance['pasivo_no_corriente'].values())
        patrimonio_neto = sum(balance['patrimonio_neto'].values())
        
        fig = go.Figure()
        
        # Activo
        fig.add_trace(go.Bar(
            name='Activo',
            x=['Activo Corriente', 'Activo No Corriente'],
            y=[activo_corriente, activo_no_corriente],
            marker_color=[self.colores['primario'], self.colores['secundario']],
            text=[f'{activo_corriente:,.0f}€', f'{activo_no_corriente:,.0f}€'],
            textposition='auto',
        ))
        
        # Pasivo y Patrimonio Neto
        fig.add_trace(go.Bar(
            name='Pasivo + PN',
            x=['Pasivo Corriente', 'Pasivo No Corriente', 'Patrimonio Neto'],
            y=[pasivo_corriente, pasivo_no_corriente, patrimonio_neto],
            marker_color=[self.colores['terciario'], self.colores['cuaternario'], self.colores['quintenario']],
            text=[f'{pasivo_corriente:,.0f}€', f'{pasivo_no_corriente:,.0f}€', f'{patrimonio_neto:,.0f}€'],
            textposition='auto',
        ))
        
        fig.update_layout(
            title={
                'text': f'Balance de Situación - {self.nombre_empresa}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'black'}
            },
            xaxis_title='Partidas del Balance',
            yaxis_title='Importe (€)',
            barmode='group',
            height=600,
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def crear_cuenta_resultados(self, datos: Dict) -> go.Figure:
        """Crear visualización de la Cuenta de Resultados"""
        cuenta_resultados = datos['cuenta_resultados']
        
        ventas = cuenta_resultados['ventas_netas']
        coste_ventas = cuenta_resultados['coste_ventas']
        gastos_operativos = sum(cuenta_resultados['gastos_operativos'].values())
        otros_ingresos = cuenta_resultados['otros_ingresos']
        otros_gastos = cuenta_resultados['otros_gastos']
        intereses = cuenta_resultados['intereses']
        impuestos = cuenta_resultados['impuestos']
        
        beneficio_bruto = ventas - coste_ventas
        beneficio_operativo = beneficio_bruto - gastos_operativos
        beneficio_antes_impuestos = beneficio_operativo + otros_ingresos - otros_gastos - intereses
        beneficio_neto = beneficio_antes_impuestos - impuestos
        
        fig = go.Figure()
        
        # Crear gráfico de cascada
        fig.add_trace(go.Waterfall(
            name="Cuenta de Resultados",
            orientation="h",
            measure=["relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x=[ventas, -coste_ventas, -gastos_operativos, otros_ingresos, -otros_gastos, -intereses, -impuestos, beneficio_neto],
            textposition="outside",
            text=[f"{ventas:,.0f}€", f"-{coste_ventas:,.0f}€", f"-{gastos_operativos:,.0f}€", 
                  f"+{otros_ingresos:,.0f}€", f"-{otros_gastos:,.0f}€", f"-{intereses:,.0f}€", 
                  f"-{impuestos:,.0f}€", f"{beneficio_neto:,.0f}€"],
            y=["Ventas Netas", "Coste de Ventas", "Gastos Operativos", "Otros Ingresos", 
               "Otros Gastos", "Intereses", "Impuestos", "Beneficio Neto"],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": self.colores['cuaternario']}},
            increasing={"marker": {"color": self.colores['terciario']}},
            totals={"marker": {"color": self.colores['primario']}}
        ))
        
        fig.update_layout(
            title={
                'text': f'Cuenta de Resultados - {self.nombre_empresa}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'black'}
            },
            xaxis_title='Importe (€)',
            height=600,
            showlegend=False,
            template='plotly_white'
        )
        
        return fig
    
    def crear_ratios_financieros(self, ratios: Dict) -> go.Figure:
        """Crear dashboard de ratios financieros"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Ratios de Liquidez', 'Ratios de Solvencia', 
                          'Ratios de Rentabilidad', 'Ratios de Endeudamiento'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Ratio de Liquidez Corriente
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=ratios['liquidez_corriente'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Liquidez Corriente"},
            delta={'reference': 1.5},
            gauge={
                'axis': {'range': [None, 3]},
                'bar': {'color': self.colores['primario']},
                'steps': [
                    {'range': [0, 1], 'color': "lightgray"},
                    {'range': [1, 2], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 1.5
                }
            }
        ), row=1, col=1)
        
        # Ratio de Solvencia
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=ratios['solvencia'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Solvencia"},
            delta={'reference': 2},
            gauge={
                'axis': {'range': [None, 4]},
                'bar': {'color': self.colores['secundario']},
                'steps': [
                    {'range': [0, 1.5], 'color': "lightgray"},
                    {'range': [1.5, 3], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 2
                }
            }
        ), row=1, col=2)
        
        # ROE
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=ratios['roe'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ROE (%)"},
            delta={'reference': 15},
            gauge={
                'axis': {'range': [None, 30]},
                'bar': {'color': self.colores['terciario']},
                'steps': [
                    {'range': [0, 10], 'color': "lightgray"},
                    {'range': [10, 20], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 15
                }
            }
        ), row=2, col=1)
        
        # Ratio de Endeudamiento
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=ratios['endeudamiento'] * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Endeudamiento (%)"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': self.colores['cuaternario']},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 70], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ), row=2, col=2)
        
        fig.update_layout(
            title={
                'text': f'Ratios Financieros Clave - {self.nombre_empresa}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'black'}
            },
            height=800,
            template='plotly_white'
        )
        
        return fig
    
    def crear_evolucion_historica(self, datos: Dict) -> go.Figure:
        """Crear gráfico de evolución histórica"""
        datos_historicos = datos['datos_historicos']
        años = [self.año_actual - 3, self.año_actual - 2, self.año_actual - 1, self.año_actual]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Evolución de Ventas', 'Evolución del Beneficio Neto',
                          'Evolución del Margen de Beneficio', 'Evolución del ROE'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Ventas
        fig.add_trace(
            go.Scatter(x=años, y=datos_historicos['ventas'], 
                      mode='lines+markers', name='Ventas',
                      line=dict(color=self.colores['primario'], width=3),
                      marker=dict(size=8)),
            row=1, col=1
        )
        
        # Beneficio Neto
        fig.add_trace(
            go.Scatter(x=años, y=datos_historicos['beneficio_neto'], 
                      mode='lines+markers', name='Beneficio Neto',
                      line=dict(color=self.colores['secundario'], width=3),
                      marker=dict(size=8)),
            row=1, col=2
        )
        
        # Margen de Beneficio
        fig.add_trace(
            go.Scatter(x=años, y=datos_historicos['margen_beneficio'], 
                      mode='lines+markers', name='Margen (%)',
                      line=dict(color=self.colores['terciario'], width=3),
                      marker=dict(size=8)),
            row=2, col=1
        )
        
        # ROE
        fig.add_trace(
            go.Scatter(x=años, y=datos_historicos['roe'], 
                      mode='lines+markers', name='ROE (%)',
                      line=dict(color=self.colores['cuaternario'], width=3),
                      marker=dict(size=8)),
            row=2, col=2
        )
        
        fig.update_layout(
            title={
                'text': f'Evolución Histórica - {self.nombre_empresa}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'black'}
            },
            height=800,
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    def crear_flujo_caja(self, datos: Dict) -> go.Figure:
        """Crear visualización del Flujo de Caja"""
        flujo_caja = datos['flujo_caja']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Actividades Operativas', 'Actividades Inversoras', 'Actividades Financieras'],
            y=[flujo_caja['actividades_operativas'], flujo_caja['actividades_inversoras'], 
               flujo_caja['actividades_financieras']],
            marker_color=[self.colores['primario'], self.colores['secundario'], self.colores['terciario']],
            text=[f'{flujo_caja["actividades_operativas"]:,.0f}€', 
                  f'{flujo_caja["actividades_inversoras"]:,.0f}€',
                  f'{flujo_caja["actividades_financieras"]:,.0f}€'],
            textposition='auto',
        ))
        
        fig.update_layout(
            title={
                'text': f'Flujo de Caja - {self.nombre_empresa}',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': 'black'}
            },
            xaxis_title='Tipos de Actividades',
            yaxis_title='Flujo de Caja (€)',
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def generar_informe_completo(self) -> Dict:
        """Generar informe financiero completo"""
        datos = self.generar_datos_ejemplo()
        ratios = self.calcular_ratios_financieros(datos)
        
        informe = {
            'datos': datos,
            'ratios': ratios,
            'graficos': {
                'balance': self.crear_balance_situacion(datos),
                'cuenta_resultados': self.crear_cuenta_resultados(datos),
                'ratios': self.crear_ratios_financieros(ratios),
                'evolucion': self.crear_evolucion_historica(datos),
                'flujo_caja': self.crear_flujo_caja(datos)
            }
        }
        
        return informe

def crear_app_streamlit():
    """Crear aplicación Streamlit para el informe financiero"""
    st.set_page_config(
        page_title="Informe Financiero PYME",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Informe Financiero Ejecutivo")
    st.subheader("Sistema de Análisis Financiero para PYMEs Españolas")
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        nombre_empresa = st.text_input("Nombre de la Empresa", "Mi Empresa S.L.")
        año_actual = st.number_input("Año de Análisis", min_value=2020, max_value=2030, value=2024)
        
        st.header("📈 Filtros")
        mostrar_ratios = st.checkbox("Mostrar Ratios Financieros", value=True)
        mostrar_evolucion = st.checkbox("Mostrar Evolución Histórica", value=True)
        mostrar_flujo_caja = st.checkbox("Mostrar Flujo de Caja", value=True)
    
    # Generar informe
    informe = InformeFinancieroPYME(nombre_empresa, año_actual)
    datos_completos = informe.generar_informe_completo()
    
    # Resumen ejecutivo
    st.header("📋 Resumen Ejecutivo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Ventas Netas",
            value=f"{datos_completos['datos']['cuenta_resultados']['ventas_netas']:,.0f}€",
            delta="+8.2%"
        )
    
    with col2:
        st.metric(
            label="Beneficio Neto",
            value=f"{datos_completos['datos']['cuenta_resultados']['ventas_netas'] - sum(datos_completos['datos']['cuenta_resultados']['gastos_operativos'].values()) - datos_completos['datos']['cuenta_resultados']['coste_ventas']:,.0f}€",
            delta="+12.1%"
        )
    
    with col3:
        st.metric(
            label="ROE",
            value=f"{datos_completos['ratios']['roe']:.1f}%",
            delta="+1.6%"
        )
    
    with col4:
        st.metric(
            label="Liquidez Corriente",
            value=f"{datos_completos['ratios']['liquidez_corriente']:.2f}",
            delta="+0.15"
        )
    
    # Balance de Situación
    st.header("💰 Balance de Situación")
    st.plotly_chart(datos_completos['graficos']['balance'], use_container_width=True)
    
    # Cuenta de Resultados
    st.header("📈 Cuenta de Resultados")
    st.plotly_chart(datos_completos['graficos']['cuenta_resultados'], use_container_width=True)
    
    # Ratios Financieros
    if mostrar_ratios:
        st.header("📊 Ratios Financieros Clave")
        st.plotly_chart(datos_completos['graficos']['ratios'], use_container_width=True)
        
        # Tabla de ratios
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ratios de Liquidez y Solvencia")
            ratios_liquidez = {
                'Ratio': ['Liquidez Corriente', 'Liquidez Inmediata', 'Solvencia', 'Endeudamiento'],
                'Valor': [
                    f"{datos_completos['ratios']['liquidez_corriente']:.2f}",
                    f"{datos_completos['ratios']['liquidez_inmediata']:.2f}",
                    f"{datos_completos['ratios']['solvencia']:.2f}",
                    f"{datos_completos['ratios']['endeudamiento']:.2%}"
                ]
            }
            st.dataframe(pd.DataFrame(ratios_liquidez))
        
        with col2:
            st.subheader("Ratios de Rentabilidad")
            ratios_rentabilidad = {
                'Ratio': ['Margen Bruto', 'Margen Operativo', 'Margen Neto', 'ROA', 'ROE'],
                'Valor': [
                    f"{datos_completos['ratios']['margen_bruto']:.1f}%",
                    f"{datos_completos['ratios']['margen_operativo']:.1f}%",
                    f"{datos_completos['ratios']['margen_neto']:.1f}%",
                    f"{datos_completos['ratios']['roa']:.1f}%",
                    f"{datos_completos['ratios']['roe']:.1f}%"
                ]
            }
            st.dataframe(pd.DataFrame(ratios_rentabilidad))
    
    # Evolución Histórica
    if mostrar_evolucion:
        st.header("📈 Evolución Histórica")
        st.plotly_chart(datos_completos['graficos']['evolucion'], use_container_width=True)
    
    # Flujo de Caja
    if mostrar_flujo_caja:
        st.header("💸 Flujo de Caja")
        st.plotly_chart(datos_completos['graficos']['flujo_caja'], use_container_width=True)
    
    # Análisis y Recomendaciones
    st.header("💡 Análisis y Recomendaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Fortalezas")
        st.markdown("""
        - **Liquidez sólida**: Ratio de liquidez corriente superior a 1.5
        - **Rentabilidad creciente**: ROE del 16.8% con tendencia positiva
        - **Solvencia adecuada**: Ratio de solvencia superior a 2.0
        - **Crecimiento sostenido**: Incremento anual de ventas del 8.2%
        """)
    
    with col2:
        st.subheader("⚠️ Áreas de Mejora")
        st.markdown("""
        - **Gestión de existencias**: Optimizar rotación de inventarios
        - **Control de gastos**: Reducir gastos operativos como % de ventas
        - **Estructura de deuda**: Evaluar refinanciación de deuda a largo plazo
        - **Diversificación**: Ampliar base de clientes y productos
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(f"*Informe generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}*")

if __name__ == "__main__":
    crear_app_streamlit()