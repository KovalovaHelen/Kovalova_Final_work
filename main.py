
import random
from enum import IntEnum
from typing import Optional

import os


def cls():
    os.system("cls" if os.name == "nt" else "clear")


class TicTacToe:
    class _Player(IntEnum):
        X = 0b01
        O = 0b10

    _PLAYER_NAME = {
        _Player.X: "X",
        _Player.O: "O",
    }
    _playground: int
    _ai_player: _Player
    _player: _Player
    _combinations = (
        # Строки
        *(tuple((j, i) for i in range(0, 3)) for j in range(0, 3)),
        # Столбцы
        *(tuple((i, j) for i in range(0, 3)) for j in range(0, 3)),
        # Диагонали
        tuple((i, i) for i in range(0, 3)),
        ((0, 2), (1, 1), (2, 0)),
    )

    def __init__(self):
        self.playground = 0
        self._ai_player = random.choice((self._Player.X, self._Player.O))
        self._player = 0b11 ^ self._ai_player

    def _print_playground(self):
        cls()
        for bitshift in range(0, 18, 2):
            end = "\n" if bitshift % 6 == 4 else ""
            player = self._get_field_value(bitshift)
            cell_value = self._PLAYER_NAME.get(player, " ")
            print(f"[{cell_value}]", end=end)

    def _get_field_value(self, idx: int) -> Optional[_Player]:
        value = self.playground >> idx & 0b11
        return self._Player(value) if value else None

    def _own_cell(self, player: _Player, x: int, y: int):
        if min(x, y) < 0 or max(x, y) >= 3:
            raise IndexError("Неверный выбор клетки")
        idx = (x * 3 + y) * 2
        if owned_by := self._get_field_value(idx):
            raise KeyError(f"Клетка занята игроком", self._PLAYER_NAME[owned_by])
        self.playground |= player << idx

    def _check_win(self) -> Optional[_Player]:
        for combination in self._combinations:
            players = {self._get_field_value((x * 3 + y) * 2) for x, y in combination}
            if None not in players and len(players) == 1:
                return players.pop()

    def _engage_ai(self):
        chances = []
        for combination in self._combinations:
            players = [self._get_field_value((x * 3 + y) * 2) for x, y in combination]
            if None not in players:
                continue
            chance = players.count(self._ai_player) - players.count(self._player)
            idx_to_set = combination[players.index(None)]
            chances.append((chance, idx_to_set))
        if sum(x[0] for x in chances) == 0:
            idx_to_set = random.choice(chances)
        else:
            idx_to_set = max(chances, key=lambda x: x[0])
        self._own_cell(self._ai_player, *idx_to_set[1])

    def _get_player_choice(self):
        while True:
            try:
                user_choice = input(
                    f"Вы играете за {self._PLAYER_NAME[self._player]}, выберите клетку в формате x, y: "
                )
                x, y = user_choice.split(",")
                x, y = int(x), int(y)
                self._own_cell(self._player, x - 1, y - 1)
                break
            except ValueError:
                print("Ведено не число")
            except IndexError as e:
                print(*e.args)
            except KeyError as e:
                print(*e.args)

    def _play_loop(self):
        current_player = self._Player.X
        for _ in range(9):
            if self._player == current_player:
                self._print_playground()
                self._get_player_choice()
            else:
                self._engage_ai()
            if winner := self._check_win():
                print(f"Победитель: {self._PLAYER_NAME[winner]}")
                break
            current_player = 0b11 ^ current_player
        else:
            print("Победила дружба!")

    def play(self):
        try:
            self._play_loop()
        except KeyboardInterrupt:
            exit()


def main():
    game = TicTacToe()
    game.play()


if __name__ == "__main__":
    main()
