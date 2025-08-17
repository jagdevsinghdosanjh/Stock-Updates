import plotly.graph_objects as go # noqa

def annotate_chart(fig, df):
    last_close = df['Close'].iloc[-1]
    fig.add_annotation(x=df.index[-1], y=last_close,
                       text="🔥 Agni Zone", showarrow=True,
                       arrowhead=2, font=dict(color="red"))
