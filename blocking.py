#!/usr/bin/env python2

from mpi4py import MPI
import numpy as np
import matrix

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    # main process
    ARRAY_DIM = 2
    ARRAY_SIZE = ARRAY_DIM * ARRAY_DIM
    a = np.arange(ARRAY_SIZE).reshape(ARRAY_DIM, ARRAY_DIM)
    np.set_printoptions(precision=3)
    b = np.arange(ARRAY_SIZE, 2 * ARRAY_SIZE).reshape(ARRAY_DIM, ARRAY_DIM)
    c = np.zeros((ARRAY_DIM, ARRAY_DIM), dtype=np.int32)

    start, stop = matrix.get_rank_indexes(rank,size, ARRAY_DIM)
    c_elements = matrix.mul_matrix_partial(a, b,start, stop, ARRAY_DIM)
    matrix.copy_matrix_slice(c, c_elements, start, stop, ARRAY_DIM)

    i=1
    while i < size:
        comm.send(a, dest=i,tag=10)
        comm.send(b, dest=i, tag=11)
        comm.send(ARRAY_DIM, dest=i, tag=12)
        status = MPI.Status()
        c_elements = comm.recv(source=MPI.ANY_SOURCE,tag=13, status=status)
        source = status.Get_source()
        start, stop = matrix.get_rank_indexes(source, size, ARRAY_DIM)
        matrix.copy_matrix_slice(c, c_elements, start, stop, ARRAY_DIM)
        i += 1
    print "result matrix\n" ,c
    print "true result\n", np.dot(a,b)

else:
    status = MPI.Status()
    a = comm.recv(source=0,tag=10, status=status)
    b = comm.recv(source=0,tag=11, status=status)
    ARRAY_DIM = comm.recv(source=0,tag=12, status=status)
    c = np.zeros((ARRAY_DIM, ARRAY_DIM), dtype=np.int32)
    start, stop = matrix.get_rank_indexes(rank,size, ARRAY_DIM)
    c_elements = matrix.mul_matrix_partial(a, b,start, stop, ARRAY_DIM)
    matrix.copy_matrix_slice(c, c_elements, start, stop, ARRAY_DIM)
    comm.send(c_elements, dest=0,tag=13)