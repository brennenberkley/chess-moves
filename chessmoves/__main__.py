from chessmoves.movevalidator import MoveValidator


def main():
    print("-----------------------------------------")
    print("           Chess PGN Generator           ")
    print("-----------------------------------------")

    # Collect info about the game
    white = input("White player: ").strip()
    while white == "":
        white = input("Please enter the white player's name: ").strip()

    black = input("Black player: ").strip()
    while black == "":
        black = input("Please enter the black player's name: ").strip()

    event = input("Event: ").strip()
    site = input("Site (i.e. New York City, NY USA): ").strip()
    date = input("Date (YYYY.MM.DD): ").strip()
    round = input("Round: ").strip()

    validator = MoveValidator(white, black, event, site, date, round)

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
