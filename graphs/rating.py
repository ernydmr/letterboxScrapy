import pandas as pd
import plotly.express as px
import plotly.io as pio
import re

# Read the JSON file
file_path = "letterbox.json"
df = pd.read_json(file_path)

# Extract numerical part of the rating and convert to float
df['rating'] = df['rating'].apply(lambda x: float(re.search(r"(\d+\.\d+)", x).group(1)))

# Ensure ratings are sorted in ascending order
ratings_sorted = sorted(df['rating'].unique())

# Create a histogram
fig = px.histogram(df, x='rating', title='Distribution of Movie Ratings',
                   labels={'rating': 'Movie Rating'},
                   category_orders={'rating': ratings_sorted})

# Update hover template to replace "=" with ":" and change count label
fig.update_traces(
    hovertemplate='Movie Rating: %{x}<br>Count of Movies: %{y}<extra></extra>'
)

# Show the plot and save it as HTML
fig.show()
pio.write_html(fig, file='rating_histogram.html')
