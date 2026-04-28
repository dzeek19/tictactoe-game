#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║ QUANTUM TIC-TAC-TOE · Rich Terminal UX · RGB Edition ║
║ Minimax + Alpha-Beta Pruning · Verbose Strategic Stream ║
║ 3 Difficulty Levels · Win/Draw/Loss Tracking ║
╚══════════════════════════════════════════════════════════════╝
"""
import time
import random
import math
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.text import Text
from rich.live import Live
from rich.columns import Columns

console = Console()

# ─── RGB palette (Rich markup gradient helpers) ─────────────────────────────
def _rgb(r, g, b):
    return f"rgb({r},{g},{b})"

CYAN_NEON = _rgb(0, 255, 255)
MAGENTA_HOT = _rgb(255, 0, 200)
GOLD = _rgb(255, 215, 0)
GREEN_LIME = _rgb(50, 255, 80)
RED_FIRE = _rgb(255, 60, 30)
PURPLE = _rgb(180, 0, 255)
BLUE_ICE = _rgb(30, 140, 255)
ORANGE = _rgb(255, 140, 0)
WHITE_GLOW = _rgb(230, 230, 255)

X_COLOR = CYAN_NEON
O_COLOR = MAGENTA_HOT
BOARD_GRID = _rgb(80, 80, 120)

# ─── Strategic commentary library (AI voice) ────────────────────────────────
OPENING_REMARKS = [
    "Evaluating the quantum state of the board...",
    "Running minimax tree at depth {d} — {nodes:,} nodes searched.",
    "Alpha-beta pruning cut {pruned}% of branches. Optimal line found.",
    "Identifying forced win sequences and defensive pivots...",
    "Board entropy: {entropy:.3f} — positional tension is {tension}.",
    "Scanning for fork threats, block candidates, and tempo advantages...",
]

MOVE_REASONS = {
    'win': [
        "Executing winning move — checkmate sequence confirmed.",
        "Terminal node detected. Collapsing to victory state.",
        "Win probability: 1.00. No response sufficient for opponent."
    ],
    'block': [
        "Blocking opponent's winning threat — critical defensive move.",
        "Neutralising forced win vector. Threat probability was 0.97.",
        "Opponent had corner fork setup. Intercepting trajectory."
    ],
    'center': [
        "Claiming center — maximizes branching factor by 23%.",
        "Center control: highest utility node in opening theory.",
        "Occupying [4] elevates win probability by +0.18."
    ],
    'corner': [
        "Corner seizure — sets up dual fork opportunity.",
        "Opposite corner strategy initiated. Fork probability: 0.71.",
        "Corner nodes yield 2.3× more terminal win paths than edges."
    ],
    'edge': [
        "Edge placement — only option remaining. Minimizing opponent's forks.",
        "Forced edge. Calculating best damage-limitation move.",
        "All high-utility cells occupied. Selecting least-bad edge."
    ],
    'general': [
        "Minimax depth search complete. Best move selected by expected value.",
        "Nash equilibrium move — no unilateral deviation improves outcome.",
        "Quantum superposition collapsed: this cell maximizes utility."
    ],
}

TAUNT_LINES = [
    "Interesting. You chose {cell}. Suboptimal, but noted.",
    "Move {cell} — courage over strategy. Respect.",
    "Oh, {cell}? That's exactly what I anticipated.",
    "Bold choice, {cell}. My response was precomputed 3 moves ago.",
    "Classic human pattern: {cell}. Predictable. Containable.",
    "You played {cell}. The tree narrows. I see 2 paths to my win from here.",
]

WIN_TAUNTS = [
    "Game resolved. The outcome was statistically inevitable.",
    "Optimal play executed. You played well — I played better.",
    "Checkmate in Tic-Tac-Toe. A rare achievement. Congratulations to me.",
    "The minimax oracle is undefeated. Long may it reign.",
]

LOSE_LINES = [
    "You... won? Recalibrating. You found the optimal line.",
    "Defeat acknowledged. Your pattern-reading exceeded my heuristic.",
    "Impressive. Genuinely. You outplayed a perfect algorithm.",
    "I'll need to examine how this happened. Well played, human.",
]

DRAW_LINES = [
    "Stalemate. Both agents played near-perfectly. Draw by exhaustion.",
    "Board saturated with no terminal state. Quantum draw achieved.",
    "Optimal play from both sides leads here — the draw is the equilibrium.",
]

# ─── Game state ─────────────────────────────────────────────────────────────
EMPTY = 0
X_MARK = 1  # Human (or AI in AI-vs-AI)
O_MARK = 2  # AI

WIN_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
    [0, 4, 8], [2, 4, 6],  # diags
]

# ─── Stats tracking ─────────────────────────────────────────────────────────
stats = {"wins": 0, "losses": 0, "draws": 0, "games": 0}
_pruned_counter = [0]
_nodes_counter = [0]

# ─── Board utils ────────────────────────────────────────────────────────────
def new_board():
    return [EMPTY] * 9

def check_winner(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a], line
    return None, None

def is_full(board):
    return all(c != EMPTY for c in board)

def available(board):
    return [i for i, c in enumerate(board) if c == EMPTY]

def score_terminal(board, depth):
    winner, _ = check_winner(board)
    if winner == O_MARK:
        return 10 - depth
    if winner == X_MARK:
        return depth - 10
    return 0

# ─── Minimax with alpha-beta pruning ────────────────────────────────────────
def minimax(board, depth, alpha, beta, is_maximizing, max_depth=9):
    _nodes_counter[0] += 1
    winner, _ = check_winner(board)
    if winner or is_full(board) or depth >= max_depth:
        return score_terminal(board, depth)

    if is_maximizing:
        best = -math.inf
        for move in available(board):
            board[move] = O_MARK
            val = minimax(board, depth + 1, alpha, beta, False, max_depth)
            board[move] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                _pruned_counter[0] += 1
                break
        return best
    else:
        best = math.inf
        for move in available(board):
            board[move] = X_MARK
            val = minimax(board, depth + 1, alpha, beta, True, max_depth)
            board[move] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                _pruned_counter[0] += 1
                break
        return best

def ai_best_move(board, difficulty="hard"):
    moves = available(board)
    if not moves:
        return None

    _nodes_counter[0] = 0
    _pruned_counter[0] = 0

    # Easy: 40% random, Medium: takes wins/blocks but misses forks, Hard: perfect
    if difficulty == "easy":
        if random.random() < 0.6:
            return random.choice(moves)
    elif difficulty == "medium":
        if random.random() < 0.25:
            return random.choice(moves)

    max_depth = {"easy": 3, "medium": 6, "hard": 9}[difficulty]

    best_score = -math.inf
    best_move = moves[0]
    alpha, beta = -math.inf, math.inf

    # Shuffle to break ties randomly for variety
    random.shuffle(moves)
    for move in moves:
        board[move] = O_MARK
        score = minimax(board, 0, alpha, beta, False, max_depth)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, best_score)

    return best_move

def classify_move(board, move, player):
    """Categorise an AI move for the verbal commentary."""
    # Check for win
    board[move] = player
    w, _ = check_winner(board)
    board[move] = EMPTY
    if w == player:
        return 'win'

    # Check for block
    opp = X_MARK if player == O_MARK else O_MARK
    board[move] = opp
    w, _ = check_winner(board)
    board[move] = EMPTY
    if w == opp:
        return 'block'

    if move == 4:
        return 'center'
    if move in [0, 2, 6, 8]:
        return 'corner'
    return 'edge'

# ─── Board rendering ────────────────────────────────────────────────────────
CELL_ART = {
    EMPTY: (" · ", BOARD_GRID),
    X_MARK: (" ╳╳╳ ", X_COLOR),
    O_MARK: (" ○○○ ", O_COLOR),
}

WIN_CELL_ART = {
    X_MARK: (" ★╳★ ", GOLD),
    O_MARK: (" ★○★ ", GOLD),
}

def render_board(board, winning_line=None):
    """Render a 3×3 board as a Rich Table with RGB colours."""
    tbl = Table(show_header=False, show_edge=True, padding=(0, 0),
                border_style=BOARD_GRID, box=None)
    for _ in range(3):
        tbl.add_column(justify="center", min_width=7)

    for row in range(3):
        cells_text = []
        for col in range(3):
            idx = row * 3 + col
            cell_val = board[idx]
            if winning_line and idx in winning_line:
                art, color = WIN_CELL_ART.get(cell_val, CELL_ART[cell_val])
            else:
                art, color = CELL_ART[cell_val]
            cells_text.append(f"[{color}]{art}[/{color}]")
        tbl.add_row(*cells_text)
        if row < 2:
            tbl.add_row(
                f"[{BOARD_GRID}]{'─'*7}[/{BOARD_GRID}]",
                f"[{BOARD_GRID}]{'─'*7}[/{BOARD_GRID}]",
                f"[{BOARD_GRID}]{'─'*7}[/{BOARD_GRID}]",
            )
    return tbl

def render_number_guide():
    """Small reference table showing cell indices 1-9."""
    tbl = Table(show_header=False, show_edge=True, padding=(0, 1),
                border_style=BOARD_GRID, box=None)
    for _ in range(3):
        tbl.add_column(justify="center", min_width=3)
    for row in range(3):
        tbl.add_row(*[f"[{BOARD_GRID}]{row*3+col+1}[/{BOARD_GRID}]" for col in range(3)])
        if row < 2:
            tbl.add_row(*[f"[{BOARD_GRID}]─[/{BOARD_GRID}]"]*3)
    return tbl

def render_scoreboard():
    t = Table(title="Session Score", title_style=f"bold {GOLD}",
              border_style=BLUE_ICE, show_edge=True)
    t.add_column("Result", style=f"bold {WHITE_GLOW}")
    t.add_column("Count", justify="right")
    t.add_row(f"[{GREEN_LIME}]Wins[/{GREEN_LIME}]", f"[{GREEN_LIME}]{stats['wins']}[/{GREEN_LIME}]")
    t.add_row(f"[{RED_FIRE}]Losses[/{RED_FIRE}]", f"[{RED_FIRE}]{stats['losses']}[/{RED_FIRE}]")
    t.add_row(f"[{GOLD}]Draws[/{GOLD}]", f"[{GOLD}]{stats['draws']}[/{GOLD}]")
    t.add_row(f"[dim]Games[/dim]", f"[dim]{stats['games']}[/dim]")
    return t

# ─── Streaming commentary ────────────────────────────────────────────────────
def stream_text(text, color=WHITE_GLOW, delay=0.018, newline=True):
    """Print text character-by-character for dramatic AI 'thinking' effect."""
    for ch in text:
        console.print(f"[{color}]{ch}[/{color}]", end="", highlight=False)
        time.sleep(delay)
    if newline:
        console.print()

def ai_commentary(board, move, difficulty):
    """Verbose strategic stream — the AI narrates its thought process."""
    nodes = _nodes_counter[0]
    total = nodes + _pruned_counter[0] * 3  # rough branch estimate
    pruned_pct = int(min(95, (_pruned_counter[0] / max(1, total)) * 100 + 30))
    depth_map = {"easy": 3, "medium": 6, "hard": 9}
    d = depth_map[difficulty]
    entropy = round(random.uniform(0.3, 1.8), 3)
    tension = random.choice(["HIGH", "MODERATE", "CRITICAL", "LOW"])

    # Opening remark
    opener = random.choice(OPENING_REMARKS).format(
        d=d, nodes=max(nodes, 12), pruned=pruned_pct,
        entropy=entropy, tension=tension
    )
    console.print(f"\n [{BLUE_ICE}]◈ AI ANALYSIS[/{BLUE_ICE}]", highlight=False)
    stream_text(f" {opener}", color=BLUE_ICE, delay=0.014)

    # Move classification + reason
    kind = classify_move(board[:], move, O_MARK)
    reason = random.choice(MOVE_REASONS.get(kind, MOVE_REASONS['general']))
    stream_text(f" [{CYAN_NEON}]→ Cell {move+1}: {reason}[/{CYAN_NEON}]", color=CYAN_NEON, delay=0.016)

    if difficulty == "hard":
        stream_text(f" [{PURPLE}]Minimax depth={d} | nodes={nodes:,} | pruned≈{pruned_pct}%[/{PURPLE}]",
                    color=PURPLE, delay=0.010)

def human_taunt(cell):
    line = random.choice(TAUNT_LINES).format(cell=cell)
    stream_text(f"\n [{ORANGE}]AI: {line}[/{ORANGE}]", color=ORANGE, delay=0.022)

# ─── Win / Draw / Loss animations ───────────────────────────────────────────
def _flash_banner(text, color, flashes=4):
    for i in range(flashes):
        c = color if i % 2 == 0 else "dim white"
        console.print(Panel(f"[bold {c}]{text}[/bold {c}]", style=c), highlight=False)
        time.sleep(0.15)

def victory_animation(winner_mark, board, winning_line):
    console.print(render_board(board, winning_line))
    if winner_mark == O_MARK:
        _flash_banner(" ★ AI WINS ★ ", RED_FIRE)
        stream_text(f"\n {random.choice(WIN_TAUNTS)}", color=RED_FIRE, delay=0.025)
    elif winner_mark == X_MARK:
        _flash_banner(" ★ YOU WIN ★ ", GREEN_LIME)
        stream_text(f"\n {random.choice(LOSE_LINES)}", color=GREEN_LIME, delay=0.025)
    else:
        _flash_banner(" ◈ DRAW ◈ ", GOLD)
        stream_text(f"\n {random.choice(DRAW_LINES)}", color=GOLD, delay=0.025)

# ─── Single game ────────────────────────────────────────────────────────────
def play_game(difficulty="hard", human_first=True):
    board = new_board()
    human = X_MARK
    ai = O_MARK
    current = X_MARK if human_first else O_MARK
    stats["games"] += 1

    console.print(Rule(f"[bold {CYAN_NEON}]GAME {stats['games']}[/bold {CYAN_NEON}]"))
    console.print(Columns([
        Panel(render_board(board),
              title=f"[{CYAN_NEON}]You = ╳[/{CYAN_NEON}] [{MAGENTA_HOT}]AI = ○[/{MAGENTA_HOT}]",
              style=BOARD_GRID),
        Panel(render_number_guide(), title="[dim]Cell Guide[/dim]", style=BOARD_GRID),
        Panel(render_scoreboard(), title="[dim]Score[/dim]", style=BOARD_GRID),
    ]))

    while True:
        winner, winning_line = check_winner(board)
        if winner:
            if winner == human:
                stats["wins"] += 1
            elif winner == ai:
                stats["losses"] += 1
            victory_animation(winner, board, winning_line)
            return winner

        if is_full(board):
            stats["draws"] += 1
            victory_animation(None, board, None)
            return None

        if current == human:
            # Human turn
            while True:
                try:
                    raw = Prompt.ask(f"\n[bold {GREEN_LIME}]Your move (1-9)[/bold {GREEN_LIME}]")
                    cell = int(raw.strip()) - 1
                    if cell < 0 or cell > 8:
                        raise ValueError
                    if board[cell] != EMPTY:
                        console.print(f"[{RED_FIRE}] Cell {cell+1} is taken. Choose another.[/{RED_FIRE}]")
                        continue
                    break
                except (ValueError, KeyboardInterrupt):
                    console.print(f"[{RED_FIRE}] Enter a number 1–9.[/{RED_FIRE}]")

            board[cell] = human
            human_taunt(cell + 1)

        else:
            # AI turn
            console.print(f"\n [{MAGENTA_HOT}]AI is computing...[/{MAGENTA_HOT}]", highlight=False)
            t0 = time.time()
            move = ai_best_move(board, difficulty)
            elapsed = time.time() - t0
            ai_commentary(board, move, difficulty)
            board[move] = ai
            console.print(f" [{MAGENTA_HOT}]AI places ○ at cell {move+1} [{elapsed*1000:.0f}ms][/{MAGENTA_HOT}]",
                          highlight=False)

        # Refresh display
        winner, winning_line = check_winner(board)
        console.print()
        console.print(Columns([
            Panel(render_board(board, winning_line if winner else None),
                  title=f"[{CYAN_NEON}]You = ╳[/{CYAN_NEON}] [{MAGENTA_HOT}]AI = ○[/{MAGENTA_HOT}]",
                  style=BOARD_GRID),
            Panel(render_number_guide(), title="[dim]Cell Guide[/dim]", style=BOARD_GRID),
            Panel(render_scoreboard(), title="[dim]Score[/dim]", style=BOARD_GRID),
        ]))

        current = O_MARK if current == X_MARK else X_MARK

# ─── Main menu ──────────────────────────────────────────────────────────────
def show_title():
    title_lines = [
        f"[bold {CYAN_NEON}] ██████╗ ██╗ ██╗ █████╗ ███╗ ██╗████████╗██╗ ██╗███╗ ███╗[/bold {CYAN_NEON}]",
        f"[bold {BLUE_ICE}] ██╔═══╝ ██║ ██║██╔══██╗████╗ ██║╚══██╔══╝██║ ██║████╗ ████║[/bold {BLUE_ICE}]",
        f"[bold {PURPLE}] ██║ ███╗██║ ██║███████║██╔██╗ ██║ ██║ ██║ ██║██╔████╔██║[/bold {PURPLE}]",
        f"[bold {MAGENTA_HOT}] ██║ ██║██║ ██║██╔══██║██║╚██╗██║ ██║ ██║ ██║██║╚██╔╝██║[/bold {MAGENTA_HOT}]",
        f"[bold {RED_FIRE}] ╚██████╔╝╚██████╔╝██║ ██║██║ ╚████║ ██║ ╚██████╔╝██║ ╚═╝ ██║[/bold {RED_FIRE}]",
        f"[{GOLD}] ╚═════╝ ╚═════╝ ╚═╝ ╚═╝╚═╝ ╚═══╝ ╚═╝ ╚═════╝ ╚═╝ ╚═╝[/{GOLD}]",
        "",
        f"[bold {GOLD}] T I C · T A C · T O E[/bold {GOLD}] "
        f"[{PURPLE}]Minimax · Alpha-Beta · Verbose Strategic AI[/{PURPLE}]",
    ]
    console.print(Panel("\n".join(title_lines), style=BOARD_GRID, padding=(1, 2)))

def main():
    show_title()

    while True:
        console.print(Rule(f"[bold {GOLD}]MAIN MENU[/bold {GOLD}]"))
        console.print(f" [{GREEN_LIME}]1[/{GREEN_LIME}] — Play vs AI")
        console.print(f" [{BLUE_ICE}]2[/{BLUE_ICE}] — Change difficulty")
        console.print(f" [{GOLD}]3[/{GOLD}] — View scoreboard")
        console.print(f" [{RED_FIRE}]q[/{RED_FIRE}] — Quit\n")

        difficulty = "hard"
        human_first = True

        choice = Prompt.ask(
            f"[bold {WHITE_GLOW}]Choice[/bold {WHITE_GLOW}]",
            choices=["1", "2", "3", "q"],
            default="1"
        )

        if choice == "q":
            console.print(Panel(
                f"[bold {GOLD}]Thanks for playing. The quantum oracle bows out.[/bold {GOLD}]",
                style=GOLD))
            break

        elif choice == "3":
            console.print(Panel(render_scoreboard(), style=BOARD_GRID, title="[dim]Session Score[/dim]"))
            Prompt.ask("Press Enter to continue")
            continue

        elif choice == "2":
            difficulty = Prompt.ask(
                f"[{PURPLE}]Select difficulty[/{PURPLE}]",
                choices=["easy", "medium", "hard"],
                default="hard"
            )
            console.print(f"[{PURPLE}]Difficulty set to: {difficulty.upper()}[/{PURPLE}]")
            continue

        elif choice == "1":
            # Pre-game options
            difficulty = Prompt.ask(
                f"[{PURPLE}]Difficulty[/{PURPLE}]",
                choices=["easy", "medium", "hard"],
                default="hard"
            )
            go_first_choice = Prompt.ask(
                f"[{CYAN_NEON}]Do you want to go first? (X)[/{CYAN_NEON}]",
                choices=["y", "n"],
                default="y"
            )
            human_first = (go_first_choice == "y")

            console.print(f"\n[{BLUE_ICE}]Difficulty: [bold]{difficulty.upper()}[/bold] | "
                         f"You go: [bold]{'FIRST (╳)' if human_first else 'SECOND (╳)'}[/bold][/{BLUE_ICE}]")

            play_game(difficulty=difficulty, human_first=human_first)

            again = Confirm.ask(f"\n[bold {GOLD}]Play again?[/bold {GOLD}]", default=True)
            if not again:
                console.print(Panel(
                    f"[bold {GOLD}]Session complete. "
                    f"[{GREEN_LIME}]W:{stats['wins']}[/{GREEN_LIME}] "
                    f"[{RED_FIRE}]L:{stats['losses']}[/{RED_FIRE}] "
                    f"[{GOLD}]D:{stats['draws']}[/{GOLD}][/bold {GOLD}]",
                    style=GOLD))
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n[{GOLD}]Interrupted. Quantum oracle offline.[/{GOLD}]")
