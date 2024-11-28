# Dj-algebra

![Logo de calcX](https://github.com/SamChav07/Dj-algebra/raw/main/my_algebra_calculator/eliminacionGauss/staticWeb/assets/calcXlogo.svg)

## Modulos actuales
- |-> Método Escalonado
- |--> Operaciones Combinadas de Vectores 
- |---> Multiplicación Vector fila por columna

## Instalación 
El primer paso es crear el entorno virtual:
**MacOs**
```
python3 -m venv algebraLineal
```
**Windows**
```
py -m venv algebraLineal
```

Luego se debe de activar el Venv: `source algebraLineal/bin/activate`, una vez activado se mostrará de esta manera `(algebraLineal)...$`.
Django se puede instalar por medio del `pip3`:
```
python3 -m pip install Django
```
### Ejecución del proyecto
1. Acceder a la carpeta `/my_algebra_calculator`
2. Ejecutar el siguiente comando:
```
# mOs
python3 manage.py runserver
# Wnds
py manage.py runserver
```
Al final del mensaje en la terminal aparecerá un mensaje similar a este:
```
Django version 5.1, using settings 'my_algebra_calculator.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
3. Debes de acceder al link por default `http://127.0.0.1:8000/`

> ***|--> Obviamente el servidor se cae una vez detenido. Para detener el servidor local se usa `control + c` o `^C`***

## Tablas

### Método Escalonado
Input:
- Ecuaciones Y
- Variables X
> ***Se crea una tabla de nY+1 y nX, donde se le suma una columna de resultado de la ecuación.***

### Operaciones Combinadas de Vectores
Input: 
- Numero de Vectores X
- Dimension de vectores Y
> ***Se crean dos tablas, la primera es de vectores con el numero de vectores nX y componentes(Dimension) nY, la segunda tabla corresponde a los escalares vector nY escalar nX.*** 

### Multiplicación de Vector Fila x Vector Columna
Input:
- Dimension del vector Y & X
> ***Crea dos tablas, la primera una fila nY = 1 y nX(Dimension), la segunda tabla es una columna nX = 1 y nY(Dimension).***
