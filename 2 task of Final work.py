import random
from enum import Enum
from typing import Type


class StringEnum(str, Enum):
    pass


class Figure(StringEnum):
    Rock = "камень"
    Scissors = "ножницы"
    Paper = "бумага"
    Lizard = "ящерица"
    Spoke = "спок"

    def __gt__(self, other: 'Figure'):
        match (self, other):
            case (Figure.Rock, Figure.Scissors | Figure.Lizard) | \
                 (Figure.Scissors, Figure.Paper | Figure.Lizard) | \
                 (Figure.Paper, Figure.Rock | Figure.Spoke) | \
                 (Figure.Lizard, Figure.Paper | Figure.Spoke) | \
                 (Figure.Spoke, Figure.Scissors | Figure.Rock):
                return True
            case _:
                return False


class Answer(StringEnum):
    Yes = "д"
    No = "н"

    def __bool__(self):
        return self == self.Yes


def get_player_input(question_text: str, question: Type[StringEnum], separator: str) -> StringEnum:
    while True:
        player_input = ""
        try:
            variants = separator.join(x for x in question)
            player_input = input(f"{question_text} ({variants})?\n")
            return question(player_input.lower())
        except ValueError:
            print(f"Неправильный ввод \"{player_input}\"")


def play() -> bool:
    player_choice = get_player_input("Выберите фигуру", Figure, " ")
    computer_choice = random.choice([f for f in Figure])
    print(f"Игрок выбрал: {player_choice}")
    print(f"Компьютер выбрал: {computer_choice}")
    if player_choice == computer_choice:
        print("Ничья!")
    elif player_choice > computer_choice:
        print("Игрок победил!")
    else:
        print("Компьютер победил!")
        return True
    return False


def main():
    player_playing = True
    computer_playing = True
    while player_playing and computer_playing:
        is_computer_won_or_draw = play()
        if not is_computer_won_or_draw or random.randint(0, 1):
            player_playing = get_player_input("Повторим", Answer, "/")
        else:
            print("Компьютер не хочет продолжать игру")


if __name__ == '__main__':
    main()
