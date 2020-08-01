import numpy as np

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

global global_step

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
    global global_step
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
                    global_step = global_step + 1
                    if global_step % 1000 == 0:
                        print(global_step)
                        print(a)
                    if not is_legal(a, diagonal):
                        continue
                    if backtracking_solver(a, diagonal):
                        return True
                return False
    return False

def sudoku_solver(problem, diagonal=False):
    global global_step
    prob = np.vstack([[int(j) for j in list(r)] for r in problem.replace(' ', '').split('\n')])

    #print(prob)
    global_step = 0
    backtracking_solver(prob)


if __name__ == "__main__":
    sudoku_solver(problm3)


