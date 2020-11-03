import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# import plotly.figure_factory as ff

import prob


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


n = 10
array_len, n_event, PDF, norm_PDF, max_PDF, CDF = prob.create_probability_table(n)
# print(norm_PDF)
# hist_data = [norm_PDF]
group_labels = ['prob']


# fig_pdf = px.bar(PDF, x='숫자 합', y='경우의 수')
fig_pdf = px.bar(PDF)
fig_pdf.update_layout(
    xaxis=dict(tickmode='linear')
)

fig_cdf = px.bar(CDF)
fig_cdf.update_layout(
    xaxis=dict(tickmode='linear')
)

# fig2 = ff.create_distplot(hist_data, group_labels)
fig_norm_pdf = px.line(norm_PDF)

bar_x = [i for i in range(array_len)]
bar_y = [0] * array_len
bar_y[27] = max_PDF
fig_norm_pdf.add_bar(x=bar_x, y=bar_y)

################################################################################
from dash.dependencies import Input, Output


ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

app.layout = html.Div(children=[
        html.Center([
            html.H1(children='당첨 숫자 예측'),

            html.Div(children='경쟁률을 입력하세요.'),

            dcc.Input(
                id='competition ratio',
                type='number',
                placeholder='2.0'
            ),

            dcc.Graph(
                id='graph pdf',
                figure=fig_pdf
            ),

            dcc.Graph(
                id='graph cdf',
                figure=fig_cdf
            ),

            dcc.Graph(
                id='example-graph',
                figure=fig_norm_pdf
            )
        ])
    ] +
    [
        dcc.Input(
            id="input_{}".format(_),
            type=_,
            placeholder="input type {}".format(_),
        )
        for _ in ALLOWED_TYPES
    ]
    + [html.Div(id="out-all-types")]
)

@app.callback(
    Output("out-all-types", "children"),
    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
)

def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))
################################################################################
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8501, debug=True)


# pip install dash==1.16.3 plotly pandas scipy
# http://127.0.0.1:8050/
# http://meta.nctts.net:8050/
