import numpy as np
from scipy.optimize import linprog
import tkinter as tk
from tkinter import messagebox

class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Simplex")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Labels y entradas para la función objetivo
        tk.Label(self.root, text="Coeficientes de la función objetivo").grid(row=0, column=0, columnspan=3)
        
        self.obj_vars = []
        for i in range(3):  # Suponiendo 3 variables para simplicidad
            var = tk.DoubleVar()
            entry = tk.Entry(self.root, textvariable=var)
            entry.grid(row=1, column=i)
            self.obj_vars.append(var)
        
        # Labels y entradas para las restricciones
        tk.Label(self.root, text="Coeficientes de las restricciones").grid(row=2, column=0, columnspan=3)
        
        self.constraint_vars = []
        self.constraint_entries = []
        for i in range(3):  # Suponiendo 3 restricciones para simplicidad
            row_vars = []
            row_entries = []
            for j in range(3):
                var = tk.DoubleVar()
                entry = tk.Entry(self.root, textvariable=var)
                entry.grid(row=i+3, column=j)
                row_vars.append(var)
                row_entries.append(entry)
            self.constraint_vars.append(row_vars)
            self.constraint_entries.append(row_entries)
        
        # Entradas para los lados derechos de las restricciones
        tk.Label(self.root, text="Lados derechos de las restricciones").grid(row=2, column=3)
        
        self.rhs_vars = []
        for i in range(3):  # Suponiendo 3 restricciones para simplicidad
            var = tk.DoubleVar()
            entry = tk.Entry(self.root, textvariable=var)
            entry.grid(row=i+3, column=3)
            self.rhs_vars.append(var)
        
        # Botón para resolver
        tk.Button(self.root, text="Resolver", command=self.solve).grid(row=6, column=0, columnspan=4)
        
        # Área para mostrar resultados
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=7, column=0, columnspan=4)
        
    def solve(self):
        # Obtener los coeficientes de la función objetivo
        c = np.array([var.get() for var in self.obj_vars])
        
        # Obtener los coeficientes de las restricciones
        A = np.array([[var.get() for var in row_vars] for row_vars in self.constraint_vars])
        
        # Obtener los valores del lado derecho de las restricciones
        b = np.array([var.get() for var in self.rhs_vars])
        
        # Convertir las restricciones a <= en lugar de >=
        A = -A
        b = -b
        
        # Restricciones de no negatividad
        bounds = [(0, None)] * len(c)
        
        # Resolver el problema de programación lineal
        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='simplex')
        
        # Mostrar los resultados
        if result.success:
            result_str = 'La solución óptima es:\n'
            for i in range(len(c)):
                result_str += f'X{i+1} = {result.x[i]:.4f}\n'
            result_str += f'El valor mínimo de Z es: {result.fun:.4f}\n'
            
            # Mostrar la tabla final
            result_str += "\nTabla final (última iteración):\n"
            result_str += "================================\n"
            result_str += f"{'Variable':<10} {'Coeficiente':<15} {'Valor':<10}\n"
            result_str += f"{'-'*35}\n"
            for i, (coef, val) in enumerate(zip(c, result.x), start=1):
                result_str += f"{'X' + str(i):<10} {coef:<15} {val:<10.4f}\n"
            for i, slack in enumerate(result.slack, start=1):
                result_str += f"{'Slack ' + str(i):<10} {'-':<15} {slack:<10.4f}\n"
            result_str += f"{'Z':<10} {'':<15} {result.fun:<10.4f}\n"
        else:
            result_str = 'No se encontró una solución óptima.'
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_str)

# Crear la ventana principal
root = tk.Tk()
app = SimplexApp(root)
root.mainloop()
