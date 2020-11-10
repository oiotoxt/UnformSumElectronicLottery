#
# 돌아만 가도록 급조된 코드입니다;;
#

import plotly.express as px
import dash
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
import dash_core_components as dcc
import dash_html_components as html

import lottery_prob as prob


_mark = [0, 400, 600, 800, 900, 1000]
_conv = [0, 10, 100, 1000, 10000, 1000000]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig_pdf = px.bar(y=prob.PDF,
                 labels={'x': '숫자 합', 'y': '전체 백만 명 중 사람 수'})

fig_pdf.add_shape(type="rect",
                  x0=0, y0=0, x1=27, y1=60000,
                  line=dict(width=0),
                  fillcolor='rgba(255, 0, 0, 0.2)')

fig_pdf.update_layout(title_x=0.5,
                      xaxis=dict(tickmode='linear')
                      )

server.layout = html.Div(children=[
    html.Center([
        html.Br(),

        dcc.Markdown('''
            # 당첨 숫자 예측
        '''),

        html.Br(),

        dcc.Markdown('''
            ```경쟁률이 [3.5 대 1] 이라면 [3.5]를 입력하시거나,```
        '''),

        dcc.Markdown('''
            ```아래 <슬라이드바>에서 [3.5]를 선택해 주세요.```
        '''),

        html.Div(id='output-warning',
                 style={'color': 'red', 'margin-bottom': '0px'}),

        dcc.Input(
            id='rate',
            type='number',
            placeholder='경쟁률',
            min=1,
            max=1e6,
            value=2.0,
            style={'textAlign': 'center', 'margin-bottom': '40px'}),

        dcc.Slider(
            id='rate-slider',
            min=int(_mark[1]*0.1),
            max=1000,
            step=1,
            marks={
                int(_mark[1]*0.1): '1',
                _mark[1]: f"{_conv[1]:,}",
                _mark[2]: f"{_conv[2]:,}",
                _mark[3]: f"{_conv[3]:,}",
                _mark[4]: f"{_conv[4]:,}",
                _mark[5]: f"{_conv[5]:,}",
            },
            value=int(_mark[1]*0.2),
            updatemode='drag'),

        html.Div(id='output-predict',
                 style={'font-weight': 'bold',
                        'font-size': '2.0em',
                        'margin-top': '60px',
                        'margin-bottom': '0px'}),

        html.Div(id='output-percentile',
                 style={'margin-top': '0px', 'margin-bottom': '0px'}),

        dcc.Graph(id='graph-pdf',
                  figure=fig_pdf),

        html.A("Null - 알고리즘 설명 및 코드",
               href='https://null.ncsoft.com/questions/4781', target="_blank"),
    ])
])


def convert_slider_value(value):
    for i in range(1, len(_mark)):
        if value <= _mark[i]:
            return (value - _mark[i-1]) * (_conv[i] - _conv[i-1]) / (_mark[i] - _mark[i-1]) + _conv[i-1]


@server.callback(
    Output('graph-pdf', 'figure'),
    [Input('rate', 'value')],
    [State('graph-pdf', 'figure')])
def update_output_input(value, fig):
    if value is not None:
        target_percentile = prob.rate_to_percentile(value)
        fig['layout']['shapes'][0]['x1'] = prob.predict(target_percentile)
    return fig


@server.callback(
    Output('rate', 'value'),
    [Input('rate-slider', 'value')])
def update_output_slider(value):
    return convert_slider_value(value)


@server.callback(
    [Output('output-warning', 'children'),
     Output('output-percentile', 'children'),
     Output('output-predict', 'children')],
    [Input('rate', 'value')])
def update_output_guess(value):
    if value is None:
        return [f'유효 입력 범위 : [1 ~ 백만]', f'목표 백분위 : ???', f'당첨되려면 아마도 ??? 이상이 필요할거에요~']
    else:
        target_percentile = prob.rate_to_percentile(value)
        pred = prob.predict(target_percentile)
        return [f'', f'목표 백분위 : {target_percentile*100:.8f}+', f'당첨되려면 아마도 {pred} 이상이 필요할거에요~']


if __name__ == '__main__':
    server.run_server(host='0.0.0.0', port=8501, debug=False)
