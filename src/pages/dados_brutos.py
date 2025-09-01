import streamlit as st
import requests
import pandas as pd
from functions import converte_csv, mensagem_sucesso

st.title('Dados Brutos')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra']
                                         , format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas'
                             , options=list(dados.columns)
                             , default=list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos'
                                      , options=dados['Produto'].unique()
                                      , default=dados['Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço'
                              , min_value=0, max_value=5000
                              , value=(0,5000))
with st.sidebar.expander('Frente da venda'):
    frete = st.slider('Frete'
                      , min_value=0
                      ,max_value=250
                      ,value=(0,250))

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data'
                                , (dados['Data da Compra'].min()
                                , dados['Data da Compra'].max()))
    
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores'
                                , dados['Vendedor'].unique()
                                , dados['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra'
                                  , dados['Local da compra'].unique()
                                  , dados['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra'
                          ,min_value=1
                          ,max_value=5, value = (1,5))
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento'
                                    ,dados['Tipo de pagamento'].unique()
                                    , dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas'
                             ,min_value= 1
                             ,max_value= 24
                             ,value= (1,24))
    
query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo:')
coluna_1, coluna_2 = st.columns(2)
with coluna_1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value = 'dados')
    nome_arquivo += '.csv'
with coluna_2:
    st.download_button('Download em csv'
                       , data = converte_csv(dados_filtrados)
                       , file_name = nome_arquivo
                       , mime = 'text/csv', on_click= mensagem_sucesso)