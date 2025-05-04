import requests
import streamlit as st
from dotenv import load_dotenv

# Function to get odds data from the API
def get_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "regions": "us",
        "markets": "player_points,player_assists,player_rebounds",  # Multiple markets
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": "9f3bdc38a31f49ed103ac514d45b15bc"  # Replace with your API key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Streamlit app code
st.title("NBA Betting Predictions")

# Get data from the API
odds_data = get_odds_data()

if odds_data:
    for game in odds_data:
        # Display the game details
        teams = game['teams']
        st.subheader(f"{teams[0]} vs {teams[1]}")

        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**Bookmaker: {bookmaker['title']}**")

            for market in bookmaker.get("markets", []):
                st.write(f"**Market: {market['key']}**")  # Show the market type (e.g., player_points)
                
                for outcome in market.get("outcomes", []):
                    # Display odds for each outcome
                    st.write(f"{outcome['name'] if 'name' in outcome else 'Unknown Player'} - "
                             f"Under: {outcome['price']}")

events = fetch_events()
for event in events[:5]:  # Limit to first 5 events for brevity
    st.subheader(f"{event['home_team']} vs {event['away_team']}")
    odds_data = fetch_player_props(event['id'])
    if odds_data:
        for bookmaker in odds_data.get("bookmakers", []):
            st.markdown(f"**Bookmaker: {bookmaker['title']}**")
            for market in bookmaker.get("markets", []):
                st.markdown(f"*Market: {market['key']}*")
                for outcome in market.get("outcomes", []):
                    label = outcome.get("name", "Unknown Player")  # Try to get the player name
            st.write(f"{label}: {outcome['price']}")
# --- API Setup ---
API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"
BASE_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
params = {
    "regions": "us",
    "markets": "player_points,player_assists,player_rebounds",
    "oddsFormat": "decimal",
    "dateFormat": "iso",
    "apiKey": "9f3bdc38a31f49ed103ac514d45b15bc"
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    st.error(f"API request failed: {e}")
    st.stop()

if not data:
    st.warning("No player prop data available.")
    st.stop()

# Display data for first 5 games
for game in data[:5]:
    teams = game.get("teams", [])
    if len(teams) >= 2:
        st.subheader(f"{teams[0]} vs {teams[1]}")
    else:
        st.subheader("Teams not available")

    for bookmaker in game.get("bookmakers", []):
        st.write(f"### {bookmaker['title']}")
        for market in bookmaker.get("markets", []):
            st.write(f"**Market**: {market['key']}")
            for outcome in market.get("outcomes", []):
                st.write(f"{outcome['name']}: {outcome['price']}")


player_props_params = {
    "regions": "us",
    "oddsFormat": "decimal",
    "dateFormat": "iso",
    "apiKey": API_KEY
}

# --- Helper function to fetch data ---
def fetch_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        return []

# --- Load game odds ---
game_data = fetch_data(BASE_URL, params)

# --- Load player props ---
props_data = fetch_data(PLAYER_PROPS_URL, player_props_params)

# --- Display Results ---
if not game_data:
    st.warning("No game data available.")
else:
    for game in game_data[:5]:
        st.markdown("---")
        teams = game.get("teams", [])
        commence = game.get("commence_time")
        time_str = datetime.fromisoformat(commence).strftime('%Y-%m-%d %H:%M') if commence else "TBD"
        st.subheader(f"{teams[0]} vs {teams[1]}")
        st.caption(f"Start time: {time_str}")

        for bookmaker in game.get("bookmakers", [])[:1]:  # Only show first bookmaker for simplicity
            st.markdown(f"**Odds from {bookmaker['title']}**")
            for market in bookmaker.get("markets", []):
                st.markdown(f"**Market: {market['key'].capitalize()}**")
                for outcome in market.get("outcomes", []):
                    st.write(f"{outcome['name']}: {outcome['price']}")

        # Show player props matching this game
        for prop_game in props_data:
            if set(prop_game.get("teams", [])) == set(game.get("teams", [])):
                st.markdown("**Popular Player Props**")
                for bookmaker in prop_game.get("bookmakers", [])[:1]:
                    for market in bookmaker.get("markets", []):
                        if market["key"] in ["player_points", "player_assists", "player_rebounds"]:
                            st.markdown(f"*{market['key'].replace('_', ' ').title()}*")
                            for outcome in market.get("outcomes", [])[:3]:
                                st.write(f"{outcome['name']}: {outcome['price']}")
                break
