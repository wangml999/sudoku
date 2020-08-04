## Back Tracking Algorithm
I started solving sudoku with a back tracking solver which basically is a brute-force method to try every number in the blank cells and tested by the constrains. If pass then it is solved otherwise try next number. Back tracking eventually will solve the puzzle but it will take exceptional long time on some puzzles. For example those have many blank cells in the beginning cells. 

## Simulated Annealing Algorithm
I then tried Stochastic method which is simulated annealing algorithm in this case. I might try genetic algorithm later if I have time. The simulated annealing on sudoku is to fill the blank cells with random number but satisfy the constrain of 3x3 meaning each 3x3 box will have number 1 to 9 each. Then I randomly select a 3x3 box and swap a pair of numbers in that box. So the new solution still satisfies the box constrain. It might have duplicates in the rows or columns though. To evaluate the new solution is better or not, the duplicates in rows and columns were counted. When sudoku is solved, there will be no duplicates so the score is zero. 

If I always select the better solution than the current one, the algorithm will get stuck at some point which cannot be improved anymore. This is so called local minima. Simulated Annealing uses a temperature to control the randomness. If a solution is worse by the scoring, the algorithm does not simply discard it. Instead using function P(E(s), E(snew), T) to calculate an acceptance probability. This basically says when new solution is better, select it. When it is worse, give it some probability to be selected. The probability is related to the how worse it is and the current temperature. The higher temperature the higher probability. 

Simulated Annealing is not a perfect solution. Even though added with some randomness, it will still get stuck in local minima which gives a solution with very low errors but not solving the puzzle. The Hyperparameters need to be fine tuned. But it is an interesting algorithm which can be applied to many problems. 

## Exact Cover Algorithm
Exact Cover is a perfect algorithm to solve sudoku. Imagine the blank cells of sudoku puzzle are sets of possible numbers. Exact cover is an algorithm to find the a group of sets which exactly covers the puzzle. That's how I understood it. The detail explaination can be found in the reference links. The basic idea is to represent all constrains of the puzzle with a 729x324 matrix. The elements of the matrix is either 0 or 1 representing a constrain is satisfied or not. And starting reducting the matrix by deleting rows and columns until it is empty. During the process, recording the rows being deleted which is the solution. 

Exact cover algorithm is beautiful and easy to implement. I was surprised it only took a few dozens of lines to implement and 1 second or two to solve almost any sudoku puzzles. The only thing I did not follow was I implemented it with numpy instead of double links. I found numpy runs fast on my old Macbook so I will leave it as is. 

## Reference
https://en.wikipedia.org/wiki/Sudoku_solving_algorithms <br>
https://en.wikipedia.org/wiki/Simulated_annealing <br>
https://gieseanw.wordpress.com/2011/06/16/solving-sudoku-revisited/ <br>



