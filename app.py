from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
try:
    data = pd.read_csv('historical_automobile_sales.csv')
except Exception as e:
    print(f"Error loading data: {e}")

# Initialize the Dash app
app = Dash(__name__)

# List of years for the dropdown
year_list = sorted(data['Year'].unique())

# Create the layout of the app
app.layout = html.Div(style={'textAlign': 'center', 'padding': '20px'}, children=[
    html.H1("Automobile Statistics Dashboard", style={'color': 'red'}),

    # Dropdown to select statistics type
    html.Div([
        html.Label("Select Statistics:", style={'font-weight': 'bold', 'font-size': '18px'}),
        dcc.Dropdown(
            id='select-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            style={'font-weight': 'bold', 'font-size': '18px'}
        )
    ], style={'width': '60%', 'margin': 'auto', 'padding': '15px'}),

    # Dropdown to select year
    html.Div([
        html.Label("Select Year:", style={'font-weight': 'bold', 'font-size': '18px'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=year_list[0]
        )
    ], style={'width': '60%', 'margin': 'auto', 'padding': '15px'}),

    # Container for visualizations
    html.Div(id='output-container', style={'width': '100%', 'margin': 'auto', 'display': 'inline-block'})
])

# Callback to enable/disable year selection based on statistics type
@app.callback(
    Output('select-year', 'disabled'),
    Input('select-statistics', 'value')
)
def update_input_container(selected_statistics):
    """Enable or disable year dropdown based on selected statistics type."""
    return selected_statistics != 'Yearly Statistics'

# Callback to update visualizations
@app.callback(
    Output('output-container', 'children'),
    [Input('select-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    """Update visualizations based on user selections."""
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Line chart of sales during recession
        plot1 = px.line(recession_data, x='Year', y='Automobile_Sales', 
                        title='Automobile Sales During Recession')
        
        # Pie chart of vehicle type sales during recession
        plot2 = px.pie(recession_data, names='Vehicle_Type', values='Automobile_Sales', 
                       title='Sales Distribution by Vehicle Type (Recession Period)')
        
        return [dcc.Graph(figure=plot1), dcc.Graph(figure=plot2)]
    
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]
        
        # Monthly sales trend line chart
        plot1 = px.line(yearly_data, x='Month', y='Automobile_Sales', 
                        title=f'Automobile Sales Trend in {input_year}')
        
        # Sales by vehicle type pie chart
        plot2 = px.pie(yearly_data, names='Vehicle_Type', values='Automobile_Sales', 
                       title=f'Sales Distribution by Vehicle Type in {input_year}')
        
        # Sales comparison by year
        yearly_sales = data.groupby('Year').sum().reset_index()
        plot3 = px.bar(yearly_sales, x='Year', y='Automobile_Sales', 
                       title='Yearly Automobile Sales Comparison')
        
        return [dcc.Graph(figure=plot1), dcc.Graph(figure=plot2), dcc.Graph(figure=plot3)]
    
    return None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
