import numpy as np
#source: https://github.com/peleccom/spolks-2013-2014-sem2-050503_pitkin/blob/master/mpi/matrix.py

def mul_matrix(a,b,c,dim):
    """multiply matrix"""
    for i in range(dim):
        for j in range(dim):
            sum = 0
            for k in range(dim):
                sum += a[i, k] * b[k,j]
            c[i,j] = sum


def mul_matrix_partial(a,b, start, stop, dim):
    '''Multiply elemetns two matrix
       Return list
    '''
    c =  []
    l = stop - start
    c = np.empty(l, dtype=np.int32)
    c_index = 0
    for index in range(start, stop):
        i = index / dim
        j = index % dim
        sum = 0
        for k in range(dim):
            sum += a[i, k] * b[k,j]
        c[c_index] = sum
        c_index += 1
    return c


def copy_matrix_slice(a, elements, start, stop, dim):
    """Copy list to matrix"""
    index = 0
    for ind in range(start, stop):
        i = ind / dim
        j = ind % dim
        a[i,j] = elements[index]
        index += 1


def get_rank_indexes(rank, size, dim):
    total_size = dim * dim
    int_portion = (total_size / size)
    left_portion = total_size % size
    begin_index = 0
    for i in range(rank):
        begin_index += int_portion
        if i <  left_portion:
            begin_index += 1
    end_index = begin_index
    end_index += int_portion
    if rank < left_portion:
        end_index += 1

    #calculate row index
    return begin_index,end_index
