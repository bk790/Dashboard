import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('historical_automobile_sales.csv')

# Title
st.title("Automobile Statistics Dashboard")

# Dropdown to select statistics type
statistics_type = st.selectbox("Select Statistics:", 
                                ["Yearly Statistics", "Recession Period Statistics"])

# Dropdown to select year (only if "Yearly Statistics" is selected)
if statistics_type == "Yearly Statistics":
    year_list = sorted(data['Year'].unique())
    selected_year = st.selectbox("Select Year:", year_list)

# Display visuals based on selection
if statistics_type == 'Recession Period Statistics':
    recession_data = data[data['Recession'] == 1]
    st.plotly_chart(px.line(recession_data, x='Year', y='Automobile_Sales', title='Automobile Sales During Recession'))
    st.plotly_chart(px.pie(recession_data, names='Vehicle_Type', values='Automobile_Sales', title='Sales Distribution by Vehicle Type (Recession Period)'))
elif statistics_type == 'Yearly Statistics' and 'selected_year' in locals():
    yearly_data = data[data['Year'] == selected_year]
    st.plotly_chart(px.line(yearly_data, x='Month', y='Automobile_Sales', title=f'Automobile Sales Trend in {selected_year}'))
    st.plotly_chart(px.pie(yearly_data, names='Vehicle_Type', values='Automobile_Sales', title=f'Sales Distribution by Vehicle Type in {selected_year}'))
    yearly_sales = data.groupby('Year').sum().reset_index()
    st.plotly_chart(px.bar(yearly_sales, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales Comparison'))


# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get("PORT", 8050)), debug=True)

