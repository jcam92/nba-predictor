import streamlit as st
import requests

st.set_page_config(page_title="NBA Betting Predictor", layout="centered")
st.title("\U0001F3C0 NBA Playoff Betting Predictor")

API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"

# --- Fetch data from Odds API ---
def fetch_odds_data():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "regions": "us",
        "markets": "player_points,player_assists,player_rebounds,h2h,spreads,totals",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return []

# --- Display game and player props ---
def display_odds():
    data = fetch_odds_data()

    if not data:
        st.warning("No odds data available at the moment.")
        return

    for game in data[:5]:  # show up to 5 games for mobile usability
        teams = game.get("teams", ["Unknown", "Unknown"])
        commence_time = game.get("commence_time", "Unknown time")
        bookmakers = game.get("bookmakers", [])

        st.markdown("---")
        st.subheader(f"{teams[0]} vs {teams[1]}")
        st.caption(f"Start Time: {commence_time}")

        for bookmaker in bookmakers:
            st.markdown(f"**Bookmaker:** {bookmaker.get('title', 'N/A')}")
            markets = bookmaker.get("markets", [])

            for market in markets:
                market_key = market.get("key", "")
                outcomes = market.get("outcomes", [])

                if market_key.startswith("player_"):
                    st.markdown(f"**Market:** {market_key.replace('_', ' ').title()}")
                    for outcome in outcomes:
                        name = outcome.get("name", "N/A")
                        price = outcome.get("price", "-")
                        point = outcome.get("point", "")
                        st.markdown(f"- **{name}**: {point} @ {price}")

                elif market_key in ["h2h", "spreads", "totals"]:
                    st.markdown(f"**Market:** {market_key.title()}**")
                    for outcome in outcomes:
                        name = outcome.get("name", "N/A")
                        price = outcome.get("price", "-")
                        point = outcome.get("point", "")
                        st.markdown(f"- {name}: {point} @ {price}")

# --- Run app ---
display_odds()

st.markdown("---")
st.caption("Data provided by The Odds API | Streamlined for mobile viewing")
