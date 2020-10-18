import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto

app = dash.Dash(__name__)

with open('data/sample_network.txt', 'r') as f:
    network_data = f.read().split('\n')

edges = network_data[:750]
nodes = set()

following_node_di = {}  # user id -> list of users they are following
following_edges_di = {}  # user id -> list of cy edges starting from user id

followers_node_di = {}  # user id -> list of followers (cy_node format)
followers_edges_di = {}  # user id -> list of cy edges ending at user id

cy_nodes = []

for edge in edges:
    if " " not in edge:
        continue

    source, target = edge.split(" ")

    cy_edge = {'data': {'id': source+target, 'source': source, 'target': target}}
    cy_target = {"data": {"id": target, "label": "User #" + str(target[-5:])}}
    cy_source = {"data": {"id": source, "label": "User #" + str(source[-5:])}}

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append(cy_source)
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append(cy_target)

    # Process dictionary of following
    if not following_node_di.get(source):
        following_node_di[source] = []
    if not following_edges_di.get(source):
        following_edges_di[source] = []

    following_node_di[source].append(cy_target)
    following_edges_di[source].append(cy_edge)

    # Process dictionary of followers
    if not followers_node_di.get(target):
        followers_node_di[target] = []
    if not followers_edges_di.get(target):
        followers_edges_di[target] = []

    followers_node_di[target].append(cy_source)
    followers_edges_di[target].append(cy_edge)

genesis_node = cy_nodes[0]
genesis_node['classes'] = "genesis"
default_elements = [genesis_node]

app.layout = html.Div([
    html.Div(className='ten columns', children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=default_elements,
            layout={'name': 'grid'},
        )
    ]),
    html.Div(className='two columns', children=[
        html.H4('Layouts'),
        dcc.Dropdown(
            id='dropdown-layout',
            options=[
                {'label': 'random', 'value': 'random'},
                {'label': 'grid', 'value': 'grid'},
                {'label': 'circle', 'value': 'circle'},
                {'label': 'concentric', 'value': 'concentric'},
                {'label': 'breadthfirst', 'value': 'breadthfirst'},
                {'label': 'cose', 'value': 'cose'},
            ],
            value='grid',
            clearable=False,
        ),
        html.Br(),
        html.H4('Expand'),
        dcc.RadioItems(
            id='radio-expand',
            options=[
                {'label': 'followers', 'value': 'followers'},
                {'label': 'following', 'value': 'following'},
            ],
            value='followers',
        ),
    ]),
])

@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}

def unexpand(nodeData, elements, expansion_mode):
    for element in elements:
        if nodeData['id'] == element['data']['id']:
            element['data']['expanded'] = False
            break

    if expansion_mode == 'followers':
        exclude_nodes = followers_node_di.get(nodeData['id'])
        exclude_edges = followers_edges_di.get(nodeData['id'])
    elif expansion_mode == 'following':
        exclude_nodes = following_node_di.get(nodeData['id'])
        exclude_edges = following_edges_di.get(nodeData['id'])

    if exclude_edges:
        exclude_ids = [node['data']['id'] for node in exclude_edges]
        elements = list(filter(lambda e: not e['data']['id'] in exclude_ids, elements))

    if exclude_nodes:
        exclude_ids = [node['data']['id'] for node in exclude_nodes if node['data']['id'] != genesis_node['data']['id']]

        for ex_id in exclude_ids:
            index = next((i for i, node in enumerate(elements) if node['data']['id'] == ex_id), -1)
            if index >= 0:
                del elements[index]

    return elements

@app.callback(Output('cytoscape', 'elements'),
              [Input('cytoscape', 'tapNodeData')],
              [State('cytoscape', 'elements'),
               State('radio-expand', 'value')])
def generate_elements(nodeData, elements, expansion_mode):
    if not nodeData:
        return default_elements

    if nodeData.get('expanded'):
        return unexpand(nodeData, elements, expansion_mode)

    for element in elements:
        if nodeData['id'] == element['data']['id']:
            element['data']['expanded'] = True
            break

    if expansion_mode == 'followers':
        followers_nodes = followers_node_di.get(nodeData['id'])
        followers_edges = followers_edges_di.get(nodeData['id'])

        if followers_nodes:
            for node in followers_nodes:
                node['classes'] = 'followerNode'
            elements.extend(followers_nodes)

        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge['classes'] = 'followerEdge'
            elements.extend(followers_edges)

    elif expansion_mode == 'following':
        following_nodes = following_node_di.get(nodeData['id'])
        following_edges = following_edges_di.get(nodeData['id'])

        if following_nodes:
            for node in following_nodes:
                if node['data']['id'] != genesis_node['data']['id']:
                    node['classes'] = 'followingNode'
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge['classes'] = 'followingEdge'
            elements.extend(following_edges)

    return elements


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
