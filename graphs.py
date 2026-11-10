"""
graphs.py
---------
Matplotlib visualization module for the Symbolic vs Numeric Comparison project.

Provides publication-quality, dark-themed plots with navy, purple, and blue accents:
1. Original Function Graph: f(x) over a suitable range with key evaluation points.
2. Symbolic Derivative Graph: Exact f'(x) derived via SymPy.
3. Derivative Comparison Graph: Symbolic derivative curve vs. Numerical Finite Difference values.
4. Integration Graph: Function curve, shaded exact area [a, b], and visible trapezoidal approximations.

Handles invalid functions, math domain warnings, and plotting errors gracefully.
"""

import os
import tempfile

# Prevent matplotlib permission errors on temporary directories
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# -----------------------------------------------------------------------------
# THEME CONFIGURATION (Navy, Purple & Blue Accents - Premium Dark Theme)
# -----------------------------------------------------------------------------
THEME_BG = "#0B1120"         # Deep Navy background
CARD_BG = "#17243A"          # Dark Blue card background
TEXT_COLOR = "#F8FAFC"       # White text
MUTED_TEXT = "#CBD5E1"       # Light grey text
GRID_COLOR = "#223554"       # Subtle navy grid
SPINE_COLOR = "#2D4263"      # Card border lines

ACCENT_BLUE = "#3B82F6"      # Bright Blue (Primary)
ACCENT_PURPLE = "#A78BFA"    # Purple (Secondary)
ACCENT_GREEN = "#2DD4BF"     # Cyan / Teal (Success values)
ACCENT_CORAL = "#F87171"     # Soft Coral / Red for limits
ACCENT_AMBER = "#FBBF24"     # Warm Amber for upper limits
ACCENT_INDIGO = "#818CF8"    # Soft Indigo for chords


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------

def compute_smart_range(x_val: float, a: float, b: float, margin_factor: float = 0.5):
    """
    Computes a smart x-axis domain that encompasses the evaluation point x,
    as well as the integration interval [a, b], with proportional margins.
    """
    points = [float(x_val), float(a), float(b)]
    p_min = min(points)
    p_max = max(points)
    span = p_max - p_min
    if span < 1e-5:
        span = 2.0
    margin = max(1.0, span * margin_factor)
    return p_min - margin, p_max + margin


def safe_evaluate_function(func, x_arr):
    """
    Evaluates a callable on a NumPy array safely, handling scalar outputs,
    division by zero, and non-finite numbers (NaN/Inf).
    """
    try:
        y_arr = func(x_arr)
        if np.isscalar(y_arr):
            y_arr = np.full_like(x_arr, fill_value=float(y_arr), dtype=float)
        else:
            y_arr = np.asarray(y_arr, dtype=float)

        # Replace infs and nans for clean plotting
        y_arr = np.nan_to_num(y_arr, nan=np.nan, posinf=np.nan, neginf=np.nan)
        return y_arr, None
    except Exception as e:
        return None, str(e)


def create_error_figure(title: str, error_msg: str):
    """
    Generates a fallback figure displaying an informative error message
    if mathematical plotting fails.
    """
    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    ax.set_facecolor(CARD_BG)
    ax.text(
        0.5, 0.5,
        f"Unable to plot:\n{error_msg}",
        color=ACCENT_CORAL,
        ha="center", va="center",
        fontsize=11, fontweight="bold"
    )
    ax.set_title(title, color=TEXT_COLOR, fontsize=12, fontweight="bold", pad=10)
    ax.tick_params(colors=MUTED_TEXT, which="both")
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    fig.tight_layout()
    return fig


def apply_dark_theme(ax, title: str, xlabel: str, ylabel: str):
    """Applies the consistent dark navy styling to a Matplotlib axes."""
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT_COLOR, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, color=MUTED_TEXT, fontsize=9.5)
    ax.set_ylabel(ylabel, color=MUTED_TEXT, fontsize=9.5)
    ax.tick_params(colors=MUTED_TEXT, which="both", labelsize=8.5)
    ax.grid(True, linestyle="--", alpha=0.35, color=GRID_COLOR)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)


# -----------------------------------------------------------------------------
# GRAPH 1: ORIGINAL FUNCTION GRAPH
# -----------------------------------------------------------------------------

def plot_original_function(num_func, x_val: float = 2.0, a: float = 0.0, b: float = 2.0, x_range=None):
    """
    1. Original Function Graph:
       Plots the input function f(x) over a suitable range.
       Highlights the evaluation point (x, f(x)) and integration bounds [a, b].
    """
    if x_range is None:
        x_min, x_max = compute_smart_range(x_val, a, b, margin_factor=0.6)
    else:
        x_min, x_max = x_range

    x_dense = np.linspace(x_min, x_max, 400)
    y_dense, err = safe_evaluate_function(num_func, x_dense)

    if err or y_dense is None:
        return create_error_figure("1. Original Function f(x)", err or "Function evaluation failed.")

    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    apply_dark_theme(ax, "1. Original Function Graph: f(x)", "x", "f(x)")

    # Plot continuous function curve
    ax.plot(x_dense, y_dense, color=ACCENT_BLUE, linewidth=2.5, label="f(x) Function Curve")

    # Baseline y = 0
    ax.axhline(0, color="#475569", linestyle="-", linewidth=0.8, alpha=0.7)

    # Highlight evaluation point (x_val, f(x_val))
    try:
        y_pt = float(num_func(x_val))
        ax.scatter(
            [x_val], [y_pt],
            color=ACCENT_GREEN, s=80, zorder=6,
            label=f"Eval Point ({x_val:.2f}, {y_pt:.2f})"
        )
        ax.axvline(x_val, color=ACCENT_GREEN, linestyle=":", alpha=0.5, linewidth=1.0)
    except Exception:
        pass

    # Mark integration bounds [a, b]
    ax.axvline(a, color=ACCENT_CORAL, linestyle="--", linewidth=1.2, alpha=0.8, label=f"Lower Limit a={a:.2f}")
    ax.axvline(b, color=ACCENT_AMBER, linestyle="--", linewidth=1.2, alpha=0.8, label=f"Upper Limit b={b:.2f}")

    legend = ax.legend(facecolor=CARD_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_COLOR, fontsize=8.5, loc="best")
    legend.get_frame().set_alpha(0.85)

    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# GRAPH 2: SYMBOLIC DERIVATIVE GRAPH
# -----------------------------------------------------------------------------

def plot_symbolic_derivative(sym_deriv, x_val: float = 2.0, a: float = 0.0, b: float = 2.0, x_range=None):
    """
    2. Symbolic Derivative Graph:
       Plots the exact derivative f'(x) calculated using SymPy.
       Marks the exact derivative value at the evaluation point x.
    """
    try:
        x_sym = sp.Symbol('x', real=True)
        deriv_func = sp.lambdify(x_sym, sym_deriv, modules=['numpy'])
    except Exception as e:
        return create_error_figure("2. Symbolic Derivative f'(x)", f"SymPy conversion error: {e}")

    if x_range is None:
        x_min, x_max = compute_smart_range(x_val, a, b, margin_factor=0.6)
    else:
        x_min, x_max = x_range

    x_dense = np.linspace(x_min, x_max, 400)
    y_deriv, err = safe_evaluate_function(deriv_func, x_dense)

    if err or y_deriv is None:
        return create_error_figure("2. Symbolic Derivative f'(x)", err or "Derivative evaluation failed.")

    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    apply_dark_theme(ax, "2. Symbolic Derivative Graph: f'(x)", "x", "f'(x)")

    # Plot symbolic derivative curve
    ax.plot(x_dense, y_deriv, color=ACCENT_PURPLE, linewidth=2.5, label="Symbolic f'(x) [SymPy]")

    # Baseline y = 0
    ax.axhline(0, color="#475569", linestyle="-", linewidth=0.8, alpha=0.7)

    # Highlight evaluated point (x_val, f'(x_val))
    try:
        exact_val = float(sym_deriv.subs(x_sym, x_val).evalf())
        ax.scatter(
            [x_val], [exact_val],
            color=ACCENT_GREEN, s=85, zorder=6,
            label=f"Exact f'({x_val:.2f}) = {exact_val:.3f}"
        )
        ax.axvline(x_val, color=ACCENT_GREEN, linestyle=":", alpha=0.5, linewidth=1.0)
    except Exception:
        pass

    legend = ax.legend(facecolor=CARD_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_COLOR, fontsize=8.5, loc="best")
    legend.get_frame().set_alpha(0.85)

    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# GRAPH 3: DERIVATIVE COMPARISON GRAPH (SYMBOLIC VS NUMERICAL CFD)
# -----------------------------------------------------------------------------

def plot_derivative_comparison(num_func, sym_deriv, x_val: float = 2.0, h: float = 0.0001, a: float = 0.0, b: float = 2.0, x_range=None):
    """
    3. Derivative Comparison Graph:
       Compares the continuous symbolic derivative curve with numerical
       finite-difference derivative values sampled across the domain.
    """
    try:
        x_sym = sp.Symbol('x', real=True)
        deriv_func = sp.lambdify(x_sym, sym_deriv, modules=['numpy'])
    except Exception as e:
        return create_error_figure("3. Derivative Comparison", f"SymPy conversion error: {e}")

    if x_range is None:
        x_min, x_max = compute_smart_range(x_val, a, b, margin_factor=0.6)
    else:
        x_min, x_max = x_range

    # Continuous curve for symbolic derivative
    x_dense = np.linspace(x_min, x_max, 400)
    y_sym_deriv, err = safe_evaluate_function(deriv_func, x_dense)

    if err or y_sym_deriv is None:
        return create_error_figure("3. Derivative Comparison", err or "Evaluation failed.")

    # Discrete sample points for numerical CFD: [f(x+h) - f(x-h)] / (2h)
    sample_points = np.linspace(x_min, x_max, 22)
    try:
        f_plus = num_func(sample_points + h)
        f_minus = num_func(sample_points - h)
        y_cfd = (f_plus - f_minus) / (2.0 * h)
    except Exception as e:
        return create_error_figure("3. Derivative Comparison", f"CFD calculation error: {e}")

    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    apply_dark_theme(ax, "3. Derivative Comparison: Symbolic vs Central Difference", "x", "f'(x)")

    # 1. Exact Symbolic continuous curve
    ax.plot(x_dense, y_sym_deriv, color=ACCENT_PURPLE, linewidth=2.5, label="Symbolic Derivative (Exact)")

    # 2. Numerical CFD sample points
    ax.scatter(
        sample_points, y_cfd,
        color=ACCENT_BLUE, s=45, marker="o", facecolors="none", edgecolors=ACCENT_BLUE, linewidth=1.5,
        label=f"Numerical CFD Samples (h = {h})"
    )

    # 3. User evaluation point x_val
    try:
        exact_at_x = float(sym_deriv.subs(x_sym, x_val).evalf())
        approx_at_x = float((num_func(x_val + h) - num_func(x_val - h)) / (2.0 * h))
        ax.scatter(
            [x_val], [approx_at_x],
            color=ACCENT_GREEN, s=95, marker="*", zorder=7,
            label=f"Target x={x_val:.2f} (Err: {abs(exact_at_x - approx_at_x):.1e})"
        )
    except Exception:
        pass

    # Baseline y = 0
    ax.axhline(0, color="#475569", linestyle="-", linewidth=0.8, alpha=0.7)

    legend = ax.legend(facecolor=CARD_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_COLOR, fontsize=8.5, loc="best")
    legend.get_frame().set_alpha(0.85)

    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# GRAPH 4: INTEGRATION GRAPH (SHADED AREA & TRAPEZOIDAL APPROXIMATION)
# -----------------------------------------------------------------------------

def plot_integration_graph(num_func, a: float = 0.0, b: float = 2.0, n: int = 1000, exact_area: float = -4.0, approx_area: float = -4.000008, x_range=None):
    """
    4. Integration Graph:
       Shows the function curve, shaded exact area between lower limit 'a'
       and upper limit 'b', and visible trapezoidal geometric approximations.
    """
    if x_range is None:
        x_min, x_max = compute_smart_range((a + b) / 2.0, a, b, margin_factor=0.5)
    else:
        x_min, x_max = x_range

    x_dense = np.linspace(x_min, x_max, 400)
    y_dense, err = safe_evaluate_function(num_func, x_dense)

    if err or y_dense is None:
        return create_error_figure("4. Integration Graph", err or "Function evaluation failed.")

    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    apply_dark_theme(ax, "4. Integration: Exact Area vs Trapezoidal Approximation", "x", "f(x)")

    # 1. Plot continuous curve f(x)
    ax.plot(x_dense, y_dense, color=ACCENT_BLUE, linewidth=2.2, label="f(x) Function Curve")

    # 2. Shaded exact integral area between a and b
    left_bound, right_bound = min(a, b), max(a, b)
    x_fill = np.linspace(left_bound, right_bound, 250)
    y_fill, _ = safe_evaluate_function(num_func, x_fill)
    if y_fill is not None:
        ax.fill_between(
            x_fill, y_fill, 0,
            color=ACCENT_PURPLE, alpha=0.25,
            label=f"Exact Area ∫[{a:.1f},{b:.1f}] = {exact_area:.4f}"
        )

    # 3. Trapezoidal approximation visualization
    # We display up to 20 visible trapezoids so the geometric chords and pillars are distinct
    vis_n = max(2, min(int(n), 20))
    trap_x = np.linspace(a, b, vis_n + 1)
    trap_y, _ = safe_evaluate_function(num_func, trap_x)

    if trap_y is not None:
        for i in range(vis_n):
            # Draw vertical pillar sides of each trapezoid
            ax.plot([trap_x[i], trap_x[i]], [0, trap_y[i]], color=ACCENT_INDIGO, linestyle=":", linewidth=1.2, alpha=0.6)
            # Fill trapezoid with slight color
            ax.fill_between(
                [trap_x[i], trap_x[i + 1]],
                [trap_y[i], trap_y[i + 1]],
                0,
                color=ACCENT_GREEN, alpha=0.12
            )
        # Draw final pillar
        ax.plot([trap_x[-1], trap_x[-1]], [0, trap_y[-1]], color=ACCENT_INDIGO, linestyle=":", linewidth=1.2, alpha=0.6)

        # Plot piecewise linear trapezoid top edges
        ax.plot(
            trap_x, trap_y,
            color=ACCENT_GREEN, linestyle="-", marker=".", markersize=7, linewidth=1.6,
            label=f"Trapezoids ({vis_n} shown, n={n} used, approx={approx_area:.4f})"
        )

    # Baseline y = 0
    ax.axhline(0, color="#475569", linestyle="-", linewidth=0.8, alpha=0.7)

    # Mark limits a and b
    ax.axvline(a, color=ACCENT_CORAL, linestyle="--", linewidth=1.3, label=f"Lower Limit a={a:.2f}")
    ax.axvline(b, color=ACCENT_AMBER, linestyle="--", linewidth=1.3, label=f"Upper Limit b={b:.2f}")

    legend = ax.legend(facecolor=CARD_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_COLOR, fontsize=8.2, loc="best")
    legend.get_frame().set_alpha(0.85)

    fig.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# BACKWARDS COMPATIBILITY WRAPPERS (if existing code calls older names)
# -----------------------------------------------------------------------------
def plot_differentiation_visual(num_func, x_val, exact_deriv, approx_deriv, h):
    """Wrapper mapping to plot_derivative_comparison."""
    sym_x = sp.Symbol('x', real=True)
    # Estimate a simple linear or constant representation for fallback if needed
    return plot_derivative_comparison(
        num_func=num_func,
        sym_deriv=sp.sympify(exact_deriv),
        x_val=x_val,
        h=h
    )

def plot_integration_visual(num_func, a, b, n, exact_area, approx_area):
    """Wrapper mapping to plot_integration_graph."""
    return plot_integration_graph(
        num_func=num_func,
        a=a,
        b=b,
        n=n,
        exact_area=exact_area,
        approx_area=approx_area
    )


def plot_comparison_placeholder():
    """Placeholder function to maintain 100% backward compatibility."""
    fig, ax = plt.subplots(figsize=(7, 4.2), facecolor=THEME_BG)
    apply_dark_theme(ax, "Comparison Plot (Placeholder)", "x", "y")
    x_sample = np.linspace(0, 10, 100)
    y_sample = np.sin(x_sample)
    ax.plot(x_sample, y_sample, label="sin(x)", color=ACCENT_BLUE)
    ax.legend(facecolor=CARD_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_COLOR)
    fig.tight_layout()
    return fig

