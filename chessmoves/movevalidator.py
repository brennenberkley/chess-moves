from copy import deepcopy


class MoveValidator:
    _current_move = int(1)
    _white_can_castle_kingside = True
    _white_can_castle_queenside = True
    _black_can_castle_kingside = True
    _black_can_castle_queenside = True
    _white_can_ep_file = None
    _black_can_ep_file = None
    _last_move = ""

    # First letter indicates color, second letter indicates piece
    _board_position = [
        #  A     B     C     D     E     F     G     H
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],  # 1
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # 2
        [None, None, None, None, None, None, None, None],  # 3
        [None, None, None, None, None, None, None, None],  # 4
        [None, None, None, None, None, None, None, None],  # 5
        [None, None, None, None, None, None, None, None],  # 6
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # 7
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]   # 8
    ]

    def get_board_position(self):
        board = "  +----+----+----+----+----+----+----+----+\n"
        for rank in range(7, -1, -1):
            board += str(rank + 1) + " "
            for file in range(0, 8):
                piece = self._board_position[rank][file]
                piece = piece if piece is not None else "  "
                board += "| " + piece + " "

            board += "|\n"
            board += "  +----+----+----+----+----+----+----+----+\n"
        board += "    a    b    c    d    e    f    g    h   \n"
        return board

    def get_last_move(self):
        return self._last_move

    def add_move(self, move_input):
        move = move_input

        comment = None
        # strip off extra symbols
        if "??" in move:
            comment = "??"
        elif "!!" in move:
            comment = "!!"
        elif "?!" in move:
            comment = "?!"
        elif "!?" in move:
            comment = "!?"

        move = move.replace("x", "")
        move = move.replace("?", "")
        move = move.replace("!", "")
        move = move.replace("+", "")
        move = move.replace("#", "")
        move = move.replace("e.p.", "")
        move = move.replace("ep.", "")
        move = move.replace("ep", "")
        move = move.replace(" ", "")

        # Handle special cases
        if move == "0-0" or move == "o-o" or move == "O-O":
            return self._castle_kingside()
        if move == "0-0-0" or move == "o-o-o" or move == "O-O-O":
            return self._castle_queenside()

        if len(move) < 2:
            return False

        try:
            destination = Square(move[-2:])
        except ValueError:
            return False

        move = move[:-2]

        piece = "p"
        if len(move) > 0:
            if move[0] in "KQRBN":
                piece = move[0]
                move = move.replace(piece, "")

        origin_file = None
        origin_rank = None

        if len(move) == 1:
            if move in "abcdefgh":
                origin_file = "abcdefgh".find(move)
                # Check if the move was en passant
                if self.get_color_to_move() == "white":
                    if destination.file == self._white_can_ep_file and destination.rank == 5:
                        self._move_piece(Square(origin_file, 4), destination)
                        self._move_piece(Square(destination.file, 4), None)
                        self._last_move = "abcdefgh"[origin_file] + "5x" + "abcdefgh"[destination.file] + "6e.p."
                        self._current_move += 1;
                        return True
                else:
                    if destination.file == self._black_can_ep_file and destination.rank == 2:
                        self._move_piece(Square(origin_file, 5), destination)
                        self._move_piece(Square(destination.file, 5), None)
                        self._last_move = "abcdefgh"[origin_file] + "4x" + "abcdefgh"[destination.file] + "3e.p."
                        self._current_move += 1;
                        return True
            elif move in "12345678":
                origin_rank = "12345678".find(move)
            else:
                return False
        elif len(move) == 2:
            try:
                origin = Square(move)
                origin_rank = origin.rank
                origin_file = origin.file
            except ValueError:
                return False

        # Check for a piece on the destination square
        capture = False
        if self._board_position[destination.rank][destination.file]:
            if self._board_position[destination.rank][destination.file][0] == self.get_color_to_move()[0]:
                return False
            else:
                capture = True

        # Process the move
        squares = self._get_origin_squares(piece, destination, capture)
        use_origin_rank = False
        use_origin_file = False

        if len(squares) == 0:
            return False
        elif len(squares) > 1:
            # Filter squares if needed
            ranks = []
            files = []
            duplicate_ranks = False
            duplicate_files = False
            for square in squares:
                if square.rank in ranks:
                    duplicate_ranks = True
                else:
                    ranks.append(square.rank)

                if square.file in files:
                    duplicate_files = True
                else:
                    files.append(square.file)

                if origin_file and origin_file != square.file:
                    squares.remove(square)
                if origin_rank and origin_rank != square.rank:
                    squares.remove(square)

            if not duplicate_files:
                use_origin_file = True
            elif not duplicate_ranks:
                use_origin_rank = True
            else:
                use_origin_file = True
                use_origin_rank = True

        if len(squares) != 1:
            return False

        origin = squares[0]

        old_board = deepcopy(self._board_position)
        self._move_piece(origin, destination)
        if self._king_is_in_check(self.get_color_to_move()):
            # Move puts king in check and is invalid. Undo move
            self._board_position = old_board
            return False

        # Update castling ability if applicable
        if origin.file == 0 and origin.rank == 0:
            self._white_can_castle_queenside = False
        elif origin.file == 7 and origin.rank == 0:
            self._white_can_castle_kingside = False
        elif origin.file == 0 and origin.rank == 7:
            self._black_can_castle_queenside = False
        elif origin.file == 7 and origin.rank == 7:
            self._black_can_castle_kingside = False
        if piece == "K":
            if self.get_color_to_move() == "white":
                self._white_can_castle_kingside = False
                self._white_can_castle_queenside = False
            else:
                self._black_can_castle_kingside = False
                self._black_can_castle_queenside = False

        if self.get_color_to_move() == "white":
            self._white_can_ep_file = None
            if piece == "p" and destination.rank - origin.rank == 2:
                self._black_can_ep_file = destination.file
        else:
            self._black_can_ep_file = None
            if piece == "p" and destination.rank - origin.rank == -2:
                self._white_can_ep_file = destination.file
        self._current_move += 1

        check = self._king_is_in_check(self.get_color_to_move())

        # get the text representation of the move
        last_move = ""
        if piece == "p":
            if capture:
                last_move += "abcdefgh"[origin_file]
        else:
            last_move += piece
            if use_origin_file:
                last_move += "abcdefgh"[origin_file]
            if use_origin_rank:
                last_move += "12345678"[origin_rank]

        if capture:
            last_move += "x"

        last_move += destination.to_string()
        if check:
            last_move += "+"
        if comment:
            last_move += comment
        self._last_move = last_move
        return True

    def get_move_number(self):
        if self._current_move % 2 == 0:
            return str(int(self._current_move / 2)) + "..."
        else:
            move_number = ((self._current_move - 1) / 2) + 1
            return str(int(move_number)) + "."

    def get_color_to_move(self):
        return "black" if self._current_move % 2 == 0 else "white"

    def _king_is_in_check(self, color):
        # Find the king
        king = color[0] + "K"
        square = None
        for rank in range(0, 8):
            for file in range(0, 8):
                if self._board_position[rank][file] == king:
                    square = Square(file, rank)
                    break

        return self._square_is_in_check(color, square)

    def _square_is_in_check(self, color, square):
        for rank in range(0, 8):
            for file in range(0, 8):
                piece = self._board_position[rank][file]
                if piece is not None and piece[0] != color[0]:
                    squares = self._get_attacked_squares(Square(file, rank))
                    for s in squares:
                        if s == square:
                            return True
        return False

    def _get_attacked_squares(self, square):
        coordinates = []
        piece = self._board_position[square.rank][square.file]
        if piece is None:
            return []

        color = piece[0]
        piece = piece[1]
        if piece == "p":
            if color == "w":
                coordinates.append(Coordinate(square.file + 1, square.rank + 1))
                coordinates.append(Coordinate(square.file + 1, square.rank + 1))
            else:
                coordinates.append(Coordinate(square.file + 1, square.rank - 1))
                coordinates.append(Coordinate(square.file + 1, square.rank - 1))
        if piece == "N":
            offsets = [
                [+1, +2],
                [+1, -2],
                [-1, +2],
                [-1, -2],
                [+2, +1],
                [+2, -1],
                [-2, +1],
                [-2, -1]
            ]
            for offset in offsets:
                    coordinates.append(Coordinate(square.file + offset[0], square.rank + offset[1]))
        if piece == "K":
            offsets = [
                [1, 1],
                [1, 0],
                [1, -1],
                [0, 1],
                [0, -1],
                [-1, 1],
                [-1, 0],
                [-1, -1]
            ]
            for offset in offsets:
                    coordinates.append(Coordinate(square.file + offset[0], square.rank + offset[1]))
        if piece == "Q" or piece == "B":
            for offset in range(-7, 8):
                coordinates.append(Coordinate(square.file + offset, square.rank + offset))
                coordinates.append(Coordinate(square.file + offset, square.rank - offset))
        if piece == "Q" or piece == "R":
            for offset in range(-7, 8):
                coordinates.append(Coordinate(square.file, square.rank + offset))
                coordinates.append(Coordinate(square.file + offset, square.rank))
        squares = []
        for coordinate in coordinates:
            try:
                attacked_square = Square(coordinate.file, coordinate.rank)
                if self._open_path(square, attacked_square or piece == "N"):
                    squares.append(attacked_square)
            except ValueError:
                continue
        return squares

    def _get_origin_squares(self, piece, destination, capture):
        valid_squares = []
        possible_squares = []
        color = self.get_color_to_move()

        if piece == "p":
            if capture:
                if color == 'white':
                    if destination.file > 0 and destination.rank > 0:
                        possible_squares.append(Square(destination.file - 1, destination.rank - 1))
                    if destination.file < 7 and destination.rank > 0:
                        possible_squares.append(Square(destination.file + 1, destination.rank - 1))
                else:
                    if destination.file > 0 and destination.rank < 7:
                        possible_squares.append(Square(destination.file - 1, destination.rank + 1))
                    if destination.file < 7 and destination.rank < 7:
                        possible_squares.append(Square(destination.file + 1, destination.rank + 1))
            else:
                if color == 'white':
                    if destination.rank > 0:
                        possible_squares.append(Square(destination.file, destination.rank - 1))
                    if destination.rank == 3:
                        possible_squares.append(Square(destination.file, destination.rank - 2))
                else:
                    if destination.rank < 7:
                        possible_squares.append(Square(destination.file, destination.rank + 1))
                    if destination.rank == 4:
                        possible_squares.append(Square(destination.file, destination.rank + 2))
        if piece == "N":
            offsets = [
                [+1, +2],
                [+1, -2],
                [-1, +2],
                [-1, -2],
                [+2, +1],
                [+2, -1],
                [-2, +1],
                [-2, -1]
            ]
            for offset in offsets:
                try:
                    square = Square(destination.file + offset[0], destination.rank + offset[1])
                    possible_squares.append(square)
                except ValueError:
                    continue
        if piece == "K":
            offsets = [
                [1, 1],
                [1, 0],
                [1, -1],
                [0, 1],
                [0, -1],
                [-1, 1],
                [-1, 0],
                [-1, -1]
            ]
            for offset in offsets:
                try:
                    square = Square(destination.file + offset[0], destination.rank + offset[1])
                    possible_squares.append(square)
                except ValueError:
                    continue
        if piece == "Q" or piece == "B":
            for offset in range(-7, 8):
                try:
                    square = Square(destination.file + offset, destination.rank + offset)
                    possible_squares.append(square)
                except ValueError:
                    pass
                try:
                    square = Square(destination.file + offset, destination.rank - offset)
                    possible_squares.append(square)

                except ValueError:
                    pass
        if piece == "Q" or piece == "R":
            for offset in range(-7, 8):
                try:
                    square = Square(destination.file, destination.rank + offset)
                    possible_squares.append(square)
                except ValueError:
                    pass
                try:
                    square = Square(destination.file + offset, destination.rank)
                    possible_squares.append(square)
                except ValueError:
                    pass

        # Try each origin square
        for square in possible_squares:
            if square == destination:
                continue
            if not self._open_path(square, destination) and piece != "N":
                continue

            if self._board_position[square.rank][square.file] == color[0] + piece:
                valid_squares.append(square)

        return valid_squares

    def _castle_kingside(self):
        color = self.get_color_to_move()
        if color == "white":
            if not self._white_can_castle_kingside:
                return False
            if not self._open_path(Square("h1"), Square("e1")):
                return False
            if (self._square_is_in_check("white", Square("e1"))
                    or self._square_is_in_check("white", Square("f1"))
                    or self._square_is_in_check("white", Square("g1"))):
                return False

            self._move_piece(Square("h1"), Square("f1"))  # Rook
            self._move_piece(Square("e1"), Square("g1"))  # King
            self._white_can_castle_kingside = False
            self._white_can_castle_queenside = False
        else:
            if not self._black_can_castle_kingside:
                return False
            if not self._open_path(Square("h8"), Square("e8")):
                return False
            if (self._square_is_in_check("black", Square("e8"))
                    or self._square_is_in_check("black", Square("f8"))
                    or self._square_is_in_check("black", Square("g8"))):
                return False

            self._move_piece(Square("h8"), Square("f8"))  # Rook
            self._move_piece(Square("e8"), Square("g8"))  # King
            self._black_can_castle_kingside = False
            self._black_can_castle_queenside = False
        self._current_move += 1
        self._last_move = "O-O"
        return True

    def _castle_queenside(self):
        color = self.get_color_to_move()
        if color == "white":
            if not self._white_can_castle_queenside:
                return False
            if not self._open_path(Square("a1"), Square("e1")):
                return False
            if (self._square_is_in_check("white", Square("e1"))
                    or self._square_is_in_check("white", Square("d1"))
                    or self._square_is_in_check("white", Square("c1"))):
                return False

            self._move_piece(Square("a1"), Square("d1"))  # Rook
            self._move_piece(Square("e1"), Square("c1"))  # King
            self._white_can_castle_kingside = False
            self._white_can_castle_queenside = False
        else:
            if not self._white_can_castle_queenside:
                return False
            if not self._open_path(Square("a8"), Square("e8")):
                return False
            if (self._square_is_in_check("black", Square("e8"))
                    or self._square_is_in_check("black", Square("d8"))
                    or self._square_is_in_check("black", Square("c8"))):
                return False

            self._move_piece(Square("a8"), Square("d8"))  # Rook
            self._move_piece(Square("e8"), Square("c8"))  # King
            self._black_can_castle_kingside = False
            self._black_can_castle_queenside = False
        self._current_move += 1
        self._last_move = "O-O-O"
        return True

    def _open_path(self, square1, square2):
        f1 = square1.file
        r1 = square1.rank
        f2 = square2.file
        r2 = square2.rank

        if f1 == f2:
            # vertical movement
            if r1 < r2:
                for rank in range(r1 + 1, r2):
                    if self._board_position[rank][f1] is not None:
                        return False
            else:
                for rank in range(r2 + 1, r1):
                    if self._board_position[rank][f1] is not None:
                        return False

        elif r1 == r2:
            # horizontal movement
            if r1 < r2:
                for file in range(f1 + 1, f2):
                    if self._board_position[r1][file] is not None:
                        return False
            else:
                for file in range(f2 + 1, f1):
                    if self._board_position[r1][file] is not None:
                        return False

        else:
            # diagonal movement
            if f1 < f2:
                for offset in range(1, f2 - f1):
                    if r1 < r2:
                        if self._board_position[r1 + offset][f1 + offset] is not None:
                            return False
                    else:
                        if self._board_position[r1 - offset][f1 + offset] is not None:
                            return False
            else:
                for offset in range(1, f1 - f2):
                    if r1 < r2:
                        if self._board_position[r1 + offset][f1 - offset] is not None:
                            return False
                    else:
                        if self._board_position[r1 - offset][f1 - offset] is not None:
                            return False

        return True

    def _move_piece(self, origin, destination):
        if destination is None:
            self._board_position[origin.rank][origin.file] = None
            return

        self._board_position[destination.rank][destination.file] = self._board_position[origin.rank][origin.file]
        self._board_position[origin.rank][origin.file] = None


class Square:
    file = None
    rank = None

    def __init__(self, *args):
        if len(args) == 2:
            self.file = args[0]
            self.rank = args[1]
            if self.rank < 0 or self.file < 0 or self.rank > 7 or self.file > 7:
                raise ValueError('Invalid square')
        elif len(args) == 1:
            self.file = "abcdefgh".find(args[0][0])
            self.rank = "12345678".find(args[0][1])
            if self.rank < 0 or self.file < 0 or self.rank > 7 or self.file > 7:
                raise ValueError('Invalid square')

    def to_string(self) -> str:
        return "abcdefgh"[self.file] + "12345678"[self.rank]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Coordinate:
    file = None
    rank = None

    def __init__(self, file, rank):
            self.file = file
            self.rank = rank

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
