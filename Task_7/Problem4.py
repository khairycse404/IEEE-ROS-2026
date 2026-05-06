class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score


class Team:
    def __init__(self):
        self.members = []

    def add_player(self, player_object):
        self.members.append(player_object)


# Test
t = Team()
t.add_player(Player("Ali", 10))
t.add_player(Player("Omar", 20))

print(len(t.members))