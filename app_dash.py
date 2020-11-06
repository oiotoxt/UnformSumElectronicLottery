# refs:
#   https://dash.plotly.com/dash-core-components/graph
#   https://dash.plotly.com/basic-callbacks
#   https://dash.plotly.com/live-updates

import numpy as np
import plotly.express as px
import dash
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import dash_core_components as dcc
import dash_html_components as html

import prob_short as prob


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig_pdf = px.bar(y=prob.PDF,
                 labels={'x': '숫자 합', 'y': '전체 백만 명 중 사람 수'})

fig_pdf.add_shape(type="rect",
    x0=0, y0=0, x1=27, y1=60000,
    line=dict(
        width=0,
    ),
    fillcolor='rgba(255, 0, 0, 0.2)',
)

fig_pdf.update_layout(
    # title_text='백만 명이 추첨에 참여한 경우',
    title_x=0.5,
    xaxis=dict(tickmode='linear')
)

fig_cdf = px.bar(y=prob.CDF,
                 labels={'x': '숫자 합', 'y': '전체 백만 명 중 사람 수 (누적)'})

fig_cdf.update_layout(
    xaxis=dict(tickmode='linear')
)

def convert_slider_value(val):
    mark = [200, 400, 600, 800, 1000]
    conv = [10, 100, 1000, 10000, 1000000]
    if val <= 2.0:
        val = 1.0
    elif val <= mark[0]:
        val /= mark[0] / 10
    elif val <= mark[1]:
        val = ((val - mark[0]) / (mark[1] - mark[0]) * (conv[1] - conv[0])) + conv[0]
        val = int(val)
    elif val <= mark[2]:
        val = ((val - mark[1]) / (mark[2] - mark[1]) * (conv[2] - conv[1])) + conv[1]
        val = int(val)
    elif val <= mark[3]:
        val = ((val - mark[2]) / (mark[3] - mark[2]) * (conv[3] - conv[2])) + conv[2]
        val = int(val)
    elif val <= mark[4]:
        val = ((val - mark[3]) / (mark[4] - mark[3]) * (conv[4] - conv[3])) + conv[3]
        val = int(val)
    return val

app.layout = html.Div(children=[
    html.Center([
        # html.H1(children='당첨 숫자 예측',
        #         style={'margin-top': '40px', 'margin-bottom': '60px'}
        #         ),

        html.Br(),

        dcc.Markdown('''
            # 당첨 숫자 예측
        '''),

        html.Br(),

        dcc.Markdown('''
            ```경쟁률이 [3.5 대 1]이라면 [3.5]를 입력해 주세요```
        '''),

        html.Div(id='output-warning',
                 style={'color': 'red', 'margin-bottom': '0px'}
                 ),

        dcc.Input(
            id='rate',
            type='number',
            placeholder='경쟁률',
            min=1,
            max=1e6,
            # step=0.05,
            value=2.0,
            style={'textAlign': 'center', 'margin-bottom': '0px'}
        ),

        html.Div(id='output-msg1',
                 style={'margin-top': '20px','margin-bottom': '20px'}
                 ),

        # dcc.Slider(
        #     id='my-slider',
        #     min=1,
        #     max=1e6,
        #     step=0.05,
        #     # tooltip={'always_visible': True},
        #     marks={
        #         1: '1',
        #         200000: '10',
        #         400000: '100',
        #         600000: '1000',
        #         800000: '10000',
        #         1000000: '1000000',
        #     },
        #     value=2.0,
        #     updatemode='drag'
        # ),

        dcc.Slider(
            id='my-slider',
            min=20,
            max=1000,
            step=1,
            # tooltip={'always_visible': True},
            marks={
                20: '1',
                200: '10',
                400: '100',
                600: '1000',
                800: '10000',
                1000: '1000000',
            },
            value=40.0,
            updatemode='drag'
        ),

        html.Div(id='output-msg2',
                 style={ 'font-weight': 'bold',
                        'font-size': '2.0em',
                     'margin-bottom': '40px'}
                 ),

        # dcc.Graph(id='live-update-graph'),

        dcc.Graph(
            id='graph pdf',
            figure=fig_pdf,
            # config={
            #     'editable': True,
            #     'edits': {
            #         'shapePosition': True,
            #     }
            # }
        ),

        # dcc.Graph(
        #     id='graph cdf',
        #     figure=fig_cdf
        # ),

        # html.Div(id='hidden-div', style={'display': 'none'})
    ])
])


def rate_to_percentile(rate):
    return 1.0 - (1.0 / rate)


@app.callback(
    Output('graph pdf', 'figure'),
    [Input('rate', 'value')],
    [State('graph pdf', 'figure')])
def update_output_input(val, fig):
    if val is not None:
        fig['layout']['shapes'][0]['x1'] = prob.predict(val)
    return fig


@app.callback(
    Output('rate', 'value'),
    [Input('my-slider', 'value')])
def update_output_slider(value):
    # print('``````````````````````````', value)
    return convert_slider_value(value)


@app.callback(
    [Output('output-warning', 'children'),
    Output('output-msg1', 'children'),
    Output('output-msg2', 'children')],
    [Input('rate', 'value')])
def update_output_guess(value):
    if value is None:
        return [f'유효 입력 범위 : [1 ~ 백만]', f'목표 백분위 : ???', f'당첨되려면 아마도 ??? 이상이 필요할거에요~']
    else:
        percentile = rate_to_percentile(value) * 100
        pred = prob.predict(value)
        return [f'', f'목표 백분위 : {percentile:.8f}+', f'당첨되려면 아마도 {pred} 이상이 필요할거에요~']


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8501, debug=True)
