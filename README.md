# 🔍 Reverse Turing Detective - Quiz Edition

A fun 2-player game where Player 1 answers questions as themselves, and Player 2 tries to identify which answers are human vs AI-generated.

## Game Concept

**The Challenge:** Can you distinguish human answers from AI responses?

- **Player 1** answers 10 questions authentically
- **Player 2** sees multiple choice answers (2 AI + 1 Human) and guesses which is human
- Score: How many did you get right out of 10?

## Game Flow

### Player 1: Provide Answers
1. Answer all 10 questions as yourself
2. Be genuine - this is what Player 2 will try to identify!
3. Pass the device to Player 2

### Player 2: Guess
1. For each question, you'll see 3 options (A, B, C)
2. 2 are AI-generated, 1 is from Player 1
3. Select which one you think is the human answer
4. Get instant feedback
5. Final score: How many did you identify correctly?

## Questions

1. What's your biggest fear?
2. What did you have for breakfast?
3. Tell me about your most memorable moment.
4. How do you handle stress?
5. What's your ideal weekend?
6. What's a hobby you're passionate about?
7. Describe a time you failed. What did you learn?
8. What's something that always makes you laugh?
9. Where do you see yourself in 5 years?
10. What's your most unpopular opinion?

## Setup

### Requirements
- Python 3.7+
- No external dependencies needed!

### Installation

1. **Start the backend:**
```bash
cd c:\Users\tck1wmb\Repos\Hackathon-test
py game_backend.py
```

Server will run on `http://localhost:5000`

2. **Start the web server (new terminal):**
```bash
cd c:\Users\tck1wmb\Repos\Hackathon-test
py -m http.server 8000
```

3. **Open the game:**
```
http://localhost:8000
```

## How It Works

- **Human answers** come directly from Player 1
- **AI options** are pre-generated alternative responses to make it challenging
- **Scoring** is based on how many human answers Player 2 correctly identifies
- **Perfect game** = 10/10 correct identifies

## Gameplay Tips for Player 2

- Look for **specificity and personal details** - humans tend to be more specific
- **AI can be too formal** - check for overly structured responses
- **Emotional authenticity** - genuine human emotion is hard for AI to fake
- **Casual language** - humans use "um," "haha," etc. more often
- **Contradictions** - humans are more self-aware about their own quirks

## Files

- `game_backend.py` - Quiz server (Python HTTP server, no dependencies)
- `index.html` - Game UI
- `requirements.txt` - Documentation (no packages needed!)

## Architecture

- **Backend**: Pure Python built-in HTTP server
- **Frontend**: Vanilla JavaScript
- **Data**: Pre-generated AI responses + real-time Player 1 input
- **Scoring**: Real-time feedback on correct/incorrect guesses

## API Endpoints

- `GET /api/quiz/questions` - Get all 10 questions
- `POST /api/quiz/start` - Start new quiz with Player 1 answers
- `POST /api/quiz/get-question` - Get next multiple choice question
- `POST /api/quiz/check-answer` - Verify Player 2's answer and get score

## Fun Facts

- This is **completely peer-to-peer** - no internet needed, runs locally
- **Zero dependencies** - pure Python standard library
- **Instant feedback** - know immediately if you're right
- **Different every time** - questions are shuffled, options are randomized

Have fun spotting the human! 🕵️
