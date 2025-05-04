
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/"

def fetch_nba_odds():
    params = {
        "regions": "us",
        "markets": "h2h,spreads,totals,player_points",
        "oddsFormat": "decimal",
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return []

def display_game_odds(games):
    for game in games:
        teams = f"{game['home_team']} vs {game['away_team']}"
        st.subheader(teams)
        st.caption(f"Commence time: {datetime.fromisoformat(game['commence_time'][:-1])}")
        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**{bookmaker['title']}**")
            for market in bookmaker.get("markets", []):
                st.markdown(f"__{market['key'].replace('_', ' ').title()}__")
                for outcome in market.get("outcomes", []):
                    st.write(f"{outcome['name']}: {outcome['price']}")

st.set_page_config(page_title="NBA Betting Predictions", layout="centered")

st.title("🏀 NBA Betting Predictions")
st.markdown("#### Powered by The Odds API")

games = fetch_nba_odds()
if games:
    display_game_odds(games)
else:
    st.warning("No games found or unable to retrieve data.")
