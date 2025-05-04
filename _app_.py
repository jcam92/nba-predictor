import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NBA Betting Predictions", layout="centered")

API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api.the-odds-api.com"
}

# --- Helper Functions ---
def get_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "regions": "us",
        "markets": "h2h,spreads,totals,player_points",
        "oddsFormat": "decimal",
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def display_game(game):
    teams = game['home_team'], game['away_team']
    st.subheader(f"{teams[1]} @ {teams[0]}")
    for bookmaker in game['bookmakers']:
        st.markdown(f"**Bookmaker:** {bookmaker['title']}")
        for market in bookmaker['markets']:
            st.markdown(f"**Market:** {market['key'].capitalize()}")
            odds_table = pd.DataFrame(market['outcomes'])
            st.table(odds_table)

# --- App UI ---
st.title("🏀 NBA Betting Predictions")
st.markdown("Get real-time odds and player props for NBA games.")

with st.spinner("Fetching latest data..."):
    try:
        data = get_odds_data()
        if not data:
            st.warning("No game data available.")
        else:
            for game in data[:5]:  # limit to 5 games for mobile usability
                display_game(game)
    except Exception as e:
        st.error("Failed to load data from API.")
        st.exception(e)

st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
