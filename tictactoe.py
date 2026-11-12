"""Tic-tac-toe for the terminal. Play a friend or the computer."""

from __future__ import annotations

import os
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRID = "\033[90m"

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


def color_enabled() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def paint(text: str, *codes: str) -> str:
    if not color_enabled():
        return text
    return f"{''.join(codes)}{text}{RESET}"


def enable_windows_color() -> None:
    if os.name != "nt" or not color_enabled():
        return
    import ctypes

    kernel = ctypes.windll.kernel32
    handle = kernel.GetStdHandle(-11)
    mode = ctypes.c_uint()
    if kernel.GetConsoleMode(handle, ctypes.byref(mode)):
        kernel.SetConsoleMode(handle, mode.value | 0x0004)


def cell_text(mark: str, number: int) -> str:
    if mark == "X":
        return paint("X", BOLD, CYAN)
    if mark == "O":
        return paint("O", BOLD, MAGENTA)
    return paint(str(number), DIM)


def mark_label(mark: str) -> str:
    return cell_text(mark, 0) if mark in {"X", "O"} else mark


def render(board: list[str]) -> None:
    cells = [cell_text(mark, i + 1) for i, mark in enumerate(board)]
    bar = paint("---+---+---", GRID)
    pipe = paint("|", GRID)
    print()
    for row in range(3):
        a, b, c = cells[row * 3 : row * 3 + 3]
        print(f" {a} {pipe} {b} {pipe} {c} ")
        if row < 2:
            print(bar)
    print()


def say(text: str, *codes: str) -> None:
    print(paint(text, *codes))


def ask_move(board: list[str], mark: str) -> int:
    while True:
        raw = input(f"Player {mark_label(mark)}, pick a square (1-9): ").strip()
        if not raw.isdigit() or not 1 <= int(raw) <= 9:
            say("Enter a number from 1 to 9.", RED)
            continue
        index = int(raw) - 1
        if board[index]:
            say("That square is taken.", YELLOW)
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

    say("Squares are numbered 1-9, left to right, top to bottom.", DIM)
    if vs_computer:
        print(f"You are {mark_label(human)}. The computer is {mark_label(computer)}.")

    while True:
        render(board)
        if vs_computer and turn == computer:
            index = best_move(board, computer)
            say(f"Computer plays {index + 1}.", MAGENTA)
        else:
            index = ask_move(board, turn)
        board[index] = turn

        who = winner(board)
        if who:
            render(board)
            if vs_computer and who == computer:
                say("Computer wins.", YELLOW, BOLD)
            elif vs_computer and who == human:
                say("You win.", GREEN, BOLD)
            else:
                print(f"Player {mark_label(who)} wins.")
            return
        if full(board):
            render(board)
            say("Draw.", YELLOW, BOLD)
            return
        turn = "O" if turn == "X" else "X"


def main() -> None:
    enable_windows_color()
    say("Tic-tac-toe", BOLD, CYAN)
    while True:
        choice = input("Play against the computer? [Y/n] ").strip().lower()
        vs_computer = choice not in {"n", "no"}
        play(vs_computer)
        again = input("Play again? [Y/n] ").strip().lower()
        if again in {"n", "no"}:
            say("Thanks for playing.", DIM)
            return


if __name__ == "__main__":
    main()
