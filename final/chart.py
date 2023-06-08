from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import yfinance as yf

# Specify the file path
file_path = "stock_code.txt"
# Read all lines and store them in a list
with open(file_path, "r") as file:
    all_stock = [line.strip() for line in file]
stock_options = all_stock.copy()
interval_options = ["1m", "2m", "5m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"]

app = Dash(__name__)


app.layout = html.Div([
  html.H1('Simple Interactive Stock Chart Application', style={'text-align': 'center'}),
  html.H4('Data Source From Yahoo Finance'),
  # html.H4('Data Source From Yahoo Finance', style={'text-align': 'center'}),

  # make multiple tabs
  dcc.Tabs(children=[
          dcc.Tab(label='All Stock Info', 
                  children = [
                  html.Div(id = 'first-section', children = [
                  html.Div(children = [
                          html.H4('Interval:', style={'display': 'inline-block', 'margin-right': '10px'}),
                          dcc.RadioItems(id = "interval-option-1", 
                                        options = interval_options, 
                                        value = '1m', 
                                        inline=True,
                                        style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                        ),
                          ]
                  ),

                  html.Div(children = [
                          html.H4('Period:', style={'display': 'inline-block', 'margin-right': '10px'}),
                          dcc.RadioItems(id = "period-option-1", 
                                        options = period_options, 
                                        value = '5d', 
                                        inline= True,
                                        style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                        ),
                          ]
                  ),
                  html.Button('All', id='button-all', 
                              style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                              'text-align': 'center', 'text-decoration': 'none', 'display': 'flex',
                              'font-size': '12px', 'margin': '4px 2px', 'cursor': 'pointer'}),
                                

                  html.Div(id='parent-container-1'),
                  ]),

                  ]
                  ),

          dcc.Tab(label='Detail Analysis', 
                  children = [
                  html.Div(id = 'second-section', 
                  children = [
                  html.Div(children = [
                          html.H4('Interval:', style={'display': 'inline-block', 'margin-right': '10px'}),
                          dcc.RadioItems(id = "interval-option-2", 
                                        options = interval_options, 
                                        value = '1m', 
                                        inline=True,
                                        style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                        ),
                          ]
                  ),

                  html.Div(children = [
                          html.H4('Period:', style={'display': 'inline-block', 'margin-right': '10px'}),
                          dcc.RadioItems(id = "period-option-2", 
                                        options = period_options, 
                                        value = '1d', 
                                        inline= True,
                                        style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                        ),
                          ]
                  ),
                  html.P("Select stock:"),
                  dcc.Dropdown(
                    id="stock-code",
                    options= stock_options,
                    multi = True,
                    clearable=True,
                  ),

                  html.Div(id='parent-container-2'),
                  ])
                  ]),

          dcc.Tab(label='Search for more stock',
                  children= [
                  html.H4('Interval:', style={'display': 'inline-block', 'margin-right': '10px'}),
                  dcc.RadioItems(id = "interval-option-3", 
                                options = interval_options, 
                                value = '1m', 
                                inline=True,
                                style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                ),
                  # ]
                  # ),

                  html.Div(children = [
                          html.H4('Period:', style={'display': 'inline-block', 'margin-right': '10px'}),
                          dcc.RadioItems(id = "period-option-3", 
                                        options = period_options, 
                                        value = '1d', 
                                        inline= True,
                                        style={"display": "inline-block", "justify-content": "center", "margin-bottom": "10px"},
                                        ),
                          ]
                  ),
                  # html.Div([
                  # html.Div([
                  dcc.Input(
                      id="search-box",
                      type="text",
                      placeholder="Enter a stock code",
                      style={
                          "marginRight": "10px",
                          "padding": "10px",
                          "textAlign": "center",
                      },
                  ),
                  html.Button(
                      "Find",
                      id="find-button",
                      n_clicks=0,
                      style={
                          "backgroundColor": "lightblue",
                          "padding": "10px",
                          "textAlign": "center",
                      },
                  ),

              html.Div(id='parent-container-3'),

              ],

),
                  ]
                  ),
])


@app.callback(
  Output('parent-container-1', 'children'),
  [
  Input("button-all", "n_clicks"),
  Input("interval-option-1", "value"),
  Input("period-option-1", "value")
  ]
)
def display_all_stock_graph(n_clicks, interval, period):
  print(n_clicks, interval, period)
  if n_clicks:
    stock_code = all_stock
    figure = graph_for_multiple_tickers(stock_code, interval, period)
    return dcc.Graph(figure = figure)
  else:
    figure = go.Figure()
    return dcc.Graph(figure = figure)


@app.callback(
  Output('parent-container-2', 'children'),
  [
  Input("stock-code", "value"),
  Input("interval-option-2", "value"),
  Input("period-option-2", "value")
  ]
)
def display_time_series(stock_code, interval, period):
  # The default option
  print("First time enter the app")
  print(stock_code)
  if stock_code:
    print("Other times")
    # other times when code change
    if len(stock_code) == 0:
      print("No stock chosen")
      return dcc.Graph(figure = go.Figure())
    elif len(stock_code) == 1:
      print("one stock code")
      stock_code = stock_code[0]
      figure = graph_for_single_ticker(stock_code, interval, period)
      return dcc.Graph(figure = figure)

    else:
      print("multiple stock code")
      figure = graph_for_multiple_tickers(stock_code, interval, period)
      return dcc.Graph(figure = figure)
    

@app.callback(
  Output('parent-container-3', 'children'),
  [
  Input("search-box", "value"),
  Input("find-button", "n_clicks"),
  Input("interval-option-3", "value"),
  Input("period-option-3", "value")
  ]
)
# def search_result(keyword, n_clicks, interval = "1m", period = "1d"):
def search_result(keyword, n_clicks, interval, period):
  print(f"This is the search key: {keyword}")
  if n_clicks > 0:
    figure = graph_for_single_ticker(keyword, interval, period)
    return dcc.Graph(figure = figure)


def graph_for_single_ticker(stock_code, interval = "1m", period = "1day"):
  # df = yf.download(stock_code, period='1d', start='2019-03-01', end='2023-06-01')
  # either set start, end params or period param, not both
  try:
    df = yf.download(stock_code, interval = interval, period = period)
  except Exception as e:
    print("*" * 20)
    print(e)
    print("*" * 20)
    return go.Figure()
  
  if len(df) ==0:
    print(f"No matching stock code with the search key: {stock_code}")
    return go.Figure()
  
  df['diff'] = df['Close'] - df['Open']
  df['color'] = df['diff'].apply(lambda x: 'green' if x >= 0 else 'red')

  fig = make_subplots(specs=[[{"secondary_y": True}]])
  fig.add_trace(go.Candlestick(x=df.index,
                              open=df['Open'],
                              high=df['High'],
                              low=df['Low'],
                              close=df['Close'],
                              name='Price'))
  # some indicator
  fig.add_trace(go.Scatter(x=df.index, y=df['Close'].rolling(window=50).mean(), marker_color='blue', name='50 period MA'))
  fig.add_trace(go.Scatter(x=df.index, y=df['Close'].rolling(window=200).mean(), marker_color='orange', name='200 period MA'))
  fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker={'color':df['color']}),secondary_y=True)
  fig.update_layout(title={'text': stock_code, 'x':0.4})

  lower_price = df.Close.min() * 0.99
  upper_price = df.Close.max() * 1.01
  upper_volume = df.Volume.max() * 1.5

  fig.update_yaxes(range=[lower_price, upper_price])
  fig.update_yaxes(range=[0, upper_volume], secondary_y=True)

  fig.update_layout(
    xaxis_title="Date", yaxis_title="Dollar"
)
  return fig

def graph_for_multiple_tickers(stock_codes, interval = '1m', period = "1d"):
  df = yf.download(stock_codes, interval = interval, period = period)
  fig = make_subplots()
  for code in stock_codes:
    fig.add_trace(go.Scatter(x=df.index, 
                            y=df.Close[code], 
                            name= code))
    
  fig.update_layout(title={'text': "All chosen stocks", 'x':0.5})
  lower_price = min(df.Close.min()) * 0.99
  upper_price = max(df.Close.max()) * 1.01
  fig.update_yaxes(range=[lower_price, upper_price])

  fig.update_layout(
    xaxis_title="Date", yaxis_title="Dollar"
  )
  return fig

if __name__ == "__main__":
    app.run_server(debug=True, port = 9900)
