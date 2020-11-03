import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div([
    html.Button('Button 1', id='btn-1'),
    html.Button('Button 2', id='btn-2'),
    html.Button('Button 3', id='btn-3'),
    html.Button('Button 4', id='btn-4'),
    html.Button('Button 5', id='btn-5'),
    html.Div([
    dcc.Link(id='hidden_link', href='/relation/freezer',
        children=[html.Img(src=app.get_asset_url('logo.png')),
            html.H3('냉장고')]),
    ]),
    dcc.Link(id='hidden_link', href='/relation/washer',
        children=[html.Img(src=app.get_asset_url('logo.png')),
            html.H3('세탁기')]),
    #dcc.Link(id='hidden_link', href='/page-2', style={'display': 'none'}),

    html.Div([
        html.Button('Load image', id='load-button'),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload image', id='upload-button')
        )
    ]),
])


#@app.callback([Output('local', 'data'), Output('hidden_link', 'target')],
#              [Input('btn-1', 'n_clicks'),
#               Input('btn-2', 'n_clicks'),
#               Input('btn-3', 'n_clicks'),
#               Input('btn-4', 'n_clicks'),
#               Input('btn-5', 'n_clicks')],
#              [State('local', 'data')])
##def displayClick(btn1, btn2, btn3, btn4, btn5, data):
#def displayClick(*args):
#    *btns, data = args
#    if not any(btns):
#        raise PreventUpdate 
#
#    print('')
#    print(f'triggered {dash.callback_context.triggered}')
#    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#    print(f'changed_id {changed_id}')
#    data = data or {'clicks': 0}
#    data['clicks'] = data['clicks'] + 1
#    return data, '/page-2'
