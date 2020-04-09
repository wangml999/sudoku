import numpy as np

problem = '008 000 003\n'\
          '050 008 960\n'\
          '702 006 540\n'\
          '040 005 801\n'\
          '000 904 000\n'\
          '205 800 090\n'\
          '027 100 406\n'\
          '081 600 020\n'\
          '600 000 100'


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

def solver(A, diagonal=False):
    if is_solved(A, diagonal):
        print(A)
        return True

    for r in range(A.shape[0]):
        for c in range(A.shape[1]):
            if A[r, c] == 0:
                for i in range(1,10):
                    a = np.copy(A)
                    a[r, c] = i
                    if not is_legal(a, diagonal):
                        continue
                    if solver(a, diagonal):
                        return True
                return False
    return False

def sudoku_solver(problem, diagonal=False):
    prob = np.vstack([[int(j) for j in list(r)] for r in problem.replace(' ', '').split('\n')])
    solver(prob)


if __name__ == "__main__":
    sudoku_solver(problem)


