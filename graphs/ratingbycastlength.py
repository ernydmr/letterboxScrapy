import pandas as pd
import plotly.express as px
import plotly.io as pio

# Read the JSON file
file_path = "letterbox.json"
df = pd.read_json(file_path)

# Calculate the length of the cast list
df['length_cast_list'] = df['Cast List'].apply(len)

# Sort by rating values
df = df.sort_values(by='rating')

# Create a scatter plot
fig = px.scatter(df, x='length_cast_list', y='rating', title='Movie Ratings by Length of Cast List',
                 labels={'length_cast_list': 'Length of Cast List', 'rating': 'Movie Rating'})
# Update hover template to replace "=" with ":"
fig.update_traces(
    hovertemplate='Length of Cast List: %{x}<br>Movie Rating: %{y}<extra></extra>'
)

# Show the plot and save it as HTML
fig.show()
pio.write_html(fig, file='castlist_rating_scatter.html')
