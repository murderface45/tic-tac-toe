import os
from typing import NoReturn, Iterable


class GameBoard:
    def __init__(self):
        self.board = list(range(1, 10))

    @staticmethod
    def clear() -> NoReturn:
        os.system('cls' if os.name == 'nt' else 'clear')

    def move(self, player, pos):
        self.board[pos - 1] = player.fig

    def draw_board(self) -> NoReturn:
        self.clear()
        print("-" * 13)
        for i in range(3):
            print("|", self.board[0 + i * 3], "|", self.board[1 + i * 3], "|", self.board[2 + i * 3], "|")
            print("-" * 13)

    def check_fill_board(self) -> bool:
        if all([isinstance(i, str) for i in self.board]):
            return True
        return False


class GameRound:
    def __init__(self, *players):
        self.end_round = False
        self.gb = GameBoard()
        self.players = list(players)

    def turn(self) -> Iterable:
        while True:
            self.players[:] = self.players[::-1]
            yield self.players[1]

    def move(self, player) -> NoReturn:
        while True:
            try:
                inp = int(input(f'{player.name}, enter number 1-9: '))
            except ValueError:
                print('incorrect input')
                continue
            if inp in self.gb.board:
                player.move(inp)
                self.gb.move(player, inp)
                break
            if self.gb.check_fill_board():
                break

    def start(self) -> NoReturn:
        self.gb.draw_board()
        turn_player_gen = self.turn()
        while not self.end_round:
            turn_player = next(turn_player_gen)
            self.move(turn_player)
            self.gb.draw_board()
            if self.gb.check_fill_board():
                print('Draw!')
                self.end_round = True
            if self.check_win(turn_player):
                turn_player.increment_point()
                print(f'{turn_player.name} win!')
                self.end_round = True
        else:
            [i.clear_movelist() for i in self.players]

    @staticmethod
    def check_win(player) -> bool:
        if any([
            all(player.movelist[:3]),
            all(player.movelist[3:6]),
            all(player.movelist[6:]),
            all([player.movelist[0], player.movelist[3], player.movelist[6]]),
            all([player.movelist[1], player.movelist[4], player.movelist[7]]),
            all([player.movelist[2], player.movelist[5], player.movelist[8]]),
            all([player.movelist[0], player.movelist[4], player.movelist[8]]),
            all([player.movelist[2], player.movelist[4], player.movelist[6]]),
        ]):
            return True
        return False


class Player:
    players_count = 1

    def __new__(cls, *args, **kwargs):
        if Player.players_count <= 2:
            return super(Player, cls).__new__(cls)
        else:
            print('No more 2 players')

    def __init__(self, name: str):
        self.name = name
        self.points = 0
        self.movelist = [0 for _ in range(9)]
        self.turn = 1 if Player.players_count == 1 else 0
        self.fig = 'X' if Player.players_count == 1 else 'O'
        Player.players_count += 1

    def move(self, pos: int) -> NoReturn:
        self.movelist[pos - 1] = 1

    def clear_movelist(self) -> NoReturn:
        self.movelist = [0 for _ in range(9)]

    def increment_point(self) -> NoReturn:
        self.points += 1


class Game:
    def __init__(self):
        self.end_game = False
        self.first_player = Player('Kirill')
        self.second_player = Player('Katya')

    def start(self) -> NoReturn:
        while not self.end_game:
            gr = GameRound(self.first_player, self.second_player)
            gr.start()
            new_game = input('Try again? (y/n): ')
            if new_game != 'y':
                self.end_game = True
            print(
                f'{self.first_player.name} ({self.first_player.points}) : ({self.second_player.points}) {self.second_player.name}')


def main() -> NoReturn:
    g = Game()
    g.start()


if __name__ == '__main__':
    main()
