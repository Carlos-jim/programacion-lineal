import numpy as np

def print_tableau(tableau):
    """
    Imprimir la tabla del Simplex.
    """
    print("\nTabla actual del Simplex:")
    print(tableau)
    print()

def simplex(c, A, b):
    """
    Resolver el método Simplex.
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
            raise ValueError("Error, intentelo nuevamente, parece no haber solución")

        ratios = np.divide(tableau[:-1, -1], tableau[:-1, pivot_col], 
                           out=np.full(m, np.inf), where=tableau[:-1, pivot_col] > 0)
        pivot_row = np.argmin(ratios)

        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element
        for i in range(m + 1):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

        print_tableau(tableau)  # Imprimir tabla después de cada pivote

    solution = np.zeros(n)
    for i in range(n):
        col = tableau[:-1, i]
        if np.count_nonzero(col) == 1 and np.any(col == 1):
            solution[i] = tableau[np.where(col == 1)[0][0], -1]

    optimal_value = tableau[-1, -1]

    return solution, optimal_value

def get_user_input():
    while True:
        try:
            print("Introduce el número de variables de decisión:")
            n = int(input())
            
            print("Introduce el número de restricciones:")
            m = int(input())

            print("Introduce los coeficientes de la función objetivo separados por espacios:")
            c = np.array(list(map(float, input().split())))

            print("¿Deseas maximizar o minimizar la función objetivo? (max/min):")
            objective = input().strip().lower()

            if objective not in ['max', 'min']:
                raise ValueError("Por favor, introduce 'max' o 'min' para la función objetivo.")

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
                if constraint_type not in [1, 2, 3]:
                    raise ValueError("Por favor, introduce un tipo de restricción válido (1, 2, 3).")
                constraints.append(constraint_type)
                print(f"Introduce el valor del término independiente de la restricción {i + 1}:")
                b[i] = float(input())

                if constraint_type == 3:
                    A[i] = -A[i]
                    b[i] = -b[i]

            return c, A, b, constraints, objective
        except ValueError as e:
            print(e)
            print("Por favor, inténtelo de nuevo.\n")

def main():
    while True:
        try:
            c, A, b, constraints, objective = get_user_input()
            solution, optimal_value = simplex(c, A, b)
            if objective == 'min':
                optimal_value = -optimal_value
            print(f"Solución óptima: {solution}")
            print(f"Valor óptimo de la función objetivo: {optimal_value}")
            break
        except ValueError as e:
            print(e)
            print("Error en el proceso. Por favor, inténtelo de nuevo.\n")

if __name__ == "__main__":
    main()
