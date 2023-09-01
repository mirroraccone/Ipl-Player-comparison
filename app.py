import pandas as pd
import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import matplotlib.pyplot as plt
import plotly.express as px
import time



data=pd.read_csv('cleaned_ipl_batting.csv')
data2=pd.read_csv('cleaned_ipl_bowling.csv')

#!! page config
st.set_page_config(
    page_title="IPL",
    page_icon="🏏",
    # layout="wide",
    initial_sidebar_state="collapsed",
)


progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1)
my_bar.empty()


# st.title(':blue[IPL Player Comparison]')
st.header(':red[IPL Player Comparison]',divider='rainbow')

#!! Player Name Selection
# Player1=selectbox("Select Player 1:",data['unique'].unique(),placeholder="Choose any Player",no_selection_label="")
# st.write(Player1)
Player1 = st.selectbox("Select Player 1:",data["unique"].unique(),index=0)

# Player2=selectbox("Select Player 2:",data['unique'].unique(),placeholder="Choose any Player",no_selection_label="")
# st.write(Player2)
Player2 = st.selectbox("Select Player 2:", data["unique"].unique(),index=0)

#!! Select Divison
Batting_Bowling=st.selectbox('Select Batting or Bowling:',['Batting','Bowling'],key='batting_bowling',index=0,placeholder="Choose Batting or Bowling")
if Batting_Bowling=="Batting":

    #!! Selected Catogories
    comparison_category = st.selectbox("Select Comparison Category:", ["Runs", "Inns", "Mat", "Avg", "SR","NO", "100", "50", "4s", "6s", "BF"],
                                    index=0, key="comparison_category",placeholder='Select any category')
    #!! Year Selection
    selected_year =st.selectbox("Select Year:", [""] + list(data["year"].unique()),placeholder="Choose any Year")
    if selected_year == "":
        st.write("Choose a year or it will show whole carrer stats")
    else:
        st.write("Selected year:", selected_year)


    #!! Get player images
    player1_image_url = data[data["unique"] == Player1]["imaged_url"].values[0]
    player2_image_url = data[data["unique"] == Player2]["imaged_url"].values[0]

    #!! Displayed Image
    col1,col2=st.columns(2)

    with col1:
        st.image(player1_image_url, caption=Player1, use_column_width="always")
    with col2:
        st.image(player2_image_url, caption=Player2, use_column_width="always")

    #!! Comparison Logic
    def compare_players():
        st.subheader(f"Comparison between {Player1} and {Player2}")
        
        if selected_year:
            player1_data = data[(data["unique"] == Player1) & (data["year"] >= int(selected_year))]
            player2_data = data[(data["unique"] == Player2) & (data["year"] >= int(selected_year))]
        else:
            player1_data = data[data["unique"] == Player1]
            player2_data = data[data["unique"] == Player2]

        attributes_to_sum = ["Mat", "Inns", "Runs", "NO", "100", "50", "4s", "6s", "BF"]
        attributes_to_max = ["HS"]
        attributes_to_mean = ["Avg", "SR"]

        Player1_runs = player1_data[attributes_to_sum].sum()["Runs"]
        Player2_runs = player2_data[attributes_to_sum].sum()["Runs"]

        Player1_inns = player1_data[attributes_to_sum].sum()["Inns"]
        Player2_inns = player2_data[attributes_to_sum].sum()["Inns"]

        Player1_no = player1_data[attributes_to_sum].sum()["NO"]
        Player2_no = player2_data[attributes_to_sum].sum()["NO"]

        Player1_century = player1_data[attributes_to_sum].sum()["100"]
        Player2_century = player2_data[attributes_to_sum].sum()["100"]

        Player1_matches = player1_data[attributes_to_sum].sum()["Mat"]
        Player2_matches = player2_data[attributes_to_sum].sum()["Mat"]

        Player1_fours = player1_data[attributes_to_sum].sum()["4s"]
        Player2_fours = player2_data[attributes_to_sum].sum()["4s"]

        Player1_sixes = player1_data[attributes_to_sum].sum()["6s"]
        Player2_sixes = player2_data[attributes_to_sum].sum()["6s"]

        Player1_fifty = player1_data[attributes_to_sum].sum()["50"]
        Player2_fifty = player2_data[attributes_to_sum].sum()["50"]

        Player1_BF = player1_data[attributes_to_sum].sum()["BF"]
        Player2_BF = player2_data[attributes_to_sum].sum()["BF"]

        # Highest score
        Player1_hs = player1_data[attributes_to_max].max()["HS"]
        Player2_hs = player2_data[attributes_to_max].max()["HS"]

        # Average and Strike Rate
        Player1_average = player1_data[attributes_to_mean].mean()["Avg"]
        Player2_average = player2_data[attributes_to_mean].mean()["Avg"]

        Player1_sr = player1_data[attributes_to_mean].mean()["SR"]
        Player2_sr = player2_data[attributes_to_mean].mean()["SR"]

        #!! Display Comparison Results
        st.write(f"Total Matches: {Player1_matches} - {Player2_matches}")
        st.write(f"Total Innings: {Player1_inns} - {Player2_inns}")
        st.write(f"Total Runs: {Player1_runs} - {Player2_runs}")
        st.write(f"Total Strike Rate: {Player1_sr:.2f} - {Player2_sr:.2f}")
        st.write(f"Total Average: {Player1_average:.2f} - {Player2_average:.2f}")
        st.write(f"Total Highest Run: {Player1_hs} - {Player2_hs}")
        st.write(f"Total fity's: {Player1_fifty} - {Player2_fifty}")
        st.write(f"Total Four's: {Player1_fours} - {Player2_fours}")
        st.write(f"Total Sixes: {Player1_sixes} - {Player2_sixes}")
        st.write(f"Total Century: {Player1_century} - {Player2_century}")
        st.write(f"Total Ball Faced: {Player1_BF} - {Player2_BF}")
        st.write(f"Total Not Out: {Player1_no} - {Player2_no}")

        # Call the plotting function
        plot_comparison_graph(player1_data, player2_data, selected_year,comparison_category)

    # Define the function to plot the comparison graph
    def plot_comparison_graph(player1_data, player2_data, selected_year,comparison_category):
        if selected_year:
            player1_data = player1_data[player1_data["year"] >= int(selected_year)]
            player2_data = player2_data[player2_data["year"] >= int(selected_year)]

            print(player1_data)
            print(player2_data)

        fig = px.scatter()

        fig.add_scatter(x=player1_data["year"], y=player1_data[comparison_category], mode="lines+markers", name=Player1,
                        hovertext=player1_data[comparison_category], hoverinfo="text")
        fig.add_scatter(x=player2_data["year"], y=player2_data[comparison_category], mode="lines+markers", name=Player2,
                        hovertext=player2_data[comparison_category], hoverinfo="text")

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Runs",
            title=f"Player Comparison: on {comparison_category} the Over Years",  # Set x-axis range from selected year to 2023
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig)

    compare_button = st.button("Compare", key="compare_button")
    if compare_button:
        # compare_players()

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1)
        my_bar.empty()
        compare_players()

#!! ...........Bowling coding down there...........

else:
    #!! Selected Catogories
    comparison_category = st.selectbox("Select Comparison Category:", ["Wkts","Ov","Inns", "Mat", "Avg","Econ", "SR","BBI","4w", "5w"],
                                    index=0, key="comparison_category",placeholder='Select any category')

    #!! Year Selection
    selected_year =st.selectbox("Select Year:", [""] + list(data["year"].unique()),placeholder="Choose any Year")
    if selected_year == "":
        st.write("Choose a year or it will show whole carrer stats")
    else:
        st.write("Selected year:", selected_year)

    #!! Get player images
    player1_image_url = data[data["unique"] == Player1]["imaged_url"].values[0]
    player2_image_url = data[data["unique"] == Player2]["imaged_url"].values[0]

    #!! Displayed Image
    col1,col2=st.columns(2)

    with col1:
        st.image(player1_image_url, caption=Player1, use_column_width="always")
    with col2:
        st.image(player2_image_url, caption=Player2, use_column_width="always")


        #!! Comparison Logic
    def compare_players():
        st.subheader(f"Comparison between {Player1} and {Player2}")
        
        if selected_year:
            player1_data = data2[(data2["unique"] == Player1) & (data2["year"] == int(selected_year))]
            player2_data = data2[(data2["unique"] == Player2) & (data2["year"] == int(selected_year))]
        else:
            player1_data = data2[data2["unique"] == Player1]
            player2_data = data2[data2["unique"] == Player2]

        attributes_to_sum = ["Mat", "Inns", "Runs", "Ov", "4w", "5w"]
        attributes_to_max = ["BBI"]
        attributes_to_mean = ["Avg", "SR","Econ"]

        Player1_runs = player1_data[attributes_to_sum].sum()["Runs"]
        Player2_runs = player2_data[attributes_to_sum].sum()["Runs"]

        Player1_inns = player1_data[attributes_to_sum].sum()["Inns"]
        Player2_inns = player2_data[attributes_to_sum].sum()["Inns"]

        Player1_ov = player1_data[attributes_to_sum].sum()["Ov"]
        Player2_ov = player2_data[attributes_to_sum].sum()["Ov"]

        Player1_4w = player1_data[attributes_to_sum].sum()["4w"]
        Player2_4w = player2_data[attributes_to_sum].sum()["4w"]

        Player1_matches = player1_data[attributes_to_sum].sum()["Mat"]
        Player2_matches = player2_data[attributes_to_sum].sum()["Mat"]

        Player1_5w = player1_data[attributes_to_sum].sum()["5w"]
        Player2_5w = player2_data[attributes_to_sum].sum()["5w"]

        # Highest score
        Player1_bbi = player1_data[attributes_to_max].max()["BBI"]
        Player2_bbi = player2_data[attributes_to_max].max()["BBI"]

        # Average and Strike Rate
        Player1_average = player1_data[attributes_to_mean].mean()["Avg"]
        Player2_average = player2_data[attributes_to_mean].mean()["Avg"]

        Player1_sr = player1_data[attributes_to_mean].mean()["SR"]
        Player2_sr = player2_data[attributes_to_mean].mean()["SR"]

        Player1_econ = player1_data[attributes_to_mean].mean()["Econ"]
        Player2_econ = player2_data[attributes_to_mean].mean()["Econ"]


        #!! Display Comparison Results
        st.write(f"Total Matches: {Player1_matches} - {Player2_matches}")
        st.write(f"Total Over: {Player1_ov} - {Player2_ov}")
        st.write(f"Total Innings: {Player1_inns} - {Player2_inns}")
        st.write(f"Total Runs: {Player1_runs} - {Player2_runs}")
        st.write(f"Total Average: {Player1_average:.2f} - {Player2_average:.2f}")
        st.write(f"Total Economy: {Player1_econ:.2f} - {Player2_econ:.2f}")
        st.write(f"Total Strike Rate: {Player1_sr:.2f} - {Player2_sr:.2f}")
        st.write(f"Best Bowling Figure: {Player1_bbi} - {Player2_bbi}")
        st.write(f"Total 5w: {Player1_5w} - {Player2_5w}")
        st.write(f"Total 4w: {Player1_4w} - {Player2_4w}")


        # Call the plotting function
        plot_comparison_graph(player1_data, player2_data, selected_year,comparison_category)

    # Define the function to plot the comparison graph
    def plot_comparison_graph(player1_data, player2_data, selected_year,comparison_category):
        if selected_year:
            player1_data = player1_data[player1_data["year"] == int(selected_year)]
            player2_data = player2_data[player2_data["year"] == int(selected_year)]


        fig = px.scatter()

        fig.add_scatter(x=player1_data["year"], y=player1_data[comparison_category], mode="lines+markers", name=Player1,
                        hovertext=player1_data[comparison_category], hoverinfo="text")
        fig.add_scatter(x=player2_data["year"], y=player2_data[comparison_category], mode="lines+markers", name=Player2,
                        hovertext=player2_data[comparison_category], hoverinfo="text")

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Runs",
            title=f"Player Comparison: on {comparison_category} Over the Years",
            xaxis=dict(tickmode='linear', dtick=1),  # Set the tick mode to linear and dtick to 1 to show only whole years
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig)

    compare_button = st.button("Compare", key="compare_button")
    if compare_button:
        # compare_players()

        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1)
        my_bar.empty()
        compare_players()

        

#!! CSS Styling
with open('style.css')as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)


home_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
# background-image: url("https://c4.wallpaperflare.com/wallpaper/416/929/240/cricket-4k-desktop-background-wallpaper-preview.jpg");
background: #00F260;  /* fallback for old browsers */
background: -webkit-linear-gradient(to right, #0575E6, #00F260);  /* Chrome 10-25, Safari 5.1-6 */
background: linear-gradient(to right, #0575E6, #00F260); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
background-size: cover;
background-repeat: no-repeat;
background-position: center;

}}
</style>
"""

st.markdown(home_bg_img,unsafe_allow_html=True)
