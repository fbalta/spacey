# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder='Select a Launch Site here',
                 searchable=True
                ),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P('Payload range (Kg):'),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 1000: '1000', 2000:'2000', 3000:'3000', 4000:'4000', 5000:'5000', 6000:'6000', 7000:'7000', 8000:'8000', 9000:'9000'},
                    value=[0, 10000]
                   ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Filter for successful flights (class=1) and group by launch site
        data = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts().reset_index()
        data.columns = ['Launch Site', 'Success Count']
        figure = px.pie(data, values='Success Count', names='Launch Site', title='Success Distribution Across Launch Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_labels = {1: 'Success', 0: 'Failure'}
        filtered_df['class_labels'] = filtered_df['class'].map(class_labels)
        data = filtered_df['class_labels'].value_counts().reset_index()
        data.columns = ['class', 'count']
        figure = px.pie(data, values='count', names='class', title=f'Success vs. Failure for {entered_site}')
    return figure
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property= 'value')])
def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    figure = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload Mass vs. Outcome')
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server()
