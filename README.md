# 🔍 Reverse Turing Detective

A fun game where you need to spot the human among AI-generated responses!

## Game Concept

You interview 5 suspects. 4 are AI-generated, 1 is human-written. Can you detect who's really human?

### Mechanics
- Ask questions to suspects
- Limited to 10 turns
- Vote on who you think is human
- Try to identify human patterns vs AI patterns

## Setup

### Requirements
- Python 3.7+
- Node.js (optional, for serving static files)

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask backend:
```bash
python game_backend.py
```

The server will start on `http://localhost:5000`

3. Open `index.html` in your browser or serve it:
```bash
# Using Python
python -m http.server 8000
# Then visit http://localhost:8000
```

## How to Play

1. Start the game
2. Read the suspect profiles
3. Choose a suspect to question
4. Select a question from the available options
5. Read their response carefully
6. Ask more questions to gather information
7. When you run out of turns or feel confident, cast your vote
8. Choose who you think is the human
9. See if you were right!

## Game Features

- 5 unique suspects with different backgrounds
- 5 different questions to ask
- Randomized human suspect each game
- Distinctive human vs AI response patterns
- Responsive web interface
- Simple REST API backend

## Files

- `game_backend.py` - Flask backend server
- `index.html` - Game UI and client-side logic
- `requirements.txt` - Python dependencies

## Tips for Finding the Human

- Look for natural conversation patterns
- Humans are more likely to be casual, self-aware, and include personal anecdotes
- AI tends to be more structured and formal
- Watch for emotional authenticity
- Notice inconsistencies or over-explanations

## API Endpoints

- `POST /api/game/start` - Start a new game
- `POST /api/game/<game_id>/ask` - Ask a question
- `POST /api/game/<game_id>/vote` - Submit your vote
- `GET /api/questions` - Get available questions

Have fun! 🕵️
