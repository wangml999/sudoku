import numpy as np
import math

problm1 = '008 000 003\n'\
          '050 008 960\n'\
          '702 006 540\n'\
          '040 005 801\n'\
          '000 904 000\n'\
          '205 800 090\n'\
          '027 100 406\n'\
          '081 600 020\n'\
          '600 000 100'

problm2 = '020 089 100\n'\
          '008 000 040\n'\
          '700 000 009\n'\
          '006 200 004\n'\
          '100 040 020\n'\
          '200 008 090\n'\
          '900 000 001\n'\
          '007 000 030\n'\
          '080 063 200'

problm3 = '000 104 000\n'\
          '005 000 082\n'\
          '400 080 009\n'\
          '042 008 060\n'\
          '003 020 900\n'\
          '090 500 230\n'\
          '700 050 004\n'\
          '580 000 600\n'\
          '000 406 000'

problm4 = '000 000 010\n'\
          '000 000 063\n'\
          '900 024 850\n'\
          '102 605 000\n'\
          '700 080 001\n'\
          '000 301 705\n'\
          '021 930 008\n'\
          '480 000 000\n'\
          '090 000 000'

problm5 = '000 000 001\n'\
          '000 000 023\n'\
          '004 005 000\n'\
          '000 100 000\n'\
          '000 030 600\n'\
          '007 000 580\n'\
          '000 067 000\n'\
          '010 004 000\n'\
          '520 000 000'

problm6 = '800 000 000\n'\
          '003 600 000\n'\
          '070 090 200\n'\
          '050 007 000\n'\
          '000 045 700\n'\
          '000 100 030\n'\
          '001 000 068\n'\
          '008 500 010\n'\
          '090 000 400'

def get_duplication(a):
    a_, counts = np.unique(a, return_counts=True)
    #return np.sum(np.where(counts>1, counts, 0))
    return 9-len(a_)

def is_unique(a):
    a_, counts = np.unique(a, return_counts=True)

    for x in zip(a_, counts):
        if x[0]!=0 and x[1]>1:
            return False
    return True

def is_solved(A, diagonal=False):
    if 0 in A:
        return False
    return is_legal(A, diagonal)

def has_zero(A):
    return np.all((A == 0))

def is_legal(A, diagonal=False):
    for i in range(A.shape[0]):
        if not is_unique(A[i]):
            return False

    for i in range(A.shape[1]):
        if not is_unique(A[:,i]):
            return False

    for i in range(3):
        for j in range(3):
            sub = A[i*3:(i+1)*3, j*3:(j+1)*3].flatten()
            if not is_unique(sub):
                return False

    if diagonal:
        if not is_unique(A.diagonal()):
            return False

        if not is_unique(np.fliplr(A).diagonal()):
            return False

    return True

def backtracking_solver(A, diagonal=False):
    if is_solved(A, diagonal):
        print(A)
        return True

    full = np.array([x for x in range(1,10)])

    for r in range(A.shape[0]):
        for c in range(A.shape[1]):
            if A[r, c] == 0:
                v = np.setdiff1d(full, A[r])
                v = np.setdiff1d(v, A[:,c])
                k = A[int(r / 3) * 3:(int(r / 3) + 1) * 3, int(c / 3) * 3:(int(c / 3) + 1) * 3].flatten()
                v = np.setdiff1d(v, k)
                for i in v:
                    a = np.copy(A)
                    a[r, c] = i
                    print(a)
                    if not is_legal(a, diagonal):
                        continue
                    if backtracking_solver(a, diagonal):
                        return True
                return False
    return False

'''
get the number of errors as the score
'''
def score(A):
    error = 0

    for i in range(A.shape[0]):
        error = error + get_duplication(A[i])

    for i in range(A.shape[1]):
        error = error + get_duplication(A[:,i])

    for i in range(3):
        for j in range(3):
            sub = A[i*3:(i+1)*3, j*3:(j+1)*3].flatten()
            error = error + get_duplication(sub)

    return error

def P(e, e1, T):
    if e == e1:
        return 0.5
    else:
        return math.exp(-(e1-e)/T)

"""
this method fills random number 1 to 9 to the blank.
"""
def simulated_annealing_solver2(A, diagonal=False):
    empty_cells = np.where(A==0)
    empty_cells = [x for x in zip(empty_cells[0], empty_cells[1])]

    x = np.random.randint(1, 10, size=81).reshape(9,9)
    s = np.where(A!=0, A, x)
    #print(s)
    error = score(s)

    temperature = 10
    k = 0
    while temperature > 0.5:
        temperature = temperature * 0.99999

        s_copy = np.copy(s)

        r, c = empty_cells[np.random.randint(0, len(empty_cells))]
        n = np.random.randint(1, 10, 1)
        s[r, c] = n

        if is_legal(s):
            print(s)
            print('Found solution')
            return

        error1 = score(s)
        p = P(error, error1, temperature)
        z = np.random.uniform(0, 1)
        if p >= z:
            print(r, c, n, error, error1, temperature, p, z)
            print(s)
            error = error1
        else:
            s = s_copy


    print("failed")

"""
this method fills 1 to 9 to each box. every time shuffles two numbers in a box so the box constrains are always satisfied. 
"""
def simulated_annealing_solver(A, diagonal=False):
    print(A)

    empty_cells = []
    for i in range(3):
        for j in range(3):
            empty_cells.append([])
            for p in range(i*3, i*3+3):
                for q in range(j * 3, j * 3 + 3):
                    if A[p, q] == 0:
                        empty_cells[i * 3 + j].append((p, q))

    s = np.copy(A)
    full = np.array([x for x in range(1, 10)])

    for i in range(3):
        for j in range(3):
            sub = A[i*3:(i+1)*3, j*3:(j+1)*3].flatten()
            sub = np.setdiff1d(full, sub)
            np.random.shuffle(sub)
            x = 0
            for p in range(i*3, i*3+3):
                for q in range(j * 3, j * 3 + 3):
                    if A[p, q] == 0:
                        s[p, q] = sub[x]
                        x = x + 1

    print(s)
    error = score(s)

    k = 0
    temperature = 10
    while temperature > 0.5:
        temperature = temperature * 0.99999

        if is_legal(s):
            print(s)
            print('Found solution')
            return

        s_copy = np.copy(s)

        #randomly pick a 3x3 square and shuffle two numbers in it
        cell = np.random.randint(0, 9)
        pos = np.array([x for x in range(0, len(empty_cells[cell]))])
        np.random.shuffle(pos)
        pos = pos[0:2]

        #swap
        c1 = empty_cells[cell][pos[0]]
        c2 = empty_cells[cell][pos[1]]

        temp = s[c1[0], c1[1]]
        s[c1[0], c1[1]] = s[c2[0], c2[1]]
        s[c2[0], c2[1]] = temp

        error1 = score(s)
        p = P(error, error1, temperature)
        z = np.random.uniform(0, 1)
        k = k + 1
        if p >= z:
            print(s)
            print(c1, c2, error, error1, temperature, p, z)
            error = error1
        else:
            s = s_copy


    print("failed")

"""
ref https://en.wikipedia.org/wiki/Exact_cover#Sudoku for details

columns:
 - row_1 has 1, row_1 has 2, row_1 has 3...row_9 has 1, row_9 has 2...row_9 has 9. 81 columns
 - col_1 has 1, col_1 has 2, col_1 has 3...col_9 has 1, col_9 has 2...col_9 has 9. 81 columns
 - cell_1 has number, cell_2 has number, ..., cell_81 has number
 - box_1 has 1, box_1 has 2, ...box 9 has 1, box_9 has 2, box_9 has 9. 81 columns
 
rows:
 - cell (1, 1) is 1
 - cell (1, 1) is 2
  ...
 - cell (1, 1) is 9
 - cell (1, 2) is 1
 - cell (1, 2) is 2
  ...
 - cell (1, 2) is 9
 ...
 - cell (9, 9) is 1
 - cell (9, 9) is 2
  ...
 - cell (9, 9) is 9
"""
def exact_cover_solver(A):
    length = 3
    size = length**2
    matrix = np.zeros([size**3, size**2*4], dtype=int)
    row_names = []
    for r in range(size):
        for c in range(size):
            for n in range(size):
                row_names.append('{0}_{1}_{2}'.format(r, c, n+1))
            if A[r, c] == 0:
                row_set = range(size)
            else:
                row_set = [A[r,c]-1] #zero based index

            for n in row_set:
                matrix[r*size**2+c*size+n, r*size+n] = 1  # row (r) must have value n
                matrix[r*size**2+c*size+n, size**2+c*size+n] = 1 # col(c) must have value n
                matrix[r*size**2+c*size+n, size**2*2+r*size+c] = 1 #cell(r, c) must have a number
                box = int(r/length)*length+int(c/length)
                matrix[r*size**2+c*size+n, size**2*length+box*size+n] = 1 #box x must have value n

    row_names = np.vstack(row_names)

    gen = algorithm_x(row_names, matrix, [])
    for sol in gen:
        k = solution_to_array(sol)
        print(k)

    return

def test_algorithm_x():
    matrix = np.zeros([6, 7], dtype=int)
    matrix[0,] = [1,0,0,1,0,0,1]
    matrix[1,] = [1,0,0,1,0,0,0]
    matrix[2,] = [0,0,0,1,1,0,1]
    matrix[3,] = [0,0,1,0,1,1,0]
    matrix[4,] = [0,1,1,0,0,1,1]
    matrix[5,] = [0,1,0,0,0,0,1]

    row_names = np.vstack(['A', 'B', 'C', 'D', 'E', 'F'])
    gen = algorithm_x(row_names, matrix, [])
    for sol in gen:
        print(sol)

def solution_to_array(solution):
    k = np.zeros([9, 9], dtype=int)
    for s in solution:
        x, y, n = [int(z) for z in s.split('_')]
        k[x, y] = n
    return k


def algorithm_x(row_names, matrix, solution):
    if matrix.size == 0:
        yield solution
        return

    colsum = matrix.sum(axis=0)
    min_val = np.amin(colsum)
    if min_val == 0:
        return
    min_index = np.where(colsum == min_val)[0][0]
    col = matrix[:, min_index] #select first column with min #1s
    row_indexes = np.where(col==1)[0]  #get all rows with 1 in this column. they are the candidates

    for ridx in row_indexes: #loop through candidate list
        col_indexes = np.where(matrix[ridx,]==1)[0]  #get all #1 columns in the candidate row
        sub = matrix[:, col_indexes] #get the sub matrix of these columns
        col_sum = np.sum(sub, axis=1)
        rows_to_delete = np.where(col_sum > 0)[0] #filter the rows has 1. these are ones to be deleted

        solution.append(row_names[ridx][0])
        #print(row_names[ridx][0])
        reducted = np.delete(matrix, rows_to_delete, axis=0)
        reducted = np.delete(reducted, col_indexes, axis=1)
        reducted_rows = np.delete(row_names, rows_to_delete, axis=0)

        yield from algorithm_x(reducted_rows, reducted, solution)
        solution.pop()

def sudoku_solver(problem, diagonal=False):
    prob = np.vstack([[int(j) for j in list(r)] for r in problem.replace(' ', '').split('\n')])

    #print(prob)
    #simulated_annealing_solver(prob)
    #backtracking_solver(prob)
    print(prob)
    print(end='\n')
    exact_cover_solver(prob)

if __name__ == "__main__":
    #test_algorithm_x()
    sudoku_solver(problm6)


