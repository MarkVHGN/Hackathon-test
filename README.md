# 💀 Reverse Turing Detective 💀

A dark, dystopian 2-player detection game where Player 1 answers questions authentically, and Player 2 must identify which responses came from a human mind versus the void of artificial intelligence.

## Game Concept

**The Trial:** Can your human intuition pierce the veil between authentic consciousness and artificial void?

- **Player 1** answers 10 dark questions with brutal honesty
- **Player 2** encounters 3 responses per question (1 human + 2 AI) and must identify the authentic
- **Final Judgment:** Your detection mastery score revealed out of 10

## Game Flow

### Player 1: Seal Your Testimony
1. Answer all 10 inquiries with authentic truth
2. Speak from your deepest mind - this is what Player 2 will hunt
3. Your words will be woven into the void, hidden among the artificial

### Player 2: The Detection Trial
1. For each question, 3 responses await you (A, B, C)
2. One pulses with genuine humanity, two are born from the abyss
3. Your intuition must pierce the veil - select which is human
4. Instant judgment reveals your accuracy
5. The final reckoning: How many detected correctly out of 10?

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
