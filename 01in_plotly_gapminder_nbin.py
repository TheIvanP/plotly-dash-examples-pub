#%%
# %% [markdown]

# ---

# # Visualisation with Plotly.express

# [plotly.express](https://plotly.com/python/plotly-express/) is a library for creating interactive visualisations in one statement\
# \
# - Many visualisations are supported out-of-the box: [line](https://plotly.com/python/line-and-scatter/#line-plots-with-plotly-express), [scatter](https://plotly.com/python/line-and-scatter/) or treemaps

# - The output is a plotly graph object json structure plotted browser side by plotly.js
#
#%%
import plotly.express as px

#%%
# %% [markdown]

# ### Dataset

# A [gapminder](https://www.gapminder.org/) dataset comes with plotly.express and is used here for illustration.
#%%
# built-in example DataFrame
df = px.data.gapminder()

# select a year to plot
filtered_df = df[df.year == 2007]


#%%
# %% [markdown]
# ---
### Line chart with axes and legend
# - Axes are auto-labelled with some logic to set sensible units
# - Colors are assigned to legend
# - We can hover to inspect the data at points along the graph

#%%
fig = px.line(
    df.loc[df["continent"] == "Oceania"],
    x="year",
    y="pop",
    color="country",
    hover_name="country",
    title="Population, Oceania 1952 - 2007",
)

# %% [markdown]
# plotly supports multiple [renderes] (https://plotly.com/python/renderers/)
# .show() will attempt to use a sensible default

#%%
fig.show()
# %% [markdown]
# ---
### Legend and navigation
# - We can show both continent and country using color/symbol args
# - Double/shift click on legend to filter
# - We can nagivate the plot using menu on top right
#%%
fig = px.line(
    df,
    x="year",
    y="pop",
    color="continent",
    symbol="country",
    line_group="country",
    hover_name="country",
)
fig.show()

# %% [markdown]
### Stacked bar chart
# - Plot re-renders if we filter the legend
# - Hover to see name of countries

#%%
fig = px.bar(
    df,
    x="year",
    y="pop",
    color="continent",
    hover_name="country",
)
fig.show()

# %% [markdown]
# ---
### Histograms
# - Plotly has built-in binning and cutting for genereating histograms/
# - The labels for the x axis have been automatically rotated to display the country names and sampled to accomodate the full view
# - We can zoom y axis to explore values and see all country names
#%%
fig = px.histogram(
    filtered_df,
    x="country",
    y="pop",
    color="continent",
    title="Histogram of population sizes 2007",
)
fig.update_xaxes(categoryorder="total ascending")
fig.show()
#%%
fig = px.histogram(
    df,
    x="year",
    y="gdpPercap",
    color="continent",
    barmode="stack",
    barnorm="fraction",
    title="Relative change of population size 1953 - 2007",
)
fig.show()

# %% [markdown]
# ---
### Parametizing plot
# -  We pass the DataFrame to the plotting method, and column names are used to parametize the plot
# - [This particular visualisation](https://youtu.be/FACK2knC08E?t=2678) was made famous by [Prof. Hans Rosling](https://en.wikipedia.org/wiki/Hans_Rosling)
#%%
#%%
# scatterplot, taking DataFrame as first arg
# plot data from columns in graph
fig = px.scatter(
    filtered_df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    title="2007 Gross Domestic Product and life expectancy",
)
fig.show()

# %% [markdown]
# ---
### Hireachical plots
# - Plotly supports multiple types - [sunburst](https://plotly.com/python/sunburst-charts/) and [treemap](https://plotly.com/python/treemaps/)
# - Sunburst graphs are related to ['Diagram of causes of mortality'](https://commons.wikimedia.org/wiki/File:Nightingale-mortality.jpg) by [Florence Nightingale](https://en.wikipedia.org/wiki/Florence_Nightingale), English social reformer, statistician and the founder of modern nursing.
# - `path` arg sets the order and components in the hierachy
#%%
#%%
# %% [markdown]
# sunburst
#%%
fig = px.sunburst(
    filtered_df,
    path=["continent", "country"],
    values="gdpPercap",
    title="GDP divided by population size",
)
fig.show()
#%%
# %% [markdown]
# treemap
#%%
fig = px.treemap(
    filtered_df,
    path=["continent", "country"],
    values="gdpPercap",
    title="2007 Gross Domestic Product divided by population size",
)
fig.show()
#%%
# %% [markdown]
# ---
### Modifying the layout
# - The graph object is a json datastructure which is parsed by plotly.js for the browser side rendering
# ```
# Figure({
#            'data': [{'branchvalues': 'total',
#            'customdata': array([[1.58341221e+0 <...> ': {'tracegroupgap': 0},
#            'margin': {'t': 60},
#            'template': '...'}
#            })
# ```
# - We can modify this to e.g. remove the legend or change aspects of the plot
# - Plotly has built-in methods for setting most attributes saving us having to traverse the json directly
#%%
fig = px.treemap(
    filtered_df,
    path=["continent", "country"],
    values="gdpPercap",
    color="pop",
    title="2007 Gross Domestic Product divided by population size<br>Highlight population size",
)
fig = fig.update_coloraxes(showscale=False)
fig.show()
# %%
# %% [markdown]
# ---
### Facet plots
# - We can plot multiple elements 'facets' of one dataframe
# - Sub-plots are labelled automatically


#%%
fig = px.line(
    df,
    x="year",
    y="pop",
    facet_col="continent",
    color="country",
    symbol="country",
    line_group="country",
    hover_name="country",
)
fig.show()

# %% [markdown]
# ---
### Faceted trend 'thumbnail' recipe
# - Facet plots can be used to produce trendline plots
# - We set `facet_col` to `"country"` and `color` to `"continent"`
# - Plotly will complain about size of plot vs number of facets.
# - To fix this we set `facet_row_spacing` and `height`
# - We still have issues here:
# -- y axis scale is synchronized across facets. This is good for compparing between countries
# -- We can remove sync on y axis to see change scaled to the facet itself
# -- All the labels are creating a lot of noise

#%%
fig = px.line(
    df,
    x="year",
    y="pop",
    facet_col="country",
    color="continent",
    facet_col_wrap=4,
    facet_row_spacing=0.006,
    hover_name="country",
    height=3200,
    width=1000,
)
fig.show()
# %% [markdown]
# ### Facet plot with relative change and cleaned up axis labels


#%%
# Set facet_row_spacing
fig = px.line(
    df,
    x="year",
    y="pop",
    facet_col="country",
    color="continent",
    facet_col_wrap=4,
    facet_row_spacing=0.006,
    facet_col_spacing=0.002,
    hover_name="country",
    height=3200,
    width=1000,
)
# don't sync y axes
fig.update_yaxes(matches=None, ticklabelposition="inside")

# For facet plot titles, keep only the name of the country
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

from plotly.graph_objects import layout as go_layout

for axis in fig.layout:
    if type(fig.layout[axis]) == go_layout.YAxis:
        fig.layout[axis].title.text = ""
    if type(fig.layout[axis]) == go_layout.XAxis:
        fig.layout[axis].title.text = ""

fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))

fig.show()
#%%
