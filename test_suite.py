"""
test_suite.py
--------------
Automated test suite for the Symbolic vs Numeric Comparison project.
Executes all verification criteria programmatically and reports results.
"""

import math
import numpy as np
import sympy as sp
import calculations
import graphs

def run_all_tests():
    passed = 0
    failed = 0
    details = []

    def record_test(name, success, info=""):
        nonlocal passed, failed
        if success:
            passed += 1
            status = "[PASS]"
        else:
            failed += 1
            status = "[FAIL]"
        details.append((status, name, info))
        print(f"{status} - {name} {info}")

    print("=" * 70)
    print("STARTING TEST SUITE: Symbolic vs Numeric Comparison")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # TEST 1: Default Function Simplification
    # -------------------------------------------------------------------------
    try:
        p = calculations.parse_and_simplify("x**3 - 3*x**3 + 2*x")
        orig_str = str(p["original_sym"])
        simp_poly = str(p["expanded_poly"])
        expected_poly = "-2*x**3 + 2*x"
        success = (simp_poly == expected_poly)
        record_test("1. Default Function Simplification", success,
                    f"(Original: {p['original_str']} -> Simplified: {simp_poly})")
    except Exception as e:
        record_test("1. Default Function Simplification", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 2: Symbolic Derivative at x = 2 is -22
    # -------------------------------------------------------------------------
    try:
        sym_res = calculations.compute_symbolic_derivative(p["simplified_sym"], x_val=2.0)
        deriv_formula = str(sym_res["derivative_sym"])
        exact_val = sym_res["exact_value"]
        success = math.isclose(exact_val, -22.0, rel_tol=1e-9)
        record_test("2. Symbolic Derivative Evaluation at x=2", success,
                    f"(Formula: f'(x)={deriv_formula}, Evaluated: {exact_val})")
    except Exception as e:
        record_test("2. Symbolic Derivative Evaluation at x=2", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 3: Numerical Derivative (CFD) approximately -22
    # -------------------------------------------------------------------------
    try:
        num_res = calculations.compute_numeric_derivative(p["num_func"], x_val=2.0, h=0.0001)
        approx_val = num_res["approx_value"]
        diff_err = calculations.compute_absolute_error(exact_val, approx_val)
        success = math.isclose(approx_val, -22.0, rel_tol=1e-5)
        record_test("3. Numerical Derivative (Central Difference, h=0.0001)", success,
                    f"(Approx: {approx_val:.8f}, Abs Error: {diff_err['absolute_error']:.2e})")
    except Exception as e:
        record_test("3. Numerical Derivative (Central Difference, h=0.0001)", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 4: Symbolic Indefinite Integral is -x**4/2 + x**2 + C
    # -------------------------------------------------------------------------
    try:
        indef_res = calculations.compute_symbolic_indefinite_integral(p["simplified_sym"])
        antideriv_str = str(indef_res["antiderivative_sym"])
        latex_str = indef_res["latex_indefinite"]
        # In SymPy string: -x**4/2 + x**2
        x_sym = sp.Symbol('x', real=True)
        expected_sym = -x_sym**4 / 2 + x_sym**2
        diff_expr = sp.simplify(indef_res["antiderivative_sym"] - expected_sym)
        success = (diff_expr == 0)
        record_test("4. Symbolic Indefinite Integral", success,
                    f"(Formula: {antideriv_str} + C, LaTeX: {latex_str})")
    except Exception as e:
        record_test("4. Symbolic Indefinite Integral", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 5: Exact Definite Integral from 0 to 2 is -4
    # -------------------------------------------------------------------------
    try:
        def_res = calculations.compute_symbolic_definite_integral(p["simplified_sym"], a=0.0, b=2.0)
        exact_def = def_res["exact_value"]
        success = math.isclose(exact_def, -4.0, rel_tol=1e-9)
        record_test("5. Symbolic Definite Integral [0 to 2]", success,
                    f"(Evaluated: {exact_def})")
    except Exception as e:
        record_test("5. Symbolic Definite Integral [0 to 2]", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 6: Numerical Trapezoidal Result is approx -4.000008
    # -------------------------------------------------------------------------
    try:
        trap_res = calculations.compute_numeric_trapezoidal_integral(p["num_func"], a=0.0, b=2.0, n=1000)
        approx_trap = trap_res["approx_value"]
        int_err = calculations.compute_absolute_error(exact_def, approx_trap)
        success = math.isclose(approx_trap, -4.000008, rel_tol=1e-5)
        record_test("6. Numerical Definite Integral (Trapezoidal, n=1000)", success,
                    f"(Approx: {approx_trap:.8f}, Abs Error: {int_err['absolute_error']:.2e})")
    except Exception as e:
        record_test("6. Numerical Definite Integral (Trapezoidal, n=1000)", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 7: Dynamic Parameter & Function Switching
    # -------------------------------------------------------------------------
    try:
        # Case 7A: sin(x)
        res_sin = calculations.run_full_comparison("sin(x)", x_val=float(np.pi/3), h=0.0001, a=0.0, b=float(np.pi), n=1000)
        exact_d_sin = res_sin["differentiation"]["symbolic"]["exact_value"] # cos(pi/3) = 0.5
        exact_i_sin = res_sin["integration"]["definite_symbolic"]["exact_value"] # 2.0
        s_sin = math.isclose(exact_d_sin, 0.5, rel_tol=1e-5) and math.isclose(exact_i_sin, 2.0, rel_tol=1e-5)

        # Case 7B: exp(x)
        res_exp = calculations.run_full_comparison("exp(x)", x_val=1.0, h=0.0001, a=0.0, b=1.0, n=1000)
        exact_d_exp = res_exp["differentiation"]["symbolic"]["exact_value"] # e = 2.71828...
        exact_i_exp = res_exp["integration"]["definite_symbolic"]["exact_value"] # e - 1 = 1.71828...
        s_exp = math.isclose(exact_d_exp, math.e, rel_tol=1e-5) and math.isclose(exact_i_exp, math.e - 1, rel_tol=1e-5)

        success = s_sin and s_exp
        record_test("7. Dynamic Function & Parameter Switching", success,
                    f"(sin(x): d={exact_d_sin:.4f}, i={exact_i_sin:.4f}; exp(x): d={exact_d_exp:.4f}, i={exact_i_exp:.4f})")
    except Exception as e:
        record_test("7. Dynamic Function & Parameter Switching", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 8: All 4 Graphs Rendering & Returning Valid Matplotlib Figures
    # -------------------------------------------------------------------------
    try:
        f1 = graphs.plot_original_function(p["num_func"], x_val=2.0, a=0.0, b=2.0)
        f2 = graphs.plot_symbolic_derivative(sym_res["derivative_sym"], x_val=2.0, a=0.0, b=2.0)
        f3 = graphs.plot_derivative_comparison(p["num_func"], sym_res["derivative_sym"], x_val=2.0, h=0.0001, a=0.0, b=2.0)
        f4 = graphs.plot_integration_graph(p["num_func"], a=0.0, b=2.0, n=1000, exact_area=exact_def, approx_area=approx_trap)

        import matplotlib.figure
        s1 = isinstance(f1, matplotlib.figure.Figure)
        s2 = isinstance(f2, matplotlib.figure.Figure)
        s3 = isinstance(f3, matplotlib.figure.Figure)
        s4 = isinstance(f4, matplotlib.figure.Figure)
        success = s1 and s2 and s3 and s4
        record_test("8. All Four Graphs Generation & Type Check", success,
                    f"(All 4 return valid matplotlib.figure.Figure: {s1, s2, s3, s4})")
    except Exception as e:
        record_test("8. All Four Graphs Generation & Type Check", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 9: Invalid Expressions & Limits Error Handling
    # -------------------------------------------------------------------------
    try:
        e1_caught, e2_caught, e3_caught, e4_caught = False, False, False, False

        # 9A: Syntax error (e.g. unclosed parenthesis or trailing operator)
        try:
            calculations.parse_and_simplify("x** + ")
        except ValueError:
            e1_caught = True

        # 9B: Forbidden keyword (security)
        try:
            calculations.parse_and_simplify("__import__('os')")
        except ValueError:
            e2_caught = True

        # 9C: Step size h <= 0
        try:
            calculations.compute_numeric_derivative(p["num_func"], 2.0, h=-0.01)
        except ValueError:
            e3_caught = True

        # 9D: Intervals n < 1
        try:
            calculations.compute_numeric_trapezoidal_integral(p["num_func"], 0, 2, n=0)
        except ValueError:
            e4_caught = True

        # 9E: Identical limits a == b (trivial integral = 0)
        res_zero = calculations.compute_numeric_trapezoidal_integral(p["num_func"], 2.0, 2.0, n=100)
        zero_lim_ok = math.isclose(res_zero["approx_value"], 0.0)

        # 9F: Reversed limits a > b
        res_rev = calculations.run_full_comparison("x**3 - 3*x**3 + 2*x", 2.0, 0.0001, a=2.0, b=0.0, n=1000)
        rev_lim_ok = math.isclose(res_rev["integration"]["definite_symbolic"]["exact_value"], 4.0)

        success = e1_caught and e2_caught and e3_caught and e4_caught and zero_lim_ok and rev_lim_ok
        record_test("9. Invalid Inputs & Boundary Edge Cases", success,
                    f"(Syntax error caught: {e1_caught}, Security caught: {e2_caught}, h<=0 caught: {e3_caught}, n<1 caught: {e4_caught}, a==b: {zero_lim_ok}, a>b: {rev_lim_ok})")
    except Exception as e:
        record_test("9. Invalid Inputs & Boundary Edge Cases", False, f"Exception: {e}")

    # -------------------------------------------------------------------------
    # TEST 10: Import Consistency & Backward Compatibility Functions
    # -------------------------------------------------------------------------
    try:
        # Check all required exports in graphs.py
        expected_graph_attrs = [
            "plot_original_function",
            "plot_symbolic_derivative",
            "plot_derivative_comparison",
            "plot_integration_graph",
            "plot_differentiation_visual",
            "plot_integration_visual",
            "plot_comparison_placeholder"
        ]
        missing_attrs = [attr for attr in expected_graph_attrs if not hasattr(graphs, attr)]

        # Check calculations.py exports
        expected_calc_attrs = [
            "parse_and_simplify",
            "compute_symbolic_derivative",
            "compute_numeric_derivative",
            "compute_symbolic_indefinite_integral",
            "compute_symbolic_definite_integral",
            "compute_numeric_trapezoidal_integral",
            "compute_absolute_error",
            "run_full_comparison"
        ]
        missing_calc = [attr for attr in expected_calc_attrs if not hasattr(calculations, attr)]

        success = (len(missing_attrs) == 0 and len(missing_calc) == 0)
        record_test("10. Missing Imports & Function Mismatch Check", success,
                    f"(Missing graphs: {missing_attrs}, Missing calc: {missing_calc})")
    except Exception as e:
        record_test("10. Missing Imports & Function Mismatch Check", False, f"Exception: {e}")

    print("=" * 70)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 70)

    return passed, failed, details

if __name__ == "__main__":
    run_all_tests()
