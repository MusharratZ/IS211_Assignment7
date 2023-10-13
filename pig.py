import random
import argparse
import sys


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll_die(self):
        roll = random.randint(1, 6)
        if roll == 1:
            self.turn_total = 0
        else:
            self.turn_total += roll
            self.score += roll
        return roll

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0


class PigGame:
    def __init__(self, num_players):
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]
        self.current_player = 0
        self.winning_score = 100
        random.seed(0)

    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def play(self):
        while all(player.score < self.winning_score for player in self.players):
            player = self.players[self.current_player]
            print(f"\n{player.name}'s turn")
            while True:
                decision = input(
                    "Enter 'r' to roll or 'h' to hold or 'q' to quit: "
                ).lower()
                if decision == "r":
                    roll = player.roll_die()
                    print(f"Rolled a {roll}")
                    print(
                        f"Turn total: {player.turn_total}, Total score: {player.score}"
                    )
                    if roll == 1:
                        print("Turn over, no points gained.")
                        break
                elif decision == "h":
                    player.hold()
                    print(
                        f"{player.name} held. Turn total: {player.turn_total}, Total score: {player.score}"
                    )
                    break
                elif decision == "q":
                    print("Goodbye!")
                    sys.exit()

                else:
                    print("Invalid input. Enter 'r' to roll or 'h' to hold.")

            if max(player.score for player in self.players) >= self.winning_score:
                winning_players = [
                    player.name
                    for player in self.players
                    if player.score >= self.winning_score
                ]
                print(f"Player(s) {', '.join(winning_players)} wins!")
                break

            self.switch_player()


def main():
    parser = argparse.ArgumentParser(
        description="Play Pig game with a configurable number of players."
    )
    parser.add_argument("--numPlayers", type=int, help="Number of players")
    args = parser.parse_args()

    while True:
        if args.numPlayers is None:
            try:
                num_players = int(input("Enter the number of players (minimum 2): "))
                if num_players < 2:
                    print("Number of players must be at least 2.")
                    continue
            except ValueError as e:
                print(f"Invalid input: {e}")
                continue
        else:
            num_players = args.numPlayers

        game = PigGame(num_players)
        game.play()

        play_again = input("Do you want to play another game? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            sys.exit()


if __name__ == "__main__":
    main()