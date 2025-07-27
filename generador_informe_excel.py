#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Informes Financieros en Excel
Sistema profesional para crear informes ejecutivos con formato de alta calidad
"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Color
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.utils.dataframe import dataframe_to_rows
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

class GeneradorInformeExcel:
    """
    Clase para generar informes financieros en Excel con formato profesional
    """
    
    def __init__(self, nombre_empresa: str, año_actual: int = 2024):
        self.nombre_empresa = nombre_empresa
        self.año_actual = año_actual
        self.año_anterior = año_actual - 1
        self.setup_estilos()
        
    def setup_estilos(self):
        """Configurar estilos profesionales para Excel"""
        # Colores corporativos
        self.colores = {
            'primario': '2E86AB',      # Azul corporativo
            'secundario': 'A23B72',    # Púrpura
            'terciario': 'F18F01',     # Naranja
            'cuaternario': 'C73E1D',   # Rojo
            'quintenario': '3A86FF',   # Azul claro
            'gris': '6C757D',          # Gris
            'verde': '28A745',         # Verde
            'amarillo': 'FFC107'       # Amarillo
        }
        
        # Estilos de fuente
        self.fuente_titulo = Font(name='Calibri', size=16, bold=True, color='FFFFFF')
        self.fuente_subtitulo = Font(name='Calibri', size=14, bold=True, color='FFFFFF')
        self.fuente_encabezado = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
        self.fuente_normal = Font(name='Calibri', size=11)
        self.fuente_negrita = Font(name='Calibri', size=11, bold=True)
        
        # Estilos de relleno
        self.relleno_titulo = PatternFill(start_color=self.colores['primario'], 
                                         end_color=self.colores['primario'], 
                                         fill_type='solid')
        self.relleno_subtitulo = PatternFill(start_color=self.colores['secundario'], 
                                            end_color=self.colores['secundario'], 
                                            fill_type='solid')
        self.relleno_encabezado = PatternFill(start_color=self.colores['gris'], 
                                             end_color=self.colores['gris'], 
                                             fill_type='solid')
        
        # Estilos de borde
        self.borde_fino = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Alineación
        self.align_centro = Alignment(horizontal='center', vertical='center')
        self.align_derecha = Alignment(horizontal='right', vertical='center')
        self.align_izquierda = Alignment(horizontal='left', vertical='center')
        
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
    
    def crear_hoja_resumen(self, wb: Workbook, datos: Dict, ratios: Dict):
        """Crear hoja de resumen ejecutivo"""
        ws = wb.create_sheet("Resumen Ejecutivo")
        
        # Título principal
        ws['A1'] = f'INFORME FINANCIERO EJECUTIVO - {self.nombre_empresa}'
        ws['A1'].font = self.fuente_titulo
        ws['A1'].fill = self.relleno_titulo
        ws['A1'].alignment = self.align_centro
        ws.merge_cells('A1:H1')
        
        # Fecha del informe
        ws['A3'] = f'Fecha del Informe: {datetime.now().strftime("%d/%m/%Y")}'
        ws['A3'].font = self.fuente_normal
        ws['A3'].alignment = self.align_izquierda
        
        # Período de análisis
        ws['A4'] = f'Período de Análisis: {self.año_actual}'
        ws['A4'].font = self.fuente_normal
        ws['A4'].alignment = self.align_izquierda
        
        # Métricas clave
        ws['A6'] = 'MÉTRICAS CLAVE'
        ws['A6'].font = self.fuente_subtitulo
        ws['A6'].fill = self.relleno_subtitulo
        ws['A6'].alignment = self.align_centro
        ws.merge_cells('A6:H6')
        
        # Crear tabla de métricas
        metricas = [
            ['Ventas Netas', f"{datos['cuenta_resultados']['ventas_netas']:,.0f}€", '+8.2%'],
            ['Beneficio Neto', f"{datos['cuenta_resultados']['ventas_netas'] - sum(datos['cuenta_resultados']['gastos_operativos'].values()) - datos['cuenta_resultados']['coste_ventas']:,.0f}€", '+12.1%'],
            ['ROE', f"{ratios['roe']:.1f}%", '+1.6%'],
            ['Liquidez Corriente', f"{ratios['liquidez_corriente']:.2f}", '+0.15'],
            ['Solvencia', f"{ratios['solvencia']:.2f}", '+0.07'],
            ['Endeudamiento', f"{ratios['endeudamiento']:.1%}", '-2.1%']
        ]
        
        # Encabezados de la tabla
        ws['A8'] = 'Métrica'
        ws['B8'] = 'Valor Actual'
        ws['C8'] = 'Variación vs Año Anterior'
        
        for col in ['A8', 'B8', 'C8']:
            ws[col].font = self.fuente_encabezado
            ws[col].fill = self.relleno_encabezado
            ws[col].alignment = self.align_centro
            ws[col].border = self.borde_fino
        
        # Datos de la tabla
        for i, (metrica, valor, variacion) in enumerate(metricas, 9):
            ws[f'A{i}'] = metrica
            ws[f'B{i}'] = valor
            ws[f'C{i}'] = variacion
            
            for col in ['A', 'B', 'C']:
                ws[f'{col}{i}'].font = self.fuente_normal
                ws[f'{col}{i}'].alignment = self.align_centro
                ws[f'{col}{i}'].border = self.borde_fino
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 25
    
    def crear_hoja_balance(self, wb: Workbook, datos: Dict):
        """Crear hoja del Balance de Situación"""
        ws = wb.create_sheet("Balance de Situación")
        
        # Título
        ws['A1'] = f'BALANCE DE SITUACIÓN - {self.nombre_empresa}'
        ws['A1'].font = self.fuente_titulo
        ws['A1'].fill = self.relleno_titulo
        ws['A1'].alignment = self.align_centro
        ws.merge_cells('A1:F1')
        
        # Fecha
        ws['A3'] = f'Fecha: 31/12/{self.año_actual}'
        ws['A3'].font = self.fuente_normal
        
        # Estructura del balance
        balance = datos['balance']
        
        # Activo
        ws['A5'] = 'ACTIVO'
        ws['A5'].font = self.fuente_subtitulo
        ws['A5'].fill = self.relleno_subtitulo
        ws['A5'].alignment = self.align_centro
        ws.merge_cells('A5:C5')
        
        # Encabezados del activo
        ws['A6'] = 'Concepto'
        ws['B6'] = 'Importe (€)'
        ws['C6'] = '% del Total'
        
        for col in ['A6', 'B6', 'C6']:
            ws[col].font = self.fuente_encabezado
            ws[col].fill = self.relleno_encabezado
            ws[col].alignment = self.align_centro
            ws[col].border = self.borde_fino
        
        # Datos del activo
        fila = 7
        activo_total = 0
        
        # Activo Corriente
        ws[f'A{fila}'] = 'ACTIVO CORRIENTE'
        ws[f'A{fila}'].font = self.fuente_negrita
        fila += 1
        
        for concepto, importe in balance['activo_corriente'].items():
            ws[f'A{fila}'] = concepto.replace('_', ' ').title()
            ws[f'B{fila}'] = importe
            activo_total += importe
            fila += 1
        
        # Activo No Corriente
        ws[f'A{fila}'] = 'ACTIVO NO CORRIENTE'
        ws[f'A{fila}'].font = self.fuente_negrita
        fila += 1
        
        for concepto, importe in balance['activo_no_corriente'].items():
            ws[f'A{fila}'] = concepto.replace('_', ' ').title()
            ws[f'B{fila}'] = importe
            activo_total += importe
            fila += 1
        
        # Total Activo
        ws[f'A{fila}'] = 'TOTAL ACTIVO'
        ws[f'A{fila}'].font = self.fuente_negrita
        ws[f'B{fila}'] = activo_total
        ws[f'A{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        ws[f'B{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        
        # Pasivo y Patrimonio Neto
        ws['E5'] = 'PASIVO Y PATRIMONIO NETO'
        ws['E5'].font = self.fuente_subtitulo
        ws['E5'].fill = self.relleno_subtitulo
        ws['E5'].alignment = self.align_centro
        ws.merge_cells('E5:G5')
        
        # Encabezados del pasivo
        ws['E6'] = 'Concepto'
        ws['F6'] = 'Importe (€)'
        ws['G6'] = '% del Total'
        
        for col in ['E6', 'F6', 'G6']:
            ws[col].font = self.fuente_encabezado
            ws[col].fill = self.relleno_encabezado
            ws[col].alignment = self.align_centro
            ws[col].border = self.borde_fino
        
        # Datos del pasivo
        fila_pasivo = 7
        pasivo_total = 0
        
        # Pasivo Corriente
        ws[f'E{fila_pasivo}'] = 'PASIVO CORRIENTE'
        ws[f'E{fila_pasivo}'].font = self.fuente_negrita
        fila_pasivo += 1
        
        for concepto, importe in balance['pasivo_corriente'].items():
            ws[f'E{fila_pasivo}'] = concepto.replace('_', ' ').title()
            ws[f'F{fila_pasivo}'] = importe
            pasivo_total += importe
            fila_pasivo += 1
        
        # Pasivo No Corriente
        ws[f'E{fila_pasivo}'] = 'PASIVO NO CORRIENTE'
        ws[f'E{fila_pasivo}'].font = self.fuente_negrita
        fila_pasivo += 1
        
        for concepto, importe in balance['pasivo_no_corriente'].items():
            ws[f'E{fila_pasivo}'] = concepto.replace('_', ' ').title()
            ws[f'F{fila_pasivo}'] = importe
            pasivo_total += importe
            fila_pasivo += 1
        
        # Patrimonio Neto
        ws[f'E{fila_pasivo}'] = 'PATRIMONIO NETO'
        ws[f'E{fila_pasivo}'].font = self.fuente_negrita
        fila_pasivo += 1
        
        patrimonio_total = 0
        for concepto, importe in balance['patrimonio_neto'].items():
            ws[f'E{fila_pasivo}'] = concepto.replace('_', ' ').title()
            ws[f'F{fila_pasivo}'] = importe
            patrimonio_total += importe
            fila_pasivo += 1
        
        # Total Pasivo y Patrimonio Neto
        ws[f'E{fila_pasivo}'] = 'TOTAL PASIVO Y PN'
        ws[f'E{fila_pasivo}'].font = self.fuente_negrita
        ws[f'F{fila_pasivo}'] = pasivo_total + patrimonio_total
        ws[f'E{fila_pasivo}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        ws[f'F{fila_pasivo}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        
        # Aplicar formato a todas las celdas
        for row in ws.iter_rows(min_row=6, max_row=max(fila, fila_pasivo), min_col=1, max_col=7):
            for cell in row:
                cell.border = self.borde_fino
                if cell.column in [2, 6]:  # Columnas de importes
                    cell.number_format = '#,##0€'
                    cell.alignment = self.align_derecha
        
        # Ajustar ancho de columnas
        for col in ['A', 'E']:
            ws.column_dimensions[col].width = 30
        for col in ['B', 'F']:
            ws.column_dimensions[col].width = 15
        for col in ['C', 'G']:
            ws.column_dimensions[col].width = 12
    
    def crear_hoja_cuenta_resultados(self, wb: Workbook, datos: Dict):
        """Crear hoja de la Cuenta de Resultados"""
        ws = wb.create_sheet("Cuenta de Resultados")
        
        # Título
        ws['A1'] = f'CUENTA DE RESULTADOS - {self.nombre_empresa}'
        ws['A1'].font = self.fuente_titulo
        ws['A1'].fill = self.relleno_titulo
        ws['A1'].alignment = self.align_centro
        ws.merge_cells('A1:D1')
        
        # Período
        ws['A3'] = f'Período: {self.año_actual}'
        ws['A3'].font = self.fuente_normal
        
        # Encabezados
        ws['A5'] = 'Concepto'
        ws['B5'] = 'Importe (€)'
        ws['C5'] = '% de Ventas'
        ws['D5'] = 'Variación vs Año Anterior'
        
        for col in ['A5', 'B5', 'C5', 'D5']:
            ws[col].font = self.fuente_encabezado
            ws[col].fill = self.relleno_encabezado
            ws[col].alignment = self.align_centro
            ws[col].border = self.borde_fino
        
        # Datos de la cuenta de resultados
        cuenta_resultados = datos['cuenta_resultados']
        ventas = cuenta_resultados['ventas_netas']
        
        fila = 6
        
        # Ventas
        ws[f'A{fila}'] = 'VENTAS NETAS'
        ws[f'B{fila}'] = ventas
        ws[f'C{fila}'] = 100.0
        ws[f'D{fila}'] = '+8.2%'
        fila += 1
        
        # Coste de ventas
        ws[f'A{fila}'] = 'COSTE DE VENTAS'
        ws[f'B{fila}'] = cuenta_resultados['coste_ventas']
        ws[f'C{fila}'] = cuenta_resultados['coste_ventas'] / ventas * 100
        ws[f'D{fila}'] = '-2.1%'
        fila += 1
        
        # Beneficio bruto
        beneficio_bruto = ventas - cuenta_resultados['coste_ventas']
        ws[f'A{fila}'] = 'BENEFICIO BRUTO'
        ws[f'B{fila}'] = beneficio_bruto
        ws[f'C{fila}'] = beneficio_bruto / ventas * 100
        ws[f'D{fila}'] = '+15.3%'
        ws[f'A{fila}'].font = self.fuente_negrita
        fila += 1
        
        # Gastos operativos
        ws[f'A{fila}'] = 'GASTOS OPERATIVOS'
        ws[f'A{fila}'].font = self.fuente_negrita
        fila += 1
        
        gastos_operativos = 0
        for concepto, importe in cuenta_resultados['gastos_operativos'].items():
            ws[f'A{fila}'] = f'  {concepto.replace("_", " ").title()}'
            ws[f'B{fila}'] = importe
            ws[f'C{fila}'] = importe / ventas * 100
            gastos_operativos += importe
            fila += 1
        
        # Beneficio operativo
        beneficio_operativo = beneficio_bruto - gastos_operativos
        ws[f'A{fila}'] = 'BENEFICIO OPERATIVO'
        ws[f'A{fila}'].font = self.fuente_negrita
        ws[f'B{fila}'] = beneficio_operativo
        ws[f'C{fila}'] = beneficio_operativo / ventas * 100
        ws[f'D{fila}'] = '+12.8%'
        fila += 1
        
        # Otros ingresos y gastos
        ws[f'A{fila}'] = 'OTROS INGRESOS'
        ws[f'B{fila}'] = cuenta_resultados['otros_ingresos']
        ws[f'C{fila}'] = cuenta_resultados['otros_ingresos'] / ventas * 100
        fila += 1
        
        ws[f'A{fila}'] = 'OTROS GASTOS'
        ws[f'B{fila}'] = cuenta_resultados['otros_gastos']
        ws[f'C{fila}'] = cuenta_resultados['otros_gastos'] / ventas * 100
        fila += 1
        
        # Intereses
        ws[f'A{fila}'] = 'INTERESES'
        ws[f'B{fila}'] = cuenta_resultados['intereses']
        ws[f'C{fila}'] = cuenta_resultados['intereses'] / ventas * 100
        fila += 1
        
        # Beneficio antes de impuestos
        beneficio_antes_impuestos = beneficio_operativo + cuenta_resultados['otros_ingresos'] - cuenta_resultados['otros_gastos'] - cuenta_resultados['intereses']
        ws[f'A{fila}'] = 'BENEFICIO ANTES DE IMPUESTOS'
        ws[f'A{fila}'].font = self.fuente_negrita
        ws[f'B{fila}'] = beneficio_antes_impuestos
        ws[f'C{fila}'] = beneficio_antes_impuestos / ventas * 100
        ws[f'D{fila}'] = '+11.2%'
        fila += 1
        
        # Impuestos
        ws[f'A{fila}'] = 'IMPUESTOS'
        ws[f'B{fila}'] = cuenta_resultados['impuestos']
        ws[f'C{fila}'] = cuenta_resultados['impuestos'] / ventas * 100
        fila += 1
        
        # Beneficio neto
        beneficio_neto = beneficio_antes_impuestos - cuenta_resultados['impuestos']
        ws[f'A{fila}'] = 'BENEFICIO NETO'
        ws[f'A{fila}'].font = self.fuente_negrita
        ws[f'B{fila}'] = beneficio_neto
        ws[f'C{fila}'] = beneficio_neto / ventas * 100
        ws[f'D{fila}'] = '+12.1%'
        ws[f'A{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        ws[f'B{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        ws[f'C{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        ws[f'D{fila}'].fill = PatternFill(start_color='E0E0E0', end_color='E0E0E0', fill_type='solid')
        
        # Aplicar formato
        for row in ws.iter_rows(min_row=5, max_row=fila, min_col=1, max_col=4):
            for cell in row:
                cell.border = self.borde_fino
                if cell.column == 2:  # Columna de importes
                    cell.number_format = '#,##0€'
                    cell.alignment = self.align_derecha
                elif cell.column == 3:  # Columna de porcentajes
                    cell.number_format = '0.0%'
                    cell.alignment = self.align_derecha
                else:
                    cell.alignment = self.align_izquierda
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 20
    
    def crear_hoja_ratios(self, wb: Workbook, ratios: Dict):
        """Crear hoja de ratios financieros"""
        ws = wb.create_sheet("Ratios Financieros")
        
        # Título
        ws['A1'] = f'RATIOS FINANCIEROS - {self.nombre_empresa}'
        ws['A1'].font = self.fuente_titulo
        ws['A1'].fill = self.relleno_titulo
        ws['A1'].alignment = self.align_centro
        ws.merge_cells('A1:D1')
        
        # Año de análisis
        ws['A3'] = f'Año de Análisis: {self.año_actual}'
        ws['A3'].font = self.fuente_normal
        
        # Crear tabla de ratios
        fila = 5
        
        # Ratios de Liquidez
        ws[f'A{fila}'] = 'RATIOS DE LIQUIDEZ'
        ws[f'A{fila}'].font = self.fuente_subtitulo
        ws[f'A{fila}'].fill = self.relleno_subtitulo
        ws[f'A{fila}'].alignment = self.align_centro
        ws.merge_cells(f'A{fila}:D{fila}')
        fila += 1
        
        # Encabezados
        ws[f'A{fila}'] = 'Ratio'
        ws[f'B{fila}'] = 'Valor'
        ws[f'C{fila}'] = 'Benchmark'
        ws[f'D{fila}'] = 'Evaluación'
        
        for col in ['A', 'B', 'C', 'D']:
            ws[f'{col}{fila}'].font = self.fuente_encabezado
            ws[f'{col}{fila}'].fill = self.relleno_encabezado
            ws[f'{col}{fila}'].alignment = self.align_centro
            ws[f'{col}{fila}'].border = self.borde_fino
        fila += 1
        
        # Datos de ratios de liquidez
        ratios_liquidez = [
            ('Liquidez Corriente', ratios['liquidez_corriente'], 1.5, 'Excelente'),
            ('Liquidez Inmediata', ratios['liquidez_inmediata'], 1.0, 'Bueno')
        ]
        
        for ratio, valor, benchmark, evaluacion in ratios_liquidez:
            ws[f'A{fila}'] = ratio
            ws[f'B{fila}'] = valor
            ws[f'C{fila}'] = benchmark
            ws[f'D{fila}'] = evaluacion
            
            for col in ['A', 'B', 'C', 'D']:
                ws[f'{col}{fila}'].border = self.borde_fino
                ws[f'{col}{fila}'].alignment = self.align_centro
            
            fila += 1
        
        fila += 1  # Espacio
        
        # Ratios de Solvencia
        ws[f'A{fila}'] = 'RATIOS DE SOLVENCIA'
        ws[f'A{fila}'].font = self.fuente_subtitulo
        ws[f'A{fila}'].fill = self.relleno_subtitulo
        ws[f'A{fila}'].alignment = self.align_centro
        ws.merge_cells(f'A{fila}:D{fila}')
        fila += 1
        
        # Encabezados
        ws[f'A{fila}'] = 'Ratio'
        ws[f'B{fila}'] = 'Valor'
        ws[f'C{fila}'] = 'Benchmark'
        ws[f'D{fila}'] = 'Evaluación'
        
        for col in ['A', 'B', 'C', 'D']:
            ws[f'{col}{fila}'].font = self.fuente_encabezado
            ws[f'{col}{fila}'].fill = self.relleno_encabezado
            ws[f'{col}{fila}'].alignment = self.align_centro
            ws[f'{col}{fila}'].border = self.borde_fino
        fila += 1
        
        # Datos de ratios de solvencia
        ratios_solvencia = [
            ('Solvencia', ratios['solvencia'], 2.0, 'Excelente'),
            ('Endeudamiento', ratios['endeudamiento'], 0.5, 'Aceptable')
        ]
        
        for ratio, valor, benchmark, evaluacion in ratios_solvencia:
            ws[f'A{fila}'] = ratio
            ws[f'B{fila}'] = valor
            ws[f'C{fila}'] = benchmark
            ws[f'D{fila}'] = evaluacion
            
            for col in ['A', 'B', 'C', 'D']:
                ws[f'{col}{fila}'].border = self.borde_fino
                ws[f'{col}{fila}'].alignment = self.align_centro
            
            fila += 1
        
        fila += 1  # Espacio
        
        # Ratios de Rentabilidad
        ws[f'A{fila}'] = 'RATIOS DE RENTABILIDAD'
        ws[f'A{fila}'].font = self.fuente_subtitulo
        ws[f'A{fila}'].fill = self.relleno_subtitulo
        ws[f'A{fila}'].alignment = self.align_centro
        ws.merge_cells(f'A{fila}:D{fila}')
        fila += 1
        
        # Encabezados
        ws[f'A{fila}'] = 'Ratio'
        ws[f'B{fila}'] = 'Valor'
        ws[f'C{fila}'] = 'Benchmark'
        ws[f'D{fila}'] = 'Evaluación'
        
        for col in ['A', 'B', 'C', 'D']:
            ws[f'{col}{fila}'].font = self.fuente_encabezado
            ws[f'{col}{fila}'].fill = self.relleno_encabezado
            ws[f'{col}{fila}'].alignment = self.align_centro
            ws[f'{col}{fila}'].border = self.borde_fino
        fila += 1
        
        # Datos de ratios de rentabilidad
        ratios_rentabilidad = [
            ('Margen Bruto', ratios['margen_bruto'], 25.0, 'Bueno'),
            ('Margen Operativo', ratios['margen_operativo'], 15.0, 'Excelente'),
            ('Margen Neto', ratios['margen_neto'], 8.0, 'Excelente'),
            ('ROA', ratios['roa'], 10.0, 'Excelente'),
            ('ROE', ratios['roe'], 15.0, 'Excelente')
        ]
        
        for ratio, valor, benchmark, evaluacion in ratios_rentabilidad:
            ws[f'A{fila}'] = ratio
            ws[f'B{fila}'] = valor
            ws[f'C{fila}'] = benchmark
            ws[f'D{fila}'] = evaluacion
            
            for col in ['A', 'B', 'C', 'D']:
                ws[f'{col}{fila}'].border = self.borde_fino
                ws[f'{col}{fila}'].alignment = self.align_centro
            
            fila += 1
        
        # Aplicar formato a las columnas de valores
        for row in ws.iter_rows(min_row=6, max_row=fila-1, min_col=2, max_col=2):
            for cell in row:
                if cell.value is not None and isinstance(cell.value, (int, float)):
                    if 'margen' in cell.column_letter.lower() or 'roa' in cell.column_letter.lower() or 'roe' in cell.column_letter.lower():
                        cell.number_format = '0.0%'
                    else:
                        cell.number_format = '0.00'
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 25
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
    
    def generar_informe_excel(self, nombre_archivo: str = None) -> str:
        """Generar informe financiero completo en Excel"""
        if nombre_archivo is None:
            nombre_archivo = f'Informe_Financiero_{self.nombre_empresa}_{self.año_actual}.xlsx'
        
        # Crear workbook
        wb = Workbook()
        
        # Eliminar hoja por defecto
        wb.remove(wb.active)
        
        # Generar datos
        datos = self.generar_datos_ejemplo()
        ratios = self.calcular_ratios_financieros(datos)
        
        # Crear hojas
        self.crear_hoja_resumen(wb, datos, ratios)
        self.crear_hoja_balance(wb, datos)
        self.crear_hoja_cuenta_resultados(wb, datos)
        self.crear_hoja_ratios(wb, ratios)
        
        # Guardar archivo
        wb.save(nombre_archivo)
        
        return nombre_archivo

def main():
    """Función principal para demostrar el generador de informes Excel"""
    # Crear instancia del generador
    generador = GeneradorInformeExcel("Mi Empresa S.L.", 2024)
    
    # Generar informe
    nombre_archivo = generador.generar_informe_excel()
    
    print("✅ Informe financiero Excel generado exitosamente")
    print(f"📊 Archivo: {nombre_archivo}")
    print(f"🏢 Empresa: {generador.nombre_empresa}")
    print(f"📅 Año de análisis: {generador.año_actual}")
    print("\n📋 Hojas incluidas:")
    print("   - Resumen Ejecutivo")
    print("   - Balance de Situación")
    print("   - Cuenta de Resultados")
    print("   - Ratios Financieros")

if __name__ == "__main__":
    main()