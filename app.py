from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

def load_ghg_emissions_data():
    """Loads GHG emissions data."""
    data_df = pd.read_csv("static/data/GHG_emissions_by_sector.csv")
    print(data_df)
    return pd.read_csv("static/data/GHG_emissions_by_sector.csv")

def prepare_ghg_emissions_bar_chart_data(data_df):
    """Prepares data for the GHG emissions horizontal bar chart."""
    # Exclude the 'Total' row
    data_df = data_df[data_df['Year'] != 'Total (tCO2e)']
    # Reshape the DataFrame for Plotly Express
    # 'Year' column has sector names, and the headers of other columns are actual years
    df_melted = data_df.melt(id_vars='Sector', var_name='Year', value_name='Emissions')
    # Convert Emissions to numeric, removing any commas
    df_melted['Emissions'] = pd.to_numeric(df_melted['Emissions'].str.replace(',', ''), errors='coerce')
    # Correctly rename the columns for clarity
    df_melted.columns = ['Sector', 'Year', 'Emissions']
    return df_melted



def create_ghg_emissions_bar_chart(data_df):
    """Creates a horizontal bar chart for GHG emissions data."""
    fig = px.bar(data_df, x="Emissions", y="Year", color='Sector', orientation='h',
                 hover_data={"Year": True, "Emissions": ':.2f', "Sector": True},
                 height=400,
                 title='GHG Emissions by Sector')

    # Update x-axis labels and range
    fig.update_xaxes(
        tickvals=[-100000, -50000, 0, 50000, 100000, 150000, 200000, 250000],
        ticktext=["-100,000", "-50,000", "0", "50,000", "100,000", "150,000", "200,000", "250,000"],
        range=[-100000, 250000]
    )

    return fig




def setup_dash_layout(app, fig_bar_chart):
    """Sets up the layout of the Dash app."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='ghg-emissions-bar-chart', figure=fig_bar_chart)
        ]),
    ], id='ghg-emissions-bar-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_ghg_emissions_data()
    df_melted = prepare_ghg_emissions_bar_chart_data(data_df)

    # Create bar chart
    fig_bar_chart = create_ghg_emissions_bar_chart(df_melted)

    # Setup layout
    setup_dash_layout(app, fig_bar_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
