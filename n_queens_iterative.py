# Reference(s):
#	https://en.wikipedia.org/wiki/Eight_queens_puzzle
#	https://en.wikipedia.org/wiki/Min-conflicts_algorithm
#	https://medium.com/@carlosgonzalez_39141/using-ai-to-solve-the-n-queens-problem-2a5a9cc5c84c

class NQueens_Iterative:
	class Tile:
		def __init__(self, bQueen):
			self.bQueen = bQueen
			self.attack = 0
	
	def __init__(self):
		self.boardData = []
	
	def InitializeState(self, boardSize, seed):
		self.nRow = boardSize
		self.seed = seed
		self.boardData = []
		for i in range(self.nRow * self.nRow):
			self.boardData.append(self.Tile(False))
		self.queenPos = [-1 for i in range(self.nRow)]
	
	def BoardAt(self, iRow, iCol):
		return self.boardData[iRow * self.nRow + iCol]

	def RegisterQueen(self, iRow, iCol):
		self.queenPos[iRow] = iCol
		self.BoardAt(iRow, iCol).bQueen = True

	def PrintBoard(self):
		print('==================================')
		for i in range(self.nRow):
			print('[', end='')
			for j in range(self.nRow):
				at = self.BoardAt(i, j)
				s = str(at.attack)
				if at.bQueen:
					s = '\033[31m' + s + '\033[0m'	# Make queen tiles red with the blood of her enemies
				if j != self.nRow - 1:
					s += ', '
				print(s, end='')
			print(']')
	
	# --------------------------------------------------------------------------------------
	
	def GetAttackCount(self, iRow, iCol):
		def SearchDir(sRow, sCol):
			r = iRow
			c = iCol
			while True:
				r += sRow
				c += sCol
				if not (r >= 0 and r < self.nRow and c >= 0 and c < self.nRow):
					break
				if self.BoardAt(r, c).bQueen:
					return True
			return False
		
		nAtk = 0
		for ipDir in ((-1, 0), (1, 0), (0, -1), (0, 1), \
			(-1, -1), (1, -1), (-1, 1), (1, 1)):	# Search in all 8 directions
			if SearchDir(ipDir[0], ipDir[1]):
				nAtk += 1
		return nAtk

	def LoadAttacksSingle(self, iRow, iCol):
		nAtk = self.GetAttackCount(iRow, iCol)
		self.BoardAt(iRow, iCol).attack = nAtk
	def LoadAttacks(self, iRow):
		for iCol in range(self.nRow):
			self.LoadAttacksSingle(iRow, iCol)
	def UpdateAttacks(self, iRow, iCol):
		for i in range(self.nRow):
			for j in range(self.nRow):
				if i == iRow or j == iCol or (abs(i - iRow) == abs(j - iCol)):
					self.LoadAttacksSingle(i, j)

	def GetMinAttacksInRow(self, iRow, bExcludeQueen=False):
		nMin = self.nRow + 1			# Initialize to maximum possible attacks
		for i in range(self.nRow):
			at = self.BoardAt(iRow, i)
			if bExcludeQueen and at.bQueen:
				continue
			if at.attack < nMin:
				nMin = at.attack
		return nMin

	def IsAllQueenSafe(self):
		for i in range(self.nRow):
			if self.BoardAt(i, self.queenPos[i]).attack > 0:
				return False
		return True
	
	# --------------------------------------------------------------------------------------
	
	def PopulateInital(self):
		for iRow in range(self.nRow):
			pPlace = 0
			if iRow > 0:
				minAtk = self.GetMinAttacksInRow(iRow)
				for j in range(self.nRow):
					if self.BoardAt(iRow, j).attack == minAtk:
						pPlace = j
						break
			else:
				pPlace = self.seed % self.nRow
			
			self.RegisterQueen(iRow, pPlace)
			self.UpdateAttacks(iRow, pPlace)
			# self.PrintBoard()
	
	def SolveConfiguration(self):
		cMoves = 0
		
		def _SolveConfiguration():
			nonlocal cMoves
			cMoves = 0
			
			select_seed = self.seed
			iQueenRow = 0
			while not self.IsAllQueenSafe():
				pQueen = self.queenPos[iQueenRow]
				
				atQueen = self.BoardAt(iQueenRow, pQueen)
				if atQueen.attack > 0:
					rowMinAttack = self.GetMinAttacksInRow(iQueenRow, bExcludeQueen=True)
					listMoveNext = []
					
					# Load all potential movements
					for j in range(self.nRow):
						if j != pQueen and self.BoardAt(iQueenRow, j).attack <= rowMinAttack:
							listMoveNext.append(j)
					
					# Select one movement based on the rand seed
					if len(listMoveNext) > 0:
						pMove = listMoveNext[select_seed % len(listMoveNext)]
						select_seed += 1
						
						atQueen.bQueen = False
						self.RegisterQueen(iQueenRow, pMove)
						
						self.UpdateAttacks(iQueenRow, pQueen)
						self.UpdateAttacks(iQueenRow, pMove)
						
						cMoves += 1
				
				# self.PrintBoard()
				iQueenRow = (iQueenRow + 1) % self.nRow
				
				if cMoves > (self.nRow * self.nRow * 2):		# Algorithm is probably stuck in a local maxima
					return False
			return True
		
		while True:
			if _SolveConfiguration():
				break
			# Retry with a different seed
			self.InitializeState(self.nRow, self.seed + 1)
			self.PopulateInital()
		
		return cMoves

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
	
	nq = NQueens_Iterative()
	nq.InitializeState(nRow, seed)
	
	timeBegin = time.perf_counter_ns()
	
	nq.PopulateInital()
	cMoves = nq.SolveConfiguration()
	
	timeEnd = time.perf_counter_ns()
	
	nq.PrintBoard()
	print('Moves taken: {0}'.format(cMoves))
	print('Time taken (iterative approach): {0}us'.format((timeEnd - timeBegin) // 1000))