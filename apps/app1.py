import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from app import app

products = ('세탁기', '냉장고', 'TV', '에어컨', '제습기')
layout = html.Div([
#    html.Button('Button 1', id='세탁기'),
#    html.Button('Button 2', id='냉장고'),
#    html.Button('Button 3', id='TV'),
#    html.Button('Button 4', id='에어컨'),
#    html.Button('Button 5', id='제습기'),
#    html.Div([
#    dcc.Link(id='hidden_link', href='/relation/freezer',
#        children=[html.Img(src=app.get_asset_url('logo.png')),
#            html.H3('냉장고')]),
#    ]),
#    dcc.Link(id='hidden_link', href='/relation/washer',
#        children=[html.Img(src=app.get_asset_url('logo.png')),
#            html.H3('세탁기')]),
#    #dcc.Link(id='hidden_link', href='/page-2', style={'display': 'none'}),
    html.Div([html.Button(p, id=p) for p in products]),

    html.Div([
        html.Button('Load image', id='load-button'),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload image', id='upload-button')
        )
    ]),
])


@app.callback([Output('local', 'data'), Output('url', 'pathname')],
#              [Input('세탁기', 'n_clicks'),
#               Input('냉장고', 'n_clicks'),
#               Input('TV', 'n_clicks'),
#               Input('에어컨', 'n_clicks'),
#               Input('제습기', 'n_clicks')],
              [Input(p, 'n_clicks') for p in products])
#              [State('local', 'data')])
def displayClick(*args):
    if not any(args):
        raise PreventUpdate

    print('')
    print(f'triggered {dash.callback_context.triggered}')
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(f'changed_id {changed_id}')

    data = {'product': changed_id.split('.')[0]}
    return data, '/page-2'
