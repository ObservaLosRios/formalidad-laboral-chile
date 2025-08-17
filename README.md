# 📊 Análisis de Informalidad Laboral - Región de Los Ríos, Chile

Este proyecto presenta un análisis integral de la **informalidad laboral en la Región de Los Ríos**, Chile, utilizando datos oficiales del Instituto Nacional de Estadísticas (INE) para el período 2017-2024.

## 🎯 Objetivo

Desarrollar un pipeline analítico completo que permita:
- Analizar la evolución temporal de la informalidad laboral
- Generar visualizaciones interactivas estilo The Economist en Jupyter
- Proporcionar insights sobre tendencias del mercado laboral regional
- Documentar metodología y hallazgos del análisis

## 📈 Indicadores Principales

El proyecto analiza tres indicadores clave:

1. **Tasa de Ocupación Informal (%)**: Porcentaje de trabajadores en empleos informales
2. **Ocupados Informales (personas)**: Número absoluto de trabajadores informales  
3. **Tasa Informal No Agropecuario (%)**: Informalidad excluyendo sector agrícola

## 🗂️ Estructura del Proyecto

```
formalidad-informalidad-laboral-sector-chile/
│
├── 📁 data/                           # Datos originales del INE
│   ├── INF_NOAGRO_12082025235027711.csv    # Tasa informal no agropecuario
│   ├── INF_OI_12082025234959741.csv        # Ocupados informales
│   └── INF_TOSI_12082025235103516.csv      # Tasa ocupación informal
│
├── 📁 data_clean/                     # Datos procesados y limpios
│   ├── INF_NOAGRO_CHL14_clean.csv         # Datos no agro limpios
│   ├── INF_OI_CHL14_clean.csv             # Datos ocupados limpios
│   └── INF_TOSI_CHL14_clean.csv           # Datos tasa informal limpios
│
├── 📁 data_processed/                 # Datos transformados para análisis
│   ├── etl_ocupados_informales_chl14.csv
│   ├── etl_tasa_ocupacion_informal_chl14.csv
│   ├── etl_tasa_ocupacion_noagro_chl14.csv
│   ├── metadata_pipeline_*.json           # Metadatos del pipeline
│   └── quality_report_chl14*.csv          # Reportes de calidad
│
├── 📁 data_processed_ml/              # Datos preparados para ML
│   ├── diccionario_variables_*.csv        # Diccionario de variables
│   └── resumen_pipeline_*.json            # Resumen del pipeline ML
│
├── 📁 notebooks/                      # Análisis y experimentación
│   ├── pipeline_informalidad.ipynb        # Pipeline principal de análisis
│   └── pipeline_informalidad_01.ipynb     # Backup del notebook
│
├── 📁 scripts/                        # Scripts de procesamiento ETL
│   ├── etl_chl14.py                       # Script ETL principal
│   ├── etl_INF_NOAGRO_CHL14.py           # ETL datos no agropecuario
│   ├── etl_INF_OI_CHL14.py               # ETL ocupados informales
│   └── etl_INF_TOSI_CHL14.py             # ETL tasa ocupación informal
│
├── 📄 README.md                       # Este archivo
└── 📄 requirements.txt                # Dependencias del proyecto
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- Jupyter Notebook

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/SanMabruno/formalidad-informalidad-laboral-sector-chile.git
cd formalidad-informalidad-laboral-sector-chile

# Crear ambiente virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución
```bash
# Ejecutar pipeline de datos (opcional)
python scripts/etl_chl14.py

# Abrir notebook principal de análisis
jupyter notebook notebooks/pipeline_informalidad.ipynb
```

## 📊 Fuentes de Datos

Los datos provienen del **Instituto Nacional de Estadísticas (INE)** de Chile:
- [Informalidad Laboral - INE](https://www.ine.gob.cl/estadisticas/sociales/mercado-laboral/informalidad-laboral)
- **Período**: 2017-2024 (81 trimestres móviles)
- **Cobertura**: Región de Los Ríos (Región XIV)
- **Actualización**: Trimestral

## 🛠️ Tecnologías Utilizadas

### Análisis de Datos
- **Python 3.8+**: Lenguaje principal
- **Pandas**: Manipulación de datos
- **Plotly**: Visualizaciones interactivas
- **Jupyter**: Notebooks de análisis
- **Scikit-learn**: Preprocessing y ML
- **NumPy**: Computación científica
- **Matplotlib/Seaborn**: Gráficos estadísticos

### Herramientas
- **Git**: Control de versiones
- **VS Code**: Editor de código
- **GitHub**: Repositorio remoto

## 📈 Características del Análisis

El notebook principal proporciona:
- ✅ **Pipeline Completo**: Desde datos crudos hasta visualizaciones finales
- ✅ **Visualizaciones Interactivas**: Gráficos estilo The Economist con Plotly
- ✅ **Análisis Temporal**: Evolución de 81 trimestres (2017-2024)
- ✅ **Calidad de Datos**: Reportes automáticos de validación
- ✅ **3 Indicadores Clave**: Métricas principales de informalidad
- ✅ **Documentación**: Explicaciones detalladas de metodología

## 🔄 Pipeline de Datos

1. **Extracción**: Carga datos desde archivos CSV del INE
2. **Limpieza**: Procesamiento y estandarización de formatos
3. **Transformación**: Cálculo de indicadores y métricas derivadas
4. **Análisis**: Exploración estadística y temporal
5. **Visualización**: Generación de gráficos interactivos
6. **Documentación**: Reportes automáticos de calidad y resumen

## 📋 Próximas Mejoras

- [ ] Automatización de descarga de datos desde INE
- [ ] Modelos predictivos de informalidad laboral
- [ ] Comparación con otras regiones de Chile
- [ ] API REST para acceso programático a datos
- [ ] Integración con bases de datos PostgreSQL/SQLite
- [ ] Exportación de reportes en PDF
- [ ] Análisis de series temporales avanzado
- [ ] Dashboard web interactivo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 👥 Autores

- **Bruno San Martín** - *Desarrollo inicial* - [@SanMabruno](https://github.com/SanMabruno)

## 🏛️ Institución

**Universidad Austral de Chile - Centro de Estudios Regionales**
- Facultad de Ciencias Económicas y Administrativas
- Región de Los Ríos, Chile

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

Para consultas sobre el proyecto:
- **Email**: [email@uach.cl](mailto:email@uach.cl)
- **Institución**: Universidad Austral de Chile
- **GitHub**: [SanMabruno](https://github.com/SanMabruno)

---

> **Nota**: Este proyecto forma parte de la investigación en políticas laborales y desarrollo económico regional de la Universidad Austral de Chile.
