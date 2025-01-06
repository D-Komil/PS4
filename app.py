import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

st.header('Car Sales Advertisement')

# Filters
manufacturer_filter = st.multiselect(
    'Select Manufacturer', options=df['manufacturer'].unique(), default=df['manufacturer'].unique()
)
min_year, max_year = st.slider(
    'Select Model Year Range', 
    min_value=int(df['model_year'].min()), 
    max_value=int(df['model_year'].max()), 
    value=(int(df['model_year'].min()), int(df['model_year'].max()))
)
price_filter = st.slider(
    'Select Price Range', 
    min_value=int(df['price'].min()), 
    max_value=int(df['price'].max()), 
    value=(int(df['price'].min()), int(df['price'].max()))
)
odometer_filter = st.slider(
    'Select Mileage Range', 
    min_value=int(df['odometer'].min()), 
    max_value=int(df['odometer'].max()), 
    value=(int(df['odometer'].min()), int(df['odometer'].max()))
)

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

# Checkbox to toggle between filtered and unfiltered data
st.write("### Display Options")
show_unfiltered = st.checkbox('Show Unfiltered Data')

if show_unfiltered:
    st.write("Unfiltered Table:")
    st.dataframe(df)
else:
    st.write("Filtered Table:")
    st.dataframe(filtered_df)

st.header('Car Condition by Mileage')

# Use filtered_df for the histogram
fig = px.histogram(
    filtered_df, 
    x='odometer', 
    color='condition',
    title='Car Condition by Mileage',
    labels={'odometer': 'Mileage (miles)', 'condition': 'Condition'}
)
st.write(fig)

st.header('Model Condition by Year')

# Use filtered_df for the histogram
fig = px.histogram(
    filtered_df, 
    x='model_year', 
    color='condition',
    title='Model Condition by Year',
    labels={'model_year': 'Model Year', 'condition': 'Condition'}
)
st.write(fig)

st.header('Price vs Mileage Scatter Plot')

# Use filtered_df for the scatter plot
scatter_fig = px.scatter(
    filtered_df,
    x='odometer',
    y='price',
    color='condition',
    size='model_year',  # Optional, adjust size based on model year
    hover_data=['manufacturer', 'model'],
    title='Price vs Mileage by Condition',
    labels={'odometer': 'Mileage (miles)', 'price': 'Price ($)'}
)
st.write(scatter_fig)