import numpy as np

def print_tableau(tableau):
    """
    Imprimir la tabla
    """
    print("\nTabla actual del Simplex:")
    print(tableau)
    print()

def simplex(c, A, b):
    """
    Resolver el método simplex
    """
    m, n = A.shape

    # Crear el tableau
    tableau = np.zeros((m + 1, n + m + 1))
    tableau[:-1, :n] = A
    tableau[:-1, n:n + m] = np.eye(m)
    tableau[:-1, -1] = b
    tableau[-1, :n] = -c

    print_tableau(tableau)  # Imprimir tabla inicial 

    while True:
        if np.all(tableau[-1, :-1] >= 0):
            break

        pivot_col = np.argmin(tableau[-1, :-1])

        if np.all(tableau[:-1, pivot_col] <= 0):
            raise ValueError("Error, inténtelo nuevamente, parece no haber solución")

        ratios = np.divide(tableau[:-1, -1], tableau[:-1, pivot_col], 
                           out=np.full(m, np.inf), where=tableau[:-1, pivot_col] > 0)
        pivot_row = np.argmin(ratios)

        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element
        for i in range(m + 1):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

        print_tableau(tableau)  # Imprimir tabla después de cada pivoteo

    solution = np.zeros(n)
    for i in range(n):
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.any(col == 1):
            solution[i] = tableau[np.where(col == 1)[0][0], -1]

    optimal_value = tableau[-1, -1]

    return solution, optimal_value

def get_user_input():
    print("Introduce el número de variables de decisión:")
    n = int(input())
    
    print("Introduce el número de restricciones:")
    m = int(input())

    print("Introduce los coeficientes de la función objetivo separados por espacios:")
    c = np.array(list(map(float, input().split())))

    print("¿Deseas maximizar o minimizar la función objetivo? (max/min):")
    objective = input().strip().lower()

    if objective == 'min':
        c = -c

    A = np.zeros((m, n))
    b = np.zeros(m)
    constraints = []

    for i in range(m):
        print(f"Introduce los coeficientes de la restricción {i + 1} separados por espacios:")
        A[i] = np.array(list(map(float, input().split())))
        print("Selecciona el tipo de restricción:")
        print("1. <=\n2. =\n3. >=")
        constraint_type = int(input())
        constraints.append(constraint_type)
        print(f"Introduce el valor del término independiente de la restricción {i + 1}:")
        b[i] = float(input())

        if constraint_type == 3:
            A[i] = -A[i]
            b[i] = -b[i]

    return c, A, b, constraints, objective

def main():
    # Suprimir la notación científica en los resultados de impresión
    np.set_printoptions(suppress=True)
    
    c, A, b, constraints, objective = get_user_input()
    try:
        solution, optimal_value = simplex(c, A, b)
        if objective == 'min':
            optimal_value = -optimal_value
        print(f"Solución óptima: {solution}")
        print(f"Valor óptimo de la función objetivo: {optimal_value}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
