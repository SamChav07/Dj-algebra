import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definimos la matriz A y el vector B
A = np.array([[2, 3, 1],
              [4, 1, 2],
              [3, 2, 3]])

B = np.array([1, 2, 3])

# Resolviendo el sistema de ecuaciones AX = B usando eliminación gaussiana
X = np.linalg.solve(A, B)

# Imprimimos los resultados
print("Solución del sistema:")
print(f"x = {X[0]}, y = {X[1]}, z = {X[2]}")

# Visualización en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Creamos una cuadrícula para graficar las soluciones
x_vals = np.linspace(-1, 1, 10)
y_vals = np.linspace(-1, 1, 10)
x_grid, y_grid = np.meshgrid(x_vals, y_vals)

# Calculamos z para cada par (x,y) usando la primera ecuación como ejemplo
z_grid = (1 - 2*x_grid - 3*y_grid)

# Graficamos la superficie resultante
ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.5, rstride=100, cstride=100)

# Añadimos puntos de solución
ax.scatter(X[0], X[1], X[2], color='r', s=100) # Punto de solución

# Etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Visualización de la Solución del Sistema de Ecuaciones')

# Mostramos el gráfico
plt.show()
