import time

def nQueens(n):
    cols = [False] * n  
    diag1 = [False] * (2 * n - 1)  
    diag2 = [False] * (2 * n - 1)  
    solution = [-1] * n 
    solutions = []

    def solve(row):
        if row == n:
            solutions.append(solution[:])
            return

        
        start = 0 if row > 0 else n // 2

        for col in range(start, n):
            if not cols[col] and not diag1[row - col + n - 1] and not diag2[row + col]:
                solution[row] = col
                cols[col] = diag1[row - col + n - 1] = diag2[row + col] = True

                solve(row + 1)

                cols[col] = diag1[row - col + n - 1] = diag2[row + col] = False

    solve(0)

    
    final_solutions = solutions[:]
    for sol in solutions:
        flipped = [n - 1 - x for x in sol]
        final_solutions.append(flipped)

    return final_solutions



start = time.time()
n = int(input("Enter n: "))
solutions = nQueens(n)

stop = time.time()
time_taken = stop - start

print("\nSolutions:")
for i, solution in enumerate(solutions, start=1):
    print(f"Solution {i}: {solution}")

    
print(f"Number of solutions: {len(solutions)}")


print(f"Time taken for {n}: {time_taken} seconds")
