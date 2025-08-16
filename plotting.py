import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Creates a scatter plot with a DOTTED RED regression line and returns base64 data URI (PNG)
# Ensures file size < ~100kB by using small figure + PNG optimization.

def scatter_with_regression(x, y, xlabel: str, ylabel: str, title: str = "") -> str:
    x = np.asarray(x).reshape(-1, 1)
    y = np.asarray(y)
    # Fit linear regression
    model = LinearRegression().fit(x, y)
    x_line = np.linspace(x.min(), x.max(), 100).reshape(-1, 1)
    y_line = model.predict(x_line)

    fig = plt.figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(x, y)
    ax.plot(x_line, y_line, linestyle=':', color='red')  # dotted red
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    data = base64.b64encode(buf.getvalue()).decode('ascii')
    uri = f"data:image/png;base64,{data}"
    # If too big, downscale once
    if len(data) > 100_000:
        fig = plt.figure(figsize=(3.2, 2.4), dpi=90)
        ax = fig.add_subplot(111)
        ax.scatter(x, y)
        ax.plot(x_line, y_line, linestyle=':', color='red')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        buf2 = BytesIO()
        fig.tight_layout()
        fig.savefig(buf2, format='png', bbox_inches='tight')
        plt.close(fig)
        data = base64.b64encode(buf2.getvalue()).decode('ascii')
        uri = f"data:image/png;base64,{data}"
    return uri
