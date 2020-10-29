import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('hello dash!')
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
