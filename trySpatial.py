import plotly.express as px

# Load data
df = px.data.gapminder()

# Create the plot
fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     animation_frame="year",
                     projection="natural earth")

# Show the plot
fig.show()
