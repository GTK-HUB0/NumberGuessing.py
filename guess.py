import os, math, sys, time, shutil
from datetime import datetime

# --- Basic terminal helpers ---

def supports_ansi():
    if os.name == "nt":
        return 'ANSICON' in os.environ or "WT_SESSION" in os.environ or os.getenv("TERM_PROGRAM")=="vscode"
    return True

ANSI = supports_ansi()

def color(text, code):
    return f"\033[{code}m{text}\033[0m" if ANSI else text

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    # Stays always at top
    print(color("MADE BY GTK", "36").center(70))

def clear_screen_except_banner():
    clear_screen()
    banner()

# --- Guessing engine ---

class Engine:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.attempts = 0
        self.last = None

        # memory for U / R
        self.undo_stack = []
        self.redo_stack = []

        # keeps recent direction bias
        self.bias = 0
        self.dir_memory = []

        # history for final display
        self.history = []

    def save_state(self):
        self.undo_stack.append((
            self.low, self.high, self.attempts, self.bias, list(self.dir_memory)
        ))

    def load_state(self, state):
        self.low, self.high, self.attempts, self.bias, self.dir_memory = state

    def undo(self):
        if not self.undo_stack:
            print(color("Nothing to undo.", "31"))
            return False

        prev = self.undo_stack.pop()
        # push current to redo
        self.redo_stack.append((
            self.low, self.high, self.attempts, self.bias, list(self.dir_memory)
        ))

        self.load_state(prev)
        return True

    def redo(self):
        if not self.redo_stack:
            print(color("Nothing to redo.", "31"))
            return False

        nxt = self.redo_stack.pop()
        # push current to undo
        self.undo_stack.append((
            self.low, self.high, self.attempts, self.bias, list(self.dir_memory)
        ))
        self.load_state(nxt)
        return True

    def guess(self):
        base = (self.low + self.high) // 2

        # bias drift (tiny correction that increases late-game accuracy)
        drift = (self.bias % 3) - 1
        g = base + drift

        if len(self.dir_memory) > 4:
            curve = sum(self.dir_memory[-4:])
            g += max(-1, min(1, curve))

        g = max(self.low, min(self.high, g))
        self.last = g
        return g

    def feed(self, guess, fb):
        self.save_state()
        self.history.append((guess, fb, datetime.now()))

        if fb == 'h':
            self.low = guess + 1
            self.dir_memory.append(1)
            self.bias += 1
        elif fb == 'l':
            self.high = guess - 1
            self.dir_memory.append(-1)
            self.bias -= 1

        self.attempts += 1

    def contradiction(self):
        return self.low > self.high


# --- UI functions ---

def intro():
    clear_screen()
    banner()
    print(color("Commands: H = higher, L = lower, U = undo, R = redo, D = done", "36"))
    input("\nPress Enter to start…")

def prompt_range():
    while True:
        try:
            l = int(input("Lowest number: "))
            h = int(input("Highest number: "))
            if h < l:
                print(color("Highest must be >= lowest.", "31"))
                continue
            return l, h
        except:
            print(color("Invalid number.", "31"))

def show_status(engine):
    print(color(f"Range: {engine.low} to {engine.high} | Attempts: {engine.attempts}", "36"))
    size = engine.high - engine.low + 1
    opt = math.ceil(math.log2(size)) if size > 1 else 0
    print(color(f"Remaining: {size} | Optimal: {opt}", "35"))

def show_history(engine):
    print("\nHistory:")
    for g, fb, ts in engine.history:
        print(f"{ts.strftime('%H:%M:%S')} — {g} → {fb.upper()}")


# --- Main loop ---

def main():
    intro()
    clear_screen_except_banner()

    print(color("Set your range:", "36"))
    low, high = prompt_range()

    engine = Engine(low, high)
    clear_screen_except_banner()

    while True:
        if engine.contradiction():
            print(color("Input contradiction detected.", "31"))
            show_history(engine)
            return

        g = engine.guess()

        print()
        print(color(f"My guess: {g}", "34"))
        show_status(engine)

        cmd = input(color("\n(H/L/U/R/D): ", "36")).strip().lower()

        if cmd not in ('h','l','u','r','d'):
            print(color("Invalid command.", "31"))
            continue

        if cmd == 'u':
            engine.undo()
            clear_screen_except_banner()
            continue

        if cmd == 'r':
            engine.redo()
            clear_screen_except_banner()
            continue

        if cmd == 'd':
            clear_screen()
            banner()
            print(color(f"\nGuessed correctly: {g}", "32"))
            print(color(f"Attempts: {engine.attempts + 1}", "32"))
            engine.history.append((g, 'd', datetime.now()))
            show_history(engine)
            return

        engine.feed(g, cmd)
        clear_screen_except_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
