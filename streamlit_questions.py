import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
import geopandas
from PIL import Image

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

@st.cache(allow_output_mutation=True)
def get_image(path2):
    imag1 = Image.open(path2)

    return imag1

def data_groupby(data, grou):
    cou = data[[grou[0], grou[1]]].groupby(grou[0]).median().reset_index()

    return cou

def data_merge(data, df, mer):
    merg = pd.merge(data, df, on=mer, how='inner')

    return merg

def data_rename(data, cols, ren):
    df = data.rename({cols[0]: ren[0], cols[1]: ren[1]}, axis='columns')

    return df

def data_reset():
    data = pd.read_csv('kc_house_data.csv')

    return data

def data_aprimorate(data):

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    for i in range(len(data)):
        if (data.loc[i, 'bathrooms'] > 0) & (data.loc[i, 'bathrooms'] < 1):
            data.loc[i, 'bathrooms'] = 1

        elif (data.loc[i, 'bathrooms'] > 1) & (data.loc[i, 'bathrooms'] < 2):
            data.loc[i, 'bathrooms'] = 2

        elif (data.loc[i, 'bathrooms'] > 2) & (data.loc[i, 'bathrooms'] < 3):
            data.loc[i, 'bathrooms'] = 3

        elif (data.loc[i, 'bathrooms'] > 3) & (data.loc[i, 'bathrooms'] < 4):
            data.loc[i, 'bathrooms'] = 4

        elif (data.loc[i, 'bathrooms'] > 4) & (data.loc[i, 'bathrooms'] < 5):
            data.loc[i, 'bathrooms'] = 5

        elif (data.loc[i, 'bathrooms'] > 5) & (data.loc[i, 'bathrooms'] < 6):
            data.loc[i, 'bathrooms'] = 6

        elif (data.loc[i, 'bathrooms'] > 6) & (data.loc[i, 'bathrooms'] < 7):
            data.loc[i, 'bathrooms'] = 7

        elif (data.loc[i, 'bathrooms'] > 7) & (data.loc[i, 'bathrooms'] < 8):
            data.loc[i, 'bathrooms'] = 8

    for i in range(len(data)):
        if (data.loc[i, 'waterfront'] == 0):
            data.loc[i, 'waterfront'] = 'no'

        elif (data.loc[i, 'waterfront'] == 1):
            data.loc[i, 'waterfront'] = 'yes'

    for i in range(len(data)):
        if (data.loc[i, 'floors'] > 1) & (data.loc[i, 'floors'] < 2):
            data.loc[i, 'floors'] = 2

        elif (data.loc[i, 'floors'] > 2) & (data.loc[i, 'floors'] < 3):
            data.loc[i, 'floors'] = 3

        elif (data.loc[i, 'floors'] > 3) & (data.loc[i, 'floors'] < 4):
            data.loc[i, 'floors'] = 4

    grou = ['zipcode', 'price']

    df = data_groupby(data, grou)

    grou = ['zipcode', 'sqft_lot']

    df1 = data_groupby(data, grou)

    df2 = data_merge(data, df, 'zipcode')

    df2 = data_merge(df2, df1, 'zipcode')

    cols = ['price_y', 'price_x']
    ren = ['price_median', 'price']

    df2 = data_rename(df2, cols, ren)

    cols = ['sqft_lot_x', 'sqft_lot_y']
    ren = ['sqft_lot', 'lot_median']

    df2 = data_rename(df2, cols, ren)

    for i in range(len(df2)):
        if (df2.loc[i, 'price'] < df2.loc[i, 'price_median']) & (df2.loc[i, 'condition'] >= 3) & (df2.loc[i, 'bedrooms'] >= 2) & (df2.loc[i, 'bathrooms'] >= 2):
            df2.loc[i, 'status'] = 'good offer'

            if (df2.loc[i, 'sqft_lot'] > df2.loc[i, 'lot_median']) & (df2.loc[i, 'sqft_basement'] > 0):
                df2.loc[i, 'status'] = 'great offer'

                if (df2.loc[i, 'floors'] >= 2):
                    df2.loc[i, 'status'] = 'excellent offer'

        else:
            df2.loc[i, 'status'] = 'bad offer'

    for i in range(len(df2)):

        if (df2.loc[i, 'date'] >= '2014-06-01') & (df2.loc[i, 'date'] <= '2014-08-31'):
            df2.loc[i, 'seasons'] = 'summer'

        elif (df2.loc[i, 'date'] >= '2014-09-01') & (df2.loc[i, 'date'] <= '2014-11-30'):
            df2.loc[i, 'seasons'] = 'autumn'

        elif (df2.loc[i, 'date'] >= '2014-03-01') & (df2.loc[i, 'date'] <= '2014-05-31'):
            df2.loc[i, 'seasons'] = 'spring'

        else:
            df2.loc[i, 'seasons'] = 'winter'

    cols = ['seasons', 'price']

    kc = data_groupby(df2, cols)

    df = data_merge(df2, kc, 'seasons')

    cols = ['price_x', 'price_y']
    ren = ['price', 'season_median']

    df2 = data_rename(df, cols, ren)

    for i in range(len(df)):

        if (df2.loc[i, 'status'] == 'good offer'):
            df2.loc[i, 'exchange_upgrade'] = '+20%'

        elif (df2.loc[i, 'status'] == 'great offer'):
            df2.loc[i, 'exchange_upgrade'] = '+30%'

        elif (df2.loc[i, 'status'] == 'excellent offer'):
            df2.loc[i, 'exchange_upgrade'] = '+40%'

        else:
            df2.loc[i, 'exchange_upgrade'] = '10% or less'

    return df2

def premises_plan(imag1):
    st.title('1. Premissas e Planejamento da Solução:')

    st.image(imag1, caption='Criado Por Valcílio Silva')

    st.subheader('1.1. Premissas:')

    st.write('Esse projeto tem como premissa ajudar a empresa "House Sales in King County, USA", '
             'a detectar boas oportunidades de compra de casas para depois poder '
             'revender por um preço maior e assim obter um lucro maior graças a isso.')
    st.write('A House Rocket solicitou duas perguntas principais:')
    st.write('1. Quais imóveis comprar e por quanto vender?')
    st.write('2. Qual o melhor momento para a venda desses imóveis?')
    st.write('Desse modo, esse projeto possui como premissas ser capaz de responder essas questões,'
             'e também produzir outros insights relevantes que possam ser capazes de causar impactos '
             'reais na tomada de decisão e consequentemente no negócio em si.')

    st.subheader('1.2. Planejamento da Solução:')

    st.write('O planejamento pode ser dito como dividido em 4 partes: boas oportunidades de compra,'
             'aumento no preço para poder vender, melhor momento para revenda e hipóteses a '
             'serem validadas ou desvalidadas. Desse modo, segue abaixo o detalhamento de cada uma delas:')

    st.write('Oportunidades de compra > nesse ponto foi realizado a análise em ordem crescente considerando os seguintes aspectos: tamanho, preço, andares, vista para a água, quantidade de quartos e de banheiros. Todos esses aspectos em ordem crescente, ou seja, quanto mais desses aspectos forem cumprindo (ex.: 2 banheiros, 2 quartos, preço abaixo da mediana e etc...), melhor será a classificação das casas, considerando essa ordem da pior classificação até a melhor: Bad > Good > Great > Excellent')

    st.write('Aumento no preço das casas para revendas > foi realizado de acordo com um estudo do preço médio das casas'
             ' com essas condicionais e de suas ofertas.')

    st.write('Melhor momento para revenda > foi realizado de acordo com uma análise do preço médio nas'
             ' temporadas do ano encontrando assim qual seria o momento mais ideal.')

    st.write('Foram tomadas 10 hipóteses que foram validadas ou desvalidadas no decorrer desse projeto:')
    st.write('H1 - O preço das casas com condição 3 a 4 com relação as casas com condição 1 é cerca de 41% maior.')
    st.write('H2 - O preço das casas com 2 a 4 quartos com relação a casas sem quartos é cerca de 38,27%.')
    st.write('H3 - O preço das casas com 2 a 4 banheiros com relação a casas sem banheiro é igual ou maior que 49,30%.')
    st.write('H4 - O preço das casas com 2 andares em relação a casas com apenas 1 andar é igual ou maior do que 26,10%.')
    st.write('H5 - As casas com vista para água possuem um preço 67,86% maior do que casas sem vista para água.')
    st.write('H6 - As melhores oportunidades se encontram em maioria no sul de Seattle.')
    st.write('H7: O norte possui as casas de maiores preços.')
    st.write('H8 - O crescimento anual do preço das casas é cerca de 5%.')
    st.write('H9 - O crescimento mensal do preço das casas possui uma certa linearidade, sempre mantendo uma estabilidade de preços.')
    st.write('H10 - As casas anteriores a 1960 possuem um preço médio menor.')

    return None

def data_quest(df2):

    f_status = st.sidebar.multiselect('Filtre Pelo Status:', df2['status'].unique())

    st.title('2. Questões de Negócio:')

    if (f_status != []):
        df2 = df2.loc[df2['status'].isin(f_status)]

    else:
        df2 = df2.copy()

    st.subheader('2.1. Quais imóveis comprar e por quanto vender: (Filtro Do Lado)')
    df1 = df2.copy()
    st.dataframe(df1[['id', 'price', 'date', 'price_median', 'condition', 'bedrooms', 'bathrooms', 'sqft_lot',
                      'lot_median', 'sqft_basement',
                      'floors', 'status', 'exchange_upgrade']].sort_values('price', ascending=True),
                 height=600)

    st.write('A tabela em questão foi construída levando em consideração todos os dados da base de dados para detectar as melhores ofertas e rankeá-las adequandamente '
             'desse modo a abaixo:')
    st.write('1. bad offer: as piores ofertas com preços superavaliados e que caso revendidos, mesmo que na melhor época, daria pouco lucro. (cerca de 10% a mais)')
    st.write('2. good offer: ofertas subavaliadas que podem rendar um bom lucro devido ao baixo preço de aquisição. (cerca de 20% a mais)')
    st.write('3. great offer: ofertas subavalidas com mais quartos e banheiros e que podem render um ótimo lucro. (cerca de 30% a mais)')
    st.write('4. excellent offer: indicações de imóveis subavaliados com todos os benefícios dos outros e mais de um andar, podem render um excelente lucro. (cerca de 40% a mais)')
    st.write('')
    st.write('Todos esses aumentos no preço para revenda, foram feitos calculados com base neles serem vendidos na época certa (época indicada na próxima parte)')

    st.subheader('2.2. Melhor Momento Para Venda:')

    df2 = data_reset()

    df2['date'] = pd.to_datetime(df2['date']).dt.strftime('%Y-%m-%d')

    for i in range(len(df2)):

        if (df2.loc[i, 'date'] >= '2014-06-01') & (df2.loc[i, 'date'] <= '2014-08-31'):
            df2.loc[i, 'seasons'] = 'summer'

        elif (df2.loc[i, 'date'] >= '2014-09-01') & (df2.loc[i, 'date'] <= '2014-11-30'):
            df2.loc[i, 'seasons'] = 'autumn'

        elif (df2.loc[i, 'date'] >= '2014-03-01') & (df2.loc[i, 'date'] <= '2014-05-31'):
            df2.loc[i, 'seasons'] = 'spring'

        else:
            df2.loc[i, 'seasons'] = 'winter'

    cols = ['seasons', 'price']
    kc = data_groupby(df2, cols)
    st.dataframe(kc)
    st.write('O melhor momento para a venda é na primavera, pois, como demonstra a tabela, nessa época '
             'há um aumento no preço das casas em cerca de 4% as outras seasons.')

    return None

def data_analysis(df2):
    st.title('3. Insights Obtidos:')

    c1, c2 = st.beta_columns((1, 1))
    c3, c4 = st.beta_columns((1, 1))

    df2 = df2.copy()

    cols = ['zipcode', 'sqft_basement']

    dm1 = data_groupby(df2, cols)

    df1 = data_merge(df2, dm1, 'zipcode')

    cols = ['sqft_basement_x', 'sqft_basement_y']

    ren = ['sqft_basement', 'basement_median']

    df1 = data_rename(df1, cols, ren)

    cols = ['condition', 'price']

    dg1 = data_groupby(df1, cols)

    #percentage1 = (dg1.iloc[0, 1] / dg1.iloc[2, 1]) - 1
    #percentage2 = (dg1.iloc[0, 1] / dg1.iloc[3, 1]) - 1

    #percentage = -(percentage1 + percentage2) / 2

    #p1 = percentage * 100

    cols = ['bedrooms', 'price']

    dg2 = data_groupby(df1, cols)

    #percentage1 = (dg2.iloc[0, 1] / dg2.iloc[2, 1]) - 1
    #percentage2 = (dg2.iloc[0, 1] / dg2.iloc[5, 1]) - 1

    #percentage1 * 100, percentage2 * 100

    #percentage = -(percentage1 + percentage2) / 2

    #p2 = percentage * 100

    cols = ['bathrooms', 'price']

    dg3 = data_groupby(df1, cols)

    #percentage1 = (dg3.iloc[0, 1] / dg3.iloc[2, 1]) - 1
    #percentage2 = (dg3.iloc[0, 1] / dg3.iloc[5, 1]) - 1

    #percentage1 * 100, percentage2 * 100

    #percentage = -(percentage1 + percentage2) / 2

    #p3 = percentage * 100

    cols = ['floors', 'price']

    dg4 = data_groupby(df1, cols)

    #percentage1 = (dg4.iloc[0, 1] / dg4.iloc[2, 1]) - 1

    #p4 = -(percentage1 * 100)

    cols = ['waterfront', 'price']

    dg5 = data_groupby(df1, cols)

    #percentage1 = (dg5.iloc[0, 1] / dg5.iloc[1, 1]) - 1

    #p5 = -(percentage1 * 100)

    c1.subheader('H1 - O preço das casas com condição 3 a 4 com relação as casas '
                 'com condição 1 é cerca de 41% maior.(Verdadeira)')

    # data plot

    cols = ['condition', 'price']
    ren = ['Condition', 'Price Median']
    dg1 = data_rename(dg1, cols, ren)

    fig = px.bar(dg1.head(4), x='Condition', y='Price Median', color='Price Median', title='Median Prices Per Condition')
    c1.plotly_chart(fig)

    c1.write('O gráfico acima demonstra que as casas com condições de 3 a 4 possuem um preço cerca '
             'de 41% maior do que as casas com condições 1.')

    c2.subheader('H2 - O preço das casas com 2 a 4 quartos com relação '
                 'a casas sem quartos é cerca de 38,27%. (Verdadeira)')

    cols = ['bedrooms', 'price']
    ren = ['Bedrooms', 'Price Median']
    dg2 = data_rename(dg2, cols, ren)

    fig = px.bar(dg2.head(5), x='Bedrooms', y='Price Median', color='Price Median',
                 title='Median Prices Per Bedrooms')
    c2.plotly_chart(fig)

    c2.write('O gráfico acima demonstra que as casas com 2 a 4 quartos possuem um preço cerca de 38,27% maior do que as casas sem quartos.')

    c3.subheader('H3 - O preço das casas com 2 a 4 banheiros com relação a casas sem banheiro é igual ou maior que 49,30%.(Verdadeira)')

    cols = ['bathrooms', 'price']
    ren = ['Bathrooms', 'Price Median']
    dg3 = data_rename(dg3, cols, ren)
    fig = px.bar(dg3.head(6), x='Bathrooms', y='Price Median', color='Price Median',
                 title='Median Prices Per Bathrooms')
    c3.plotly_chart(fig)
    c3.write('O gráfico acima demonstra que as casas com 2 a 4 banheiros possuem um preço cerca de 26,10% maior do que as casas com 1 nenhum banheiro.')

    c4.subheader('H4 - O preço das casas com 2 andares em relação a casas com apenas 1 andar é igual ou maior do que 26,10%. (Verdadeira)')
    cols = ['floors', 'price']
    ren = ['Floors', 'Price Median']
    dg4 = data_rename(dg4, cols, ren)
    fig = px.bar(dg4.head(2), x='Floors', y='Price Median', color='Price Median',
                 title='Median Prices Per Floors')
    c4.plotly_chart(fig)
    c4.write('O gráfico acima demonstra que as casas com 2 andares possuem um preço cerca de 26,10% maior do que as casas com 1 andar.')

    st.subheader('H5 - As casas com vista para água possuem um preço 67,86% maior do que casas sem vista para água. (Verdadeira)')
    cols = ['waterfront', 'price']
    ren = ['Waterfront', 'Price Median']
    dg5 = data_rename(dg5, cols, ren)
    fig = px.bar(dg5, x='Waterfront', y='Price Median', color='Price Median',
                 title='Median Prices Per Waterfront')
    st.plotly_chart(fig)
    st.write('O gráfico acima demonstra que as casas com vista para água possuem um preço cerca de 67,86% maior do que as casas sem.')

    return None

def buys_map(df2, geofile):
    st.title('Visão das Melhores Oportunidades:')

    c1, c2 = st.beta_columns((1, 1))

    c1.subheader('H6 - As melhores oportunidades (excellent offers) se encontram em '
                 'maioria no sul de seattle. (Falsa)')

    df = df2[df2['status'] == 'excellent offer']

    # Base Map - Folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4}'
                            'bathrooms, status: {5}'.format(row['price'], row['date'],
                                                                row['sqft_living'], row['bedrooms'],
                                                                row['bathrooms'], row['status'])).add_to(
            marker_cluster)

    with c1:
        folium_static(density_map)

    c1.write('Está hipótese é desvalidada, pois é visível no mapa que o sul possui menos oportunidades excelentes que outras regiões.')

    # Region Price Map
    c2.subheader('H7: O norte possui as casas de maiores preços. (Falso)')

    df = df2[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    df = df.sample(50)

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[df2['lat'].mean(), df2['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')

    with c2:
        folium_static(region_price_map)

    c2.write('Essa hipotese é desvalidada, pois é visível que a maior densidade de preço (maior preço na região) estaria mais localizada ao leste e não ao norte.')

    return None

def prices_growing(df2):
    st.title('Estudo dos Crescimentos:')

    c1, c2 = st.beta_columns((1, 1))

    df2['date'] = pd.to_datetime(df2['date']).dt.strftime('%Y')

    cols = ['date', 'price']
    dg8 = data_groupby(df2, cols)

    data = pd.read_csv('kc_house_data.csv')

    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m')

    cols = ['date', 'price']
    dg9 = data_groupby(data, cols)

    cols = ['yr_built', 'price']
    dg10 = data_groupby(data, cols)

    c1.subheader('H8 - O crescimento anual do preço das casas é cerca de 5%.(Falsa)')
    cols = ['date', 'price']
    ren = ['Date', 'Price Median']
    dg8 = data_rename(dg8, cols, ren)
    fig = px.line(dg8, x='Date', y='Price Median',
                 title='Median Prices Per Year')
    c1.plotly_chart(fig, use_container_width=True)
    c1.write('O gráfico acima demonstra que o crescimento de 2014 para 2015 foi cerca de 0,11%, portanto desvalidando a hipotese.')

    c2.subheader('H9 - O crescimento mensal do preço das casas possui uma certa linearidade, sempre mantendo uma estabilidade de preços.(Falsa)')
    cols = ['date', 'price']
    ren = ['Date', 'Price Median']
    dg9 = data_rename(dg9, cols, ren)
    fig = px.line(dg9, x='Date', y='Price Median',
                 title='Median Prices Per Month')
    c2.plotly_chart(fig, use_container_width=True)
    c2.write('O gráfico acima demonstra que o crescimento do preço das casas demonstrou tendências estáveis, decaindo e aumentando no mesmo ritmo')

    st.subheader('H10 - As casas anteriores a 1960 possuem um preço médio menor.(Falso)')
    cols = ['yr_built', 'price']
    ren = ['Year Built', 'Price Median']
    dg10 = data_rename(dg10, cols, ren)
    fig = px.line(dg10, x='Year Built', y='Price Median',
                 title='Median Prices Per Year Built')
    st.plotly_chart(fig, use_container_width=True)
    st.write('O gráfico acima demonstra que em média os preços das casas anteriores a 1960 é maior.')

    return None

def financial_results():
    st.title('Resultados Financeiros:')

    st.write('É esperado que a House Rocket opte por adquirir em geral as casas que foram classificadas como '
             'excelentes ofertas de acordo com a análise fornecida e desse modo consiga obter um retorno de'
             'cerca de 40% lucro adicional graças a essa estratégia.')

    st.write('Desse modo, retirados os tributos incidentes no USA, acredito que seja possível visualizar um aumento '
             'de cerca de 35% na receita bruta e ao menos 30% no lucro líquido da empresa.')

    return None

def next_steps():
    st.title('Próximos Passos:')

    st.write('Como próximos passos é esperado que seja feita uma organização para poder implementar um '
             'algoritmo de machine learning que auxilie a House Rocket a conseguir ir realizando essas análises '
             'de modo muito mais rapído e dinâmico, além de também haver a necessidade de ocorrer uma atualização '
             'do portofólio e também de manter em vista as casas já avaliadas para caso haja mudanças nos estados '
             'delas e possam ser encontradas oportunidades.')

    return None

def conclusion():
    st.title('Conclusão')

    st.write('A House Rocket, com o auxílio das análises fornecidas nesse projeto, poderá'
             'abordar ofertas interessantes de compra e realizar vendas vantajosas para ela, '
             'além de ser capaz de compreender melhor o próprio negócio e também usufruir dos'
             'insights obtidos através desse projeto para alcançar novas marcas no mercado atual.'
             'Desse modo, conseguindo crescer o seu lucro e manter se atualizando para se manter mais sólida.')

    return None


# ETL

# Data Extraction
url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
path = 'kc_house_data.csv'
path2 = 'houses prices analytics2.png'
imag1 = get_image(path2)
data = get_data(path)
geofile = get_geofile(url)

# Transformation
premises_plan(imag1)
df_ap1 = data_aprimorate(data)
data_quest(df_ap1)
data_analysis(df_ap1)
buys_map(df_ap1, geofile)
prices_growing(data)
financial_results()
next_steps()
conclusion()
