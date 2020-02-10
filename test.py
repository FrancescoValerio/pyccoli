#%%
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")

#%%
fig = go.Figure()
df_half = df[:round(len(df)*0.5)]
df_other = df[round(len(df)*0.5)-1:]
first = True
for i in range(len(df)):
    if first:
        first = False
        fig.add_trace(go.Scatter(x=df.Date[i:i+1], y=df['AAPL.High'][i:i+1], name="AAPL High",line_color='deepskyblue'))
    else:
        fig.add_trace(go.Scatter(x=df.Date[i-1:i+1], y=df['AAPL.High'][i-1:i+1], name="AAPL High",line_color='deepskyblue'))

#fig.add_trace(go.Scatter(x=df_other.Date, y=df_other['AAPL.High'], name="AAPL High",line_color='red'))
fig.update_layout(title_text='Time Series with Rangeslider',
                  xaxis_rangeslider_visible=True)
fig.show()
# %%

from bokeh.plotting import figure, output_file, show

output_file("patch.html")

p = figure(plot_width=400, plot_height=400)

p.multi_line([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]],
             color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)

show(p)

# %%
