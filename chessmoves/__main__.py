from chessmoves.movevalidator import MoveValidator


def main():
    print("-----------------------------------------")
    print("           Chess PGN Generator           ")
    print("-----------------------------------------")

    validator = MoveValidator()

    while True:
        move = input(validator.get_move_number() + " ")

        if move == "save":
            folder = input("Save location: ")
            validator.save_game(folder)
            break

        if not validator.add_move(move):
            print("Invalid move")
            print(validator.get_board_position())




if __name__ == '__main__':
    main()
