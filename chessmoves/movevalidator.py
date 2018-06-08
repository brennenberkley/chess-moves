class MoveValidator:
    _current_move = int(1)
    _white_can_castle_kingside = True
    _white_can_castle_queenside = True
    _black_can_castle_kingside = True
    _black_can_castle_queenside = True
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

        old_board = self._board_position.copy()
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

        self._current_move += 1

        check = self._king_is_in_check("black" if self.get_color_to_move() == "white" else "white")

        # get the text representation of the move
        last_move = ""
        if piece == "p":
            if capture:
                last_move += "abcdefgh"[origin_file]
        else:
            move += piece
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

    # Placeholder function
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

    # Placeholder function
    def _square_is_in_check(self, color, square):
        return False

    # Placeholder function
    def _get_origin_squares(self, piece, destination, capture):
        return [Square("a4")]

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
















    def _move_pawn(self, new_file, new_rank, capture, origin_file):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = []

        color = self.get_color_to_move()
        # Determine valid origin squares
        if capture:
            if origin_file is None:
                return False

            if color == 'white':
                squares.append([rank - 1, self._get_index(origin_file)])
            else:
                squares.append([rank + 1, self._get_index(origin_file)])
        else:
            if origin_file:
                return False

            if color == 'white':
                squares.append([rank - 1, file])
                if rank == 3:
                    squares.append([rank - 2, file])
            else:
                squares.append([rank + 1, file])
                if rank == 4:
                    squares.append([rank + 2, file])

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue
            if not self._open_path(f, r, file, rank):
                continue

            if self._board_position[r][f] == color[0] + "p":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                return True

        return False

    def _move_knight(self, new_file, new_rank, origin_file, origin_rank):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = [
            [rank + 1, file + 2],
            [rank + 1, file - 2],
            [rank - 1, file + 2],
            [rank - 1, file - 2],
            [rank + 2, file + 1],
            [rank + 2, file - 1],
            [rank - 2, file + 1],
            [rank - 2, file - 1]
        ]
        if origin_file:
            o_file = self._get_index(origin_file)
            for square in squares:
                if square[1] != o_file:
                    squares.remove(square)
        if origin_rank:
            o_rank = self._get_index(origin_rank)
            for square in squares:
                if square[0] != o_rank:
                    squares.remove(square)

        color = self.get_color_to_move()

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue

            if self._board_position[r][f] == color[0] + "N":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                return True

        return False

    def _move_rook(self, new_file, new_rank, origin_file, origin_rank):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = []
        color = self.get_color_to_move()

        # Determine valid origin squares
        for offset in range(-7, 8):
            squares.append([rank, file + offset])
            squares.append([rank + offset, file])

        if origin_file:
            o_file = self._get_index(origin_file)
            for square in squares:
                if square[1] != o_file:
                    squares.remove(square)
        if origin_rank:
            o_rank = self._get_index(origin_rank)
            for square in squares:
                if square[0] != o_rank:
                    squares.remove(square)

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue
            if not self._open_path(f, r, file, rank):
                continue

            if self._board_position[r][f] == color[0] + "R":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                if f == 0 and r == 0:
                    self._white_can_castle_queenside = False
                elif f == 7 and r == 0:
                    self._white_can_castle_kingside = False
                elif f == 0 and r == 7:
                    self._black_can_castle_queenside = False
                elif f == 7 and r == 7:
                    self._black_can_castle_kingside = False
                return True

        return False

    def _move_bishop(self, new_file, new_rank, origin_file, origin_rank):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = []
        color = self.get_color_to_move()

        # Determine valid origin squares
        for offset in range(-7, 8):
            squares.append([rank + offset, file + offset])
            squares.append([rank + offset, file - offset])

        if origin_file:
            o_file = self._get_index(origin_file)
            for square in squares:
                if square[1] != o_file:
                    squares.remove(square)
        if origin_rank:
            o_rank = self._get_index(origin_rank)
            for square in squares:
                if square[0] != o_rank:
                    squares.remove(square)

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue
            if not self._open_path(f, r, file, rank):
                continue

            if self._board_position[r][f] == color[0] + "B":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                return True

        return False

    def _move_king(self, new_file, new_rank):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = [
            [rank + 1, file + 1],
            [rank + 1, file],
            [rank + 1, file - 1],
            [rank, file + 1],
            [rank, file - 1],
            [rank - 1, file + 1],
            [rank - 1, file],
            [rank - 1, file - 1]
        ]
        color = self.get_color_to_move()

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue

            if self._board_position[r][f] == color[0] + "N":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                if color == "white":
                    self._white_can_castle_kingside = False
                    self._white_can_castle_queenside = False
                else:
                    self._black_can_castle_kingside = False
                    self._black_can_castle_queenside = False
                return True

        return False


    def _move_queen(self, new_file, new_rank, origin_file, origin_rank):
        rank = self._get_index(new_rank)
        file = self._get_index(new_file)
        squares = []
        color = self.get_color_to_move()

        # Determine valid origin squares
        for offset in range(-7, 8):
            squares.append([rank, file + offset])
            squares.append([rank + offset, file])
            squares.append([rank + offset, file + offset])
            squares.append([rank + offset, file - offset])

        if origin_file:
            o_file = self._get_index(origin_file)
            for square in squares:
                if square[1] != o_file:
                    squares.remove(square)
        if origin_rank:
            o_rank = self._get_index(origin_rank)
            for square in squares:
                if square[0] != o_rank:
                    squares.remove(square)

        # Try each origin square
        for square in squares:
            r = square[0]
            f = square[1]
            if f < 0 or r < 0 or f > 7 or r > 7:
                continue
            if not self._open_path(f, r, file, rank):
                continue

            if self._board_position[r][f] == color[0] + "Q":
                self._update_board(f, r, file, rank)
                self._current_move += 1
                return True

        return False








class Square:
    file = None
    rank = None

    def __init__(self, file: int, rank: int):
        self.rank = rank
        self.file = file

    def __init__(self, square: str):
        self.file = "abcdefgh".find(square[0])
        self.rank = "12345678".find(square[1])
        if self.rank < 0 or self.file < 0:
            raise ValueError('Invalid square')

    def to_string(self) -> str:
        return "abcdefgh"[self.file] + "12345678"[self.rank]

