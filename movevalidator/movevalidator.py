class MoveValidator():
	current_move = int(1)

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
		square = file + rank
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
		if origin_file == None:
			origin_file = ""
		if origin_rank == None:
			origin_rank = ""

		print("piece: " + piece)
		print("origin square: " + origin_file + origin_rank)
		print("destination square: " + file + rank)
		print("capture: " + "yes" if capture else "no")

		return True


		


	def get_move_number(self):
		if self.current_move % 2 == 0:
			return str(int(self.current_move / 2)) + "..."
		else:
			move_number = ((self.current_move - 1) / 2) + 1
			return str(int(move_number)) + "."

	def __move_pawn(self, square):
		self.current_move += 1
		return True

	def __move_knight(self, square):
		self.current_move += 1
		return True

	def __move_rook(self, square):
		self.current_move += 1
		return True

	def __move_bishop(self, square):
		self.current_move += 1
		return True

	def __move_king(self, square):
		self.current_move += 1
		return True

	def __move_queen(self, square):
		self.current_move += 1
		return True