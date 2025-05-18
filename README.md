# Dj-algebra

![calcX Logo](https://github.com/SamChav07/Dj-algebra/my_algebra_calculator/eliminacionGauss/staticWeb/assets/calcXlogo.svg)

Dj-algebra is an educational web platform developed in **Django** to explore, visualize, and solve classic problems in **Linear Algebra** and **Numerical Analysis**. Its interactive interface is designed for both students and educators, facilitating step-by-step learning of fundamental algorithms such as **Gaussian Elimination**, **Cramer's Rule**, **LU Factorization**, **Vector Operations**, and **Numerical Methods like Bisection**.

---

## 🚀 Current Modules

✔️ **Linear Algebra**
- Gaussian Elimination: Step-by-step transformation of matrices into row echelon form.
- Cramer's Rule: Solving linear systems using determinants.
- LU Factorization: Decomposing a matrix into L and U factors.
- Inverse Matrix: Calculation using Gauss-Jordan elimination.
- Determinant: Evaluation with the option to display intermediate steps.
- Matrix × Vector Multiplication: Includes tests of distributive properties.
- Matrix Operations: Addition, multiplication, transposition, and scaling.

➕ **Vector Operations**
- Linear Combinations: Calculation of scaled vector combinations.
- Dot Product: Explanation and step-by-step development.

📊 **Numerical Analysis**
- **Bisection Method:** Finds function roots with detailed iteration reporting.

---

## ⚙️ Installation

### **1. Create a virtual environment**
#### MacOS / Linux
```bash
python3 -m venv algebraLineal
source algebraLineal/bin/activate
```
#### Windows
```bash
py -m venv algebraLineal
.\algebraLineal\Scripts\activate
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```
*(If you don't have `requirements.txt`, install at least: Django, SymPy, and NumPy)*

### **3. Run the development server**
```bash
cd my_algebra_calculator
python manage.py runserver
```

Once executed, the terminal will display a message similar to:
```bash
Django version 5.1, using settings 'my_algebra_calculator.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
🔗 **Access:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Module Examples

### **Gaussian Elimination**
📌 **Input:** Augmented matrix of a linear system.  
🔎 **Output:** Detailed steps of each row operation, pivot columns, final solution (unique, multiple, or nonexistent).  

### **Combined Vector Operations**
📌 **Input:** List of vectors and scalars.  
🔎 **Output:** Result of the sum of scaled vectors, along with the formatted equation.  

### **Matrix × Vector Multiplication**
📌 **Input:** Matrix A and vectors u and v.  
🔎 **Output:** Evaluation of the distributive property:  `A(u+v) = Au + Av.`

### **Bisection Method**
📌 **Input:** Mathematical function, interval `[a, b]`, tolerance.  
🔎 **Output:** Approximate root with intermediate iteration reporting and convergence analysis.  
