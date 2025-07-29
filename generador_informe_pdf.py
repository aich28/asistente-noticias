#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Informes Financieros en PDF
Sistema profesional para crear informes ejecutivos de alta calidad
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
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
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            # Si no está disponible el locale español, usar el predeterminado
            locale.setlocale(locale.LC_ALL, '')

class GeneradorInformePDF:
    """
    Clase para generar informes financieros en PDF con alta calidad visual
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
        
        # Configurar colores corporativos profesionales
        self.colores = {
            'primario': '#2E86AB',      # Azul corporativo
            'secundario': '#A23B72',    # Púrpura
            'terciario': '#F18F01',     # Naranja
            'cuaternario': '#C73E1D',   # Rojo
            'quintenario': '#3A86FF',   # Azul claro
            'gris': '#6C757D',          # Gris
            'verde': '#28A745',         # Verde
            'amarillo': '#FFC107'       # Amarillo
        }
        
        # Configurar fuentes
        plt.rcParams['font.family'] = 'DejaVu Sans'
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        
    def generar_datos_ejemplo(self) -> Dict:
        """Generar datos financieros de ejemplo realistas"""
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
            'roe': [12.5, 13.8, 15.2, 16.8],
            'liquidez_corriente': [1.35, 1.42, 1.48, 1.55],
            'solvencia': [1.85, 1.92, 1.98, 2.05]
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
    
    def crear_balance_situacion_matplotlib(self, datos: Dict) -> plt.Figure:
        """Crear visualización del Balance de Situación con matplotlib"""
        balance = datos['balance']
        
        # Preparar datos
        activo_corriente = sum(balance['activo_corriente'].values())
        activo_no_corriente = sum(balance['activo_no_corriente'].values())
        pasivo_corriente = sum(balance['pasivo_corriente'].values())
        pasivo_no_corriente = sum(balance['pasivo_no_corriente'].values())
        patrimonio_neto = sum(balance['patrimonio_neto'].values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Gráfico de Activo
        categorias_activo = ['Activo Corriente', 'Activo No Corriente']
        valores_activo = [activo_corriente, activo_no_corriente]
        colores_activo = [self.colores['primario'], self.colores['secundario']]
        
        bars1 = ax1.bar(categorias_activo, valores_activo, color=colores_activo, alpha=0.8)
        ax1.set_title('Activo', fontsize=16, fontweight='bold', color=self.colores['primario'])
        ax1.set_ylabel('Importe (€)', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars1, valores_activo):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{valor:,.0f}€', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de Pasivo y Patrimonio Neto
        categorias_pasivo = ['Pasivo Corriente', 'Pasivo No Corriente', 'Patrimonio Neto']
        valores_pasivo = [pasivo_corriente, pasivo_no_corriente, patrimonio_neto]
        colores_pasivo = [self.colores['terciario'], self.colores['cuaternario'], self.colores['quintenario']]
        
        bars2 = ax2.bar(categorias_pasivo, valores_pasivo, color=colores_pasivo, alpha=0.8)
        ax2.set_title('Pasivo + Patrimonio Neto', fontsize=16, fontweight='bold', color=self.colores['secundario'])
        ax2.set_ylabel('Importe (€)', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars2, valores_pasivo):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{valor:,.0f}€', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        fig.suptitle(f'Balance de Situación - {self.nombre_empresa}', fontsize=18, fontweight='bold', y=1.02)
        
        return fig
    
    def crear_cuenta_resultados_matplotlib(self, datos: Dict) -> plt.Figure:
        """Crear visualización de la Cuenta de Resultados con matplotlib"""
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
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Crear gráfico de cascada
        categorias = ['Ventas\nNetas', 'Coste de\nVentas', 'Gastos\nOperativos', 'Otros\nIngresos', 
                     'Otros\nGastos', 'Intereses', 'Impuestos', 'Beneficio\nNeto']
        valores = [ventas, -coste_ventas, -gastos_operativos, otros_ingresos, -otros_gastos, -intereses, -impuestos, beneficio_neto]
        colores = [self.colores['verde'], self.colores['cuaternario'], self.colores['cuaternario'], 
                  self.colores['verde'], self.colores['cuaternario'], self.colores['cuaternario'], 
                  self.colores['cuaternario'], self.colores['primario']]
        
        bars = ax.bar(categorias, valores, color=colores, alpha=0.8)
        ax.set_title(f'Cuenta de Resultados - {self.nombre_empresa}', fontsize=16, fontweight='bold')
        ax.set_ylabel('Importe (€)', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            if height >= 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{valor:,.0f}€', ha='center', va='bottom', fontweight='bold')
            else:
                ax.text(bar.get_x() + bar.get_width()/2., height - height*0.01,
                       f'{valor:,.0f}€', ha='center', va='top', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    def crear_dashboard_ratios(self, ratios: Dict) -> plt.Figure:
        """Crear dashboard de ratios financieros con matplotlib"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Ratio de Liquidez Corriente
        self.crear_gauge(ax1, ratios['liquidez_corriente'], 3, "Liquidez Corriente", 
                         self.colores['primario'], 1.5)
        
        # Ratio de Solvencia
        self.crear_gauge(ax2, ratios['solvencia'], 4, "Solvencia", 
                         self.colores['secundario'], 2.0)
        
        # ROE
        self.crear_gauge(ax3, ratios['roe'], 30, "ROE (%)", 
                         self.colores['terciario'], 15)
        
        # Ratio de Endeudamiento
        self.crear_gauge(ax4, ratios['endeudamiento'] * 100, 100, "Endeudamiento (%)", 
                         self.colores['cuaternario'], 50)
        
        fig.suptitle(f'Ratios Financieros Clave - {self.nombre_empresa}', 
                    fontsize=18, fontweight='bold', y=0.95)
        plt.tight_layout()
        
        return fig
    
    def crear_gauge(self, ax, valor, max_valor, titulo, color, umbral):
        """Crear gráfico tipo gauge para ratios"""
        # Crear semicírculo
        theta = np.linspace(0, np.pi, 100)
        r = 1
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Dibujar el semicírculo base
        ax.plot(x, y, 'k-', linewidth=2)
        ax.fill_between(x, 0, y, alpha=0.1, color='gray')
        
        # Calcular el ángulo para el valor actual
        porcentaje = min(valor / max_valor, 1.0)
        angulo = porcentaje * np.pi
        
        # Dibujar el arco del valor
        theta_valor = np.linspace(0, angulo, 50)
        x_valor = r * np.cos(theta_valor)
        y_valor = r * np.sin(theta_valor)
        ax.plot(x_valor, y_valor, color=color, linewidth=8, solid_capstyle='round')
        
        # Añadir el valor en el centro
        ax.text(0, 0, f'{valor:.2f}', ha='center', va='center', 
               fontsize=16, fontweight='bold', color=color)
        
        # Añadir título
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(0, 1.2)
        ax.axis('off')
        
        # Añadir umbral como línea punteada
        if umbral < max_valor:
            angulo_umbral = (umbral / max_valor) * np.pi
            x_umbral = r * np.cos(angulo_umbral)
            y_umbral = r * np.sin(angulo_umbral)
            ax.plot([0, x_umbral], [0, y_umbral], 'r--', linewidth=2, alpha=0.7)
    
    def crear_evolucion_historica_matplotlib(self, datos: Dict) -> plt.Figure:
        """Crear gráfico de evolución histórica con matplotlib"""
        datos_historicos = datos['datos_historicos']
        años = [self.año_actual - 3, self.año_actual - 2, self.año_actual - 1, self.año_actual]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Evolución de Ventas
        ax1.plot(años, datos_historicos['ventas'], marker='o', linewidth=3, 
                color=self.colores['primario'], markersize=8)
        ax1.set_title('Evolución de Ventas', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Ventas (€)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Añadir valores en los puntos
        for x, y in zip(años, datos_historicos['ventas']):
            ax1.text(x, y + y*0.02, f'{y:,.0f}€', ha='center', va='bottom', fontweight='bold')
        
        # Evolución del Beneficio Neto
        ax2.plot(años, datos_historicos['beneficio_neto'], marker='o', linewidth=3, 
                color=self.colores['secundario'], markersize=8)
        ax2.set_title('Evolución del Beneficio Neto', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Beneficio Neto (€)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        for x, y in zip(años, datos_historicos['beneficio_neto']):
            ax2.text(x, y + y*0.02, f'{y:,.0f}€', ha='center', va='bottom', fontweight='bold')
        
        # Evolución del Margen de Beneficio
        ax3.plot(años, datos_historicos['margen_beneficio'], marker='o', linewidth=3, 
                color=self.colores['terciario'], markersize=8)
        ax3.set_title('Evolución del Margen de Beneficio', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Margen (%)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        for x, y in zip(años, datos_historicos['margen_beneficio']):
            ax3.text(x, y + 0.1, f'{y:.2f}%', ha='center', va='bottom', fontweight='bold')
        
        # Evolución del ROE
        ax4.plot(años, datos_historicos['roe'], marker='o', linewidth=3, 
                color=self.colores['cuaternario'], markersize=8)
        ax4.set_title('Evolución del ROE', fontsize=14, fontweight='bold')
        ax4.set_ylabel('ROE (%)', fontsize=12)
        ax4.grid(True, alpha=0.3)
        
        for x, y in zip(años, datos_historicos['roe']):
            ax4.text(x, y + 0.2, f'{y:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        fig.suptitle(f'Evolución Histórica - {self.nombre_empresa}', 
                    fontsize=18, fontweight='bold', y=0.95)
        plt.tight_layout()
        
        return fig
    
    def crear_flujo_caja_matplotlib(self, datos: Dict) -> plt.Figure:
        """Crear visualización del Flujo de Caja con matplotlib"""
        flujo_caja = datos['flujo_caja']
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        categorias = ['Actividades\nOperativas', 'Actividades\nInversoras', 'Actividades\nFinancieras']
        valores = [flujo_caja['actividades_operativas'], flujo_caja['actividades_inversoras'], 
                  flujo_caja['actividades_financieras']]
        colores = [self.colores['verde'], self.colores['cuaternario'], self.colores['terciario']]
        
        bars = ax.bar(categorias, valores, color=colores, alpha=0.8)
        ax.set_title(f'Flujo de Caja - {self.nombre_empresa}', fontsize=16, fontweight='bold')
        ax.set_ylabel('Flujo de Caja (€)', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            if height >= 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{valor:,.0f}€', ha='center', va='bottom', fontweight='bold')
            else:
                ax.text(bar.get_x() + bar.get_width()/2., height - height*0.01,
                       f'{valor:,.0f}€', ha='center', va='top', fontweight='bold')
        
        plt.tight_layout()
        
        return fig
    
    def generar_informe_completo(self) -> Dict:
        """Generar informe financiero completo"""
        datos = self.generar_datos_ejemplo()
        ratios = self.calcular_ratios_financieros(datos)
        
        informe = {
            'datos': datos,
            'ratios': ratios,
            'graficos': {
                'balance': self.crear_balance_situacion_matplotlib(datos),
                'cuenta_resultados': self.crear_cuenta_resultados_matplotlib(datos),
                'ratios': self.crear_dashboard_ratios(ratios),
                'evolucion': self.crear_evolucion_historica_matplotlib(datos),
                'flujo_caja': self.crear_flujo_caja_matplotlib(datos)
            }
        }
        
        return informe

def main():
    """Función principal para demostrar el generador de informes"""
    # Crear instancia del generador
    generador = GeneradorInformePDF("Mi Empresa S.L.", 2024)
    
    # Generar informe completo
    informe = generador.generar_informe_completo()
    
    # Guardar gráficos como imágenes
    informe['graficos']['balance'].savefig('balance_situacion.png', dpi=300, bbox_inches='tight')
    informe['graficos']['cuenta_resultados'].savefig('cuenta_resultados.png', dpi=300, bbox_inches='tight')
    informe['graficos']['ratios'].savefig('ratios_financieros.png', dpi=300, bbox_inches='tight')
    informe['graficos']['evolucion'].savefig('evolucion_historica.png', dpi=300, bbox_inches='tight')
    informe['graficos']['flujo_caja'].savefig('flujo_caja.png', dpi=300, bbox_inches='tight')
    
    print("✅ Informe financiero generado exitosamente")
    print("📊 Gráficos guardados como imágenes de alta calidad")
    print(f"🏢 Empresa: {generador.nombre_empresa}")
    print(f"📅 Año de análisis: {generador.año_actual}")
    
    # Mostrar resumen de ratios
    print("\n📈 Ratios Financieros Clave:")
    for ratio, valor in informe['ratios'].items():
        if 'margen' in ratio or 'roa' in ratio or 'roe' in ratio:
            print(f"   {ratio.replace('_', ' ').title()}: {valor:.2f}%")
        elif 'endeudamiento' in ratio:
            print(f"   {ratio.replace('_', ' ').title()}: {valor:.2%}")
        else:
            print(f"   {ratio.replace('_', ' ').title()}: {valor:.2f}")

if __name__ == "__main__":
    main()