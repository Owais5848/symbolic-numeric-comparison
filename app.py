"""
app.py
------
Frontend Web Application for the Symbolic vs Numeric Comparison Project.

Built with Streamlit.
Features a modern, responsive, dark-themed UI with navy, purple, and blue accents.
Connects dynamically with the calculations.py backend and graphs.py visualization.
"""

import streamlit as st
import pandas as pd
import importlib
import calculations
import graphs

# Reload modules so a running Streamlit development server always picks up local changes
importlib.reload(calculations)
importlib.reload(graphs)

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Symbolic vs Numeric Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING (DARK THEME: NAVY, PURPLE & BLUE ACCENTS)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Background and Typography */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Navigation / Header styling */
    .main-header {
        background: linear-gradient(135deg, #111827 0%, #1E1B4B 50%, #0F172A 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(139, 92, 246, 0.15);
    }
    .main-title {
        color: #FFFFFF;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-subtitle {
        color: #94A3B8;
        font-size: 1.0rem;
        margin-bottom: 12px;
    }
    .badge-tag {
        display: inline-block;
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: #FFFFFF;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 8px;
    }
    .badge-secondary {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        letter-spacing: 0.03em;
    }

    /* Section & Content Cards */
    .content-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 10px;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #131D31 0%, #0F172A 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 12px;
        padding: 16px 18px;
        text-align: left;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-card:hover {
        border-color: rgba(168, 85, 247, 0.6);
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value-symbolic {
        font-size: 1.55rem;
        font-weight: 800;
        color: #38BDF8;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    .metric-value-numeric {
        font-size: 1.55rem;
        font-weight: 800;
        color: #A855F7;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    .metric-value-error {
        font-size: 1.55rem;
        font-weight: 800;
        color: #10B981;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    .metric-subtext {
        font-size: 0.76rem;
        color: #64748B;
        margin-top: 6px;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }

    /* Streamlit Button Styling */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #4338CA 0%, #6D28D9 100%) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Comparison Table Styling */
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #1E293B;
        margin-top: 10px;
    }
    .custom-table th {
        background-color: #1E1B4B;
        color: #E2E8F0;
        padding: 12px 14px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #312E81;
    }
    .custom-table td {
        background-color: #111827;
        color: #CBD5E1;
        padding: 12px 14px;
        font-size: 0.9rem;
        border-bottom: 1px solid #1F2937;
    }
    .custom-table tr:hover td {
        background-color: #161F33;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. SIDEBAR: INPUT CONTROLS & PARAMETERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    st.markdown("<p style='color:#94A3B8; font-size:0.85rem;'>Configure mathematical parameters for symbolic & numerical engines.</p>", unsafe_allow_html=True)
    st.divider()

    # Function Input Field with confirmed default
    st.markdown("#### 1. Function Definition")
    func_input = st.text_input(
        "Mathematical Function f(x)",
        value="x**3 - 3*x**3 + 2*x",
        help="Enter an expression in terms of x. Example: x**3 - 3*x**3 + 2*x, sin(x), exp(x)"
    )

    st.markdown("#### 2. Differentiation Controls")
    x_input = st.number_input(
        "Evaluation Point (x)",
        value=2.0,
        step=0.5,
        format="%.4f",
        help="Point x where the exact and numerical derivatives are calculated."
    )

    h_input = st.number_input(
        "Step Size (h)",
        value=0.0001,
        step=0.00005,
        format="%.6f",
        min_value=1e-8,
        help="Step size for Central Finite Difference: [f(x+h) - f(x-h)] / (2h)"
    )

    st.markdown("#### 3. Integration Controls")
    col_a, col_b = st.columns(2)
    with col_a:
        a_input = st.number_input(
            "Lower Limit (a)",
            value=0.0,
            step=0.5,
            format="%.2f",
            help="Starting point of definite integration interval."
        )
    with col_b:
        b_input = st.number_input(
            "Upper Limit (b)",
            value=2.0,
            step=0.5,
            format="%.2f",
            help="End point of definite integration interval."
        )

    n_input = st.number_input(
        "Subintervals (n)",
        value=1000,
        min_value=1,
        max_value=100000,
        step=100,
        help="Number of trapezoids used in Composite Trapezoidal Rule."
    )

    st.markdown("#### 4. Graph Display Controls")
    auto_scale = st.checkbox("Auto-scale X-Axis Range", value=True, help="Automatically centers graph domain around evaluation point x and limits [a, b].")
    custom_range = None
    if not auto_scale:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            g_min = st.number_input("X Min", value=-3.0, step=0.5)
        with col_g2:
            g_max = st.number_input("X Max", value=3.0, step=0.5)
        if g_min < g_max:
            custom_range = (float(g_min), float(g_max))
        else:
            st.warning("X Min must be less than X Max.")

    st.divider()

    # Calculate Button
    calculate_clicked = st.button("⚡ Calculate Comparison", use_container_width=True)

    # University Project Info
    st.markdown(
        """
        <div style='margin-top: 24px; padding: 12px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; border: 1px solid #1E293B;'>
            <p style='font-size:0.75rem; color:#94A3B8; margin:0;'>
                <strong>Course:</strong> Numerical & Symbolic Computing<br>
                <strong>Backend:</strong> SymPy (Exact) & NumPy (CFD / Trapezoidal)<br>
                <strong>Frontend:</strong> Streamlit Dark UI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 4. HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">
            <span>⚡ Symbolic vs Numeric Comparison</span>
        </div>
        <div class="main-subtitle">
            An interactive dashboard comparing exact Computer Algebra Systems (SymPy) with numerical discrete methods (NumPy).
        </div>
        <div>
            <span class="badge-tag">BSCS University Project</span>
            <span class="badge-secondary">SymPy 1.12+</span>
            <span class="badge-secondary">NumPy 1.24+</span>
            <span class="badge-secondary">Central Difference O(h²)</span>
            <span class="badge-secondary">Trapezoidal O(h²)</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 5. EXECUTION & BACKEND DATA RETRIEVAL
# -----------------------------------------------------------------------------
# Run backend calculation safely using calculations.run_full_comparison
error_message = None
results = None

try:
    results = calculations.run_full_comparison(
        expr_str=func_input,
        x_val=float(x_input),
        h=float(h_input),
        a=float(a_input),
        b=float(b_input),
        n=int(n_input)
    )
except Exception as e:
    error_message = str(e)

# Handle invalid input and errors gracefully
if error_message:
    st.error(f"⚠️ **Mathematical / Input Error:** {error_message}")
    st.info("💡 **Tip:** Verify that the function string is valid (e.g., `x**3 - 3*x**3 + 2*x`) and that `h > 0` and `n >= 1`.")
    st.stop()

# Unpack results safely from the structured dictionary returned by calculations.py
func_data = results["function"]
diff_data = results["differentiation"]
int_data = results["integration"]

# -----------------------------------------------------------------------------
# 6. SECTION 1: FUNCTION ALGEBRAIC BREAKDOWN (SYMPY)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="content-card">
        <div class="card-title">
            <span>🔍 1. Algebraic Function Simplification (SymPy CAS)</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col_orig, col_arrow, col_simp = st.columns([5, 1, 5])

with col_orig:
    st.markdown("**Original Input Function:**")
    st.latex(f"f(x) = {func_data['latex_original']}")
    st.caption(f"Raw Input: `{func_data['original_str']}`")

with col_arrow:
    st.markdown("<div style='text-align:center; padding-top:20px; font-size:1.6rem; color:#A855F7;'>➔</div>", unsafe_allow_html=True)

with col_simp:
    st.markdown("**Simplified Polynomial Form:**")
    st.latex(f"f(x) = {func_data['latex_simplified']}")
    st.caption("SymPy automatically identified & combined like terms ($x^3 - 3x^3 = -2x^3$).")

st.divider()

# -----------------------------------------------------------------------------
# 7. SECTION 2: DIFFERENTIATION COMPARISON
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="content-card">
        <div class="card-title">
            <span>⚡ 2. Differentiation Comparison: Exact Derivative vs Central Finite Difference</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Display mathematical definitions
st.markdown(
    f"""
    - **Symbolic Differentiation:** $\\frac{{d}}{{dx}} f(x) = {diff_data['symbolic']['latex_derivative']}$
    - **Numerical Differentiation:** Central Finite Difference: $f'(x) \\approx \\frac{{f(x+h) - f(x-h)}}{{2h}}$ with $x = {diff_data['numeric']['x_val']}$ and $h = {diff_data['numeric']['h']}$
    """
)

# Metric cards for Differentiation
col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🔮 Exact Symbolic Derivative</div>
            <div class="metric-value-symbolic">{diff_data['symbolic']['exact_value']:.8f}</div>
            <div class="metric-subtext">f'({diff_data['symbolic']['x_val']}) via SymPy calculus rules</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_d2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">⚙️ Numerical Derivative (CFD)</div>
            <div class="metric-value-numeric">{diff_data['numeric']['approx_value']:.8f}</div>
            <div class="metric-subtext">Step size h = {diff_data['numeric']['h']} (Accuracy O(h²))</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_d3:
    abs_err_d = diff_data['error']['absolute_error']
    rel_err_d = diff_data['error']['relative_error_percent']
    rel_str = f"{rel_err_d:.2e}%" if rel_err_d is not None else "N/A"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🎯 Absolute Error (|Exact - Numeric|)</div>
            <div class="metric-value-error">{abs_err_d:.2e}</div>
            <div class="metric-subtext">Relative Error: {rel_str}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------------------------------------------------------
# 8. SECTION 3: INTEGRATION COMPARISON
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="content-card">
        <div class="card-title">
            <span>📐 3. Integration Comparison: Exact Definite Integral vs Composite Trapezoidal Rule</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Indefinite integral display
st.markdown(
    f"""
    - **Symbolic Indefinite Integral (Antiderivative):** 
      $$\\int f(x) dx = {int_data['indefinite_symbolic']['latex_indefinite']}$$
    - **Definite Integral Bounds:** Interval $[a, b] = [{int_data['definite_symbolic']['a']}, {int_data['definite_symbolic']['b']}]$ with $n = {int_data['numeric_trapezoidal']['n']}$ trapezoids ($\\Delta x = {int_data['numeric_trapezoidal']['h']:.5f}$).
    """
)

# Metric cards for Integration
col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🔮 Exact Definite Integral</div>
            <div class="metric-value-symbolic">{int_data['definite_symbolic']['exact_value']:.8f}</div>
            <div class="metric-subtext">∫[{int_data['definite_symbolic']['a']} to {int_data['definite_symbolic']['b']}] f(x) dx via SymPy</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_i2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">⚙️ Numerical Trapezoidal Rule</div>
            <div class="metric-value-numeric">{int_data['numeric_trapezoidal']['approx_value']:.8f}</div>
            <div class="metric-subtext">Composite rule with {int_data['numeric_trapezoidal']['n']} intervals</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_i3:
    abs_err_i = int_data['error']['absolute_error']
    rel_err_i = int_data['error']['relative_error_percent']
    rel_str_i = f"{rel_err_i:.4f}%" if rel_err_i is not None else "N/A"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">🎯 Absolute Error (|Exact - Numeric|)</div>
            <div class="metric-value-error">{abs_err_i:.2e}</div>
            <div class="metric-subtext">Relative Error: {rel_str_i}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------------------------------------------------------------
# 9. SECTION 4: COMPREHENSIVE COMPARISON SUMMARY TABLE
# -----------------------------------------------------------------------------
st.markdown("### 📊 Comprehensive Comparison Summary Table")

# Format comparison table data cleanly
table_data = [
    {
        "Mathematical Operation": "Differentiation (Derivative)",
        "Evaluation Target": f"x = {diff_data['symbolic']['x_val']}",
        "Symbolic Method (SymPy)": "Analytical Calculus Rules",
        "Symbolic Result": f"{diff_data['symbolic']['exact_value']:.8f}",
        "Numerical Method (NumPy)": f"Central Finite Difference (h = {diff_data['numeric']['h']})",
        "Numerical Result": f"{diff_data['numeric']['approx_value']:.8f}",
        "Absolute Error": f"{diff_data['error']['absolute_error']:.2e}",
        "Order of Error": "O(h²)"
    },
    {
        "Mathematical Operation": "Definite Integration (Area)",
        "Evaluation Target": f"[{int_data['definite_symbolic']['a']}, {int_data['definite_symbolic']['b']}]",
        "Symbolic Method (SymPy)": "Fundamental Theorem of Calculus",
        "Symbolic Result": f"{int_data['definite_symbolic']['exact_value']:.8f}",
        "Numerical Method (NumPy)": f"Composite Trapezoidal (n = {int_data['numeric_trapezoidal']['n']})",
        "Numerical Result": f"{int_data['numeric_trapezoidal']['approx_value']:.8f}",
        "Absolute Error": f"{int_data['error']['absolute_error']:.2e}",
        "Order of Error": "O(h²)"
    }
]

df_comparison = pd.DataFrame(table_data)
st.dataframe(df_comparison, use_container_width=True, hide_index=True)

st.divider()

# -----------------------------------------------------------------------------
# 10. SECTION 5: INTERACTIVE VISUAL PLOTS (MATPLOTLIB & GRAPHS.PY)
# -----------------------------------------------------------------------------
st.markdown("### 📈 Visual Graphs & Geometric Interpretation")
st.markdown("<p style='color:#94A3B8;'>Visualizing the continuous analytical curves alongside discrete numerical approximations.</p>", unsafe_allow_html=True)

# Generate all 4 required figures dynamically
fig_orig = graphs.plot_original_function(
    num_func=func_data["num_func"],
    x_val=diff_data["symbolic"]["x_val"],
    a=int_data["definite_symbolic"]["a"],
    b=int_data["definite_symbolic"]["b"],
    x_range=custom_range
)

fig_sym_deriv = graphs.plot_symbolic_derivative(
    sym_deriv=diff_data["symbolic"]["derivative_sym"],
    x_val=diff_data["symbolic"]["x_val"],
    a=int_data["definite_symbolic"]["a"],
    b=int_data["definite_symbolic"]["b"],
    x_range=custom_range
)

fig_diff_comp = graphs.plot_derivative_comparison(
    num_func=func_data["num_func"],
    sym_deriv=diff_data["symbolic"]["derivative_sym"],
    x_val=diff_data["symbolic"]["x_val"],
    h=diff_data["numeric"]["h"],
    a=int_data["definite_symbolic"]["a"],
    b=int_data["definite_symbolic"]["b"],
    x_range=custom_range
)

fig_integration = graphs.plot_integration_graph(
    num_func=func_data["num_func"],
    a=int_data["definite_symbolic"]["a"],
    b=int_data["definite_symbolic"]["b"],
    n=int_data["numeric_trapezoidal"]["n"],
    exact_area=int_data["definite_symbolic"]["exact_value"],
    approx_area=int_data["numeric_trapezoidal"]["approx_value"],
    x_range=custom_range
)

# Render graphs cleanly using responsive Streamlit Tabs
tab_all, tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Complete 2x2 Dashboard View",
    "1️⃣ Original Function",
    "2️⃣ Symbolic Derivative",
    "3️⃣ Derivative Comparison",
    "4️⃣ Trapezoidal Integration"
])

with tab_all:
    # Row 1: Original Function & Symbolic Derivative
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.pyplot(fig_orig)
    with row1_col2:
        st.pyplot(fig_sym_deriv)

    # Row 2: Derivative Comparison & Integration Trapezoids
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.pyplot(fig_diff_comp)
    with row2_col2:
        st.pyplot(fig_integration)

with tab1:
    st.markdown("**1. Original Function Graph: $f(x)$**")
    st.caption("Shows the full mathematical curve across the domain, highlighting the evaluation point $x$ and integration limits $[a, b]$.")
    st.pyplot(fig_orig)

with tab2:
    st.markdown("**2. Symbolic Derivative Graph: $f'(x)$**")
    st.caption("Plots the exact rate-of-change formula derived algebraically by SymPy, with the slope at $x=2$ marked.")
    st.pyplot(fig_sym_deriv)

with tab3:
    st.markdown("**3. Derivative Comparison: Analytical vs Central Finite Difference**")
    st.caption("Visualizes how closely the discrete Central Finite Difference estimates align with the continuous exact derivative curve.")
    st.pyplot(fig_diff_comp)

with tab4:
    st.markdown("**4. Definite Integration & Trapezoidal Chords**")
    st.caption("Shows the exact shaded definite area $\\int_a^b f(x) dx$ compared with the composite trapezoid geometric approximation.")
    st.pyplot(fig_integration)

st.divider()

# -----------------------------------------------------------------------------
# 11. SECTION 6: THEORETICAL VIVA / EXAM CHEAT SHEET
# -----------------------------------------------------------------------------
with st.expander("🎓 Numerical vs. Symbolic Computing: Academic Explanations & Viva Questions", expanded=False):
    st.markdown(
        """
        ### 1. Why do we need both Symbolic and Numerical computing?
        - **Symbolic Computing (SymPy):**
          - Operates on mathematical symbols ($x, y, \\pi, \\sqrt{2}$).
          - Provides **infinite precision** and exact closed-form algebraic formulas.
          - *Limitation:* Many real-world differential equations and complex integrals do not have an elementary closed-form solution. It can also be slow for large datasets.
        - **Numerical Computing (NumPy):**
          - Operates on discrete arrays of floating-point numbers.
          - Can approximate solutions to *any* well-behaved function very quickly.
          - *Limitation:* Incurs **truncation error** (from finite approximations) and **round-off error** (from IEEE-754 64-bit floating point precision limits).

        ### 2. Why is the Central Finite Difference $O(h^2)$?
        Using Taylor expansions:
        $$f(x+h) = f(x) + f'(x)h + \\frac{f''(x)}{2!}h^2 + \\frac{f'''(x)}{3!}h^3 + \\dots$$
        $$f(x-h) = f(x) - f'(x)h + \\frac{f''(x)}{2!}h^2 - \\frac{f'''(x)}{3!}h^3 + \\dots$$
        Subtracting the two equations cancels all even-order derivative terms (including $f''(x)$):
        $$f(x+h) - f(x-h) = 2 f'(x) h + \\frac{2 f'''(x)}{6} h^3 + \\dots$$
        Dividing by $2h$:
        $$\\frac{f(x+h) - f(x-h)}{2h} = f'(x) + \\frac{f'''(x)}{6} h^2 + \\dots$$
        Hence, the leading error term is proportional to $h^2$, making it **second-order accurate**.

        ### 3. What is the Trapezoidal Rule error formula?
        For a single interval, the error is:
        $$E = -\\frac{(b - a)^3}{12} f''(\\xi)$$
        For the Composite Trapezoidal Rule over $n$ intervals with step size $h = \\frac{b-a}{n}$:
        $$E_{\\text{composite}} = -\\frac{(b - a) h^2}{12} f''(\\xi) = O(h^2)$$
        As $n$ increases, $h$ decreases, and the approximation error drops quadratically!
        """
    )
