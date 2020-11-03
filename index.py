import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import app1, app2

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div(
    [
        html.H2('Sidebar', className='display-4'),
        html.Hr(),
        html.P(
            'A simple sidebar layout with navigation links', className='lead'
        ),
        dcc.Link('Page 1', href='/page-1'), html.Br(),
        dcc.Link('Page 2', href='/page-2'), html.Br(),
        dcc.Link('Page 3', href='/page-3'),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([ dcc.Location(id='url'), sidebar, content,
    dcc.Store(id='local', storage_type='local')])

trans = {
    'washer': '세탁기',
    'freezer': '냉장고',
}

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              [State('local', 'data')]
)
def render_page_content(pathname, data):
    print(f'pathname {pathname} data {data}')

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'url' not in changed_id:
        raise PreventUpdate 


    if pathname in ['/', '/page-1']:
        return app1.layout
    if pathname == '/page-2':
        return app2.get_layout(data['product'])
    if pathname == '/page-3':
        return html.P('Oh cool, this is page 3!')
    # If the user tries to reach a different page, return a 404 message
    return [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ]


if __name__ == '__main__':
  app.run_server(host='0.0.0.0', port=8050, debug=True)
