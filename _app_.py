import requests
import streamlit as st
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

# Define the function to fetch NBA odds
def get_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "regions": "us",
        "markets": "player_points,player_assists,player_rebounds",  # Multiple markets
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": "9f3bdc38a31f49ed103ac514d45b15bc"  # API key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure request was successful
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# Define a function to fetch player props for a specific event
def fetch_player_props(event_id):
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds-player-props/{event_id}"
    params = {
        "regions": "us",  # Specify region
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": "9f3bdc38a31f49ed103ac514d45b15bc"  # API key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Ensure request was successful
        player_props = response.json()
        return player_props
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching player props: {e}")
        return None

# Streamlit app setup
st.title("NBA Betting Predictions")

# Fetch odds data
odds_data = get_odds_data()

if odds_data:
    for game in odds_data:
        teams = game['teams']
        st.subheader(f"{teams[0]} vs {teams[1]}")

        for bookmaker in game.get("bookmakers", []):
            st.markdown(f"**Bookmaker: {bookmaker['title']}**")

            for market in bookmaker.get("markets", []):
                st.write(f"**Market: {market['key']}**")  # Show the market type (e.g., player_points)

                for outcome in market.get("outcomes", []):
                    st.write(f"{outcome.get('name', 'Unknown Player')} - "
                             f"Under: {outcome['price']}")

            # If you need to fetch player props, use the event ID
            event_id = game.get('id')  # Make sure this is available
            if event_id:
                player_props = fetch_player_props(event_id)
                if player_props:
                    st.write(f"Player Props for {teams[0]} vs {teams[1]}:")
                    for prop in player_props:
                        st.write(f"{prop['name']} - {prop['market']} - {prop['price']}")
else:
    st.write("No odds data available at the moment.")
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
