# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

spacex_options = []
spacex_options.append({'label': 'All Sites', 'value': 'ALL'})

spacex_df_sites = spacex_df["Launch Site"].drop_duplicates()
spacex_df_sites = spacex_df_sites.to_frame()


for i, row in spacex_df_sites.iterrows():
    spacex_options.append({'label':str(row[0]), 'value': str(row[0])})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                        options=spacex_options,
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range

                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload]),

                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df_all = spacex_df[['Launch Site', "class"]]
        filtered_df_all_sum = filtered_df_all.groupby("Launch Site")["class"].sum()
        
        filtered_df_all_sum_new = filtered_df_all_sum.to_frame().rename(columns={"class": "class"})
        filtered_df_all_sum_new["Launch Site"] = filtered_df_all_sum_new.index
        
        fig = px.pie(filtered_df_all_sum_new, values='class', 
        names='Launch Site', 
        title='All class')
        return fig
    else:
        
        #Option 1:
        #filtered_df_selected = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        #filtered_df_selected_count = filtered_df_selected['class'].value_counts().to_frame(name="Count")

        #filtered_df_selected_count["Launch Site"] = filtered_df_selected_count.index.map(lambda x: filtered_df_selected[filtered_df_selected["class"] == x]["Launch Site"].iloc[0])
        #print(filtered_df_selected_count)
        
        #Option 2:
        filtered_df_selected = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        filtered_df_selected_count = filtered_df_selected['class'].value_counts()
        
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df_selected_count, values='count', 
        names='count', 
        title='All class')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))


def get_scatter_plot(entered_site, input_payload):
    if entered_site == 'ALL':
        filtered_df_all_payload = spacex_df[['Payload Mass (kg)', "class", "Booster Version Category"]]

        fig_scatter = px.scatter(data_frame=filtered_df_all_payload, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        
        return fig_scatter  

    else:
        if int(input_payload[0]) == min_payload:
            print("no payload specified")
            filtered_df_selected = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
            filtered_df_selected_site_payload = filtered_df_selected[['Payload Mass (kg)', "class", "Booster Version Category"]]

            fig_scatter = px.scatter(data_frame=filtered_df_selected_site_payload, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        else:
            print("input min payload: " + str(input_payload[0]))
            filtered_df_selected = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
            filtered_df_filtered_site_payload = filtered_df_selected[
                    (filtered_df_selected['Payload Mass (kg)']>=input_payload[0])
                    & (filtered_df_selected['Payload Mass (kg)']<=max_payload)
                ]
            
            filtered_df_selected_site_payload = filtered_df_filtered_site_payload[['Payload Mass (kg)', "class", "Booster Version Category"]]

            fig_scatter = px.scatter(data_frame=filtered_df_selected_site_payload, x="Payload Mass (kg)", y="class", color="Booster Version Category")

        return fig_scatter  


# Run the app
if __name__ == '__main__':
    app.run_server()

