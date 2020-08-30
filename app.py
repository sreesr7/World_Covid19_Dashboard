import pandas as pd
import io
import requests
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3
import plotly.graph_objects as go
import streamlit as st

DATA_URL="https://www.trackcorona.live/api/countries.csv"
s=requests.get(DATA_URL).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))
df.drop(['updated'],axis=1,inplace=True)
df['country_code'] = df['country_code'].str.upper()

st.title("COVID 19 TRACKER")
st.markdown("Streamlit DashBoard to Analyze covid 19🦠 cases around the World🌎")


indexNames = df[ df['country_code'] == 'XK' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '00' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '03' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '09' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '01' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '05' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '12' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '06' ].index
df.drop(indexNames , inplace=True)
indexNames = df[ df['country_code'] == '11' ].index
df.drop(indexNames , inplace=True)



df['country_code'] = df.country_code.apply(lambda x: country_name_to_country_alpha3(country_alpha2_to_country_name(x)))
df['death rate']=(df['dead']/df['confirmed'])*100
df['recovery rate']=(df['recovered']/df['confirmed'])*100
st.sidebar.title("Filter country ")
temp = df.to_dict('list')
temp['location'] = list(set(temp['location']))
data = st.sidebar.selectbox("Select Country", temp['location'])

st.subheader("NUMBER OF COVID 19 CASES AROUND THE WORLD")

fig1 = go.Figure(data=go.Choropleth(
    locations = df['country_code'],
    z = df['confirmed'],
    text = df['location'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '<>',
    colorbar_title = 'confirmed cases',
))
fig1.update_layout(
    title_text='covid 19 confirmed cases',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.trackcorona.live/api">\
            Track corona</a>',
        showarrow = False
    )]
)
st.plotly_chart(fig1)


st.subheader("NUMBER OF DEATHS AROUND THE WORLD")

fig2 = go.Figure(data=go.Choropleth(
    locations = df['country_code'],
    z = df['dead'],
    text = df['location'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '<>',
    colorbar_title = 'Deaths',
))
fig2.update_layout(
    title_text='covid 19 Deaths',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.trackcorona.live/api">\
            Track corona</a>',
        showarrow = False
    )]
)


st.plotly_chart(fig2)
st.subheader("NUMBER OF COVID 19 PATIENTS RECOVERED AROUND THE WORLD")

fig3 = go.Figure(data=go.Choropleth(
    locations = df['country_code'],
    z = df['recovered'],
    text = df['location'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '<>',
    colorbar_title = 'Recovered cases',
))
fig3.update_layout(
    title_text='covid 19 recovered cases',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.trackcorona.live/api">\
            Track corona</a>',
        showarrow = False
    )]
)
st.plotly_chart(fig3)
Index_label = df[df['location']==data].index.tolist()
ind=Index_label[0]
fig = go.Figure(go.Bar(
            x=[df.at[ind,'death rate'],df.at[ind,'recovery rate']],
            y=[data+' covid 19 mortality rate', data+' covid 19 recovery rate'],
            orientation='h'))
st.plotly_chart(fig)

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(df)
