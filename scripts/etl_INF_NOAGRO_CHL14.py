# ETL para Región de Los Ríos (CHL14) - INF_NOAGRO
# Filtra y limpia solo datos de CHL14
import pandas as pd
input_path = 'data/INF_NOAGRO_12082025235027711.csv'
output_path = 'data_clean/INF_NOAGRO_CHL14_clean.csv'
df = pd.read_csv(input_path)
df_clean = df[df['DTI_CL_REGION'] == 'CHL14']
df_clean.to_csv(output_path, index=False)
