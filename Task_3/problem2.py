def move_player(position, direction):
    x, y = position
    if direction == "up":
        y += 1
    elif direction == "down":
        y -= 1
    elif direction == "left":
        x -= 1
    elif direction == "right":
        x += 1
    return (x, y)

print(move_player((0, 0), "up"))