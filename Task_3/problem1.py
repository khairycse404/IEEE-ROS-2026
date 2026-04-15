import random

def pick_winner(names):
    if not names:
        return "No participants"
    winner = random.choice(names)
    return f"Congratulations {winner}!"

print(pick_winner(["Ali", "Omar", "Sara"]))