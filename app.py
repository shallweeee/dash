import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server  # noqa

app.layout = html.Div([
    html.Div(["Name: ", dcc.Input(id="my-input", type="text", debounce=True)]),
    html.Br(),
    html.Div(id="my-output"),
])


@app.callback(
    Output("my-output", "children"),
    Input("my-input", "value"),
    prevent_initial_call=True,
)
def update_output_div(name):
    return f"Hello {name} !"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
