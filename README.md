# Dj-algebra

![calcX Logo](https://github.com/SamChav07/Dj-algebra/raw/main/my_algebra_calculator/eliminacionGauss/static/assets/calcXlogo.svg)

## Current Modules
- |-> Row Echelon Method  
- |--> Combined Vector Operations  
- |---> Row Vector × Column Vector Multiplication  

## Installation
The first step is to create the virtual environment:  

**MacOS**
```bash
python3 -m venv algebraLineal
```

**Windows**
```bash
py -m venv algebraLineal
```

Then, activate the virtual environment:  
Run `source algebraLineal/bin/activate`, and once activated, it will be displayed as `(algebraLineal)...$`.  

Django can be installed via `pip3`:
```bash
python3 -m pip install Django
```

### Running the Project
1. Navigate to the `/my_algebra_calculator` folder.  
2. Execute the following command:  

```bash
# MacOS
python3 manage.py runserver
# Windows
py manage.py runserver
```

At the end, the terminal will display a message similar to this:
```bash
Django version 5.1, using settings 'my_algebra_calculator.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
3. Access the default link `http://127.0.0.1:8000/`.

> ***|--> Obviously, the server stops once it's terminated. To stop the local server, use `control + c` or `^C`.***

## Tables

### Row Echelon Method  
**Input:**  
- Equations Y  
- Variables X  
> ***A table is created with dimensions nY+1 and nX, where an additional column is added for the equation result.***  

### Combined Vector Operations  
**Input:**  
- Number of vectors X  
- Dimension of vectors Y  
> ***Two tables are created: The first contains the vectors with a count of nX and components (Dimension) nY. The second table corresponds to the scalars, with vector nY and scalar nX.***  

### Row Vector × Column Vector Multiplication  
**Input:**  
- Dimension of vector Y & X  
> ***Two tables are created: The first is a row with nY = 1 and nX (Dimension). The second table is a column with nX = 1 and nY (Dimension).***  
