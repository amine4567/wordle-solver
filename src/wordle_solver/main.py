import json
import random
from functools import reduce
from typing import Dict, List, Set

from .consts import WORD_SIZE


def main():
    eliminated_letters: Set[str] = set()
    known_correctly_placed_letters: Dict[int, str] = dict()
    wrongly_placed_letters: Dict[int, List[str]] = dict()

    first_guess = True

    def handle_correctly_placed_letters(elt: str) -> bool:
        if len(known_correctly_placed_letters) == 0:
            return True

        return reduce(
            lambda x, y: x and y,
            [elt[k] == v for k, v in known_correctly_placed_letters.items()],
        )

    def handle_wrongly_placed_letters(elt: str) -> bool:
        if len(wrongly_placed_letters) == 0:
            return True

        return reduce(
            lambda x, y: x and y,
            [elt[k] not in v_list for k, v_list in wrongly_placed_letters.items()],
        ) and reduce(
            lambda x, y: x and y,
            [
                letter in elt
                for sublist in wrongly_placed_letters.values()
                for letter in sublist
            ],
        )

    def analyze_response(proposed_solution: str, response: List[int]):
        assert len(proposed_solution) == len(response) == WORD_SIZE
        for i, letter in enumerate(proposed_solution):
            # TODO: use match/case
            if response[i] == 0:
                eliminated_letters.add(letter)
            elif response[i] == 1:
                known_correctly_placed_letters[i] = letter
            elif response[i] == 2:
                if i in wrongly_placed_letters:
                    wrongly_placed_letters[i].append(letter)
                else:
                    wrongly_placed_letters[i] = [letter]

    while True:
        with open("src/wordle_solver/resources/words_dictionary.json", "r") as fp:
            en_words = json.load(fp)

        words_of_interest = [elt for elt in en_words.keys() if len(elt) == WORD_SIZE]

        possible_solutions = [
            elt
            for elt in words_of_interest
            if len(set(elt).intersection(eliminated_letters)) == 0
            and handle_correctly_placed_letters(elt)
            and handle_wrongly_placed_letters(elt)
        ]
        print(f"Number of possible solutions: {len(possible_solutions)}")

        proposed_solution = random.choice(possible_solutions)

        if first_guess:
            proposed_solution = "slice"
            first_guess = False

        print(f"random possible solution: {proposed_solution}")

        response = list(map(int, list(input())))

        analyze_response(proposed_solution, response)
