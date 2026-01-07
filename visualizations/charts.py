import plotly.express as px
import plotly.graph_objects as go

def create_bar_chart(data, x, y, title):
    """Membuat bar chart"""
    fig = px.bar(data, x=x, y=y, title=title)
    return fig

def create_line_chart(data, x, y, title):
    """Membuat line chart"""
    fig = px.line(data, x=x, y=y, title=title)
    return fig

def create_pie_chart(data, values, names, title):
    """Membuat pie chart"""
    fig = px.pie(data, values=values, names=names, title=title)
    return fig
