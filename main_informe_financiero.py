#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Principal de Informes Financieros para PYMEs Españolas
Script principal para generar informes en diferentes formatos
"""

import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List

# Importar los módulos de informes
from informe_financiero_pyme import InformeFinancieroPYME, crear_app_streamlit
from generador_informe_pdf import GeneradorInformePDF
from generador_informe_excel import GeneradorInformeExcel

def mostrar_banner():
    """Mostrar banner del sistema"""
    print("=" * 80)
    print("📊 SISTEMA DE INFORMES FINANCIEROS PARA PYMEs ESPAÑOLAS")
    print("=" * 80)
    print("🎯 Generador de informes ejecutivos de alta calidad")
    print("📈 Análisis financiero, económico y contable profesional")
    print("🏢 Especializado en PYMEs españolas")
    print("=" * 80)

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n📋 OPCIONES DISPONIBLES:")
    print("1. 🖥️  Aplicación Web (Streamlit)")
    print("2. 📊 Generar gráficos de alta calidad (PNG)")
    print("3. 📄 Generar informe Excel profesional")
    print("4. 📈 Generar informe completo (todos los formatos)")
    print("5. ℹ️  Información del sistema")
    print("6. ❌ Salir")
    print("-" * 80)

def ejecutar_streamlit():
    """Ejecutar aplicación Streamlit"""
    print("\n🚀 Iniciando aplicación web Streamlit...")
    print("📱 Abriendo en el navegador...")
    print("⏹️  Para detener la aplicación, presiona Ctrl+C")
    print("-" * 80)
    
    try:
        import streamlit as st
        # Ejecutar la aplicación Streamlit
        os.system(f"streamlit run informe_financiero_pyme.py --server.port 8501")
    except Exception as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")
        print("💡 Asegúrate de tener Streamlit instalado: pip install streamlit")

def generar_graficos_png():
    """Generar gráficos de alta calidad en PNG"""
    print("\n📊 Generando gráficos de alta calidad...")
    
    try:
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
        
        print("✅ Gráficos generados exitosamente:")
        print("   📈 balance_situacion.png")
        print("   📊 cuenta_resultados.png")
        print("   📉 ratios_financieros.png")
        print("   📈 evolucion_historica.png")
        print("   💰 flujo_caja.png")
        
        # Mostrar resumen de ratios
        print("\n📈 Ratios Financieros Clave:")
        for ratio, valor in informe['ratios'].items():
            if 'margen' in ratio or 'roa' in ratio or 'roe' in ratio:
                print(f"   {ratio.replace('_', ' ').title()}: {valor:.2f}%")
            elif 'endeudamiento' in ratio:
                print(f"   {ratio.replace('_', ' ').title()}: {valor:.2%}")
            else:
                print(f"   {ratio.replace('_', ' ').title()}: {valor:.2f}")
                
    except Exception as e:
        print(f"❌ Error al generar gráficos: {e}")

def generar_informe_excel():
    """Generar informe Excel profesional"""
    print("\n📄 Generando informe Excel profesional...")
    
    try:
        # Crear instancia del generador
        generador = GeneradorInformeExcel("Mi Empresa S.L.", 2024)
        
        # Generar informe
        nombre_archivo = generador.generar_informe_excel()
        
        print("✅ Informe Excel generado exitosamente")
        print(f"📊 Archivo: {nombre_archivo}")
        print(f"🏢 Empresa: {generador.nombre_empresa}")
        print(f"📅 Año de análisis: {generador.año_actual}")
        print("\n📋 Hojas incluidas:")
        print("   - Resumen Ejecutivo")
        print("   - Balance de Situación")
        print("   - Cuenta de Resultados")
        print("   - Ratios Financieros")
        
    except Exception as e:
        print(f"❌ Error al generar informe Excel: {e}")

def generar_informe_completo():
    """Generar informe completo en todos los formatos"""
    print("\n📈 Generando informe completo en todos los formatos...")
    
    try:
        # 1. Generar gráficos PNG
        print("\n📊 Paso 1: Generando gráficos de alta calidad...")
        generar_graficos_png()
        
        # 2. Generar informe Excel
        print("\n📄 Paso 2: Generando informe Excel...")
        generar_informe_excel()
        
        print("\n✅ Informe completo generado exitosamente")
        print("📁 Archivos creados:")
        print("   📈 Gráficos PNG (5 archivos)")
        print("   📄 Informe Excel (1 archivo)")
        print("\n🎯 El sistema está listo para usar con datos reales")
        
    except Exception as e:
        print(f"❌ Error al generar informe completo: {e}")

def mostrar_informacion_sistema():
    """Mostrar información del sistema"""
    print("\nℹ️  INFORMACIÓN DEL SISTEMA")
    print("=" * 50)
    print("🏢 Sistema de Informes Financieros para PYMEs Españolas")
    print("📅 Versión: 1.0")
    print("📊 Desarrollado con Python 3.8+")
    print("\n📋 CARACTERÍSTICAS:")
    print("   ✅ Análisis financiero completo")
    print("   ✅ Visualizaciones profesionales")
    print("   ✅ Ratios financieros clave")
    print("   ✅ Evolución histórica")
    print("   ✅ Flujo de caja")
    print("   ✅ Balance de situación")
    print("   ✅ Cuenta de resultados")
    print("\n📊 FORMATOS DISPONIBLES:")
    print("   🖥️  Aplicación web interactiva (Streamlit)")
    print("   📈 Gráficos de alta calidad (PNG)")
    print("   📄 Informes Excel profesionales")
    print("\n🔧 DEPENDENCIAS PRINCIPALES:")
    print("   📊 pandas, numpy, matplotlib, seaborn")
    print("   📈 plotly, streamlit")
    print("   📄 openpyxl")
    print("\n💡 USO:")
    print("   - Ejecutar con datos de ejemplo para demostración")
    print("   - Modificar datos en los scripts para datos reales")
    print("   - Personalizar colores y estilos según necesidades")

def main():
    """Función principal"""
    mostrar_banner()
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n🎯 Selecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                ejecutar_streamlit()
            elif opcion == "2":
                generar_graficos_png()
            elif opcion == "3":
                generar_informe_excel()
            elif opcion == "4":
                generar_informe_completo()
            elif opcion == "5":
                mostrar_informacion_sistema()
            elif opcion == "6":
                print("\n👋 ¡Gracias por usar el Sistema de Informes Financieros!")
                print("📊 ¡Que tengas un excelente día!")
                break
            else:
                print("\n❌ Opción no válida. Por favor, selecciona una opción del 1 al 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

def ejecutar_con_argumentos():
    """Ejecutar con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Sistema de Informes Financieros para PYMEs Españolas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main_informe_financiero.py --streamlit
  python main_informe_financiero.py --graficos
  python main_informe_financiero.py --excel
  python main_informe_financiero.py --completo
        """
    )
    
    parser.add_argument(
        "--streamlit", 
        action="store_true", 
        help="Ejecutar aplicación web Streamlit"
    )
    parser.add_argument(
        "--graficos", 
        action="store_true", 
        help="Generar gráficos de alta calidad (PNG)"
    )
    parser.add_argument(
        "--excel", 
        action="store_true", 
        help="Generar informe Excel profesional"
    )
    parser.add_argument(
        "--completo", 
        action="store_true", 
        help="Generar informe completo en todos los formatos"
    )
    parser.add_argument(
        "--info", 
        action="store_true", 
        help="Mostrar información del sistema"
    )
    
    args = parser.parse_args()
    
    if args.streamlit:
        ejecutar_streamlit()
    elif args.graficos:
        generar_graficos_png()
    elif args.excel:
        generar_informe_excel()
    elif args.completo:
        generar_informe_completo()
    elif args.info:
        mostrar_informacion_sistema()
    else:
        # Si no se proporcionan argumentos, mostrar menú interactivo
        main()

if __name__ == "__main__":
    # Verificar si se proporcionan argumentos
    if len(sys.argv) > 1:
        ejecutar_con_argumentos()
    else:
        main()