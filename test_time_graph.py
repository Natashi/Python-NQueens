import os
import time
import matplotlib.pyplot as plt

from n_queens_iterative import *
from n_queens_recursive import *

nq_it = NQueens_Iterative()
nq_rc = NQueens_Recursive()

nRange = range(4, 20 + 1)
testCount = 20

listData_Rows = [i for i in nRange]
listData_TimesIt = []
listData_TimesRc = []
listData_TimeItAvg = []
listData_TimeRcAvg = []

for iTest in range(testCount):
	print('Test #' + str(iTest) + '...')
	
	tmpListIt = []
	tmpListRc = []
	for nRow in nRange:
		seed = time.perf_counter_ns() % 256
		
		nq_it.InitializeState(nRow, seed)
		nq_rc.InitializeState(nRow, seed)

		timeBegin = time.perf_counter_ns()
		nq_it.PopulateInital()
		cMovesIt = nq_it.SolveConfiguration()
		timeIt = time.perf_counter_ns() - timeBegin
		
		timeBegin = time.perf_counter_ns()
		resRc = nq_rc.SolveConfiguration()
		timeRc = time.perf_counter_ns() - timeBegin
		
		tmpListIt.append(timeIt // 1000)
		tmpListRc.append(timeRc // 1000)
	listData_TimesIt.append(tmpListIt)
	listData_TimesRc.append(tmpListRc)

if True:
	for j, n in enumerate(nRange):
		sumIt = 0
		sumRc = 0
		for i in range(testCount):
			sumIt += listData_TimesIt[i][j]
			sumRc += listData_TimesRc[i][j]
		listData_TimeItAvg.append(round(sumIt / testCount))
		listData_TimeRcAvg.append(round(sumRc / testCount))
	
	print('Iterative average:', listData_TimeItAvg)
	print('Recursive average:', listData_TimeRcAvg)

# ----------------------------------------------------------------

plt.xlabel('Board size')
plt.ylabel('Run time (us)')
plt.yscale('log')

for i in range(testCount):
	plt.plot(listData_Rows, listData_TimesIt[i], 'b--', linewidth=0.8, alpha=0.2)
	plt.plot(listData_Rows, listData_TimesRc[i], 'r--', linewidth=0.8, alpha=0.2)
plt.plot(listData_Rows, listData_TimeItAvg, 'bd-')
plt.plot(listData_Rows, listData_TimeRcAvg, 'r^-')

plt.show()