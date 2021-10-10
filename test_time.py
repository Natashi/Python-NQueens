import os
import time

from n_queens_iterative import *
from n_queens_recursive import *

nq_it = NQueens_Iterative()
nq_rc = NQueens_Recursive()

for nRow in range(4, 20):
	seed = time.perf_counter_ns() % 256
	
	nq_it.InitializeState(nRow, seed)
	nq_rc.InitializeState(nRow, seed)
	
	print('Board size = {0}, seed = {1}'.format(nRow, seed))
	
	timeBegin = time.perf_counter_ns()
	nq_it.PopulateInital()
	cMovesIt = nq_it.SolveConfiguration()
	timeIt = time.perf_counter_ns() - timeBegin
	print('  Iterative: {1:10d}us - {0} moves'.format(cMovesIt, timeIt // 1000))
	
	timeBegin = time.perf_counter_ns()
	resRc = nq_rc.SolveConfiguration()
	timeRc = time.perf_counter_ns() - timeBegin
	print('  Recursive: {1:10d}us - {0}'.format('Solved' if resRc else 'Unsolved', timeRc // 1000))