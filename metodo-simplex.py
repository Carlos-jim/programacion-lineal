import numpy as np
from scipy.optimize import linprog

def simplex():
    print("Método Simplex para Programación Lineal")
    print("1. Maximizar")
    print("2. Minimizar")
    choice = int(input("Elige una opción (1 o 2): "))

    if choice == 1:
        maximize = True
    elif choice == 2:
        maximize = False
    else:
        print("Opción no válida")
        return

    num_vars = int(input("Ingrese el número de variables: "))
    num_constraints = int(input("Ingrese el número de restricciones: "))

    c = []
    print("Ingrese los coeficientes de la función objetivo: ")
    for i in range(num_vars):
        coef = float(input(f"Coeficiente de x{i+1}: "))
        c.append(coef)

    if maximize:
        c = [-coef for coef in c]

    A = []
    b = []
    print("Ingrese las restricciones (forma: Ax ≤ b): ")
    for i in range(num_constraints):
        row = []
        print(f"Restricción {i+1}:")
        for j in range(num_vars):
            coef = float(input(f"Coeficiente de x{j+1}: "))
            row.append(coef)
        A.append(row)
        rhs = float(input("Ingrese el lado derecho de la restricción: "))
        b.append(rhs)

    # Resolver el problema utilizando linprog
    result = linprog(c, A_ub=A, b_ub=b, method='simplex')

    # Mostrar los resultados
    if result.success:
        print("Solución óptima encontrada:")
        for i, x in enumerate(result.x):
            print(f"x{i+1} = {x}")
        if maximize:
            print(f"Valor óptimo de la función objetivo: {-result.fun}")
        else:
            print(f"Valor óptimo de la función objetivo: {result.fun}")
    else:
        print("No se encontró una solución óptima")

if __name__ == "__main__":
    simplex()
