import streamlit as st
import requests

# Set up the API key and endpoint
API_KEY = "6d6129a9edmsh3858d3456443973p10d75fjsn476f267803e7"
API_URL = "https://bet36528.p.rapidapi.com/odds_bet365"

# Function to fetch player prop odds
def fetch_player_props(event_id):
    url = f"{API_URL}?eventId={event_id}&oddsFormat=decimal&raw=false"
    headers = {
        "x-rapidapi-host": "bet36528.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch player props data.")
        return None

# Function to fetch game odds
def fetch_game_odds():
    # Placeholder for fetching game data. 
    # You'll need to add the logic to fetch the actual events or game data.
    events = [
        {"id": "id1000001750850531", "teams": ["Cleveland Cavaliers", "Indiana Pacers"]},
        {"id": "id1000001750850532", "teams": ["Los Angeles Lakers", "Boston Celtics"]},
    ]
    return events

# Main function to display the odds
def display_odds():
    st.title("NBA Player Prop Betting Odds")

    events = fetch_game_odds()
    if events is None:
        st.error("No game data available.")
        return

    for event in events:
        st.subheader(f"{event['teams'][0]} vs {event['teams'][1]}")
        odds_data = fetch_player_props(event["id"])
        
        if odds_data is not None:
            for prop in odds_data.get("data", []):
                st.write(f"**{prop.get('market_name', 'No Market Name')}**")
                for selection in prop.get('selections', []):
                    st.write(f"- {selection.get('name')} : {selection.get('odds')}")
        else:
            st.write("No player props available for this game.")

# Call the main function to display data
if __name__ == "__main__":
    display_odds()
    
