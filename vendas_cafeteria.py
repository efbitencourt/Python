# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:06:14 2024

@author: efbitencourt
"""
#%%
import pandas as pd # manipulação de dados em formato de dataframe
import numpy as np # operações matemáticas
import seaborn as sns # visualização gráfica
import matplotlib.pyplot as plt # visualização gráfica

#%%
df_cafe = pd.read_csv('index.csv')
df_cafe.info()
df_cafe.iloc[:,[4,5]] #selecionando todas as linhas com as duas últimas colunas
df_cafe.query('coffee_name == "Latte"')
teste = df_cafe.groupby(df_cafe.cash_type)[['coffee_name']])
valor = df_cafe.groupby(df_cafe['coffee_name']).money.sum() #valor vendido por tipo de bebida
preco_medio = df_cafe.groupby(df_cafe['coffee_name']).money.mean() # preço médio de cada bebida
total_vendas = df_cafe['coffee_name'].value_counts()

pd.to_datetime(df_cafe['datetime'])

#%% Aqui o objetivo é verificar quais produtos são mais rentáveis (vende mais e com ticket médio maior)
# e se vale a pena abrir mão de algum produto no catálogo 

# transformando os dados de preço médio e total de vendas em dataframe e unificando em um outro dataframe
df_preco_medio = pd.DataFrame(preco_medio)
df_total_vendas = pd.DataFrame(total_vendas)
df_vendas_tm = df_preco_medio.merge(df_total_vendas, on='coffee_name')
df_vendas_tm

df_vendas_tm['índice'] = np.array([1,2,3,4,5,6,7,8])
df_vendas_tm = df_vendas_tm.reset_index().set_index('índice', append=True)

# Plotando o gráfico
plt.figure(figsize=(10, 6))
plt.scatter(df_vendas_tm["money"], df_vendas_tm["count"], color='blue', s=100)

# Adicionando rótulos aos pontos
for i, name in enumerate(df_vendas_tm["coffee_name"]):
    plt.text(df_vendas_tm["money"][i], df_vendas_tm["count"][i], name, fontsize=9, ha='right')

# Configurações do gráfico
plt.xlabel('Preço médio')
plt.ylabel('Total de vendas')
plt.title('Ticket Médio e total de vendas para cada tipo de café')
plt.grid(True)
plt.show()

# os dados indicam que é possível descartar o expresso das opções, pois é a bebida com menor volume de vendas e menor preço médio

#%%
# É possível reforçar a hipótese criando um indicador que multiplica o preço pelo número de vendas
df_vendas_tm['Rentabilidade do produto'] = df_vendas_tm['money'] * df_vendas_tm['count']

# Criando um indicador de vendas/preço
df_vendas_tm['Preço por venda'] = df_vendas_tm['money'] / df_vendas_tm['count']

# Refinando a nomeclatura das colunas da tabela
df_vendas_tm = df_vendas_tm.rename(columns={'money':'preço medio','count':'total de vendas','coffee_name':'produto'})

#%% Análise da evolução temporal do número de vendas por tipo de produto

#gerando tabela com número de vendas por dia e por produto
vendas_por_dia = df_cafe.groupby(['date'])['coffee_name'].value_counts()

#transofrmando em dataframe e ajustando
df_vendas_por_dia = pd.DataFrame(vendas_por_dia)
df_vendas_por_dia = df_vendas_por_dia.rename(columns={'count':'vendas'})
df_vendas_por_dia = df_vendas_por_dia.reset_index()
