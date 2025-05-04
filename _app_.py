import streamlit as st
import requests
from datetime import datetime

API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"
TEAM_ODDS_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
PLAYER_PROPS_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds-player-props"

st.set_page_config(page_title="NBA Odds & Player Props", layout="wide")
st.title("\U0001F3C0 NBA Betting Predictions & Props")


def get_team_odds():
    try:
        params = {
            "regions": "us",
            "markets": "spreads,totals",
            "oddsFormat": "decimal",
            "apiKey": API_KEY
        }
        response = requests.get(TEAM_ODDS_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Team odds request failed: {e}")
        return []


def get_player_props():
    try:
        params = {
            "regions": "us",
            "oddsFormat": "decimal",
            "apiKey": API_KEY
        }
        response = requests.get(PLAYER_PROPS_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Player props request failed: {e}")
        return []


team_odds_data = get_team_odds()
player_props_data = get_player_props()

if not team_odds_data:
    st.warning("No team odds data available.")
else:
    st.header("\U0001F3C6 Team Odds")
    for game in team_odds_data[:5]:
        teams = game["teams"]
        commence_time = datetime.fromisoformat(game["commence_time"]).strftime("%b %d, %H:%M")
        st.subheader(f"{teams[0]} vs {teams[1]} - {commence_time}")

        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**Bookmaker:** {bookmaker['title']}")
            for market in bookmaker.get("markets", []):
                st.markdown(f"- **Market:** {market['key']}")
                for outcome in market.get("outcomes", []):
                    st.write(f"  - {outcome['name']}: {outcome['price']}")

if not player_props_data:
    st.warning("No player prop data available.")
else:
    st.header("\U0001F464 Player Props")
    for game in player_props_data[:3]:  # limit for mobile-friendliness
        teams = game["teams"]
        st.subheader(f"{teams[0]} vs {teams[1]}")
        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**Bookmaker:** {bookmaker['title']}")
            for market in bookmaker.get("markets", []):
                if market['key'] in ["player_points", "player_assists", "player_rebounds"]:
                    st.markdown(f"- **Market:** {market['key']}")
                    for outcome in market.get("outcomes", [])[:5]:
                        st.write(f"  - {outcome.get('name', 'Unknown')}: {outcome['price']}")
