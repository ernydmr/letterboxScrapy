import pandas as pd
import plotly.express as px
import plotly.io as pio

# Read the JSON file
file_path = "letterbox.json"
df = pd.read_json(file_path)

# Calculate the length of the cast list
df['length_cast_list'] = df['Cast List'].apply(len)

# Sort the DataFrame by length_cast_list in descending order
df = df.sort_values(by='length_cast_list', ascending=False)

# Create a bar chart
fig = px.bar(df, x='movieName', y='length_cast_list', title='Number of Cast Members per Movie',
             labels={'length_cast_list': 'Length of Cast List', 'movieName': 'Movie Name'},
             hover_data={'movieName': False, 'length_cast_list': False})

# Update hover template
fig.update_traces(hovertemplate='<b>%{x}</b><br>Length of Cast List: %{y}')

# Hide x-axis tick labels
fig.update_layout(xaxis=dict(showticklabels=False))

# Show the plot and save it as HTML
fig.show()
pio.write_html(fig, file='castlist_histogram.html')
