import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch, Pitch, FontManager, arrowhead_marker, Sbopen
from statsbombpy import sb
from goals import add_arrow, plot_goal_sq
from heat_map import get_hm
from formation import get_formation
from shots import get_shots
from passing import get_pass

parser = Sbopen()
fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
                       'rubikmonoone/RubikMonoOne-Regular.ttf')
robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                           'RobotoSlab%5Bwght%5D.ttf')
st.set_page_config(
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.sidebar.image("logo.png", use_column_width=True)

# Initialize session state
if 'matches_data' not in st.session_state:
    st.session_state.matches_data = None

if 'selected_match_id' not in st.session_state:
    st.session_state.selected_match_id = None

if 'possession_id' not in st.session_state:
    st.session_state.possession_id = None

# Function to fetch matches data
def fetch_matches_data():
    matches = parser.competition()
    return matches

# Function to fetch event data for a selected match
def fetch_event_data(selected_match_id):
    df_event, _, _, _ = parser.event(selected_match_id)
    return df_event

# Function to filter data and update session state
def filter_data(selected_match_id):
    st.session_state.selected_match_id = selected_match_id
    df_event = fetch_event_data(selected_match_id)
    st.session_state.possession_id = df_event[df_event['outcome_name'] == 'Goal']['possession'].tolist()

# Main Streamlit app code
matches = fetch_matches_data()
selected_competition = st.sidebar.selectbox("Select a competition", matches['competition_name'].unique().tolist())
selected_season = st.sidebar.selectbox("Select a season", matches[matches['competition_name'] == selected_competition]['season_name'].tolist())

selected_season_id = matches[(matches['competition_name'] == selected_competition) & (matches['season_name'] == selected_season)][['competition_id', 'season_id']]
c_id = selected_season_id['competition_id'].iloc[0]
s_id = selected_season_id['season_id'].iloc[0]

matches = parser.match(competition_id=c_id, season_id=s_id)
matches.sort_values(by='match_week', inplace=True)
matches_dict = {f"GW {match_week} - {home_team} vs {away_team} {home_score}-{away_score}": match_id for match_week, match_id, home_team, away_team, home_score, away_score 
                in zip(matches['match_week'], matches['match_id'], matches['home_team_name'], matches['away_team_name'], 
                    matches['home_score'], matches['away_score'])}

selected_teams = st.sidebar.selectbox("Select a match", list(matches_dict.keys()))

if st.sidebar.button("Filter"):
    selected_match_id = matches_dict[selected_teams]
    print(c_id,s_id)
    filter_data(selected_match_id)

if st.session_state.selected_match_id is not None:
    selected_match_id = st.session_state.selected_match_id
    possession_id = st.session_state.possession_id

    tab1, tab2, tab3, tab4 ,tab5= st.tabs(["Goal Sequence", "Heat Map", "Formation",'Shots','Others'])
    

    with tab1:
        st.write('<h1 style="text-align: center; margin-bottom: 2rem;">Goal Sequence</h1>', unsafe_allow_html=True)
        for id in possession_id:
            plot_goal_sq(fetch_event_data(selected_match_id), id)

    with tab2:
        st.write('<h1 style="text-align: center; margin-bottom: 2rem;">Heat Map</h1>', unsafe_allow_html=True)
        get_hm(fetch_event_data(selected_match_id))

    with tab3:
        st.write('<h1 style="text-align: center; margin-bottom: 2rem;">Formation</h1>', unsafe_allow_html=True)
        get_formation(selected_match_id)

    with tab4:
        st.write('<h1 style="text-align: center; margin-bottom: 2rem;">Shots</h1>', unsafe_allow_html=True)
        get_shots(fetch_event_data(selected_match_id))
        
