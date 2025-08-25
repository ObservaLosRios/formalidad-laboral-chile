#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar datos JSON para la plantilla HTML de visualización
Convierte los datos de informalidad laboral al formato requerido por la plantilla web
"""

import pandas as pd
import json
from pathlib import Path

def load_and_process_data():
    """Carga y procesa los datos de informalidad laboral"""
    
    # Rutas de archivos
    base_path = Path(__file__).parent.parent
    data_file = base_path / "data_processed" / "etl_tasa_ocupacion_informal_chl14.csv"
    output_file = base_path / "docs" / "data_informalidad.json"
    
    print(f"📂 Cargando datos desde: {data_file}")
    
    # Cargar datos
    df = pd.read_csv(data_file)
    
    # Filtrar datos totales (ambos sexos)
    df_total = df[df['DTI_CL_SEXO'] == '_T'].copy()
    
    # Usar solo proyecciones base 2017 (más actualizadas)
    df_total = df_total[df_total['DTI_CL_INDICADOR'] == 'INF_TOSI_P2017'].copy()
    
    # Limpiar y ordenar por período
    df_total = df_total.drop_duplicates(subset=['Trimestre Móvil']).sort_values('DTI_CL_TRIMESTRE_MOVIL')
    
    print(f"✅ Datos procesados: {len(df_total)} períodos encontrados")
    
    # Convertir a formato para la plantilla HTML
    data_points = []
    for _, row in df_total.iterrows():
        data_points.append({
            "periodo": row['Trimestre Móvil'],
            "valor": round(float(row['Value']), 1)
        })
    
    # Estructura completa para la plantilla
    template_data = {
        "charts": {
            "tasa_informal": {
                "title": "Tasa de ocupación en el sector informal (%)",
                "type": "line",
                "color": "#dc2626",
                "data": data_points
            }
        }
    }
    
    # Guardar como JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Datos guardados en: {output_file}")
    
    # Mostrar preview
    print("\n📊 Preview de los datos:")
    print(f"   • Períodos: {data_points[0]['periodo']} → {data_points[-1]['periodo']}")
    print(f"   • Rango valores: {min(p['valor'] for p in data_points):.1f}% - {max(p['valor'] for p in data_points):.1f}%")
    print(f"   • Promedio: {sum(p['valor'] for p in data_points)/len(data_points):.1f}%")
    
    return template_data

def generate_complete_dashboard():
    """Genera un dashboard completo con múltiples indicadores"""
    
    base_path = Path(__file__).parent.parent
    
    # Archivos de datos
    files = {
        "tasa_informal": "etl_tasa_ocupacion_informal_chl14.csv",
        "ocupados_informales": "etl_ocupados_informales_chl14.csv", 
        "tasa_noagro": "etl_tasa_ocupacion_noagro_chl14.csv"
    }
    
    charts_data = {}
    
    for chart_key, filename in files.items():
        file_path = base_path / "data_processed" / filename
        
        if not file_path.exists():
            print(f"⚠️  Archivo no encontrado: {filename}")
            continue
            
        print(f"📊 Procesando: {filename}")
        
        try:
            df = pd.read_csv(file_path)
            
            # Filtrar datos totales
            df_filtered = df[df['DTI_CL_SEXO'] == '_T'].copy() if 'DTI_CL_SEXO' in df.columns else df.copy()
            
            # Usar proyecciones 2017 si están disponibles
            if 'DTI_CL_INDICADOR' in df_filtered.columns:
                p2017_data = df_filtered[df_filtered['DTI_CL_INDICADOR'].str.contains('P2017', na=False)]
                if not p2017_data.empty:
                    df_filtered = p2017_data.copy()
            
            # Ordenar por período
            df_filtered = df_filtered.drop_duplicates(subset=['Trimestre Móvil']).sort_values('DTI_CL_TRIMESTRE_MOVIL')
            
            # Crear datos para el gráfico
            data_points = []
            for _, row in df_filtered.iterrows():
                data_points.append({
                    "periodo": row['Trimestre Móvil'],
                    "valor": round(float(row['Value']), 1)
                })
            
            # Configuración del gráfico
            chart_config = {
                "title": get_chart_title(chart_key),
                "type": "line",
                "color": get_chart_color(chart_key),
                "data": data_points
            }
            
            charts_data[chart_key] = chart_config
            print(f"   ✅ {len(data_points)} puntos de datos procesados")
            
        except Exception as e:
            print(f"   ❌ Error procesando {filename}: {e}")
    
    # Estructura final
    dashboard_data = {
        "charts": charts_data
    }
    
    # Guardar dashboard completo
    output_file = base_path / "docs" / "dashboard_informalidad.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Dashboard completo guardado en: {output_file}")
    print(f"📊 Gráficos generados: {list(charts_data.keys())}")
    
    return dashboard_data

def get_chart_title(chart_key):
    """Obtiene el título apropiado para cada gráfico"""
    titles = {
        "tasa_informal": "Tasa de ocupación en el sector informal (%)",
        "ocupados_informales": "Ocupados en el sector informal (miles de personas)",
        "tasa_noagro": "Tasa de ocupación no agrícola informal (%)"
    }
    return titles.get(chart_key, chart_key.replace('_', ' ').title())

def get_chart_color(chart_key):
    """Obtiene el color apropiado para cada gráfico"""
    colors = {
        "tasa_informal": "#dc2626",      # Rojo
        "ocupados_informales": "#2563eb", # Azul
        "tasa_noagro": "#059669"         # Verde
    }
    return colors.get(chart_key, "#1B4F72")

if __name__ == "__main__":
    print("🚀 Generando datos para plantilla HTML de informalidad laboral")
    print("=" * 60)
    
    # Generar datos básicos
    basic_data = load_and_process_data()
    
    print("\n" + "=" * 60)
    
    # Generar dashboard completo
    dashboard_data = generate_complete_dashboard()
    
    print("\n✅ Proceso completado!")
    print("\n📝 Instrucciones:")
    print("   1. Abre docs/index.html en tu navegador")
    print("   2. Haz clic en el botón de configuración (⚙️)")
    print("   3. Copia el contenido de data_informalidad.json o dashboard_informalidad.json")
    print("   4. Pégalo en el campo 'Datos JSON' del modal")
    print("   5. Haz clic en 'Aplicar Configuración'")
