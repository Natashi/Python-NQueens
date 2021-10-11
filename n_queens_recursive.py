# Reference(s):
#	https://en.wikipedia.org/wiki/Eight_queens_puzzle
#	https://en.wikipedia.org/wiki/Backtracking

class NQueens_Recursive:
	def __init__(self):
		self.boardData = []
	
	def InitializeState(self, boardSize, seed):
		self.nRow = boardSize
		self.seed = seed
		self.boardData = []
		for i in range(self.nRow * self.nRow):
			self.boardData.append(False)
		self.queenPos = [-1 for i in range(self.nRow)]
	
	def SetAt(self, iRow, iCol, v):
		self.boardData[iRow * self.nRow + iCol] = v
	def GetAt(self, iRow, iCol):
		return self.boardData[iRow * self.nRow + iCol]

	def RegisterQueen(self, iRow, iCol):
		self.queenPos[iRow] = iCol
		self.SetAt(iRow, iCol, True)
	def DeleteQueen(self, iRow):
		qPos = self.queenPos[iRow]
		self.SetAt(iRow, qPos, False)
		self.queenPos[iRow] = -1

	def PrintBoard(self):
		print('==================================')
		for i in range(self.nRow):
			print('[', end='')
			for j in range(self.nRow):
				at = self.GetAt(i, j)
				s = ('\033[31m' + 'X' + '\033[0m') if at else 'o'
				if j != self.nRow - 1:
					s += ', '
				print(s, end='')
			print(']')
	
	# --------------------------------------------------------------------------------------
	
	def IsTileSafe(self, iRow, iCol):
		for i in range(self.nRow):
			for j in range(self.nRow):
				if i == iRow and j == iCol:
					continue
				if self.GetAt(i, j):
					if i == iRow or j == iCol or (abs(i - iRow) == abs(j - iCol)):
						return False
		return True
	
	# --------------------------------------------------------------------------------------

	def SolveConfiguration(self):
		select_seed = self.seed
		
		def _PlaceQueens(iniRow):
			nonlocal select_seed
			
			if iniRow >= self.nRow:
				return True
			
			# Get all valid queen placements
			listPlaceNext = []
			for iCol in range(self.nRow):
				if self.IsTileSafe(iniRow, iCol):
					listPlaceNext.append(iCol)
			
			nAvail = len(listPlaceNext)
			if nAvail > 0:	
				for i in range(nAvail):
					qPosNext = listPlaceNext[(i + select_seed) % nAvail]
					
					self.RegisterQueen(iniRow, qPosNext)
					select_seed += 1
					
					# Try placing queens in the rows below
					if _PlaceQueens(iniRow + 1):
						return True
					else:
						# No valid queen placements in the rows below
						for i in range(iniRow, self.nRow):
							self.DeleteQueen(i)
			
			# No valid queen placements in this row and below, backtrack
			return False
		
		return _PlaceQueens(0)

# --------------------------------------------------------------------------------------

if __name__ == '__main__':
	import os
	import sys
	import time
	os.system('')
	
	nRow = 8
	if len(sys.argv) >= 2:
		nRow = int(sys.argv[1])
		print('Board size =', nRow)
	else:
		nRow = int(input('Board size: '))
	
	if nRow < 4 or nRow > 50:
		print('Size out of range')
		exit()
	
	seed = time.perf_counter_ns() % 256
	print('Configuration seed =', seed)
	
	nq = NQueens_Recursive()
	nq.InitializeState(nRow, seed)
	
	timeBegin = time.perf_counter_ns()
	
	res = nq.SolveConfiguration()
	
	timeEnd = time.perf_counter_ns()
	
	if res:
		nq.PrintBoard()
	else:
		print('No solutions found')
	
	print('Time taken (recursive approach): {0}us'.format((timeEnd - timeBegin) // 1000))