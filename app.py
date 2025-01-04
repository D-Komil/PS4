import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Data viewer')
show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

st.dataframe(df)
st.header('Car Condition by Milage')

# create a plotly histogram figure
fig = px.histogram(df, x='odometer', color='condition')

# display the figure with streamlit
st.write(fig)

st.header('Model condition by Year')
fig = px.histogram(df, x='model_year', color='condition')
st.write(fig)

# Filters
manufacturer_filter = st.multiselect(
    'Select Manufacturer', options=df['manufacturer'].unique(), default=df['manufacturer'].unique()
)
min_year, max_year = st.slider('Select Model Year Range', min_value=int(df['model_year'].min()), max_value=int(df['model_year'].max()), value=(int(df['model_year'].min()), int(df['model_year'].max())))
price_filter = st.slider('Select Price Range', min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))
odometer_filter = st.slider('Select Milage Range', min_value=int(df['odometer'].min()), max_value=int(df['odometer'].max()), value=(int(df['odometer'].min()), int(df['odometer'].max())))

# Apply Filters
filtered_df = df[
    (df['manufacturer'].isin(manufacturer_filter)) &
    (df['model_year'] >= min_year) &
    (df['model_year'] <= max_year) &
    (df['price'] >= price_filter[0]) &
    (df['price'] <= price_filter[1]) &
    (df['odometer'] >= odometer_filter[0]) &
    (df['odometer'] <= odometer_filter[1])
]

# Display Filtered Table
st.write("Filtered Table:")
st.dataframe(filtered_df)