
import streamlit as st
import pandas as pd
import requests
from sklearn.linear_model import LogisticRegression
import numpy as np

# Title and Description
st.title("NBA Playoff Betting Predictor")
st.markdown("**Smart picks powered by stats and real-time odds.**")

# Odds API configuration
ODDS_API_KEY = "9f3bdc38a31f49ed103ac514d45b15bc"
SPORT = "basketball_nba"
REGION = "us"
MARKETS = "spreads,h2h,totals"

# Fetch odds
@st.cache_data(ttl=300)
def fetch_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGION,
        "markets": MARKETS,
        "oddsFormat": "decimal"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error("Error fetching odds: " + response.text)
        return None
    return response.json()

# Fake team stats for demonstration purposes
def generate_team_features(team_name):
    np.random.seed(hash(team_name) % 1000000)
    return np.random.rand(1, 5)  # e.g., offensive rating, defense, pace, etc.

# Fake model
model = LogisticRegression()
X_fake = np.random.rand(100, 5)
y_fake = np.random.randint(0, 2, 100)
model.fit(X_fake, y_fake)

# Load odds and make predictions
odds_data = fetch_odds()
if odds_data:
    for game in odds_data:
        home_team = game.get("home_team", "Unknown")
        away_team = None

        # Try to extract away team from outcomes in the first bookmaker
        try:
            outcomes = game["bookmakers"][0]["markets"][0]["outcomes"]
            for team_info in outcomes:
                if team_info["name"] != home_team:
                    away_team = team_info["name"]
                    break
        except (IndexError, KeyError, TypeError):
            away_team = "Unknown"

        st.subheader(f"{away_team} @ {home_team}")

        # Generate predictions
        home_features = generate_team_features(home_team)
        away_features = generate_team_features(away_team)
        home_prob = model.predict_proba(home_features)[0][1]
        away_prob = model.predict_proba(away_features)[0][1]

        prediction = home_team if home_prob > away_prob else away_team
        confidence = round(max(home_prob, away_prob) * 100, 2)

        st.write(f"**Prediction:** {prediction}")
        st.write(f"**Confidence:** {confidence}%")

        # Display betting odds
        for site in game["bookmakers"]:
            st.write(f"**{site['title']}**")
            for market in site["markets"]:
                st.write(f"- *{market['key'].capitalize()}*: {market['outcomes']}")
        st.markdown("---")
