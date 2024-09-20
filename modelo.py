import json
import re
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import unicodedata

def carregar_dados(caminho_arquivo_json):
    with open(caminho_arquivo_json, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados


def limpar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join([c for c in texto_normalizado if not unicodedata.combining(c)])
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s:;]', '', texto_sem_acento)
    texto_limpo = texto_limpo.lower()
    return texto_limpo

caminho_arquivo_json = "tabela_evolucao_nova.json"
dados = carregar_dados(caminho_arquivo_json)

print("Tipo de dados carregados:", type(dados))
print("Exemplo de dados carregados:", dados[:2]) 

dados_df = pd.DataFrame(dados)

dados_df['EVOLUCAO'] = dados_df['EVOLUCAO'].apply(limpar_texto)
dados_df['DS_CID'] = dados_df['DS_CID'].apply(limpar_texto)
dados_df['CIRURGIA'] = dados_df['CIRURGIA'].apply(limpar_texto)

# Substituir strings vazias por NaN
dados_df.replace('', np.nan, inplace=True)

print("Tipo após conversão:", type(dados_df))
print("Estrutura do DataFrame:")

# Convertendo as colunas de datas para o formato de data
dados_df['DATA_EVOLUCAO'] = pd.to_datetime(dados_df['DATA_EVOLUCAO'], errors='coerce')
dados_df['DATA_AVISO_CIRURGIA'] = pd.to_datetime(dados_df['DATA_AVISO_CIRURGIA'], errors='coerce')
dados_df['DATA_OBITO'] = pd.to_datetime(dados_df['DATA_OBITO'], errors='coerce')

# Criar DataFrame para as evoluções
evolucao_df = dados_df[['CD_PRE_MED', 'CD_PACIENTE', 'IDADE_PACIENTE', 'DATA_EVOLUCAO', 'DS_CID', 'EVOLUCAO', 
                        'OBITO', 'SEXO_F', 'SEXO_M']].copy()
evolucao_df['TIPO_EVENTO'] = 'EVOLUCAO'
evolucao_df['DATA_EVENTO'] = evolucao_df['DATA_EVOLUCAO']
evolucao_df = evolucao_df.drop(columns=['DATA_EVOLUCAO'])  # Remove a coluna original de DATA_EVOLUCAO

# Criar DataFrame para as cirurgias
cirurgia_df = dados_df[['CD_PRE_MED', 'CD_PACIENTE', 'IDADE_PACIENTE', 'DATA_AVISO_CIRURGIA', 'DS_CID', 'CIRURGIA', 
                        'CLASSIFICACAO_ASA', 'TIPO_CIRURGIA', 'INDICADOR_CIRURGIA', 'OBITO', 'SEXO_F', 'SEXO_M']].copy()
cirurgia_df['TIPO_EVENTO'] = 'CIRURGIA'
cirurgia_df['DATA_EVENTO'] = cirurgia_df['DATA_AVISO_CIRURGIA']
cirurgia_df = cirurgia_df.drop(columns=['DATA_AVISO_CIRURGIA'])  # Remove a coluna original de DATA_AVISO_CIRURGIA

# Criar DataFrame para os óbitos
obito_df = dados_df[['CD_PRE_MED', 'CD_PACIENTE', 'IDADE_PACIENTE', 'DATA_OBITO', 'DS_CID', 'OBITO', 
                     'SEXO_F', 'SEXO_M']].copy()
obito_df['TIPO_EVENTO'] = 'OBITO'
obito_df['DATA_EVENTO'] = obito_df['DATA_OBITO']
obito_df = obito_df.drop(columns=['DATA_OBITO'])  # Remove a coluna original de DATA_OBITO

# Concatenando os três DataFrames (Evolução, Cirurgia e Óbito) em um só
dados_reestruturados = pd.concat([evolucao_df, cirurgia_df, obito_df], ignore_index=True)

# Excluindo linhas onde DATA_EVENTO é NaT, se for o caso
dados_reestruturados = dados_reestruturados.dropna(subset=['DATA_EVENTO'])

# Reorganizando as colunas para uma melhor visualização
dados_reestruturados = dados_reestruturados[['CD_PRE_MED', 'CD_PACIENTE', 'IDADE_PACIENTE', 'DATA_EVENTO', 'TIPO_EVENTO',
                                             'DS_CID', 'EVOLUCAO', 'CIRURGIA', 'CLASSIFICACAO_ASA', 'TIPO_CIRURGIA', 
                                             'INDICADOR_CIRURGIA', 'OBITO', 'SEXO_F', 'SEXO_M']]


