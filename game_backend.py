from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Handle preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

# Game state storage
game_state = {}

# Suspect profiles with AI-generated and human-written responses
SUSPECTS = {
    "1": {
        "name": "Dr. Elena Martinez",
        "role": "Neuroscientist",
        "type": "ai"  # Changed to track which is human
    },
    "2": {
        "name": "James Chen",
        "role": "Software Engineer",
        "type": "ai"
    },
    "3": {
        "name": "Sarah Williams",
        "role": "Journalist",
        "type": "ai"
    },
    "4": {
        "name": "Marcus Johnson",
        "role": "Philosopher",
        "type": "ai"
    },
    "5": {
        "name": "Zara Patel",
        "role": "Author",
        "type": "human"
    }
}

# Question responses - AI vs Human patterns
AI_RESPONSES = {
    "What's your biggest fear?": {
        "1": "My greatest fear is encountering problems I cannot solve analytically. The unknown variables terrify me.",
        "2": "I fear obsolescence. Technology moves so fast that becoming irrelevant keeps me up at night.",
        "3": "Fear of missing the story. What if there's a truth I'm too blind to see?",
        "4": "The absence of meaning. What if free will is an illusion and we're all just machines?"
    },
    "What did you have for breakfast?": {
        "1": "Oatmeal with blueberries. Consistent, nutritious, efficient.",
        "2": "Cold brew coffee and a protein bar. Can't waste time cooking.",
        "3": "I made a smoothie - berries, yogurt, honey. Gives me energy for long interviews.",
        "4": "Toast and eggs. Nothing fancy, but it grounds me."
    },
    "Tell me about your most memorable moment.": {
        "1": "Publishing my research on neural plasticity. Seven years of work validated.",
        "2": "The moment my code fixed a critical production issue at 3 AM. Pure adrenaline.",
        "3": "Breaking a story that changed someone's life for the better. That's journalism.",
        "4": "A conversation with Socrates - of course I mean reading Plato for the first time as a student."
    },
    "How do you handle stress?": {
        "1": "I compartmentalize and focus on the variables I can control.",
        "2": "Gaming and coding side projects. Building things helps clear my mind.",
        "3": "Conversations. I write and talk through everything until it makes sense.",
        "4": "Meditation and philosophical reflection. Understanding the source of stress is key."
    },
    "What's your ideal weekend?": {
        "1": "Reading papers, laboratory work, and perhaps a museum visit for inspiration.",
        "2": "Contributing to open source, hiking, and trying new restaurants.",
        "3": "Meeting sources, writing, and honestly just sleeping in.",
        "4": "Long conversations over coffee, bookstores, and wandering through the city."
    }
}

HUMAN_RESPONSES = {
    "What's your biggest fear?": "Honestly? Letting down people I care about. And also flying - bad turbulence really gets to me.",
    "What did you have for breakfast?": "Haha, just some cereal. I was running late as usual. Should've made something healthier.",
    "Tell me about your most memorable moment.": "This summer I went hiking and got completely lost. Thought it was gonna be bad but ended up finding this amazing lake nobody knew about. Changed my perspective.",
    "How do you handle stress?": "I take walks, usually put on a podcast. Sometimes I just vent to my friends. Not always healthy but it works.",
    "What's your ideal weekend?": "Sleep late, hang out with friends, maybe try a new restaurant. I'm pretty simple - just want to relax and not think about deadlines."
}

@app.route('/api/game/start', methods=['POST'])
def start_game():
    """Initialize a new game"""
    game_id = f"game_{random.randint(10000, 99999)}"
    
    # Shuffle suspects
    suspects = list(SUSPECTS.items())
    random.shuffle(suspects)
    
    # Randomly pick one to be the human
    human_index = random.randint(0, 4)
    
    game_state[game_id] = {
        "suspects": dict(suspects),
        "human_index": human_index,
        "turns_remaining": 10,
        "questions_asked": [],
        "state": "playing"
    }
    
    # Return suspect list (without revealing who's human)
    suspect_list = [
        {
            "id": suspects[i][0],
            "name": suspects[i][1]["name"],
            "role": suspects[i][1]["role"]
        }
        for i in range(5)
    ]
    
    return jsonify({
        "game_id": game_id,
        "suspects": suspect_list,
        "turns_remaining": 10,
        "max_questions": len(AI_RESPONSES)
    })

@app.route('/api/game/<game_id>/ask', methods=['POST'])
def ask_question(game_id):
    """Ask a question to a suspect"""
    if game_id not in game_state:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.json
    suspect_id = data.get("suspect_id")
    question = data.get("question")
    
    game = game_state[game_id]
    
    if game["state"] != "playing":
        return jsonify({"error": "Game is not in playing state"}), 400
    
    if game["turns_remaining"] <= 0:
        return jsonify({"error": "No turns remaining"}), 400
    
    if question not in AI_RESPONSES and question not in HUMAN_RESPONSES:
        return jsonify({"error": "Invalid question"}), 400
    
    game["turns_remaining"] -= 1
    game["questions_asked"].append({"suspect": suspect_id, "question": question})
    
    # Get response
    suspects_list = list(game["suspects"].items())
    suspect_number = int(suspect_id) - 1
    
    if suspect_number == game["human_index"]:
        response = HUMAN_RESPONSES[question]
    else:
        response = AI_RESPONSES[question][str(suspect_number + 1)]
    
    return jsonify({
        "response": response,
        "turns_remaining": game["turns_remaining"],
        "suspect_name": suspects_list[suspect_number][1]["name"]
    })

@app.route('/api/game/<game_id>/vote', methods=['POST'])
def submit_vote(game_id):
    """Submit the final vote"""
    if game_id not in game_state:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.json
    guess_id = int(data.get("guess_id"))
    
    game = game_state[game_id]
    game["state"] = "ended"
    
    suspects_list = list(game["suspects"].items())
    human_suspect = suspects_list[game["human_index"]]
    
    is_correct = (guess_id - 1) == game["human_index"]
    
    return jsonify({
        "correct": is_correct,
        "human_was": {
            "id": human_suspect[0],
            "name": human_suspect[1]["name"],
            "role": human_suspect[1]["role"]
        },
        "your_guess": guess_id
    })

@app.route('/api/questions', methods=['GET'])
def get_available_questions():
    """Get all available questions"""
    questions = list(AI_RESPONSES.keys())
    return jsonify({"questions": questions})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Reverse Turing Detective Backend...")
    print("Server running on http://localhost:5000")
    print("CORS enabled for all origins")
    app.run(debug=True, port=5000, host='0.0.0.0')
