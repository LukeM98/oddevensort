


#!/usr/bin/python3
#SBATCH -n 5 
import tensorflow as tf
import numpy as np
import pandas as pd
from mpi4py import MPI
import time
import psutil


#pool = multiprocessing.Pool()

#print(pool)
comm = MPI.COMM_WORLD
me = comm.Get_rank()
 
print("Task ", me, " on CPU ", psutil.Process().cpu_num())

arr = []
if me == 0:
	arr=np.random.randint(50, size=comm.Get_size())
	print("Original array ", arr)

number = comm.scatter(arr, root=0)

#print("I'm Node ", me, "with number ", number)

for i in range(comm.Get_size()):
	if(i%2==0 and me%2 ==0):
		if(me+1 == comm.Get_size()):
			check_node = 0

		else:
			check_node = me+1

#		print("Even Iteration Node ", me, " Checking with node ", check_node)
		new_num = comm.sendrecv(sendobj=number, dest = check_node, source=check_node)
		if(new_num < number and me+1 != comm.Get_size()):
			number = new_num
		elif(new_num > number and me+1 == comm.Get_size()):
			number = new_num
	elif(i%2==1 and me%2==1):
		if(me+1 == comm.Get_size()):
			check_node = 0
		else:
			check_node = me+1
#		print("Odd Iteration! Node ", me, " Checking with node ", check_node)
		new_num = comm.sendrecv(sendobj=number, dest = check_node, source=check_node)
		if(new_num < number and me+1 != comm.Get_size()):
			number = new_num
		elif(new_num > number and me+1 == comm.Get_size()):
			number = new_num

	elif(i%2==0 and me%2 == 1):
		if(me - 1 < 0):
			check_node = comm.Get_size() -1
		else:
			check_node = me-1
		new_num = comm.sendrecv(sendobj=number, dest = check_node, source=check_node)
		if(new_num > number and me-1 > -1):
			number = new_num
		elif(new_num < number and me-1 == -1):
			number = new_num
	elif(i%2==1 and me%2==0):
		if(me - 1 < 0):
			check_node = comm.Get_size() -1
		else:
			check_node = me-1
		new_num = comm.sendrecv(sendobj=number, dest = check_node, source=check_node)

		if(new_num > number and me-1 > -1):
			number = new_num
		elif(new_num < number and me-1 == -1):
			number = new_num
	comm.Barrier()

arr = comm.gather(number, root=0)
if(me == 0):
	print("New Array ", arr)
#while(True):
#	if me == 0:
#		print("Rank ", )
#		comm.send(x, dest=1, tag=0)

#	if me == 1:
#		x = comm.recv(source=0, tag=0)



#print("Process ", me, " Value for x is ", x)
