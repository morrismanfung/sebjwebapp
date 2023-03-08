from dash import dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from scipy.stats import norm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.MINTY])

money = dash_table.FormatTemplate.money(0)
percentage = dash_table.FormatTemplate.percentage(2)

df = pd.read_csv('data/freq.csv')
edge = pd.read_csv('data/edge.csv')

advantage = [0.005*i - 0.0054 for i in range(-1, 7)]

rule = dbc.Card([
    dbc.CardHeader('Rules'),
    dbc.Row([
        dbc.Col(
            dcc.Checklist(
                id='rule-check-1',
                options={
                        'dd': 'Double Deck',
                        'd10': 'Double on 10+',
                        'd9': 'Double on 9+'
                },
                value=[],
                labelStyle = {'display': 'block'}
            ),
            width=3
        ),
        dbc.Col(
            dcc.Checklist(
                id='rule-check-2',
                options={
                        'h17': 'Dealer hits S17',
                        'european': 'No hole card',
                        'das': 'Double after split',
                },
                value=['h17'],
                labelStyle = {'display': 'block'}
            ),
            width=3
        ),
        dbc.Col(
            dcc.Checklist(
                id='rule-check-3',
                options={
                        'd3': 'Double > 2 cards',
                        'rsa': 'Resplit aces',
                        'dsa': 'Draw to splitted aces',
                },
                value=[],
                labelStyle = {'display': 'block'}
            ),
            width=3
        ),
        dbc.Col(
            dcc.Checklist(
                id='rule-check-4',
                options={
                        'late': 'Late Surrender',
                        'early': 'Early Surrender'
                },
                value=[],
                labelStyle = {'display': 'block'}
            ),
            width=3
        )
    ])
])

base = dcc.Store(id='base', data=0.00054)

personalization = dbc.Card([
    dbc.CardHeader('Personal settings'),
    dbc.CardBody(
        dash_table.DataTable(
            id='personalization_table',
            columns=[
                {'id': 'stat', 'name': ''},
                {'id': 'value', 'name': 'Input Your Value Here', 'type': 'numeric', 'editable': True}
            ],
            data=[
                {'stat': 'Bankroll', 'value': 10000},
                {'stat': 'Hour', 'value': 1},
                {'stat': 'Round per Hour', 'value': 100}
            ],
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'value',
                    },
                    'backgroundColor': 'cornsilk',
                    # 'color': 'white'
                }]
            
            #style_header = {'display': 'none'}
        )
    )
])

freq_table = dash_table.DataTable(
    id='freq-table',
    columns=[
        {'id': 'count', 'name': 'Count'},
        {'id': 'freq', 'name': 'Frequency', 'type': 'numeric', 'format': percentage},
        {'id': 'ev', 'name': 'EV', 'type': 'numeric', 'format': percentage},
        {'id': 'customized', 'name': 'Customized', 'type': 'numeric', 'format': money, 'editable': True}
    ],
    data=df.to_dict('records'),
    style_data_conditional=[
        {
            'if': {
                'column_id': 'customized',
            },
            'backgroundColor': 'cornsilk',
            # 'color': 'white'
        }]
)

stat_table = dash_table.DataTable(
    id='stat_table',
    columns=[
        {'id': 'stat', 'name': ''},
        {'id': 'value', 'name': ''}
    ],
    data=[
        {'stat': 'EV', 'value': 0},
        {'stat': 'RoR', 'value': 0},
        {'stat': 'EV (%)', 'value':0},
        {'stat': 'EV/hour', 'value':0},
        {'stat': 'Standard deviation', 'value':0},
        {'stat': 'Risk of Ruin', 'value':0}
    ],
    # style_header = {'display': 'none'}
)

worst_table = dbc.Card([
    dbc.CardHeader('Worse Case Scenario'),
    dbc.CardBody(
        dash_table.DataTable(
            id='worst_table',
            columns=[
                {'id': 'probability', 'name': 'Probability'},
                {'id': 'return', 'name': 'Return'}
            ],
            data=[
                {'probability': '1%', 'return': 0},
                {'probability': '5%', 'return': 0},
                {'probability': '10%', 'return': 0},
                {'probability': '50%', 'return': 0}
            ]
            # style_header = {'display': 'none'}
        )
    )
])

dist_graph = dcc.Graph(id='dist_graph')

main_page = [
    dbc.Row([
        dbc.Col(
            [
                rule,
                html.Br(),
                freq_table
            ],
            width=7
        ),
        dbc.Col(dist_graph, width=5)
    ]),

    # html.Br(style={"line-height": 1}),

    dbc.Row([
        dbc.Col(personalization, width=4),
        dbc.Col(stat_table, width=4),
        dbc.Col(worst_table, width=4)
    ])
]

app.layout = dbc.Container([
    # Stored data
    base,

    # Header
    html.H1('Simple and Easy Blackjack Calculator'),
    dbc.Tabs([
        dbc.Tab(label='Main Page', children=main_page),
        dbc.Tab(label='Guide', children=html.P('Guide')),
        dbc.Tab(label='Learn More', children=[
            dcc.Markdown(
            '''
            For more information, please visit our GitHub repository at [https://github.com/morrismanfung/sebjwebapp](https://github.com/morrismanfung/sebjwebapp).
            
            Source code of the web app can be accessed in the repository.
            ''')
        ])
    ]),
    
])

# Update base edge
@app.callback(
    Output(component_id='base', component_property='data'),
    [Input(component_id='rule-check-1', component_property='value'),
     Input(component_id='rule-check-2', component_property='value'),
     Input(component_id='rule-check-3', component_property='value'),
     Input(component_id='rule-check-4', component_property='value')]
)
def update_output_div(rule_1, rule_2, rule_3, rule_4):
    input_value = rule_1 + rule_2 + rule_3 + rule_4
    ddf = edge[edge['Rule'].isin(input_value)]
    if 'dd' in input_value:
        return(ddf['DD'].sum())
    else:
        return(ddf['Shoe'].sum())

# Update EV
@app.callback(
    Output(component_id='freq-table', component_property='data'),
    Input(component_id='base', component_property='data'),
    State(component_id='freq-table', component_property='data')
)
def update_output_div(input_value, rows):
    for i, row in enumerate(rows):
        row['ev'] = advantage[i] + input_value
    return rows

# Update statistics
@app.callback(
    Output(component_id='stat_table', component_property='data'),
    [Input(component_id='freq-table', component_property='data'),
     Input(component_id='personalization_table', component_property='data')],
    State(component_id='stat_table', component_property='data')
)
def update_output_div(freq, personalization, rows):
    dff = pd.DataFrame(freq)
    bankroll = pd.DataFrame(personalization).iloc[0, 1]
    round_per_hour = pd.DataFrame(personalization).iloc[2, 1]

    # Average bet
    rows[0]['stat'] = 'Average Bet'
    avg_bet = sum(dff['freq']*dff['customized'])
    rows[0]['value'] = f'${avg_bet:.2f}'

    # EV
    rows[1]['stat'] = 'Expected Value'
    ev = sum(dff['freq']*dff['ev']*dff['customized'])
    rows[1]['value'] = f'${ev:.2f}'

    # EV / hour
    rows[2]['stat'] = 'Expected Value'
    ev_hour = sum(dff['freq']*dff['ev']*dff['customized']*round_per_hour)
    rows[2]['value'] = f'${ev_hour:.2f}'

    # EV %
    rows[3]['stat'] = 'EV (%)'
    ev_percentage = ev / avg_bet
    rows[3]['value'] = f'{ev_percentage*100:.2f}%'

    # Standard deviation
    rows[4]['stat'] = 'Standard deviation'
    std = sum(dff['freq'] * 1.30 ** 2 * dff['customized'] ** 2) ** 0.5
    rows[4]['value'] = f'${std:.2f}'

    # RoR
    rows[5]['stat'] = 'Risk of Ruin'
    ror = min(
            ((1 - ev / std) / (1 + ev / std)) ** (bankroll / std), 1
            ) # if the risk f 
    rows[5]['value'] = f'{ror*100:.2f}%'

    return rows

# Update Distribution
@app.callback(
    Output(component_id='dist_graph', component_property='figure'),
    [Input(component_id='stat_table', component_property='data'),
     Input(component_id='personalization_table', component_property='data'),
     Input(component_id='worst_table', component_property='data')],
)
def update_output_div(stat, personalization, worst):
    ev = float(pd.DataFrame(stat).iloc[1, 1].strip('$'))
    sd = float(pd.DataFrame(stat).iloc[4, 1].strip('$'))
    hours = pd.DataFrame(personalization).iloc[1, 1]
    round_per_hour = pd.DataFrame(personalization).iloc[2, 1]

    worst = pd.DataFrame(worst)

    sd = sd * (hours * round_per_hour) ** 0.5                   # Taking square root because each run is independent
    z = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 10000)
    x = z * sd + ev * hours * round_per_hour
    y = norm.pdf(z)

    z50 = np.linspace(norm.ppf(0.25), norm.ppf(0.75), 1000)
    x50 = z50 * sd + ev * hours * round_per_hour
    y50 = norm.pdf(z50)

    dff_whole = pd.DataFrame({'x': x, 'y': y})
    dff_50 = pd.DataFrame({'x50': x50, 'y50': y50})

    figure = px.line(dff_whole, x='x', y='y',
        title = 'Distribution of Actual Return',
        labels={'x': 'Actual Return', 'y': 'Probability Density'})
    
    # figure.add_trace(go.Scatter(x=x50, y=y50, fill='tozeroy', mode='none'))
    
    figure.add_trace(go.Scatter(
        x=[norm.ppf(0.01) * sd + ev * hours * round_per_hour, norm.ppf(0.01) * sd + ev * hours * round_per_hour],
        y=[0, 0.5], 
        line={
            'color': 'rgb(31, 119, 180)',
            'width': 1,
            'dash': 'dashdot',
        }, name=f'Worst 1%: {worst.iloc[0, 1]}'
    ))

    figure.add_trace(go.Scatter(
        x=[norm.ppf(0.05) * sd + ev * hours * round_per_hour, norm.ppf(0.05) * sd + ev * hours * round_per_hour],
        y=[0, 0.5], 
        line={
            'color': 'rgb(255, 127, 14)',
            'width': 1,
            'dash': 'dashdot',
        }, name=f'Worst 5%: {worst.iloc[1, 1]}'
    ))

    figure.add_trace(go.Scatter(
        x=[norm.ppf(0.1) * sd + ev * hours * round_per_hour, norm.ppf(0.1) * sd + ev * hours * round_per_hour],
        y=[0, 0.5], 
        line={
            'color': 'rgb(44, 160, 44)',
            'width': 1,
            'dash': 'dashdot',
        }, name=f'Worst 10%: {worst.iloc[2, 1]}'
    ))

    figure.add_trace(go.Scatter(
        x=[norm.ppf(0.5) * sd + ev * hours * round_per_hour, norm.ppf(0.5) * sd + ev * hours * round_per_hour],
        y=[0, 0.5], 
        line={
            'color': 'rgb(148, 103, 189)',
            'width': 1,
            'dash': 'dashdot',
        }, name=f'Worst 50%: {worst.iloc[3, 1]}'
    ))

    return figure

# Update worst table
@app.callback(
    Output(component_id='worst_table', component_property='data'),
    [Input(component_id='personalization_table', component_property='data'),
     Input(component_id='stat_table', component_property='data')],
    State(component_id='worst_table', component_property='data')
)
def update_output_div(personalization, stat, rows):
    dff = pd.DataFrame(stat)
    ev = float(dff.iloc[1, 1].strip('$'))
    sd = float(dff.iloc[4, 1].strip('$'))

    dff_personalization = pd.DataFrame(personalization)
    hours = dff_personalization.iloc[1, 1]
    round_per_hour = dff_personalization.iloc[2, 1]

    # Worst 1%
    z = norm.ppf(0.01)
    r = z * sd * (hours * round_per_hour) ** 0.5 + ev * (hours * round_per_hour)
    rows[0]['return'] = f'${r:.2f}'

    # Worst 5%
    z = norm.ppf(0.05)
    r = z * sd * (hours * round_per_hour) ** 0.5 + ev * (hours * round_per_hour)
    rows[1]['return'] = f'${r:.2f}'

    # Worst 10%
    z = norm.ppf(0.1)
    r = z * sd * (hours * round_per_hour) ** 0.5 + ev * (hours * round_per_hour)
    rows[2]['return'] = f'${r:.2f}'

    # Worst 50%
    z = norm.ppf(0.5)
    r = z * sd * (hours * round_per_hour) ** 0.5 + ev * (hours * round_per_hour)
    rows[3]['return'] = f'${r:.2f}'

    return rows
    
'''
# Testing - Check whether Store is okay
@app.callback(
    Output(component_id='testing', component_property='children'),
    Input(component_id='base', component_property='data')
)
def update_output_div(input_value):
    return(input_value)
'''

if __name__ == '__main__':
    app.run_server(debug=True)
