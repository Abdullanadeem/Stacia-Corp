# Travel Chatbot
A web-based chatbot that helps users plan their trips by providing information about places to visit, restaurants, famous foods, and hotels for specific destinations.
## Features

- Asks the user for a travel destination and handles case-insensitive input.
- Retrieves and displays information about:
  - Places to visit
  - Restaurants (with cuisine preferences)
  - Famous foods
  - Hotels (with price range or rating preferences)
- Handles ambiguous inputs and asks clarifying questions.
- Provides graceful error messages when no information is available.
- Displays an initial list of available destinations.

 Prerequisites

Before running the project, ensure you have the following installed on your system:

1. *Python 3.6+*: Download from [python.org](https://www.python.org/downloads/).
2. *Flask*: A Python web framework.
3. *pip*: Python's package installer (comes with Python).

Setup Instructions

1. *Clone the Repository*:
   ```bash
   git clone https://github.com/your-username/travel-chatbot.git
   cd travel-chatbot

   Install Dependencies
pip install flask

Prepare the Data File :
Ensure the data.json file exists in the root directory.
You can add more destinations and categories to this file as needed.

Running the Application
Start the Flask Server :
python app.py
Open the Application in Your Browser :
Navigate to http://127.0.0.1:5000/ in your web browser.
Interact with the Chatbot :
The chatbot will display a welcome message with a list of available destinations.
Enter a destination and ask for information about places to visit, restaurants, famous foods, or hotels.

Testing the Chatbot
Here are some example interactions:

Initial Message :
Welcome to the Travel Chatbot! Choose a destination from the following: Goa, Paris.

Valid Destination :
Input: Goa
Response: Great! Let's explore Goa!
Places to Visit :
Input: Places to visit in Goa
Response:
• Baga Beach: A popular beach known for its vibrant nightlife.
• Anjuna Market: A famous flea market with unique handicrafts.

Ambiguous Input :
Input: What's good?
Response: Are you interested in places to visit, restaurants, famous foods, or hotels?

No Results Found :
Input: Best Italian restaurants in Goa
Response: No Italian restaurants found in Goa.

Project Structure
TravelChatbot/
│
├── app.py                # Main Flask application
├── chatbot_core.py       # Core chatbot logic (intent extraction, response generation)
├── data.json             # Data file containing destination information
├── templates/
│   └── index.html        # Frontend template for the chatbot interface
├── static/
│   └── css/
│       └── style.css     # CSS for styling the chatbot interface
└── README.md             # This file
