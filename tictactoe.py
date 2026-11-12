"""Tic-tac-toe for the terminal. Play a friend or the computer."""

from __future__ import annotations

LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def winner(board: list[str]) -> str | None:
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


def full(board: list[str]) -> bool:
    return all(board)


def render(board: list[str]) -> None:
    cells = [mark or str(i + 1) for i, mark in enumerate(board)]
    print()
    for row in range(3):
        a, b, c = cells[row * 3 : row * 3 + 3]
        print(f" {a} | {b} | {c} ")
        if row < 2:
            print("---+---+---")
    print()


def ask_move(board: list[str], mark: str) -> int:
    while True:
        raw = input(f"Player {mark}, pick a square (1-9): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            print("Enter a number from 1 to 9.")
            continue
        index = int(raw) - 1
        if board[index]:
            print("That square is taken.")
            continue
        return index


def best_move(board: list[str], mark: str) -> int:
    """Unbeatable move via minimax. Computer plays `mark`."""
    opponent = "O" if mark == "X" else "X"

    def score(current: list[str], depth: int, maximizing: bool) -> int:
        who = winner(current)
        if who == mark:
            return 10 - depth
        if who == opponent:
            return depth - 10
        if full(current):
            return 0

        turn = mark if maximizing else opponent
        best = -11 if maximizing else 11
        for i, cell in enumerate(current):
            if cell:
                continue
            current[i] = turn
            value = score(current, depth + 1, not maximizing)
            current[i] = ""
            if maximizing:
                best = max(best, value)
            else:
                best = min(best, value)
        return best

    choice = -1
    best_score = -11
    for i, cell in enumerate(board):
        if cell:
            continue
        board[i] = mark
        value = score(board, 0, False)
        board[i] = ""
        if value > best_score:
            best_score = value
            choice = i
    return choice


def play(vs_computer: bool) -> None:
    board = [""] * 9
    human = "X"
    computer = "O"
    turn = "X"

    print("Squares are numbered 1-9, left to right, top to bottom.")
    if vs_computer:
        print("You are X. The computer is O.")

    while True:
        render(board)
        if vs_computer and turn == computer:
            index = best_move(board, computer)
            print(f"Computer plays {index + 1}.")
        else:
            index = ask_move(board, turn)
        board[index] = turn

        who = winner(board)
        if who:
            render(board)
            if vs_computer and who == computer:
                print("Computer wins.")
            elif vs_computer and who == human:
                print("You win.")
            else:
                print(f"Player {who} wins.")
            return
        if full(board):
            render(board)
            print("Draw.")
            return
        turn = "O" if turn == "X" else "X"


def main() -> None:
    print("Tic-tac-toe")
    while True:
        choice = input("Play against the computer? [Y/n] ").strip().lower()
        vs_computer = choice not in {"n", "no"}
        play(vs_computer)
        again = input("Play again? [Y/n] ").strip().lower()
        if again in {"n", "no"}:
            print("Thanks for playing.")
            return


if __name__ == "__main__":
    main()
