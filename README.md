# 📊 Sistema de Informes Financieros para PYMEs Españolas

Sistema profesional para generar informes financieros, económicos y contables de alta calidad para pequeñas y medianas empresas españolas.

## 🎯 Características Principales

- **📈 Análisis Financiero Completo**: Balance de situación, cuenta de resultados, flujo de caja
- **📊 Visualizaciones Profesionales**: Gráficos interactivos y estáticos de alta calidad
- **📉 Ratios Financieros**: Cálculo automático de ratios clave de liquidez, solvencia y rentabilidad
- **📈 Evolución Histórica**: Análisis de tendencias y comparativas temporales
- **🎨 Diseño Ejecutivo**: Formato profesional apto para presentaciones ejecutivas
- **📱 Múltiples Formatos**: Web interactiva, Excel, imágenes de alta calidad

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar o descargar el proyecto
git clone <url-del-repositorio>
cd sistema-informes-financieros

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias Principales

- **pandas**: Análisis y manipulación de datos
- **numpy**: Cálculos numéricos
- **matplotlib**: Gráficos estáticos de alta calidad
- **seaborn**: Visualizaciones estadísticas
- **plotly**: Gráficos interactivos
- **streamlit**: Aplicación web interactiva
- **openpyxl**: Generación de informes Excel

## 📋 Uso del Sistema

### Opción 1: Menú Interactivo

```bash
python main_informe_financiero.py
```

### Opción 2: Línea de Comandos

```bash
# Ejecutar aplicación web
python main_informe_financiero.py --streamlit

# Generar gráficos de alta calidad
python main_informe_financiero.py --graficos

# Generar informe Excel
python main_informe_financiero.py --excel

# Generar informe completo (todos los formatos)
python main_informe_financiero.py --completo

# Mostrar información del sistema
python main_informe_financiero.py --info
```

### Opción 3: Ejecutar Scripts Individuales

```bash
# Aplicación web Streamlit
streamlit run informe_financiero_pyme.py

# Generar gráficos PNG
python generador_informe_pdf.py

# Generar informe Excel
python generador_informe_excel.py
```

## 📊 Funcionalidades

### 1. Aplicación Web Interactiva (Streamlit)

- **Dashboard Dinámico**: Interfaz web interactiva con filtros configurables
- **Visualizaciones Interactivas**: Gráficos que responden a la interacción del usuario
- **Configuración en Tiempo Real**: Cambio de parámetros sin reiniciar
- **Exportación de Datos**: Descarga de gráficos y datos

### 2. Gráficos de Alta Calidad (PNG)

- **Balance de Situación**: Visualización del activo, pasivo y patrimonio neto
- **Cuenta de Resultados**: Gráfico de cascada mostrando la evolución del beneficio
- **Ratios Financieros**: Dashboard con indicadores tipo gauge
- **Evolución Histórica**: Gráficos de líneas con tendencias temporales
- **Flujo de Caja**: Análisis de actividades operativas, inversoras y financieras

### 3. Informe Excel Profesional

- **Resumen Ejecutivo**: Métricas clave con formato profesional
- **Balance de Situación**: Estructura completa con formato contable
- **Cuenta de Resultados**: Análisis detallado de ingresos y gastos
- **Ratios Financieros**: Tablas organizadas por categorías
- **Formato Corporativo**: Colores, fuentes y estilos profesionales

## 📈 Ratios Financieros Incluidos

### Ratios de Liquidez
- **Liquidez Corriente**: Activo corriente / Pasivo corriente
- **Liquidez Inmediata**: (Caja + Clientes) / Pasivo corriente

### Ratios de Solvencia
- **Solvencia**: Activo total / Pasivo total
- **Endeudamiento**: Pasivo total / Activo total

### Ratios de Rentabilidad
- **Margen Bruto**: Beneficio bruto / Ventas
- **Margen Operativo**: Beneficio operativo / Ventas
- **Margen Neto**: Beneficio neto / Ventas
- **ROA**: Beneficio neto / Activo total
- **ROE**: Beneficio neto / Patrimonio neto

### Ratios de Actividad
- **Rotación de Activos**: Ventas / Activo total
- **Rotación de Existencias**: Coste de ventas / Existencias

## 🎨 Personalización

### Configuración de Colores

Los colores corporativos se pueden personalizar en cada script:

```python
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
```

### Datos de la Empresa

Para usar con datos reales, modificar la función `generar_datos_ejemplo()` en cada script:

```python
def generar_datos_ejemplo(self) -> Dict:
    # Reemplazar con datos reales de la empresa
    balance = {
        'activo_corriente': {
            'caja_bancos': 125000,  # Datos reales
            'clientes': 180000,      # Datos reales
            # ... más datos
        }
        # ... resto de datos
    }
```

## 📁 Estructura del Proyecto

```
sistema-informes-financieros/
├── main_informe_financiero.py      # Script principal
├── informe_financiero_pyme.py      # Aplicación web Streamlit
├── generador_informe_pdf.py        # Generador de gráficos PNG
├── generador_informe_excel.py      # Generador de informes Excel
├── requirements.txt                 # Dependencias
├── README.md                       # Documentación
└── archivos_generados/             # Carpeta de salida (se crea automáticamente)
    ├── *.png                       # Gráficos de alta calidad
    └── *.xlsx                      # Informes Excel
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Configurar empresa por defecto
export EMPRESA_NOMBRE="Mi Empresa S.L."
export ANO_ANALISIS="2024"

# Configurar puerto de Streamlit
export STREAMLIT_SERVER_PORT="8501"
```

### Personalización de Estilos

Los estilos se pueden personalizar modificando las funciones `setup_estilos()` en cada script:

```python
def setup_estilos(self):
    # Configurar fuentes
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10
    
    # Configurar colores
    self.colores = {
        # Personalizar colores aquí
    }
```

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis Rápido

```bash
# Generar informe completo rápidamente
python main_informe_financiero.py --completo
```

### Ejemplo 2: Presentación Ejecutiva

```bash
# Generar gráficos para presentación
python main_informe_financiero.py --graficos
# Los archivos PNG se pueden usar en PowerPoint
```

### Ejemplo 3: Análisis Interactivo

```bash
# Abrir aplicación web para análisis detallado
python main_informe_financiero.py --streamlit
```

## 🎯 Casos de Uso

### Para Directores Financieros
- **Análisis de Ratios**: Evaluación rápida de la salud financiera
- **Comparativas Temporales**: Seguimiento de tendencias
- **Presentaciones Ejecutivas**: Gráficos profesionales para juntas

### Para Contadores
- **Informes Estándar**: Formato contable profesional
- **Análisis Detallado**: Desglose completo de cuentas
- **Exportación Excel**: Compatibilidad con sistemas existentes

### Para Consultores
- **Análisis Comparativo**: Benchmarking con estándares del sector
- **Recomendaciones**: Identificación de áreas de mejora
- **Documentación Profesional**: Informes listos para clientes

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error de Streamlit**:
   ```bash
   pip install streamlit --upgrade
   ```

2. **Error de Matplotlib**:
   ```bash
   pip install matplotlib --upgrade
   ```

3. **Error de OpenPyXL**:
   ```bash
   pip install openpyxl --upgrade
   ```

### Verificación de Instalación

```bash
# Verificar que todas las dependencias están instaladas
python -c "import pandas, numpy, matplotlib, seaborn, plotly, streamlit, openpyxl; print('✅ Todas las dependencias están instaladas')"
```

## 📈 Próximas Funcionalidades

- [ ] **Análisis Sectorial**: Comparativas con empresas del mismo sector
- [ ] **Proyecciones**: Análisis predictivo y forecasting
- [ ] **Alertas**: Notificaciones de ratios fuera de rango
- [ ] **API REST**: Integración con sistemas externos
- [ ] **Múltiples Monedas**: Soporte para diferentes divisas
- [ ] **Auditoría**: Trazabilidad de cambios en datos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:

- 📧 Email: soporte@ejemplo.com
- 📱 Teléfono: +34 900 123 456
- 🌐 Web: https://ejemplo.com/soporte

## 🙏 Agradecimientos

- **Pandas**: Por el excelente framework de análisis de datos
- **Matplotlib**: Por las capacidades de visualización
- **Streamlit**: Por la facilidad de crear aplicaciones web
- **Plotly**: Por los gráficos interactivos de alta calidad

---

**Desarrollado con ❤️ para PYMEs españolas**

*Última actualización: Diciembre 2024*