# ETL para Región de Los Ríos (CHL14) - INF_TOSI
# Filtra y limpia solo datos de CHL14
import pandas as pd
input_path = 'data/INF_TOSI_12082025235103516.csv'
output_path = 'data_clean/INF_TOSI_CHL14_clean.csv'
df = pd.read_csv(input_path)
df_clean = df[df['DTI_CL_REGION'] == 'CHL14']
df_clean.to_csv(output_path, index=False)
+


