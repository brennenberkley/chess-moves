class MoveValidator():
	__current_move = int(1)

	# First letter indicates color, second letter indicates piece
	__board_position = [
		#  A     B     C     D     E     F     G     H    
		["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], # 1
		["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], # 2
		[None, None, None, None, None, None, None, None], # 3
		[None, None, None, None, None, None, None, None], # 4
		[None, None, None, None, None, None, None, None], # 5
		[None, None, None, None, None, None, None, None], # 6
		["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], # 7
		["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]  # 8
	]

	def add_move(self, move):
		# Decode the move
		capture = "x" in move
		move = move.replace("x", "")

		if (len(move) < 2):
			return False
		
		file = move[-2:-1]
		rank = move[-1:]
		if file not in "abcdefgh" or rank not in "12345678":
			return False
		move = move[:-2]

		piece = "p"
		if (len(move) > 0):
			if move[0] in "KQRBN":
				piece = move[0]
				move = move.replace(piece, "")

		origin_file = None
		origin_rank = None

		if (len(move) == 1):
			if move in "abcdefgh":
				origin_file = move
			elif move in "12345678":
				origin_rank = move
			else:
				return False

		elif (len(move) == 2):
			origin_file = move[0]
			origin_rank = move[1]
			if origin_file not in "abcdefgh" or origin_rank not in "12345678":
				return False
		
		# Process the move

		if piece == "p":
			return self.__move_pawn(file, rank, capture, origin_file)
		elif piece == "R":
			return self.__move_rook(file, rank, capture, origin_file, origin_rank)
		elif piece == "N":
			return self.__move_knight(file, rank, capture, origin_file, origin_rank)
		elif piece == "B":
			return self.__move_bishop(file, rank, capture, origin_file, origin_rank)
		elif piece == "K":
			return self.__move_king(file, rank, capture, origin_file, origin_rank)
		elif piece == "Q":
			return self.__move_queen(file, rank, capture, origin_file, origin_rank)
		
	def get_move_number(self):
		if self.__current_move % 2 == 0:
			return str(int(self.__current_move / 2)) + "..."
		else:
			move_number = ((self.__current_move - 1) / 2) + 1
			return str(int(move_number)) + "."

	def get_color_to_move(self):
		return "black" if self.__current_move % 2 == 0 else "white"

	def __move_pawn(self, new_file, new_rank, capture, origin_file):
		rank = self.__get_index(new_rank)
		file = self.__get_index(new_file)
		squares = []

		color = self.get_color_to_move()
		# Determine valid origin squares
		if (capture):
			if (origin_file is None):
				return False

			if color == 'white':
				squares.append([rank - 1, self.__get_index(origin_file)])
			else:
				squares.append([rank + 1, self.__get_index(origin_file)])
		else:
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
			if not self.__open_path(f, r, file, rank):
				continue

			if self.__board_position[r][f] == color[0] + "p":
				self.__update_board(f, r, file, rank)
				return True

		return False

	def __move_knight(self, new_file, new_rank, capture, origin_file, origin_rank):
		return False


	def __move_rook(self, new_file, new_rank, capture, origin_file, origin_rank):
		rank = self.__get_index(new_rank)
		file = self.__get_index(new_file)
		squares = []
		color = self.get_color_to_move()

		# Determine valid origin squares
		for offset in range(-7, 8):
			squares.append([rank, file + offset])
			squares.append([rank + offset, file])

		# Try each origin square
		for square in squares:
			r = square[0]
			f = square[1]
			if f < 0 or r < 0 or f > 7 or r > 7:
				continue
			if not self.__open_path(f, r, file, rank):
				continue

			if self.__board_position[r][f] == color[0] + "R":
				self.__update_board(f, r, file, rank)
				return True

		return False


	def __move_bishop(self, new_file, new_rank, capture, origin_file, origin_rank):
		rank = self.__get_index(new_rank)
		file = self.__get_index(new_file)
		squares = []
		color = self.get_color_to_move()

		# Determine valid origin squares
		for offset in range(-7, 8):
			squares.append([rank + offset, file + offset])
			squares.append([rank + offset, file - offset])

		# Try each origin square
		for square in squares:
			r = square[0]
			f = square[1]
			if f < 0 or r < 0 or f > 7 or r > 7:
				continue
			if not self.__open_path(f, r, file, rank):
				continue

			if self.__board_position[r][f] == color[0] + "B":
				self.__update_board(f, r, file, rank)
				return True

		return False


	def __move_king(self, file, rank, capture, origin_file, origin_rank):
		return False


	def __move_queen(self, new_file, new_rank, capture, origin_file, origin_rank):
		rank = self.__get_index(new_rank)
		file = self.__get_index(new_file)
		squares = []
		color = self.get_color_to_move()

		# Determine valid origin squares
		for offset in range(-7, 8):
			squares.append([rank, file + offset])
			squares.append([rank + offset, file])
			squares.append([rank + offset, file + offset])
			squares.append([rank + offset, file - offset])

		# Try each origin square
		for square in squares:
			r = square[0]
			f = square[1]
			if f < 0 or r < 0 or f > 7 or r > 7:
				continue
			if not self.__open_path(f, r, file, rank):
				continue

			if self.__board_position[r][f] == color[0] + "Q":
				self.__update_board(f, r, file, rank)
				return True

		return False

	def __get_index(self, value):
		if value in "abcdefgh":
			return "abcdefgh".find(value)
		else:
			return "12345678".find(value)

	def __open_path(self, f1, r1, f2, r2):
		if f1 == f2:
			# vertical movement
			if r1 < r2:
				for rank in range(r1 + 1,r2):
					if self.__board_position[rank][f1] is not None:
						return False	
			else:
				for rank in range(r2 + 1,r1):
					if self.__board_position[rank][f1] is not None:
						return False

		elif r1 == r2:
			# horizontal movement
			if r1 < r2:
				for file in range(f1 + 1,f2):
					if self.__board_position[r1][file] is not None:
						return False
			else:
				for file in range(f2 + 1,f1):
					if self.__board_position[r1][file] is not None:
						return False

		else:
			# diagonal movement
			if abs(r1 - r2) != abs(f1 - f2):
				print("Error: Not a diagonal")
				return False

			if (f1 < f2):
				for offset in range(1, f2 - f1):
					if (r1 < r2):
						if self.__board_position[r1 + offset][f1 + offset] is not None:
							return False
					else:
						if self.__board_position[r1 - offset][f1 + offset] is not None:
							return False
			else: 
				for offset in range(1, f1 - f2):
					if (r1 < r2):
						if self.__board_position[r1 + offset][f2 + offset] is not None:
							return False
					else:
						if self.__board_position[r1 - offset][f2 + offset] is not None:
							return False

		return True

	def __update_board(self, f1, r1, f2, r2):
		self.__board_position[r2][f2] = self.__board_position[r1][f1]
		self.__board_position[r1][f1] = None
		self.__current_move += 1












	def __move_pawn_old(self, file, rank, capture, o_file):
		new_rank = self.__get_index(rank)
		new_file = self.__get_index(file)
		origin_file = None
		origin_rank = None

		f = self.__get_index(file)
		r = self.__get_index(rank)
		files = None
		ranks = None

		color = self.get_color_to_move()
		# Determine valid origin squares
		if (capture):
			if (o_file is None):
				return False

			files = [self.__get_index(o_file)]
			if color == 'w':
				ranks = [r - 1]
			else:
				ranks = [r + 1]
		else:
			files = [f]
			if color == 'w':
				ranks = [r - 1]
				if r == 3:
					ranks.append(r - 2)
			else:
				ranks = [r + 1]
				if r == 4:
					ranks.append(r + 2)

		valid_starting_squares = 0
		
		# Try each origin square
		for f in files:
			for r in ranks:
				if f < 0 or r < 0 or f > 7 or r > 7:
					continue
				if not self.__open_path(f, r, new_file, new_rank):
					continue

				if self.__board_position[r][f] == color + "p":
					valid_starting_squares += 1
					origin_rank = r
					origin_file = f

		if valid_starting_squares < 1:
			return False

		if valid_starting_squares > 1:
			print("Ambiguous move")
			return False

		self.__update_board(origin_file, origin_rank, new_file, new_rank)
		return True







