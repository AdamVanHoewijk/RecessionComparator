import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

app.layout = html.Div([
    html.H1(children="Hello World"),
    ]
)


app.run_server(debug=True)