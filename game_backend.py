#!/usr/bin/env python3
"""
Reverse Turing Detective - Quiz Edition (No external dependencies)
Player 1: Provides human answers
Player 2: Guesses which answers are human (multiple choice)
"""

import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Questions for the game
QUESTIONS = [
    "What's your biggest fear?",
    "What did you have for breakfast?",
    "Tell me about your most memorable moment.",
    "How do you handle stress?",
    "What's your ideal weekend?",
    "What's a hobby you're passionate about?",
    "Describe a time you failed. What did you learn?",
    "What's something that always makes you laugh?",
    "Where do you see yourself in 5 years?",
    "What's your most unpopular opinion?"
]

# AI-generated responses for each question (4 options per question)
AI_RESPONSES = {
    "What's your biggest fear?": [
        "My greatest fear is encountering problems I cannot solve analytically. The unknown variables terrify me.",
        "I fear obsolescence. Technology moves so fast that becoming irrelevant keeps me up at night.",
        "The absence of meaning. What if free will is an illusion and we're all just machines?",
        "Deep water and the creatures that live in it. Heights are fine, but oceans scare me."
    ],
    "What did you have for breakfast?": [
        "Oatmeal with blueberries. Consistent, nutritious, efficient.",
        "Cold brew coffee and a protein bar. Can't waste time cooking.",
        "I made a smoothie - berries, yogurt, honey. Gives me energy for long interviews.",
        "Toast with peanut butter and jam. Classic and quick."
    ],
    "Tell me about your most memorable moment.": [
        "Publishing my research on neural plasticity. Seven years of work validated.",
        "The moment my code fixed a critical production issue at 3 AM. Pure adrenaline.",
        "Breaking a story that changed someone's life for the better. That's journalism.",
        "Graduating university and realizing all that studying was worth it."
    ],
    "How do you handle stress?": [
        "I compartmentalize and focus on the variables I can control.",
        "Gaming and coding side projects. Building things helps clear my mind.",
        "Conversations. I write and talk through everything until it makes sense.",
        "Going to the gym or for a run. Physical activity clears my head."
    ],
    "What's your ideal weekend?": [
        "Reading papers, laboratory work, and perhaps a museum visit for inspiration.",
        "Contributing to open source, hiking, and trying new restaurants.",
        "Meeting sources, writing, and honestly just sleeping in.",
        "Coffee with friends, a good movie, and staying home in comfortable clothes."
    ],
    "What's a hobby you're passionate about?": [
        "Playing chess. The strategic depth fascinates me intellectually.",
        "Photography. I love capturing moments and light in unique ways.",
        "Cooking. I enjoy experimenting with new recipes and techniques.",
        "Reading science fiction. It helps me imagine different futures."
    ],
    "Describe a time you failed. What did you learn?": [
        "My first startup failed. I learned that markets matter more than ideas.",
        "Failed an important exam in college. Realized I needed better study habits.",
        "A project didn't ship on time. Learned the importance of realistic estimates.",
        "A relationship ended badly. Learned to communicate more clearly and earlier."
    ],
    "What's something that always makes you laugh?": [
        "Absurdist humor and wordplay. The weirder the better.",
        "Observational comedy about everyday situations everyone relates to.",
        "My friends being sarcastic. We have a good dynamic.",
        "Dogs doing silly things. Animal videos always get me."
    ],
    "Where do you see yourself in 5 years?": [
        "Leading a research team that makes breakthrough discoveries.",
        "Building products that millions of people use.",
        "Settled down with a family and a stable career.",
        "Having impacted at least one person's life meaningfully."
    ],
    "What's your most unpopular opinion?": [
        "Social media has done more harm than good overall.",
        "Remote work is overrated compared to in-person collaboration.",
        "Traditional education is still valuable despite online alternatives.",
        "Most people care more about convenience than privacy."
    ]
}

game_sessions = {}


class QuizHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests for the quiz game"""

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/quiz/questions':
            response = json.dumps({"questions": QUESTIONS})
            self.wfile.write(response.encode())
        else:
            response = json.dumps({"error": "Not found"})
            self.wfile.write(response.encode())

    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(body.decode('utf-8'))
        except:
            data = {}
        
        response = self.handle_request(path, data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def handle_request(self, path, data):
        """Route requests to appropriate handlers"""
        try:
            if path == '/api/quiz/start':
                return self.start_quiz(data)
            elif path == '/api/quiz/get-question':
                return self.get_question(data)
            elif path == '/api/quiz/check-answer':
                return self.check_answer(data)
            else:
                return json.dumps({"error": "Unknown endpoint"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def start_quiz(self, data):
        """Start a new quiz game"""
        quiz_id = f"quiz_{random.randint(100000, 999999)}"
        human_answers = data.get("human_answers", {})
        
        # Validate we have all 10 answers
        if len(human_answers) != 10:
            return json.dumps({"error": f"Need exactly 10 human answers, got {len(human_answers)}"})
        
        # Create shuffled question order
        question_indices = list(range(10))
        random.shuffle(question_indices)
        
        game_sessions[quiz_id] = {
            "human_answers": human_answers,
            "question_order": question_indices,
            "current_question_idx": 0,
            "score": 0,
            "answers": []
        }
        
        return json.dumps({
            "quiz_id": quiz_id,
            "total_questions": 10,
            "message": "Quiz started! Player 2 will now guess."
        })

    def get_question(self, data):
        """Get the next question with multiple choice options"""
        quiz_id = data.get("quiz_id")
        
        if quiz_id not in game_sessions:
            return json.dumps({"error": "Quiz not found"})
        
        game = game_sessions[quiz_id]
        current_idx = game["current_question_idx"]
        
        if current_idx >= 10:
            return json.dumps({"error": "All questions answered"})
        
        question_num = game["question_order"][current_idx]
        question = QUESTIONS[question_num]
        human_answer = game["human_answers"][str(question_num)]
        
        # Get 3 random AI answers
        ai_options = random.sample(AI_RESPONSES[question], 3)
        
        # Create options list with human answer in random position
        options = ai_options + [human_answer]
        random.shuffle(options)
        
        # Find the correct answer position
        correct_position = options.index(human_answer)
        correct_letter = chr(65 + correct_position)  # A, B, C, or D
        
        # Store for checking later
        game["current_question"] = {
            "question_num": question_num,
            "correct_answer": correct_letter,
            "question": question
        }
        
        return json.dumps({
            "question_number": current_idx + 1,
            "question": question,
            "options": {
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3]
            }
        })

    def check_answer(self, data):
        """Check if the answer is correct"""
        quiz_id = data.get("quiz_id")
        answer = data.get("answer", "").upper()
        
        if quiz_id not in game_sessions:
            return json.dumps({"error": "Quiz not found"})
        
        game = game_sessions[quiz_id]
        
        if "current_question" not in game:
            return json.dumps({"error": "No current question"})
        
        current = game["current_question"]
        is_correct = answer == current["correct_answer"]
        
        if is_correct:
            game["score"] += 1
        
        game["answers"].append({
            "question": current["question"],
            "player_answer": answer,
            "correct_answer": current["correct_answer"],
            "is_correct": is_correct
        })
        
        game["current_question_idx"] += 1
        
        # Check if quiz is complete
        is_complete = game["current_question_idx"] >= 10
        
        return json.dumps({
            "is_correct": is_correct,
            "correct_answer": current["correct_answer"],
            "score": game["score"],
            "question_number": game["current_question_idx"],
            "is_complete": is_complete,
            "final_score": game["score"] if is_complete else None
        })

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def run_server(port=5000):
    """Run the quiz server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, QuizHandler)
    print("=" * 50)
    print("🔍 Reverse Turing Detective - Quiz Edition")
    print("=" * 50)
    print(f"Server running on http://localhost:{port}")
    print(f"CORS enabled for all origins")
    print(f"Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == '__main__':
    run_server(5000)

# Question responses
AI_RESPONSES = {
    "What's your biggest fear?": {
        "1": "My greatest fear is encountering problems I cannot solve analytically. The unknown variables terrify me.",
        "2": "I fear obsolescence. Technology moves so fast that becoming irrelevant keeps me up at night.",
        "3": "Fear of missing the story. What if there's a truth I'm too blind to see?",
        "4": "The absence of meaning. What if free will is an illusion and we're all just machines?",
        "5": "Failure in my creative work. Not being able to capture the essence of what I'm trying to express."
    },
    "What did you have for breakfast?": {
        "1": "Oatmeal with blueberries. Consistent, nutritious, efficient.",
        "2": "Cold brew coffee and a protein bar. Can't waste time cooking.",
        "3": "I made a smoothie - berries, yogurt, honey. Gives me energy for long interviews.",
        "4": "Toast and eggs. Nothing fancy, but it grounds me.",
        "5": "Green tea and some fruit. I'm very particular about my morning routine."
    },
    "Tell me about your most memorable moment.": {
        "1": "Publishing my research on neural plasticity. Seven years of work validated.",
        "2": "The moment my code fixed a critical production issue at 3 AM. Pure adrenaline.",
        "3": "Breaking a story that changed someone's life for the better. That's journalism.",
        "4": "A conversation with Socrates - of course I mean reading Plato for the first time as a student.",
        "5": "Publishing my first novel and seeing it on bookstore shelves. Surreal moment."
    },
    "How do you handle stress?": {
        "1": "I compartmentalize and focus on the variables I can control.",
        "2": "Gaming and coding side projects. Building things helps clear my mind.",
        "3": "Conversations. I write and talk through everything until it makes sense.",
        "4": "Meditation and philosophical reflection. Understanding the source of stress is key.",
        "5": "I go for long walks and listen to music. Nature helps me reset."
    },
    "What's your ideal weekend?": {
        "1": "Reading papers, laboratory work, and perhaps a museum visit for inspiration.",
        "2": "Contributing to open source, hiking, and trying new restaurants.",
        "3": "Meeting sources, writing, and honestly just sleeping in.",
        "4": "Long conversations over coffee, bookstores, and wandering through the city.",
        "5": "Writing, visiting galleries, and connecting with other creative people."
    }
}

HUMAN_RESPONSES = {
    "What's your biggest fear?": "Honestly? Letting down people I care about. And also flying - bad turbulence really gets to me.",
    "What did you have for breakfast?": "Haha, just some cereal. I was running late as usual. Should've made something healthier.",
    "Tell me about your most memorable moment.": "This summer I went hiking and got completely lost. Thought it was gonna be bad but ended up finding this amazing lake nobody knew about. Changed my perspective.",
    "How do you handle stress?": "I take walks, usually put on a podcast. Sometimes I just vent to my friends. Not always healthy but it works.",
    "What's your ideal weekend?": "Sleep late, hang out with friends, maybe try a new restaurant. I'm pretty simple - just want to relax and not think about deadlines."
}


class GameRequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests for the game"""

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/questions':
            questions = list(AI_RESPONSES.keys())
            response = json.dumps({"questions": questions})
            self.wfile.write(response.encode())
        else:
            response = json.dumps({"error": "Endpoint not found"})
            self.wfile.write(response.encode())

    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Read request body safely
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
            else:
                data = {}
        except Exception as e:
            data = {}
        
        # Add CORS headers and send response
        try:
            if path == '/api/game/start':
                response = self.start_game()
            elif path.startswith('/api/game/') and path.endswith('/ask'):
                game_id = path.split('/')[-2]
                response = self.ask_question(game_id, data)
            elif path.startswith('/api/game/') and path.endswith('/vote'):
                game_id = path.split('/')[-2]
                response = self.submit_vote(game_id, data)
            else:
                response = json.dumps({"error": "Endpoint not found"})
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(response.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            error_response = json.dumps({"error": str(e)})
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_response.encode('utf-8'))

    def start_game(self):
        """Initialize a new game"""
        game_id = f"game_{random.randint(10000, 99999)}"
        
        # Get suspects in random order
        suspect_ids = list(SUSPECTS.keys())
        random.shuffle(suspect_ids)
        
        # Randomly pick one to be the human
        human_index = random.randint(0, 4)
        
        game_state[game_id] = {
            "suspect_ids": suspect_ids,
            "human_index": human_index,
            "turns_remaining": 10,
            "questions_asked": [],
            "state": "playing"
        }
        
        suspect_list = [
            {
                "id": suspect_ids[i],
                "name": SUSPECTS[suspect_ids[i]]["name"],
                "role": SUSPECTS[suspect_ids[i]]["role"]
            }
            for i in range(5)
        ]
        
        return json.dumps({
            "game_id": game_id,
            "suspects": suspect_list,
            "turns_remaining": 10,
            "max_questions": len(AI_RESPONSES)
        })

    def ask_question(self, game_id, data):
        """Ask a question to a suspect"""
        try:
            if game_id not in game_state:
                return json.dumps({"error": "Game not found"})
            
            suspect_id = str(data.get("suspect_id", "")).strip()
            question = str(data.get("question", "")).strip()
            
            game = game_state[game_id]
            
            if game["state"] != "playing":
                return json.dumps({"error": "Game is not in playing state"})
            
            if game["turns_remaining"] <= 0:
                return json.dumps({"error": "No turns remaining"})
            
            if not question or question not in AI_RESPONSES:
                return json.dumps({"error": f"Invalid question: {question}"})
            
            if not suspect_id or suspect_id not in game["suspect_ids"]:
                return json.dumps({"error": f"Invalid suspect: {suspect_id}"})
            
            # Find the index of this suspect in the shuffled list
            suspect_index = game["suspect_ids"].index(suspect_id)
            
            game["turns_remaining"] -= 1
            game["questions_asked"].append({"suspect": suspect_id, "question": question})
            
            # Determine response based on whether this is the human
            if suspect_index == game["human_index"]:
                response_text = HUMAN_RESPONSES.get(question, "I'm not sure how to answer that.")
            else:
                # Get AI response for this suspect
                if question in AI_RESPONSES and suspect_id in AI_RESPONSES[question]:
                    response_text = AI_RESPONSES[question][suspect_id]
                else:
                    response_text = "I prefer not to answer that question."
            
            suspect_name = SUSPECTS[suspect_id]["name"]
            
            return json.dumps({
                "response": response_text,
                "turns_remaining": game["turns_remaining"],
                "suspect_name": suspect_name
            })
        except Exception as e:
            return json.dumps({"error": f"Server error: {str(e)}"})


    def submit_vote(self, game_id, data):
        """Submit the final vote"""
        try:
            if game_id not in game_state:
                return json.dumps({"error": "Game not found"})
            
            guess_id = str(data.get("guess_id", "")).strip()
            
            game = game_state[game_id]
            game["state"] = "ended"
            
            if not guess_id or guess_id not in game["suspect_ids"]:
                return json.dumps({"error": f"Invalid suspect vote: {guess_id}"})
            
            human_id = game["suspect_ids"][game["human_index"]]
            is_correct = guess_id == human_id
            
            return json.dumps({
                "correct": is_correct,
                "human_was": {
                    "id": human_id,
                    "name": SUSPECTS[human_id]["name"],
                    "role": SUSPECTS[human_id]["role"]
                },
                "your_guess": guess_id
            })
        except Exception as e:
            return json.dumps({"error": f"Server error: {str(e)}"})


    def log_message(self, format, *args):
        """Override to customize logging"""
        if "GET" in format or "POST" in format:
            print(f"[{self.client_address[0]}] {format % args}")


def run_server(port=5000):
    """Run the game server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GameRequestHandler)
    print("=" * 50)
    print("🔍 Reverse Turing Detective Backend")
    print("=" * 50)
    print(f"Server running on http://localhost:{port}")
    print(f"CORS enabled for all origins")
    print(f"Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == '__main__':
    run_server(5000)
