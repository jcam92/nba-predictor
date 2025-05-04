import streamlit as st
import requests

API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"
BASE_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba"

st.set_page_config(page_title="NBA Odds & Props", layout="centered")
st.title("🏀 NBA Odds & Player Props")

# ---- Helper Functions ----
def fetch_team_odds():
    url = f"{BASE_URL}/odds"
    params = {
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Team odds request failed: {e}")
        return []

def fetch_player_props():
    url = f"{BASE_URL}/player-props"
    params = {
        "regions": "us",
        "markets": "player_points,player_assists,player_rebounds",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Player props request failed: {e}")
        return []

# ---- Display Odds ----
team_odds_data = fetch_team_odds()
player_props_data = fetch_player_props()

if not team_odds_data:
    st.warning("No team odds data available at the moment.")

for game in team_odds_data[:5]:  # Limit for mobile usability
    teams = game.get("teams", ["Unknown", "Unknown"])
    commence = game.get("commence_time", "")
    st.subheader(f"{teams[0]} vs {teams[1]}")
    st.caption(f"Start time: {commence}")

    for bookmaker in game.get("bookmakers", []):
        st.markdown(f"**Bookmaker:** {bookmaker['title']}")
        for market in bookmaker.get("markets", []):
            st.markdown(f"*Market:* {market['key']}")
            for outcome in market.get("outcomes", []):
                st.write(f"{outcome['name']}: {outcome['price']}")
    st.divider()

# ---- Display Player Props ----
if player_props_data:
    st.header("🏅 Player Props")
    for game in player_props_data[:5]:
        teams = game.get("teams", ["Team A", "Team B"])
        st.subheader(f"{teams[0]} vs {teams[1]}")
        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**Bookmaker:** {bookmaker['title']}")
            for market in bookmaker.get("markets", []):
                st.markdown(f"*Market:* {market['key']}")
                for outcome in market.get("outcomes", []):
                    name = outcome.get("name", "Player")
                    price = outcome.get("price", "N/A")
                    st.write(f"{name}: {price}")
        st.divider()
else:
    st.warning("No player props data available at the moment.")
