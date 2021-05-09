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
    st.title('1. Premises and Solution Plan:')

    st.image(imag1, caption='Created by Valcílio Júnior')

    st.subheader('1.1. Premises:')

    st.write('This project has as premise to help the company "House Sales in King County, USA", '
             'to find good home buying opportunities and then be able to resell for a higher price '
             'and thus obtain a higher profit thanks to this.')
    st.write('House Rocket asked on the basis of two main questions:')
    st.write('1. What properties to buy and how much to sell?')
    st.write('2. When is the best time to sell these properties?')
    st.write('In this way, this project has as premises to be able to answer these questions, '
             'and also to produce other relevant insights that may be able to have an impact in '
             'decision-making and, consequently, in the business itself.')

    st.subheader('1.2. Solution Plan:')

    st.write('The planning can be said to be divided into 4 parts: good buying opportunities, '
             'increase in the price to be able to sell, best time for resale and chances to be '
             'validated or devalued. Thus, the details of each one are as follows:')

    st.write('Purchasing opportunities > at this point the analysis was carried out in ascending '
             'order considering the following aspects: size, price, floors, water view, number '
             'of bedrooms and bathrooms. All these aspects in ascending order, that is, the more these aspects before fulfilling (eg: 2 bathrooms, 2 bedrooms, price below the median and etc ...), the better the classification of houses, considering this order of the worst even the best rating: Bad> Good> Great> Excellent')

    st.write('Increase in the price of houses for resale > was carried out according to a study '
             'of the average price of houses with these conditions and their offers.')

    st.write('Best time for resale > was carried out according to an analysis of the average price '
             'in the seasons of the year, thus finding what would be the most ideal time.')

    st.write('10 hypotheses were taken, which were validated or devalued in the course of this project:')
    st.write('H1 - The price of houses with conditions 3 to 4 in relation to houses with condition 1 is about 41% higher.')
    st.write('H2 - The price of houses with 2 to 4 bedrooms in relation to houses without bedrooms is 38.27% higher or more.')
    st.write('H3 - The price of houses with 2 to 4 bathrooms in relation to houses without a bathroom is equal to or greater than 49.30%.')
    st.write('H4 - The price of houses with 2 floors in relation to houses with only 1 floor is equal to or greater than 26.10%.')
    st.write('H5 - Houses with a water view have a price 67.86% higher than houses without a water view.')
    st.write('H6 - The best opportunities are found mostly in south seattle.')
    st.write('H7: The north has the highest priced houses.')
    st.write('H8 - The annual growth in house prices is around 5%.')
    st.write('H9 - The monthly house price growth is somewhat linear, always maintaining price stability.')
    st.write('H10 - Houses before 1960 have a lower average price.')

    return None

def data_quest(df2):

    f_status = st.sidebar.multiselect('Filter status:', df2['status'].unique())

    st.title('2. Business Questions:')

    if (f_status != []):
        df2 = df2.loc[df2['status'].isin(f_status)]

    else:
        df2 = df2.copy()

    st.subheader('2.1. What properties to buy and how much to sell them: (Filter on the side)')
    df1 = df2.copy()
    st.dataframe(df1[['id', 'price', 'date', 'price_median', 'condition', 'bedrooms', 'bathrooms', 'sqft_lot',
                      'lot_median', 'sqft_basement',
                      'floors', 'status', 'exchange_upgrade']].sort_values('price', ascending=True),
                 height=600)

    st.write('The table in question was built taking into account all the data in the database to detect the best offers and rank them accordingly as follows:')
    st.write('1. bad offer: the worst offers with overvalued prices and if resold, even at the best time, it would give little profit. (about 10% more)')
    st.write('2. good offer: undervalued offers that can yield a good profit due to the low purchase price. (about 20% more)')
    st.write('3. great offer: subvalidas offers with more bedrooms and bathrooms that can yield a great profit. (about 30% more)')
    st.write('4. excellent offer: undervalued property indications with all the benefits of others and more than one floor, can yield an excellent profit. (about 40% more)')
    st.write('')
    st.write('All of these increases in the resale price were calculated based on whether they were sold at the right time. (this time is indicated below)')

    st.subheader('2.2. When is the best time to sell these properties:')

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
    st.write('The best time for sale is in the spring, as, as the table shows, at that time there is an increase in'
             'the price of houses by about 4% in the other seasons.')

    return None

def data_analysis(df2):
    st.title('3. Insights Obtained:')

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

    c1.subheader('H1 - The price of houses with conditions 3 to 4 in relation to houses with '
                 'condition 1 is about 41% higher.(True)')

    # data plot

    cols = ['condition', 'price']
    ren = ['Condition', 'Price Median']
    dg1 = data_rename(dg1, cols, ren)

    fig = px.bar(dg1.head(4), x='Condition', y='Price Median', color='Price Median', title='Median Prices Per Condition')
    c1.plotly_chart(fig)

    c1.write('The graph above shows that houses with conditions 3 to 4 have a price about 41% '
             'higher than houses with conditions 1.')

    c2.subheader('H2 - The price of houses with 2 to 4 bedrooms in relation to houses '
                 'without bedrooms is 38.27% higher or more. (True)')

    cols = ['bedrooms', 'price']
    ren = ['Bedrooms', 'Price Median']
    dg2 = data_rename(dg2, cols, ren)

    fig = px.bar(dg2.head(5), x='Bedrooms', y='Price Median', color='Price Median',
                 title='Median Prices Per Bedrooms')
    c2.plotly_chart(fig)

    c2.write('The graph above shows that houses with 2 to 4 bedrooms have a price of about 38.27% higher '
             'than houses with no bedroom.')

    c3.subheader('H3 - The price of houses with 2 to 4 bathrooms in relation to houses without '
                 'a bathroom is equal to or greater than 49.30%. (True)')

    cols = ['bathrooms', 'price']
    ren = ['Bathrooms', 'Price Median']
    dg3 = data_rename(dg3, cols, ren)
    fig = px.bar(dg3.head(6), x='Bathrooms', y='Price Median', color='Price Median',
                 title='Median Prices Per Bathrooms')
    c3.plotly_chart(fig)
    c3.write('The graph above shows that houses with 2 to 4 bathrooms are priced at '
             'about 26.10% higher than houses with 1 without bathrooms.')

    c4.subheader('H4 - The price of houses with 2 floors in relation to houses with only 1 floor '
                 'is equal to or greater than 26.10%. (True)')
    cols = ['floors', 'price']
    ren = ['Floors', 'Price Median']
    dg4 = data_rename(dg4, cols, ren)
    fig = px.bar(dg4.head(2), x='Floors', y='Price Median', color='Price Median',
                 title='Median Prices Per Floors')
    c4.plotly_chart(fig)
    c4.write('The graph above shows that houses with 2 floors have a price about 26.10% higher '
             'than houses with 1 floor.')

    st.subheader('H5 - Houses with a water view have a price 67.86% higher than houses '
                 'without a water view. (True)')
    cols = ['waterfront', 'price']
    ren = ['Waterfront', 'Price Median']
    dg5 = data_rename(dg5, cols, ren)
    fig = px.bar(dg5, x='Waterfront', y='Price Median', color='Price Median',
                 title='Median Prices Per Waterfront')
    st.plotly_chart(fig)
    st.write('The graph above shows that houses with a water view have a price of about 67.86% '
             'higher than houses without.')

    return None

def buys_map(df2, geofile):
    st.title('4. Best Opportunities Vision:')

    c1, c2 = st.beta_columns((1, 1))

    c1.subheader('H6 - The best opportunities (excellent offers) se '
                 'were found on general in the south of seattle. (False)')

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

    c1.write('This hypothesis is invalidated, as it is visible on the map that the south has fewer '
             'excellent opportunities than other regions.')

    # Region Price Map
    c2.subheader('H7: The north has the highest priced houses. (False)')

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

    c2.write('This hypothesis is invalidated, as it is visible that the higher price density '
             '(higher price in the region) would be more located to the east and not to the north.')

    return None

def prices_growing(df2):
    st.title('5. Studies of Growth:')

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

    c1.subheader('H8 - The annual growth in house prices is around 5%. (False)')
    cols = ['date', 'price']
    ren = ['Date', 'Price Median']
    dg8 = data_rename(dg8, cols, ren)
    fig = px.line(dg8, x='Date', y='Price Median',
                 title='Median Prices Per Year')
    c1.plotly_chart(fig, use_container_width=True)
    c1.write('The graph above shows that the growth from 2014 to 2015 was around 0.11%, '
             'thus devaluing the hypothesis.')

    c2.subheader('H9 - The monthly house price growth is somewhat linear, always maintaining price stability. (False)')
    cols = ['date', 'price']
    ren = ['Date', 'Price Median']
    dg9 = data_rename(dg9, cols, ren)
    fig = px.line(dg9, x='Date', y='Price Median',
                 title='Median Prices Per Month')
    c2.plotly_chart(fig, use_container_width=True)
    c2.write('The graph above shows that the growth in house prices showed stable trends, '
             'decreasing and increasing at the same pace')

    st.subheader('H10 - Houses before 1960 have a lower average price. (False)')
    cols = ['yr_built', 'price']
    ren = ['Year Built', 'Price Median']
    dg10 = data_rename(dg10, cols, ren)
    fig = px.line(dg10, x='Year Built', y='Price Median',
                 title='Median Prices Per Year Built')
    st.plotly_chart(fig, use_container_width=True)
    st.write('The graph above shows that on average, house prices before 1960 are higher.')

    return None

def financial_results():
    st.title('6. Financial Results:')

    st.write('It is expected that House Rocket will choose to purchase in general the houses that have been classified '
             'as excellent offers according to the analysis provided and thus be able to obtain a return of about 40% '
             'additional profit thanks to this strategy.')

    st.write('Thus, excluding the taxes levied in the USA, I believe it is possible to see an increase of about 35% in'
             "gross revenue and at least 30% in the company's net profit.")

    return None

def next_steps():
    st.title('7. Next Steps:')

    st.write('As next steps, it is expected that an organization will be made in order to implement a machine learning '
             'algorithm that helps House Rocket to be able to carry out these analyzes in a much faster and more '
             'dynamic way, in addition to the need to update the portfolio and also to keep in mind the houses already '
             'evaluated in case there are changes in their states and opportunities can be found.')

    return None

def conclusion():
    st.title('8. Conclusion:')

    st.write('House Rocket, with the help of the analyzes provided in this project, '
             'will be able to address interesting purchase offers and make sales that are advantageous for '
             'it, in addition to being able to better understand the business itself and also take advantage '
             'of the insights obtained through this project to reach new brands in the current market. '
             'Thus, managing to grow your profit and keep updating to remain more solid.')

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
