import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Financial Data Visualization Tool"),
    
    dcc.Input(id='stock-input', value='AAPL', type='text'),
    
    dcc.Graph(id='stock-graph'),
    
    html.Label('Select Date Range:'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2020-01-01',
        end_date='2022-01-01',
        display_format='YYYY-MM-DD'
    )
])

# Define callback to update graph
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-input', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(stock_ticker, start_date, end_date):
    df = yf.download(stock_ticker, start=start_date, end=end_date)
    trace_line = go.Scatter(x=df.index, y=df['Close'], mode='lines', name=stock_ticker)
    layout = go.Layout(title=f"{stock_ticker} Stock Prices")
    return {'data': [trace_line], 'layout': layout}

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
