import pandas as pd
import plotly.express as px
import plotly.io as pio

# Read the JSON file
file_path = "letterbox.json"
df = pd.read_json(file_path)

# Group by directors and list their movies
df['film'] = df['movieName']
df['count'] = 1  # Set each film count to 1

# Create the treemap
fig = px.treemap(df, path=[px.Constant('All Directors'), 'directorName', 'film'], values='count',
                 title='Movies per Director',
                 labels={'directorName': 'Director Name', 'film': 'Movie', 'count': 'Movie Count'})

# Use hovertemplate to hide ID and Parents information
fig.update_traces(
    hovertemplate='<b>%{label}</b><br>Movie Count: %{value}<extra></extra>'
)

# Show the plot and save it as HTML
fig.show()
pio.write_html(fig, file='director_film_treemap.html')
