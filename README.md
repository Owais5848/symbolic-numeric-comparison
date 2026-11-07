# Symbolic vs. Numeric Comparison

> **University Project for BSCS**  
> **Course:** Numerical and Symbolic Computing  
> **Author:** BSCS Student  
> **Technologies:** Python, Streamlit, SymPy, NumPy, Matplotlib  

---

## 1. Project Introduction

In scientific and computer science applications, computational problems can be addressed through two distinct paradigms: **Symbolic Computation** and **Numerical Computation**. 

This university project is an interactive, web-based demonstration and research tool developed for the **Numerical and Symbolic Computing** course. It compares:
- **Exact Computer Algebra Systems (CAS)** using **SymPy**, which manipulates mathematical expressions analytically with infinite algebraic precision.
- **Discrete Numerical Methods** using **NumPy**, which approximates mathematical operations over discrete grids using floating-point arithmetic.

The application is deployed as a modern, dark-themed **Streamlit** dashboard that computes derivatives and integrals dynamically, quantifies numerical approximation errors, and plots continuous analytical curves alongside discrete numerical approximations.

---

## 2. Problem Statement

Computer science and engineering students frequently encounter mathematical software (such as Mathematica, Maple, MATLAB, and NumPy) without a clear understanding of the trade-offs between exact symbolic calculus and numerical approximations:

1. **Symbolic systems** guarantee zero truncation error and provide closed-form algebraic formulas, but they cannot solve every non-elementary integral or differential equation, and they scale poorly for large datasets.
2. **Numerical algorithms** are computationally fast, memory-efficient, and can approximate solutions for arbitrary data points, but they introduce **truncation errors** (from finite approximations) and **round-off errors** (from IEEE-754 floating-point limitations).

Without a direct side-by-side comparison, it is difficult to visualize how step size ($h$), discretization intervals ($n$), and algorithmic stencil design dictate the precision of numerical methods.

---

## 3. Project Objectives

- **Algebraic Simplification:** Implement safe parsing and automatic algebraic simplification of polynomial expressions using SymPy without unrestricted `eval()`.
- **Exact Calculus Evaluation:** Calculate exact symbolic derivatives ($f'(x)$), indefinite integrals ($\int f(x)dx$), and definite integrals ($\int_a^b f(x)dx$).
- **Numerical Approximation:** Implement the **Central Finite Difference Method** for differentiation and the **Composite Trapezoidal Rule** for definite integration using vectorized NumPy operations.
- **Error Quantification:** Dynamically calculate absolute error ($|\text{Exact} - \text{Numeric}|$) and relative percentage error.
- **Interactive Visualizations:** Generate publication-quality Matplotlib charts showing the function curve, analytical tangent line, discrete CFD stencil points, and trapezoidal geometric approximations.
- **Course Learning Verification:** Provide an automated 10-point test suite ensuring all mathematical calculations and UI components execute correctly.

---

## 4. Course Learning Outcomes (CLOs) Addressed

| CLO | Description | How It Is Achieved in This Project |
| :---: | :--- | :--- |
| **CLO 1** | Understand the theoretical and practical differences between symbolic algebraic manipulation and floating-point computation. | Implemented side-by-side comparative engines in `calculations.py` using SymPy and NumPy. |
| **CLO 2** | Apply finite difference techniques for numerical differentiation and analyze truncation error orders. | Implemented the second-order Central Finite Difference Method ($O(h^2)$) and compared it with exact analytical derivatives. |
| **CLO 3** | Apply composite numerical quadrature algorithms to evaluate definite integrals. | Implemented the Composite Trapezoidal Rule ($O(h^2)$) over configurable subintervals $n$. |
| **CLO 4** | Design, test, and deploy interactive scientific computing software in Python. | Built a modular architecture (`app.py`, `calculations.py`, `graphs.py`) with a Streamlit dark UI and automated testing. |

---

## 5. Technologies Used

- **Python 3.10+**: Core programming language.
- **Streamlit**: Web application framework for responsive sliders, inputs, metric cards, and layout.
- **SymPy**: Computer Algebra System (CAS) used for symbolic expression parsing, algebraic simplification, differentiation, and integration.
- **NumPy**: Vectorized numerical library used for numerical differentiation, trapezoidal summation, and grid evaluation.
- **Matplotlib**: Visualization library for dark-themed, publication-quality mathematical charts.
- **Pandas**: Structured tabular presentation of comparative results and error metrics.

---

## 6. What is Symbolic Computation?

Symbolic computation (also known as Computer Algebra) involves the exact manipulation of mathematical symbols, variables, and expressions rather than decimal numbers.

- **Variables as Symbols:** Rather than storing `x = 2.0`, $x$ is treated as an abstract mathematical symbol.
- **Infinite Precision:** Quantities such as $\sqrt{2}$, $\frac{1}{3}$, and $\pi$ are stored exactly without rounding or decimal truncation.
- **Algebraic Operations:** Capable of factoring, expanding, simplifying, solving equations symbolically, and finding general derivative and antiderivative formulas.
- **Primary Tool in Python:** `sympy` (`sp.Symbol`, `sp.diff`, `sp.integrate`, `sp.simplify`).

---

## 7. What is Numerical Computation?

Numerical computation involves algorithmic approximations using finite floating-point numbers (typically 64-bit IEEE-754 precision).

- **Concrete Number Grids:** Replaces continuous mathematical domains with discrete arrays of numbers (e.g., `np.linspace(a, b, n)`).
- **High Computational Speed:** Extremely fast vector operations suitable for massive datasets, physics engines, machine learning, and real-time simulations.
- **Approximation Errors:** Incurs two distinct forms of error:
  1. **Truncation Error:** Arises from truncating higher-order terms in infinite Taylor series approximations.
  2. **Round-Off Error:** Arises because computers have finite binary bits to represent real numbers (e.g., $0.1 + 0.2 \neq 0.3$).
- **Primary Tool in Python:** `numpy` arrays and vectorized operations.

---

## 8. Mathematical Function Used

The primary benchmark function assigned for this project is:

$$\text{Original Function:} \quad f(x) = x^3 - 3x^3 + 2x$$

### Algebraic Simplification:
Using SymPy's algebraic engine, the like cubic terms ($x^3$ and $-3x^3$) are combined algebraically:

$$\text{Simplified Polynomial Form:} \quad f(x) = -2x^3 + 2x$$

$$\text{Factored Form:} \quad f(x) = 2x(1 - x^2) = 2x(1 - x)(1 + x)$$

- **Roots (Zeros):** $x = -1, \quad x = 0, \quad x = 1$
- **Degree:** Cubic polynomial (degree 3)
- **Symmetry:** Odd function ($f(-x) = -f(x)$)

---

## 9. Differentiation: SymPy vs. Central Finite Difference

### A. Symbolic Differentiation (SymPy)
Using the power rule of calculus:
$$\frac{d}{dx}[-2x^3 + 2x] = -2(3x^2) + 2(1) = 2 - 6x^2$$

Evaluating at the assigned target point $x = 2$:
$$f'(2) = 2 - 6(2^2) = 2 - 6(4) = 2 - 24 = \mathbf{-22.0}$$

### B. Numerical Differentiation: Central Finite Difference (NumPy)
The Central Finite Difference (CFD) method estimates the tangent slope using a symmetric step size $h$:

$$f'(x) \approx \frac{f(x + h) - f(x - h)}{2h}$$

Using the project default step size $h = 0.0001$ at $x = 2$:
$$f(2 + 0.0001) = f(2.0001) = -2(2.0001)^3 + 2(2.0001) = -12.00220002$$
$$f(2 - 0.0001) = f(1.9999) = -2(1.9999)^3 + 2(1.9999) = -11.99779998$$
$$f'(2) \approx \frac{-12.00220002 - (-11.99779998)}{0.0002} = \mathbf{-22.00000002002156}$$

### Why Central Difference?
Unlike Forward ($\frac{f(x+h)-f(x)}{h}$) or Backward ($\frac{f(x)-f(x-h)}{h}$) differences which have first-order error $O(h)$, the Central Difference formula cancels out all odd Taylor series terms, yielding **second-order accuracy $O(h^2)$**.

---

## 10. Integration: SymPy vs. Trapezoidal Rule

### A. Symbolic Integration (SymPy)
- **Indefinite Integral (Antiderivative):**
  $$F(x) = \int (-2x^3 + 2x) dx = -2\left(\frac{x^4}{4}\right) + 2\left(\frac{x^2}{2}\right) + C = \mathbf{-\frac{x^4}{2} + x^2 + C}$$

- **Definite Integral from $a = 0$ to $b = 2$:**
  $$\int_0^2 (-2x^3 + 2x) dx = F(2) - F(0) = \left[-\frac{2^4}{2} + 2^2\right] - [0] = (-8 + 4) - 0 = \mathbf{-4.0}$$

### B. Numerical Integration: Composite Trapezoidal Rule (NumPy)
The interval $[a, b] = [0, 2]$ is divided into $n = 1000$ uniform subintervals of width $h = \frac{b - a}{n} = \frac{2 - 0}{1000} = 0.002$:

$$\int_a^b f(x) dx \approx \frac{h}{2} \left[ f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]$$

- Numerical Result: $\mathbf{-4.00000800}$
- Absolute Error: $|-4.0 - (-4.000008)| = \mathbf{8.00 \times 10^{-6}}$

---

## 11. Summary of Mathematical Formulas

| Operation | Method | Formula | Order of Accuracy |
| :--- | :--- | :--- | :---: |
| **Differentiation** | Exact (SymPy) | $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ | Exact ($\infty$) |
| **Differentiation** | Numerical (CFD) | $f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$ | $O(h^2)$ |
| **Indefinite Integral** | Exact (SymPy) | $F(x) = \int f(x)dx + C$ | Exact ($\infty$) |
| **Definite Integral** | Exact (SymPy) | $\int_a^b f(x)dx = F(b) - F(a)$ | Exact ($\infty$) |
| **Definite Integral** | Numerical (Trapezoidal) | $\frac{h}{2}\left[f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n)\right]$ | $O(h^2)$ |
| **Absolute Error** | Analytical vs Numerical | $\text{Absolute Error} = \lvert \text{Exact} - \text{Numerical} \rvert$ | — |
| **Relative Error** | Percentage Error | $\text{Relative Error} = \frac{\lvert \text{Exact} - \text{Numerical} \rvert}{\lvert \text{Exact} \rvert} \times 100\%$ | — |

---

## 12. Project Methodology & Architecture

The application adopts a modular, clean separation of concerns:

```text
Symbolic-Numeric-Comparison/
│
├── app.py              # Presentation Layer (Streamlit Dark Dashboard, UI & Controls)
├── calculations.py     # Computation Layer (SymPy CAS & NumPy Numerical Algorithms)
├── graphs.py           # Visualization Layer (Matplotlib Publication-Grade Dark Plots)
├── test_suite.py       # Automated Verification Layer (10 Unit & Integration Tests)
├── requirements.txt    # Project Dependencies
└── README.md           # Academic Documentation & Project Guide
```

### Execution Pipeline:
1. **Input Sanitization:** User input string is cleaned, converted (`^` $\to$ `**`), and checked against restricted Python keywords to prevent code injection.
2. **Symbolic Evaluation:** SymPy parses the expression with `evaluate=False`, combines like terms with `sp.simplify()`, and calculates exact calculus formulas.
3. **NumPy Vectorization:** `sp.lambdify` generates a high-speed NumPy callable.
4. **Numerical Approximation:** Central finite difference and composite trapezoidal algorithms evaluate over discrete arrays.
5. **Error Analysis:** Quantifies absolute and relative errors.
6. **Rendering:** Streamlit renders formatted LaTeX math equations, custom metric cards, comparison dataframes, and Matplotlib figures.

---

## 13. Sample Results ($x = 2$, $a = 0$, $b = 2$, $h = 0.0001$, $n = 1000$)

| Metric / Parameter | Symbolic Value (SymPy) | Numerical Value (NumPy) | Absolute Error | Relative Error (%) | Accuracy Order |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Function Simplification** | $-2x^3 + 2x$ | $-2x^3 + 2x$ | $0.00$ | $0.00\%$ | Exact |
| **Derivative at $x = 2$** | **$-22.00000000$** | **$-22.00000002$** | **$2.00 \times 10^{-8}$** | $9.10 \times 10^{-8}\%$ | $O(h^2)$ |
| **Indefinite Integral** | $-\frac{x^4}{2} + x^2 + C$ | N/A (Analytical only) | N/A | N/A | Exact |
| **Definite Integral $[0, 2]$** | **$-4.00000000$** | **$-4.00000800$** | **$8.00 \times 10^{-6}$** | $0.0002\%$ | $O(h^2)$ |

---

## 14. Graphical Representation

The visualization module (`graphs.py`) produces four dark-themed charts matching the dashboard's navy, purple, and blue palette:

1. **Original Function Graph (`plot_original_function`):**
   - Plots the continuous curve $f(x)$ across an automatically scaled domain.
   - Highlights the derivative evaluation point $(x, f(x))$ in emerald green.
   - Marks the integration boundaries $x = a$ and $x = b$ with vertical dashed lines.

2. **Symbolic Derivative Graph (`plot_symbolic_derivative`):**
   - Plots the exact derivative curve $f'(x) = 2 - 6x^2$ derived using SymPy calculus rules.
   - Plots the horizontal zero axis ($y=0$) and marks the evaluated slope at $x=2$ ($-22.0$).

3. **Derivative Comparison Graph (`plot_derivative_comparison`):**
   - Overlays the **exact analytical derivative curve** (vibrant purple line) with **discrete Central Finite Difference estimates** (electric blue open circles).
   - Visually proves that the CFD formula accurately tracks the continuous derivative across the entire domain.

4. **Integration Graph (`plot_integration_graph`):**
   - Shaded purple region represents the exact analytical area $\int_a^b f(x)dx$.
   - Draws geometric **trapezoid pillars and chord segments** (in emerald green) over the interval $[a, b]$, making the trapezoidal approximation visually intuitive.

---

## 15. Error Calculation and Comparison

### Why do errors occur in numerical computing?

1. **Truncation Error in Differentiation:**
   By Taylor expansion:
   $$f(x+h) = f(x) + f'(x)h + \frac{f''(x)}{2!}h^2 + \frac{f'''(x)}{3!}h^3 + O(h^4)$$
   $$f(x-h) = f(x) - f'(x)h + \frac{f''(x)}{2!}h^2 - \frac{f'''(x)}{3!}h^3 + O(h^4)$$
   Subtracting the two equations eliminates all even-degree derivative terms:
   $$f(x+h) - f(x-h) = 2f'(x)h + \frac{2f'''(x)}{6}h^3 + O(h^5)$$
   Dividing by $2h$:
   $$\frac{f(x+h) - f(x-h)}{2h} = f'(x) + \underbrace{\frac{f'''(x)}{6}h^2}_{\text{Leading Truncation Error}} + O(h^4)$$
   Because $h = 0.0001$, $h^2 = 10^{-8}$. For our cubic polynomial $f'''(x) = -12$:
   $$\text{Error} \approx \frac{-12}{6}(10^{-8}) = -2.0 \times 10^{-8}$$
   This matches our observed absolute error of $2.00 \times 10^{-8}$!

2. **Truncation Error in Trapezoidal Integration:**
   The error for composite trapezoids is:
   $$E_{\text{trap}} = -\frac{(b - a) h^2}{12} f''(\xi), \quad \xi \in [a, b]$$
   With $h = 0.002$, $h^2 = 4 \times 10^{-6}$, explaining the small error of $8.00 \times 10^{-6}$.

---

## 16. Project Features

- **Interactive Parameter Control:** Sliders and inputs for evaluation point $x$, step size $h$, integration limits $a$ and $b$, and subintervals $n$.
- **Dark Dashboard UI:** Modern color palette featuring Deep Navy (`#0B0F19`), Slate (`#111827`), Electric Blue (`#38BDF8`), and Purple (`#A855F7`).
- **Dynamic Formula Rendering:** Clean LaTeX typesetting for all formulas, integrals, and derivatives.
- **Side-by-Side Metric Cards:** Instant visual comparison of Symbolic, Numerical, and Error figures.
- **Robust Security & Parsing:** Safe expression parser preventing unrestricted `eval()`, code injection, and illegal syntax.
- **Responsive 2x2 Grid & Detailed Tabs:** View all four graphs at once or inspect individual charts in high resolution.
- **Academic Viva Guide:** Built-in collapsible study notes answering theoretical exam questions on error orders and numerical stability.

---

## 17. Automated Testing Report

An automated test suite (`test_suite.py`) was executed to verify mathematical accuracy, edge-case resilience, and graphical generation:

```text
======================================================================
STARTING TEST SUITE: Symbolic vs Numeric Comparison
======================================================================
[PASS] - 1. Default Function Simplification (Original: x**3 - 3*x**3 + 2*x -> Simplified: -2*x**3 + 2*x)
[PASS] - 2. Symbolic Derivative Evaluation at x=2 (Formula: f'(x)=2 - 6*x**2, Evaluated: -22.0)
[PASS] - 3. Numerical Derivative (Central Difference, h=0.0001) (Approx: -22.00000002, Abs Error: 2.00e-08)
[PASS] - 4. Symbolic Indefinite Integral (Formula: -x**4/2 + x**2 + C, LaTeX: - \frac{x^{4}}{2} + x^{2} + C)
[PASS] - 5. Symbolic Definite Integral [0 to 2] (Evaluated: -4.0)
[PASS] - 6. Numerical Definite Integral (Trapezoidal, n=1000) (Approx: -4.00000800, Abs Error: 8.00e-06)
[PASS] - 7. Dynamic Function & Parameter Switching (sin(x): d=0.5000, i=2.0000; exp(x): d=2.7183, i=1.7183)
[PASS] - 8. All Four Graphs Generation & Type Check (All 4 return valid matplotlib.figure.Figure)
[PASS] - 9. Invalid Inputs & Boundary Edge Cases (Syntax error caught, Security caught, h<=0 caught, n<1 caught, a==b: True, a>b: True)
[PASS] - 10. Missing Imports & Function Mismatch Check (Missing graphs: [], Missing calc: [])
======================================================================
TEST SUMMARY: 10 PASSED, 0 FAILED (TOTAL 10)
======================================================================
```

---

## 18. Installation Instructions

### Prerequisites
- **Python 3.10** or higher installed on your computer.
- `pip` package manager.

### Step 1: Open Terminal in Project Directory
```bash
cd c:\Users\pc\Desktop\Symbolic-Numeric-Comparison
```

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

#### Contents of `requirements.txt`:
```text
streamlit>=1.30.0
sympy>=1.12
numpy>=1.24.0
matplotlib>=3.8.0
```

---

## 19. How to Run the Project

### To Launch the Interactive Streamlit Web App:
```bash
streamlit run app.py
```
Streamlit will automatically open the dashboard in your default web browser at:
```text
http://localhost:8501
```

### To Run the Automated Test Suite:
```bash
python test_suite.py
```

### To Run Standalone Backend Math Tests:
```bash
python calculations.py
```

---

## 20. Conclusion

This project successfully demonstrates the foundational principles of the **Numerical and Symbolic Computing** curriculum:

1. **Symbolic computation (SymPy)** serves as the ultimate mathematical reference, producing exact analytical formulas and zero truncation error for algebraic operations.
2. **Numerical computation (NumPy)** provides the high-performance computational backbone required for engineering applications, approximating complex operations with high precision when appropriate step sizes ($h$) and stencil methods (such as Central Differences and Trapezoids) are chosen.
3. The observed errors ($2.00 \times 10^{-8}$ for differentiation and $8.00 \times 10^{-6}$ for integration) rigorously validate the theoretical second-order convergence rate ($O(h^2)$) taught in numerical analysis.
