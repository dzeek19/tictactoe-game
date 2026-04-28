# Quantum Tic-Tac-Toe

A feature-rich Tic-Tac-Toe game with an unbeatable AI opponent powered by the Minimax algorithm with Alpha-Beta Pruning. Built with a beautiful terminal UI using Rich.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **3 Difficulty Levels**: Easy, Medium, and Hard (unbeatable)
- **Minimax AI**: Perfect AI opponent using minimax algorithm with alpha-beta pruning
- **Rich Terminal UI**: Beautiful RGB colors, smooth animations, and streaming text effects
- **Strategic Commentary**: AI narrates its thought process with verbose strategic analysis
- **Session Tracking**: Keep track of wins, losses, and draws
- **Choose Your Side**: Play first (X) or let the AI go first

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tictactoe-game.git
cd tictactoe-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python tictactoe.py
```

### Game Options

From the main menu, you can:
1. **Play vs AI** - Start a new game against the AI
2. **Change difficulty** - Adjust AI difficulty (easy/medium/hard)
3. **View scoreboard** - Check your session statistics
4. **Quit** - Exit the game

### Difficulty Levels

- **Easy**: AI makes random moves 40% of the time
- **Medium**: AI makes random moves 25% of the time, otherwise plays optimally
- **Hard**: Perfect play using minimax with alpha-beta pruning (unbeatable!)

## How It Works

### Minimax Algorithm

The AI uses the minimax algorithm with alpha-beta pruning to search the game tree and find the optimal move. This makes the hard difficulty completely unbeatable - the best you can hope for is a draw!

### Alpha-Beta Pruning

Alpha-beta pruning optimizes the minimax algorithm by eliminating branches that won't affect the final decision, significantly reducing the number of nodes evaluated.

## Project Structure

```
tictactoe-game/
├── tictactoe.py      # Main game file
├── requirements.txt  # Python dependencies
├── README.md        # This file
└── .gitignore       # Git ignore file
```

## Requirements

- Python 3.7+
- Rich library (install via `pip install -r requirements.txt`)

## License

MIT License - feel free to modify and distribute!

## Acknowledgments

Built with [Rich](https://github.com/Textualize/rich) library for beautiful terminal output.
