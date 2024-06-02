import pandas as pd
import plotly.express as px
import plotly.io as pio

# Read the JSON file
file_path = "letterbox.json"
df = pd.read_json(file_path)

# Create a new column for the decade
df['decade'] = (df['releaseYear'] // 10) * 10
df['decade'] = df['decade'].astype(str) + 's'

# Group by decade and count the number of movies for each decade
decade_counts = df['decade'].value_counts().reset_index()
decade_counts.columns = ['decade', 'count']

# Create a pie chart and hide percentages
fig = px.pie(decade_counts, values='count', names='decade', title='Proportion of Movies per Year',
             labels={'decade': 'Decade', 'count': 'Number of Movies'},
             hover_data={'count': True})

# Update hover template to replace "=" with ":"
fig.update_traces(
    hovertemplate='Decade: %{label}<br>Number of Movies: %{value}<extra></extra>'
)

# Hide percentages
fig.update_traces(textinfo='none')
fig.show()
pio.write_html(fig, file='releaseyear_piechart.html')
