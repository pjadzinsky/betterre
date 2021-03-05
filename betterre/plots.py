"""
Generate a lot of different graphical representations for the same data.
"""
from betterre import sample_df
import plotly.express as px
import plotly.graph_objects as go


def add_point(fig, series, bgcolor, fontcolor):
    """
    Add a point to the fig
    :param fig:
    :param series:
    :return:
    """
    return fig.add_annotation(
        x=series.mean(),
        y=0,
        xref="x",
        yref="y",
        ayref="y",
        text=series.name,
        showarrow=True,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color=fontcolor
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=0,
        ay=2,
        bordercolor=bgcolor,
        borderwidth=2,
        borderpad=4,
        bgcolor=bgcolor,
        opacity=0.8
    )
    # add_annotations(x=data["Honda Civic", "wt"],
    #                 y=data["Honda Civic", "mpg"],
    #                 text="",
    #                 xref="x",
    #                 yref="y",
    #                 showarrow=TRUE,
    #                 arrowcolor='blue',
    #                 arrowhead=1,
    #                 arrowsize=2,
    #                 ax=0,
    #                 ay=0,
    #                 axref="x",
    #                 ayref='y',
    #                 font=list(color='#264E86',
    #                           family='sans serif',
    #                           size=14))
    # fig.add_trace()


def add_histogram(fig, series, color):
    fig.add_trace(go.Histogram(series, color=color))


def plot(df, colors, title, types, format='html'):
    """

    :param df: pd.DataFrame
    :param colors: dict mapping df.columns to colors
    :param title: str
    :param mean_flag:dict mapping df.columns to bool flag
    :return:
    """
    fig = go.Figure()
    for column, color in colors.items():
        type_ = types[column]
        s = df[column]
        if type_ == "marker":
            add_point(fig, s, color, 'white')
        elif type_ == "mean_hist":
            fig.add_trace(go.Histogram(x=[s.mean()], marker_color=color, histnorm='probability', name=column))
        elif type_ == "dist":
            fig.add_trace(go.Histogram(x=s, marker_color=color, histnorm='probability', name=column))

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    fig.update_layout(width=450, height=450, plot_bgcolor='#ffffff', title="Some Property", xaxis_title="cost ($)", )
    fig.update_yaxes(color='white')
    fig.update_xaxes(range=[3, 8])

    if not title.endswith('html'):
        title += f'.{format}'
    if not title.startswith('/tmp/'):
        title = '/tmp/' + title
    fig.write_html(title)


# def mean_and_histograms(df, colors, title, ):
#     fig = go.Figure()

if __name__ == "__main__":
    df = sample_df.fake_df(gammas=[4, 5, 6], col_names=['PM', 'city'], N=100)
    colors = {"PM": "blue", "city": "green"}

    format = 'html'
    plot(df, colors, 'markers', types={'PM': "marker", 'city': "marker"}, format=format)
    plot(df, colors, "marker_dist", types={"PM": "marker", "city": "dist"}, format=format)
    plot(df, colors, "mean_hist", types={"PM": "mean_hist", "city": "mean_hist"}, format=format)
    plot(df, colors, 'dist', types={'PM': "dist", 'city': "dist"}, format=format)
    plot(df, colors, 'mixed', types={'PM': "mean_hist", 'city': "dist", }, format=format)
    #show_means(df)