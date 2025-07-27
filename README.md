# 📊 Sistema de Informes Financieros para PYMES Españolas

## 🎯 Descripción General

Este sistema genera informes financieros ejecutivos de alta calidad profesional para Pequeñas y Medianas Empresas (PYMES) españolas. La aplicación proporciona análisis financiero integral, visualizaciones interactivas y proyecciones estratégicas.

## ✨ Características Principales

### 📈 Análisis Integral
- **Resumen Ejecutivo**: Métricas clave y puntos destacados
- **Análisis Financiero**: Estructura detallada de ingresos y gastos
- **Cuenta de Resultados**: Estado comparativo multi-anual
- **Balance de Situación**: Análisis patrimonial completo
- **Ratios y KPIs**: Indicadores financieros con benchmarking sectorial
- **Análisis Temporal**: Tendencias y evolución histórica
- **Proyecciones**: Escenarios futuros (pesimista, base, optimista)
- **Conclusiones**: Análisis DAFO y recomendaciones estratégicas

### 🎨 Características Visuales
- **Interfaz moderna**: Diseño profesional con gradientes y colores corporativos
- **Gráficos interactivos**: Utilizando Plotly para visualizaciones dinámicas
- **Dashboard intuitivo**: Navegación clara y organizada
- **Responsive design**: Adaptado para diferentes dispositivos
- **Métricas destacadas**: Cards visuales para KPIs principales

### 📊 Tipos de Análisis
- **Análisis de liquidez**: Ratios corriente, ácida e inmediata
- **Análisis de solvencia**: Endeudamiento y autonomía financiera
- **Análisis de rentabilidad**: ROE, ROA y márgenes
- **Análisis temporal**: Tendencias, CAGR y volatilidad
- **Benchmarking sectorial**: Comparación con estándares del sector
- **Proyecciones financieras**: Escenarios a 5 años

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone <repository-url>
cd financial-report-system
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
streamlit run informe_financiero_pyme.py
```

4. **Abrir en el navegador**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📋 Estructura del Proyecto

```
├── informe_financiero_pyme.py   # Aplicación principal
├── asistente_noticias.py        # Aplicación auxiliar de noticias
├── requirements.txt             # Dependencias Python
└── README.md                   # Este archivo
```

## 🏢 Datos de Ejemplo

La aplicación incluye datos simulados realistas de una PYME española:

- **Empresa**: TechSolutions Innovación S.L.
- **Sector**: Tecnología y Servicios Digitales
- **Ubicación**: Madrid, España
- **Empleados**: 45
- **Facturación**: €2.5M+ (crecimiento sostenido)
- **Historial**: 5 años de datos financieros

## 📊 Secciones del Informe

### 1. 🎯 Resumen Ejecutivo
- Métricas principales (facturación, beneficio, patrimonio, liquidez)
- Gráfico de evolución financiera
- Puntos clave del ejercicio

### 2. 💰 Análisis Financiero
- Estructura de ingresos por tipo
- Distribución de gastos operativos
- Evolución mensual detallada
- Tabla de datos mensuales

### 3. 🧮 Cuenta de Resultados
- Estado comparativo multi-anual
- Gráfico de cascada (waterfall)
- Análisis de márgenes (bruto, operativo, neto)

### 4. 🏦 Balance de Situación
- Estructura del activo y pasivo
- Gráficos de composición patrimonial
- Análisis de equilibrio financiero

### 5. 📊 Ratios y KPIs
- Ratios de liquidez, endeudamiento y rentabilidad
- Evolución temporal de ratios clave
- Benchmarking sectorial con calificaciones

### 6. ⏰ Análisis Temporal
- Evolución de magnitudes principales
- Tasas de crecimiento anuales
- Análisis de tendencias y volatilidad
- CAGR (Tasa de Crecimiento Anual Compuesta)

### 7. 🔮 Proyecciones
- Configuración de escenarios interactivos
- Proyecciones a 5 años
- Análisis de sensibilidad
- Evaluación de probabilidades

### 8. 📝 Conclusiones
- Análisis DAFO financiero
- Resumen de KPIs críticos
- Recomendaciones estratégicas por plazos
- Plan de acción prioritario
- Calificación global de la empresa

## 🎨 Personalización

### Modificar Datos de la Empresa
Para adaptar el sistema a una empresa real, modifica la función `generate_sample_data()` en la clase `FinancialReportGenerator`:

```python
company_info = {
    'nombre': 'Tu Empresa S.L.',
    'cif': 'B12345678',
    'sector': 'Tu Sector',
    'ubicacion': 'Tu Ciudad, España',
    'empleados': 25,
    'año_constitucion': 2020,
    'forma_juridica': 'Sociedad de Responsabilidad Limitada'
}
```

### Configurar Datos Financieros
Ajusta los datos financieros en el mismo método modificando:
- Facturación base (`base_revenue`)
- Tasas de crecimiento (`growth_rates`)
- Ratios financieros (márgenes, estructura patrimonial)

### Personalizar Apariencia
Modifica el CSS en la sección de estilos para cambiar:
- Colores corporativos
- Fuentes y tamaños
- Espaciado y diseño
- Gradientes y efectos visuales

## 🔧 Tecnologías Utilizadas

- **Streamlit**: Framework web para aplicaciones de datos
- **Plotly**: Gráficos interactivos avanzados
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Computación numérica
- **SciPy**: Análisis estadístico y regresiones
- **Matplotlib/Seaborn**: Visualizaciones adicionales
- **ReportLab**: Generación de PDFs (preparado para futuras funciones)

## 📈 Funcionalidades Avanzadas

### Análisis Estadístico
- Regresión lineal para tendencias
- Coeficientes de variación para volatilidad
- Correlaciones y análisis de estabilidad

### Benchmarking Inteligente
- Comparación automática con estándares sectoriales
- Calificaciones por colores según rendimiento
- Evaluación multi-criterio

### Proyecciones Interactivas
- Sliders para ajustar parámetros
- Escenarios múltiples en tiempo real
- Análisis de sensibilidad automático

## 🎯 Casos de Uso

### Para Empresarios y Gerentes
- Análisis de rendimiento empresarial
- Identificación de fortalezas y debilidades
- Planificación estratégica
- Preparación para inversores

### Para Asesores Financieros
- Análisis integral de clientes PYME
- Informes profesionales para presentaciones
- Benchmarking sectorial
- Recomendaciones estratégicas

### Para Inversores
- Due diligence financiera
- Evaluación de oportunidades de inversión
- Análisis de riesgo y rentabilidad
- Proyecciones futuras

## 🔮 Roadmap Futuro

### Próximas Funcionalidades
- [ ] Exportación a PDF automática
- [ ] Conexión con APIs de datos reales
- [ ] Análisis de cash flow
- [ ] Comparación con competidores
- [ ] Alertas automáticas de KPIs
- [ ] Integración con sistemas contables

### Mejoras Planificadas
- [ ] Análisis de riesgo crediticio
- [ ] Predicción con Machine Learning
- [ ] Dashboard en tiempo real
- [ ] Versión móvil nativa
- [ ] Multi-idioma (inglés, francés)

## 📞 Soporte y Contribuciones

Para soporte técnico, sugerencias o contribuciones al proyecto:

1. **Issues**: Reportar problemas o solicitar funcionalidades
2. **Pull Requests**: Contribuir con mejoras al código
3. **Documentación**: Ayudar a mejorar la documentación

## 📄 Licencia

Este proyecto está desarrollado para fines demostrativos y educativos. Los datos utilizados son simulados y no representan empresas reales.

---

**⚠️ Importante**: Este sistema utiliza datos simulados para demostración. Para uso en producción, debe integrarse con fuentes de datos reales y validarse por profesionales financieros.

**🎯 Objetivo**: Proporcionar una herramienta profesional para el análisis financiero de PYMEs españolas con capacidades de reporting ejecutivo de alta calidad.