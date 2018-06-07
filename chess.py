#!/usr/bin/env python 

from movevalidator.movevalidator import MoveValidator


def main():
    print("-----------------------------------------")
    print("           Chess PGN Generator           ")
    print("-----------------------------------------")

    validator = MoveValidator()

    while True:
        move = input(validator.get_move_number() + " ")
        if not validator.add_move(move):
            print("Invalid move")


if __name__ == '__main__':
    main()
