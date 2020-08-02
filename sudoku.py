import numpy as np
import math
import blessings

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

global global_step

def get_duplication(a):
    a_, counts = np.unique(a, return_counts=True)
    return np.sum(np.where(counts>1, counts, 0))

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
        return 0.99
    else:
        return math.exp(-(e1-e)/T)

def simulated_annealing_solver2(A, diagonal=False):
    empty_cells = np.where(A==0)
    empty_cells = [x for x in zip(empty_cells[0], empty_cells[1])]

    x = np.random.randint(1, 10, size=81).reshape(9,9)
    s = np.where(A!=0, A, x)
    #print(s)
    error = score(s)

    temperature = 100
    k = 0
    while temperature > 0.0001:
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
            error = error1
            k = k + 1
            if k % 100 == 0:
                print(r, c, n, error, error1, temperature, p, z)
                print(s)
        else:
            s = s_copy


    print("failed")

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


    #empty_cells = np.where(A==0)
    #empty_cells = [x for x in zip(empty_cells[0], empty_cells[1])]

    term = blessings.Terminal()

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
    #x = np.random.randint(1, 10, size=81).reshape(9,9)
    #s = np.where(A!=0, A, x)
    #print(s)
    error = score(s)

    k = 0
    temperature = 3
    while temperature > 0.0001:
        temperature = temperature * 0.99999


        #r, c = empty_cells[np.random.randint(0, len(empty_cells))]
        #n = np.random.randint(1, 10, 1)
        #s[r, c] = n

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
        # with term.fullscreen():
        #     term.move(0, 0)
        #     print(c1, c2, error, error1, temperature, p, z)
        k = k + 1
        if p >= z:
            error = error1
            print(s)
            print(c1, c2, error, error1, temperature, p, z)
        else:
            s = s_copy


    print("failed")


def sudoku_solver(problem, diagonal=False):
    global global_step
    prob = np.vstack([[int(j) for j in list(r)] for r in problem.replace(' ', '').split('\n')])

    #print(prob)
    global_step = 0
    simulated_annealing_solver(prob)
    #backtracking_solver(prob)

if __name__ == "__main__":
    sudoku_solver(problm5)
