import numpy as np

# Матриця коефіцієнтів A
A = np.array([[1, 2],
              [1, 4]])

# Вектор правих частин B
B = np.array([5, 10])

# Знаходимо обернену матрицю A
A_inv = np.linalg.inv(A)

# Знаходимо розв'язок X
X = np.dot(A_inv, B)

print(X)
