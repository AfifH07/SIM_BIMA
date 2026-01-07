import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(data, column, title):
    """Plot distribusi data"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data[column], kde=True, ax=ax)
    ax.set_title(title)
    return fig
