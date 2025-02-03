from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Load data from JSON file
def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)

# Normalize destination input
def normalize_destination(destination):
    return destination.strip().capitalize()

# Extract intent and entities from user input
def extract_intent_and_entities(user_input, current_destination):
    user_input = user_input.lower()
    if "places to visit" in user_input:
        return "places_to_visit", {}
    elif "restaurants" in user_input:
        cuisine = None
        if "italian" in user_input:
            cuisine = "Italian"
        elif "seafood" in user_input:
            cuisine = "Seafood"
        elif "french" in user_input:
            cuisine = "French"
        elif "indian" in user_input:
            cuisine = "Indian"
        return "restaurants", {"cuisine": cuisine}
    elif "famous foods" in user_input:
        return "famous_foods", {}
    elif "hotels" in user_input:
        price_range = None
        if "$$$" in user_input:
            price_range = "$$$"
        elif "$$" in user_input:
            price_range = "$$"
        elif "$" in user_input:
            price_range = "$"
        return "hotels", {"price_range": price_range}
    elif any(keyword in user_input for keyword in ["what's good", "what is good", "suggest"]):
        return "ambiguous", {}
    else:
        return "unknown", {}

# Generate response based on intent and entities
def generate_response(intent, entities, destination, data):
    if intent == "places_to_visit":
        places = data.get(destination, {}).get("places_to_visit", [])
        if places:
            return "\n".join([f"• {place['name']}: {place['description']}" for place in places])
        else:
            return f"No places to visit found in {destination}."
    elif intent == "restaurants":
        restaurants = data.get(destination, {}).get("restaurants", [])
        cuisine = entities.get("cuisine")
        if cuisine:
            filtered_restaurants = [r for r in restaurants if r["cuisine"].lower() == cuisine.lower()]
            if filtered_restaurants:
                return "\n".join([f"• {r['name']} ({r['cuisine']}): {r['description']} - {r['price_range']}" for r in filtered_restaurants])
            else:
                return f"No {cuisine} restaurants found in {destination}."
        else:
            return "\n".join([f"• {r['name']} ({r['cuisine']}): {r['description']} - {r['price_range']}" for r in restaurants])
    elif intent == "famous_foods":
        foods = data.get(destination, {}).get("famous_foods", [])
        if foods:
            return "\n".join([f"• {food['name']}: {food['description']}" for food in foods])
        else:
            return f"No famous foods found in {destination}."
    elif intent == "hotels":
        hotels = data.get(destination, {}).get("hotels", [])
        price_range = entities.get("price_range")
        if price_range:
            filtered_hotels = [h for h in hotels if h["price_range"] == price_range]
            if filtered_hotels:
                return "\n".join([f"• {h['name']} ({h['rating']} stars): {h['description']} - {h['price_range']}" for h in filtered_hotels])
            else:
                return f"No hotels found in {destination} with price range {price_range}."
        else:
            return "\n".join([f"• {h['name']} ({h['rating']} stars): {h['description']} - {h['price_range']}" for h in hotels])
    elif intent == "ambiguous":
        return "Are you interested in places to visit, restaurants, famous foods, or hotels?"
    else:
        return "I'm not sure what you're asking. Please specify places to visit, restaurants, famous foods, or hotels."

# Route for the homepage
@app.route('/')
def home():
    # Load data and get all available destinations
    data = load_data()
    destinations = ", ".join(data.keys())
    initial_message = f"Welcome to the Travel Chatbot! Choose a destination from the following: {destinations}."
    return render_template('index.html', initial_message=initial_message)

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('user_input')
    session_data = data.get('session_data', {})

    # Check if a destination is already set in the session
    destination = session_data.get('destination')

    if not destination:
        # If no destination is set, assume the user is providing one
        normalized_destination = normalize_destination(user_input)
        if normalized_destination not in load_data():
            return jsonify({"response": f"Sorry, I don't have information about {normalized_destination}. Please choose from the available destinations.", "session_data": {}})
        return jsonify({"response": f"Great! Let's explore {normalized_destination}!", "session_data": {"destination": normalized_destination}})

    # Process the user's query
    intent, entities = extract_intent_and_entities(user_input, destination)
    response = generate_response(intent, entities, destination, load_data())

    # Handle ambiguous input
    if intent == "ambiguous":
        clarification = data.get('clarification')
        if clarification:
            clarified_intent, clarified_entities = extract_intent_and_entities(clarification, destination)
            response = generate_response(clarified_intent, clarified_entities, destination, load_data())
        else:
            return jsonify({"response": response, "session_data": session_data})

    return jsonify({"response": response, "session_data": session_data})

if __name__ == "__main__":
    app.run(debug=True)