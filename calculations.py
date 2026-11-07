"""
calculations.py
----------------
Mathematical Backend for the Symbolic vs Numeric Comparison Project.

This module provides separate, reusable functions for:
1. Simplifying algebraic expressions using SymPy.
2. Symbolic Differentiation and exact evaluation at x.
3. Numerical Differentiation using the Central Finite Difference Method.
4. Symbolic Indefinite and Definite Integration.
5. Numerical Definite Integration using the Composite Trapezoidal Rule.
6. Error Analysis (Absolute and Relative Error).

All calculations are computed dynamically without hardcoded values.
Safety: Expressions are parsed safely via SymPy sympify without unrestricted Python eval().
"""

import math
import sympy as sp
import numpy as np

# Global real symbol used for all single-variable calculations
x = sp.Symbol('x', real=True)

# Default configuration values specified for this project
DEFAULT_FUNCTION_STR = "x**3 - 3*x**3 + 2*x"
DEFAULT_X_VAL = 2.0
DEFAULT_H = 0.0001
DEFAULT_A = 0.0
DEFAULT_B = 2.0
DEFAULT_N = 1000

# Allowed function names for safe parsing (whitelist approach)
SAFE_LOCALS = {
    'x': x,
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'exp': sp.exp,
    'log': sp.log,
    'sqrt': sp.sqrt,
    'pi': sp.pi,
    'E': sp.E,
    'abs': sp.Abs
}

# Forbidden keywords to prevent code injection
FORBIDDEN_KEYWORDS = [
    '__', 'import', 'exec', 'eval', 'open', 'os', 'sys',
    'subprocess', 'lambda', 'globals', 'locals', 'builtins'
]


# -----------------------------------------------------------------------------
# 1. INPUT VALIDATION & SAFE PARSING
# -----------------------------------------------------------------------------

def validate_expression_string(expr_str: str) -> str:
    """
    Validates that the input string does not contain malicious code or commands.
    Replaces common syntax shortcuts (like '^' for power) with Python '**'.

    Parameters:
        expr_str (str): Mathematical expression entered by the user.

    Returns:
        str: Cleaned expression string.

    Raises:
        ValueError: If forbidden keywords or invalid characters are detected.
    """
    if not isinstance(expr_str, str) or not expr_str.strip():
        raise ValueError("Expression cannot be empty.")

    cleaned = expr_str.strip().lower()

    # Check for dangerous code injection attempts
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in cleaned:
            raise ValueError(f"Security Warning: Keyword '{keyword}' is not allowed.")

    # Convert '^' to '**' so students can use both styles of exponentiation
    cleaned = cleaned.replace('^', '**')
    return cleaned


def parse_and_simplify(expr_str: str = DEFAULT_FUNCTION_STR):
    """
    Safely parses a mathematical string into a SymPy expression,
    simplifies it using SymPy's algebraic engine, and builds a fast
    vectorized NumPy lambda function for numerical calculations.

    Parameters:
        expr_str (str): The function expression, e.g., 'x**3 - 3*x**3 + 2*x'.

    Returns:
        dict: A structured dictionary containing:
            - 'original_str': Raw input string
            - 'original_sym': Unsimplified SymPy expression
            - 'simplified_sym': Simplified SymPy expression (factored/simplified form)
            - 'expanded_poly': Simplified expression in standard polynomial form
            - 'num_func': Vectorized numerical function (callable by NumPy)
            - 'latex_original': LaTeX representation of original function
            - 'latex_simplified': LaTeX representation of simplified function
    """
    cleaned = validate_expression_string(expr_str)

    try:
        # evaluate=False keeps original terms intact (e.g. x^3 - 3x^3 + 2x)
        original_sym = sp.sympify(cleaned, locals=SAFE_LOCALS, evaluate=False)
    except Exception as e:
        raise ValueError(f"Could not parse mathematical expression: {e}")

    # Step 1: Use SymPy to simplify the original function
    # For 'x**3 - 3*x**3 + 2*x', like terms (x^3 and -3x^3) are combined to -2x^3
    simplified_sym = sp.simplify(original_sym)
    expanded_poly = sp.expand(simplified_sym)

    # Build a fast vectorized numerical function using sp.lambdify (maps to NumPy)
    num_func = sp.lambdify(x, simplified_sym, modules=['numpy'])

    return {
        "original_str": expr_str,
        "original_sym": original_sym,
        "simplified_sym": simplified_sym,
        "expanded_poly": expanded_poly,
        "num_func": num_func,
        "latex_original": sp.latex(original_sym),
        "latex_simplified": sp.latex(expanded_poly)
    }


# -----------------------------------------------------------------------------
# 2. DIFFERENTIATION: SYMBOLIC (EXACT) & NUMERICAL (CENTRAL FINITE DIFFERENCE)
# -----------------------------------------------------------------------------

def compute_symbolic_derivative(sym_expr, x_val: float = DEFAULT_X_VAL):
    """
    Calculates the exact derivative symbolically using SymPy calculus rules,
    and evaluates it at a specific value of x.

    Parameters:
        sym_expr: SymPy expression to differentiate (f(x)).
        x_val (float): Point at which to evaluate the derivative (default = 2.0).

    Returns:
        dict:
            - 'derivative_sym': Symbolic derivative formula f'(x)
            - 'x_val': The evaluation point
            - 'exact_value': Exact evaluated numerical derivative (float)
            - 'latex_derivative': LaTeX formatted string of the derivative
    """
    # SymPy diff applies differentiation rules (e.g., d/dx(-2x^3 + 2x) = -6x^2 + 2)
    deriv_sym = sp.diff(sym_expr, x)

    # Evaluate derivative at the chosen point x = x_val
    exact_val_sym = deriv_sym.subs(x, x_val)
    exact_val = float(exact_val_sym.evalf())

    return {
        "derivative_sym": deriv_sym,
        "x_val": float(x_val),
        "exact_value": exact_val,
        "latex_derivative": sp.latex(deriv_sym)
    }


def compute_numeric_derivative(num_func, x_val: float = DEFAULT_X_VAL, h: float = DEFAULT_H):
    """
    Calculates the numerical derivative using the Central Finite Difference Method:
    
        f'(x) ≈ [ f(x + h) - f(x - h) ] / (2 * h)

    Why Central Difference?
    Central difference cancels out the first-order error terms, yielding
    second-order accuracy O(h^2), making it significantly more accurate than
    forward or backward differences.

    Parameters:
        num_func: Callable Python/NumPy function representing f(x).
        x_val (float): Point at which to estimate the derivative (default = 2.0).
        h (float): Step size / grid spacing (default = 0.0001).

    Returns:
        dict:
            - 'x_val': Evaluation point
            - 'h': Step size used
            - 'approx_value': Numerical approximation of f'(x)
            - 'f_x_plus_h': f(x + h)
            - 'f_x_minus_h': f(x - h)
    """
    if h <= 0:
        raise ValueError("Step size 'h' must be strictly positive (h > 0).")

    try:
        f_plus = float(num_func(x_val + h))
        f_minus = float(num_func(x_val - h))
    except Exception as e:
        raise ValueError(f"Error evaluating function near x = {x_val}: {e}")

    # Central difference formula
    approx_val = (f_plus - f_minus) / (2.0 * h)

    return {
        "x_val": float(x_val),
        "h": float(h),
        "approx_value": float(approx_val),
        "f_x_plus_h": f_plus,
        "f_x_minus_h": f_minus
    }


# -----------------------------------------------------------------------------
# 3. INTEGRATION: SYMBOLIC (EXACT) & NUMERICAL (TRAPEZOIDAL RULE)
# -----------------------------------------------------------------------------

def compute_symbolic_indefinite_integral(sym_expr):
    """
    Calculates the symbolic indefinite integral (antiderivative) using SymPy:
    
        F(x) = ∫ f(x) dx

    Parameters:
        sym_expr: SymPy expression to integrate.

    Returns:
        dict:
            - 'antiderivative_sym': Symbolic antiderivative F(x)
            - 'latex_indefinite': LaTeX formatted string with '+ C'
    """
    # sp.integrate without limits computes the indefinite integral
    antideriv = sp.integrate(sym_expr, x)

    return {
        "antiderivative_sym": antideriv,
        "latex_indefinite": f"{sp.latex(antideriv)} + C"
    }


def compute_symbolic_definite_integral(sym_expr, a: float = DEFAULT_A, b: float = DEFAULT_B):
    """
    Calculates the exact definite integral between limits a and b using SymPy:
    
        ∫[a to b] f(x) dx = F(b) - F(a)

    Parameters:
        sym_expr: SymPy expression to integrate.
        a (float): Lower integration limit (default = 0.0).
        b (float): Upper integration limit (default = 2.0).

    Returns:
        dict:
            - 'a': Lower limit
            - 'b': Upper limit
            - 'definite_sym': Symbolic exact answer
            - 'exact_value': Floating point representation of the exact integral
            - 'latex_definite': LaTeX formatted formula
    """
    # SymPy definite integration with tuple (variable, lower_limit, upper_limit)
    definite_sym = sp.integrate(sym_expr, (x, a, b))

    try:
        exact_val = float(definite_sym.evalf())
    except TypeError:
        # Fallback to numerical approximation if non-elementary integral
        exact_val = float(sp.N(definite_sym))

    return {
        "a": float(a),
        "b": float(b),
        "definite_sym": definite_sym,
        "exact_value": exact_val,
        "latex_definite": sp.latex(definite_sym)
    }


def compute_numeric_trapezoidal_integral(num_func, a: float = DEFAULT_A, b: float = DEFAULT_B, n: int = DEFAULT_N):
    """
    Calculates numerical definite integration using NumPy's Composite Trapezoidal Rule.
    
    Mathematical Formula:
        h = (b - a) / n
        ∫[a to b] f(x) dx ≈ (h / 2) * [ f(x_0) + 2*f(x_1) + 2*f(x_2) + ... + 2*f(x_{n-1}) + f(x_n) ]

    Parameters:
        num_func: Vectorized callable Python/NumPy function for f(x).
        a (float): Lower integration limit (default = 0.0).
        b (float): Upper integration limit (default = 2.0).
        n (int): Number of subintervals (default = 1000).

    Returns:
        dict:
            - 'a': Lower limit
            - 'b': Upper limit
            - 'n': Number of intervals
            - 'h': Step size / width of each trapezoid
            - 'approx_value': Numerical approximation of the integral
            - 'grid_x': NumPy array of sample points x_i
            - 'grid_y': NumPy array of function values f(x_i)
    """
    if not isinstance(n, (int, np.integer)):
        raise TypeError(f"Number of intervals 'n' must be an integer, got {type(n).__name__}.")
    if n < 1:
        raise ValueError("Number of intervals 'n' must be at least 1.")

    # Special trivial case: zero width interval
    if math.isclose(a, b):
        return {
            "a": float(a),
            "b": float(b),
            "n": int(n),
            "h": 0.0,
            "approx_value": 0.0,
            "grid_x": np.array([a]),
            "grid_y": np.array([float(num_func(a))])
        }

    # Step width of each trapezoid
    h_int = (b - a) / float(n)

    # Discretized grid of points from a to b
    grid_x = np.linspace(a, b, n + 1)

    try:
        grid_y = num_func(grid_x)
        # Ensure grid_y is a NumPy array of floats even if num_func returns a scalar
        if np.isscalar(grid_y):
            grid_y = np.full_like(grid_x, fill_value=grid_y, dtype=float)
        else:
            grid_y = np.asarray(grid_y, dtype=float)
    except Exception as e:
        raise ValueError(f"Error evaluating function across interval [{a}, {b}]: {e}")

    # Composite Trapezoidal rule formula:
    # (h / 2) * (first + 2 * sum(interior points) + last)
    approx_val = (h_int / 2.0) * (grid_y[0] + 2.0 * np.sum(grid_y[1:-1]) + grid_y[-1])

    return {
        "a": float(a),
        "b": float(b),
        "n": int(n),
        "h": float(h_int),
        "approx_value": float(approx_val),
        "grid_x": grid_x,
        "grid_y": grid_y
    }


# -----------------------------------------------------------------------------
# 4. ERROR ANALYSIS: ABSOLUTE & RELATIVE ERROR
# -----------------------------------------------------------------------------

def compute_absolute_error(exact_value: float, approx_value: float):
    """
    Calculates the absolute error and relative percentage error between
    the symbolic (exact) result and the numerical (approximate) result.

    Formulas:
        Absolute Error = | Exact - Approximate |
        Relative Error (%) = ( | Exact - Approximate | / | Exact | ) * 100%

    Parameters:
        exact_value (float): Ground truth exact value computed via SymPy.
        approx_value (float): Estimated value computed via NumPy.

    Returns:
        dict:
            - 'exact_value': Ground truth
            - 'approx_value': Approximation
            - 'absolute_error': Absolute difference
            - 'relative_error_percent': Relative error in % (or None if exact is 0)
    """
    abs_err = abs(exact_value - approx_value)

    # Avoid division by zero if exact value is 0
    if abs(exact_value) > 1e-14:
        rel_err = (abs_err / abs(exact_value)) * 100.0
    else:
        rel_err = None

    return {
        "exact_value": float(exact_value),
        "approx_value": float(approx_value),
        "absolute_error": float(abs_err),
        "relative_error_percent": float(rel_err) if rel_err is not None else None
    }


# -----------------------------------------------------------------------------
# 5. MASTER COMPARISON FUNCTION (STRUCTURED FOR APP.PY)
# -----------------------------------------------------------------------------

def run_full_comparison(
    expr_str: str = DEFAULT_FUNCTION_STR,
    x_val: float = DEFAULT_X_VAL,
    h: float = DEFAULT_H,
    a: float = DEFAULT_A,
    b: float = DEFAULT_B,
    n: int = DEFAULT_N
):
    """
    Executes the entire mathematical pipeline and bundles all results
    into a clean, structured dictionary ready for display in Streamlit (app.py).

    Parameters:
        expr_str (str): Function to evaluate (default = 'x**3 - 3*x**3 + 2*x').
        x_val (float): Differentiation point (default = 2.0).
        h (float): Differentiation step size (default = 0.0001).
        a (float): Integration lower limit (default = 0.0).
        b (float): Integration upper limit (default = 2.0).
        n (int): Number of trapezoidal subintervals (default = 1000).

    Returns:
        dict: Complete structured comparison package.
    """
    # 1. Parse and simplify the function
    parse_result = parse_and_simplify(expr_str)
    simplified_sym = parse_result["simplified_sym"]
    num_func = parse_result["num_func"]

    # 2. Symbolic Derivative & Evaluation at x
    sym_deriv = compute_symbolic_derivative(simplified_sym, x_val=x_val)

    # 3. Numerical Derivative via Central Difference
    num_deriv = compute_numeric_derivative(num_func, x_val=x_val, h=h)

    # 4. Derivative Error Analysis
    deriv_error = compute_absolute_error(
        exact_value=sym_deriv["exact_value"],
        approx_value=num_deriv["approx_value"]
    )

    # 5. Symbolic Indefinite Integral
    sym_indef_int = compute_symbolic_indefinite_integral(simplified_sym)

    # 6. Symbolic Definite Integral
    sym_def_int = compute_symbolic_definite_integral(simplified_sym, a=a, b=b)

    # 7. Numerical Definite Integral via Composite Trapezoidal Rule
    num_def_int = compute_numeric_trapezoidal_integral(num_func, a=a, b=b, n=n)

    # 8. Integration Error Analysis
    int_error = compute_absolute_error(
        exact_value=sym_def_int["exact_value"],
        approx_value=num_def_int["approx_value"]
    )

    # Bundle all structured results together
    return {
        "function": parse_result,
        "differentiation": {
            "symbolic": sym_deriv,
            "numeric": num_deriv,
            "error": deriv_error
        },
        "integration": {
            "indefinite_symbolic": sym_indef_int,
            "definite_symbolic": sym_def_int,
            "numeric_trapezoidal": num_def_int,
            "error": int_error
        },
        "config": {
            "expr_str": expr_str,
            "x_val": x_val,
            "h": h,
            "a": a,
            "b": b,
            "n": n
        }
    }


# -----------------------------------------------------------------------------
# QUICK STANDALONE TEST
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing calculations.py backend directly...")
    results = run_full_comparison()

    print("\n--- FUNCTION SIMPLIFICATION ---")
    print(f"Original:   {results['function']['original_str']}")
    print(f"Simplified: {results['function']['expanded_poly']}")

    print("\n--- DIFFERENTIATION (at x = 2) ---")
    print(f"Symbolic f'(x):     {results['differentiation']['symbolic']['derivative_sym']}")
    print(f"Symbolic Value:     {results['differentiation']['symbolic']['exact_value']}")
    print(f"Numerical (CD):     {results['differentiation']['numeric']['approx_value']}")
    print(f"Absolute Error:     {results['differentiation']['error']['absolute_error']:.2e}")

    print("\n--- INTEGRATION (from 0 to 2) ---")
    print(f"Indefinite F(x):    {results['integration']['indefinite_symbolic']['antiderivative_sym']} + C")
    print(f"Symbolic Definite:  {results['integration']['definite_symbolic']['exact_value']}")
    print(f"Numeric Trapezoid:  {results['integration']['numeric_trapezoidal']['approx_value']}")
    print(f"Absolute Error:     {results['integration']['error']['absolute_error']:.2e}")
    print("\nAll calculations executed successfully!")
