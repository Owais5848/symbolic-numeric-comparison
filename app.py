"""
app.py
------
Frontend Web Application for the Symbolic vs Numeric Comparison Project.

Built with Streamlit.
Features a modern, responsive, premium dark-themed UI with deep navy, dark blue cards,
bright blue accents, purple secondary accents, and cyan/teal success metrics.
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
# 2. CUSTOM CSS STYLING (PREMIUM DARK DASHBOARD)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* =========================================================================
       1. GLOBAL THEME & TYPOGRAPHY
       ========================================================================= */
    :root {
        --bg-navy: #0B1120;
        --sidebar-navy: #111C32;
        --card-darkblue: #17243A;
        --card-hover: #1E2E4A;
        --border-color: #2D4263;
        --accent-blue: #3B82F6;
        --accent-purple: #A78BFA;
        --accent-teal: #2DD4BF;
        --text-white: #F8FAFC;
        --text-lightgrey: #CBD5E1;
        --text-muted: #94A3B8;
    }

    /* Main Application Canvas */
    .stApp {
        background-color: #0B1120 !important;
        color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Global Headings: 100% Crisp White with Optimal Spacing */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Body Text & Descriptions */
    .stMarkdown p, .stMarkdown span, .stMarkdown li,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] li {
        color: #CBD5E1 !important;
        font-size: 0.95rem;
        line-height: 1.65;
    }

    /* Captions & Subtext */
    .stCaption, [data-testid="stCaptionContainer"] p, .stCaption p {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        line-height: 1.4 !important;
    }

    /* Clean Section Dividers */
    hr, .stDivider, div[data-testid="stDivider"] {
        border-color: #1E2E4A !important;
        margin: 2.2rem 0 !important;
    }

    /* =========================================================================
       2. SIDEBAR STYLING
       ========================================================================= */
    section[data-testid="stSidebar"] {
        background-color: #111C32 !important;
        border-right: 1px solid #1E2E4A !important;
        padding-top: 1.5rem !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.6rem !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
    }

    /* =========================================================================
       3. INPUT CONTROLS & WIDGET LABELS
       ========================================================================= */
    label[data-testid="stWidgetLabel"],
    .stWidgetLabel p,
    .stWidgetLabel span {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        margin-bottom: 6px !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background-color: #17243A !important;
        color: #F8FAFC !important;
        border: 1px solid #2D4263 !important;
        border-radius: 9px !important;
        font-size: 0.95rem !important;
        padding: 9px 12px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
        background-color: #1A2A44 !important;
    }

    /* Stepper (+/-) buttons */
    div[data-testid="stNumberInput"] button {
        background-color: #1E2E4A !important;
        color: #CBD5E1 !important;
        border: 1px solid #2D4263 !important;
        border-radius: 6px !important;
    }

    div[data-testid="stNumberInput"] button:hover {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border-color: #3B82F6 !important;
    }

    /* Checkbox Labels */
    div[data-testid="stCheckbox"] label p {
        color: #CBD5E1 !important;
        font-size: 0.9rem !important;
    }

    /* =========================================================================
       4. PRIMARY BUTTON STYLING
       ========================================================================= */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.02rem !important;
        letter-spacing: 0.02em !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 10px !important;
        padding: 13px 26px !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 10px !important;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #1D4ED8 0%, #2563EB 100%) !important;
        border-color: #60A5FA !important;
        box-shadow: 0 6px 22px rgba(37, 99, 235, 0.55) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton > button:first-child:active {
        transform: translateY(0) !important;
    }

    /* =========================================================================
       5. STREAMLIT TABS (CLEAN HIGH-CONTRAST PILLS)
       ========================================================================= */
    div[data-baseweb="tab-list"] {
        background-color: #17243A !important;
        border-radius: 12px !important;
        padding: 6px !important;
        gap: 8px !important;
        border: 1px solid #2D4263 !important;
        margin-bottom: 24px !important;
    }

    button[data-baseweb="tab"] {
        color: #CBD5E1 !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
        background-color: rgba(59, 130, 246, 0.15) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45) !important;
    }

    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* =========================================================================
       6. MATHEMATICAL EXPRESSIONS & LATEX
       ========================================================================= */
    .katex, .katex-display, .katex-html, span.katex {
        color: #F8FAFC !important;
    }

    div[data-testid="stLatex"] {
        background-color: #17243A !important;
        border: 1px solid rgba(167, 139, 250, 0.28) !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        margin: 10px 0 !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.25) !important;
    }

    /* =========================================================================
       7. CARDS, BANNERS, HEADERS & METRICS
       ========================================================================= */
    /* Project Header Card with Generous Breathing Room */
    .main-header {
        background: linear-gradient(135deg, #111C32 0%, #17243A 60%, #1E2E4A 100%);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 16px;
        padding: 34px 38px;
        margin-bottom: 34px;
        box-shadow: 0 12px 32px -6px rgba(0, 0, 0, 0.6), 0 0 24px rgba(59, 130, 246, 0.15);
    }

    .main-title {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.25 !important;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .main-subtitle {
        color: #CBD5E1 !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        max-width: 950px;
        margin-bottom: 22px !important;
    }

    /* Badge Flex Container for Clean Multi-Screen Wrapping */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }

    .badge-tag {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
        color: #FFFFFF;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 15px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }

    .badge-purple {
        display: inline-flex;
        align-items: center;
        background: rgba(167, 139, 250, 0.15);
        color: #A78BFA;
        border: 1px solid rgba(167, 139, 250, 0.35);
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 15px;
        border-radius: 9999px;
        letter-spacing: 0.03em;
    }

    .badge-teal {
        display: inline-flex;
        align-items: center;
        background: rgba(45, 212, 191, 0.15);
        color: #2DD4BF;
        border: 1px solid rgba(45, 212, 191, 0.35);
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 15px;
        border-radius: 9999px;
        letter-spacing: 0.03em;
    }

    /* Standard Content Section Cards */
    .content-card {
        background: #17243A;
        border: 1px solid #2D4263;
        border-radius: 16px;
        padding: 26px 30px;
        margin-bottom: 28px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }

    .card-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 16px !important;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 1px solid #2D4263;
        padding-bottom: 14px;
        letter-spacing: -0.01em;
    }

    /* Metric Cards with Glowing Hover Accent */
    .metric-card {
        background: linear-gradient(145deg, #1A2942 0%, #17243A 100%);
        border: 1px solid #2D4263;
        border-radius: 14px;
        padding: 20px 22px;
        text-align: left;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        border-color: #3B82F6;
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(59, 130, 246, 0.25);
    }

    .metric-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #CBD5E1;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .metric-value-symbolic {
        font-size: 1.75rem;
        font-weight: 800;
        color: #3B82F6;
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        margin: 4px 0;
    }

    .metric-value-numeric {
        font-size: 1.75rem;
        font-weight: 800;
        color: #A78BFA;
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        margin: 4px 0;
    }

    .metric-value-error {
        font-size: 1.75rem;
        font-weight: 800;
        color: #2DD4BF;
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
        margin: 4px 0;
    }

    .metric-subtext {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-top: 8px;
        line-height: 1.45;
    }

    .formula-banner {
        background: rgba(23, 36, 58, 0.85);
        border: 1px solid #2D4263;
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 20px;
        color: #CBD5E1;
        font-size: 0.94rem;
        line-height: 1.6;
    }

    /* =========================================================================
       8. DATAFRAME & TABLE STYLING
       ========================================================================= */
    div[data-testid="stDataFrame"] {
        border: 1px solid #2D4263 !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3) !important;
    }

    /* =========================================================================
       9. ALERTS & NOTIFICATIONS
       ========================================================================= */
    div[data-testid="stAlert"] {
        background-color: #17243A !important;
        border: 1px solid #2D4263 !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
    }
    div[data-testid="stAlert"] p {
        color: #F8FAFC !important;
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
    st.markdown("<p style='color:#CBD5E1; font-size:0.86rem; line-height:1.5;'>Configure mathematical parameters for symbolic & numerical engines.</p>", unsafe_allow_html=True)
    st.divider()

    # Function Input Field with confirmed default
    st.markdown("#### 📐 1. Function Definition")
    func_input = st.text_input(
        "Mathematical Function f(x)",
        value="x**3 - 3*x**3 + 2*x",
        help="Enter an expression in terms of x. Example: x**3 - 3*x**3 + 2*x, sin(x), exp(x)"
    )

    st.markdown("#### ⚡ 2. Differentiation Controls")
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

    st.markdown("#### 📐 3. Integration Controls")
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

    st.markdown("#### 📈 4. Graph Display Controls")
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
        <div style='margin-top: 26px; padding: 16px; background: #17243A; border-radius: 12px; border: 1px solid #2D4263;'>
            <p style='font-size:0.8rem; color:#CBD5E1; margin:0; line-height: 1.6;'>
                <strong style='color:#F8FAFC;'>Course:</strong> Numerical & Symbolic Computing<br>
                <strong style='color:#F8FAFC;'>Backend:</strong> SymPy (Exact) & NumPy (CFD / Trapezoidal)<br>
                <strong style='color:#F8FAFC;'>Theme:</strong> Premium Deep Navy UI
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 4. HEADER SECTION (MORE BREATHING ROOM, BOLD TITLE, WRAPPED BADGES)
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
        <div class="badge-container">
            <span class="badge-tag">🎓 BSCS University Project</span>
            <span class="badge-purple">🔮 SymPy 1.12+ (Exact CAS)</span>
            <span class="badge-teal">⚙️ NumPy 1.24+ (Numerical)</span>
            <span class="badge-tag">⚡ Central Difference O(h²)</span>
            <span class="badge-teal">📐 Trapezoidal Rule O(h²)</span>
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
    """,
    unsafe_allow_html=True
)

col_orig, col_arrow, col_simp = st.columns([5, 1, 5])

with col_orig:
    st.markdown("<strong style='color:#F8FAFC; font-size:1.0rem;'>Original Input Function:</strong>", unsafe_allow_html=True)
    st.latex(f"f(x) = {func_data['latex_original']}")
    st.caption(f"Raw Input: `{func_data['original_str']}`")

with col_arrow:
    st.markdown("<div style='text-align:center; padding-top:30px; font-size:2.0rem; color:#A78BFA; font-weight:bold;'>➔</div>", unsafe_allow_html=True)

with col_simp:
    st.markdown("<strong style='color:#F8FAFC; font-size:1.0rem;'>Simplified Polynomial Form:</strong>", unsafe_allow_html=True)
    st.latex(f"f(x) = {func_data['latex_simplified']}")
    st.caption("SymPy automatically identified & combined like terms ($x^3 - 3x^3 = -2x^3$).")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. SECTION 2: DIFFERENTIATION COMPARISON
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="content-card">
        <div class="card-title">
            <span>⚡ 2. Differentiation Comparison: Exact Derivative vs Central Finite Difference</span>
        </div>
        <div class="formula-banner">
            <strong style="color:#F8FAFC;">Symbolic Formula:</strong> $\\frac{{d}}{{dx}} f(x) = {diff_data['symbolic']['latex_derivative']}$<br>
            <strong style="color:#F8FAFC;">Numerical Formula:</strong> Central Finite Difference $f'(x) \\approx \\frac{{f(x+h) - f(x-h)}}{{2h}}$ with $x = {diff_data['numeric']['x_val']}$ and $h = {diff_data['numeric']['h']}$
        </div>
    """,
    unsafe_allow_html=True
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

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. SECTION 3: INTEGRATION COMPARISON
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="content-card">
        <div class="card-title">
            <span>📐 3. Integration Comparison: Exact Definite Integral vs Composite Trapezoidal Rule</span>
        </div>
        <div class="formula-banner">
            <strong style="color:#F8FAFC;">Symbolic Indefinite:</strong> $\\int f(x) dx = {int_data['indefinite_symbolic']['latex_indefinite']}$<br>
            <strong style="color:#F8FAFC;">Definite Bounds:</strong> Interval $[a, b] = [{int_data['definite_symbolic']['a']}, {int_data['definite_symbolic']['b']}]$ with $n = {int_data['numeric_trapezoidal']['n']}$ trapezoids ($\\Delta x = {int_data['numeric_trapezoidal']['h']:.5f}$)
        </div>
    """,
    unsafe_allow_html=True
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

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. SECTION 4: COMPREHENSIVE COMPARISON SUMMARY TABLE
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="content-card">
        <div class="card-title">
            <span>📊 4. Comprehensive Comparison Summary Table</span>
        </div>
    """,
    unsafe_allow_html=True
)

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

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 10. SECTION 5: INTERACTIVE VISUAL PLOTS (MATPLOTLIB & GRAPHS.PY)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="content-card">
        <div class="card-title">
            <span>📈 5. Visual Graphs & Geometric Interpretation</span>
        </div>
        <p style='color:#CBD5E1; font-size:0.95rem; margin-bottom: 20px;'>
            Visualizing the continuous analytical curves alongside discrete numerical approximations.
        </p>
    """,
    unsafe_allow_html=True
)

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
    st.markdown("<strong style='color:#F8FAFC; font-size:1.02rem;'>1. Original Function Graph: $f(x)$</strong>", unsafe_allow_html=True)
    st.caption("Shows the full mathematical curve across the domain, highlighting the evaluation point $x$ and integration limits $[a, b]$.")
    st.pyplot(fig_orig)

with tab2:
    st.markdown("<strong style='color:#F8FAFC; font-size:1.02rem;'>2. Symbolic Derivative Graph: $f'(x)$</strong>", unsafe_allow_html=True)
    st.caption("Plots the exact rate-of-change formula derived algebraically by SymPy, with the slope at $x=2$ marked.")
    st.pyplot(fig_sym_deriv)

with tab3:
    st.markdown("<strong style='color:#F8FAFC; font-size:1.02rem;'>3. Derivative Comparison: Analytical vs Central Finite Difference</strong>", unsafe_allow_html=True)
    st.caption("Visualizes how closely the discrete Central Finite Difference estimates align with the continuous exact derivative curve.")
    st.pyplot(fig_diff_comp)

with tab4:
    st.markdown("<strong style='color:#F8FAFC; font-size:1.02rem;'>4. Definite Integration & Trapezoidal Chords</strong>", unsafe_allow_html=True)
    st.caption("Shows the exact shaded definite area $\\int_a^b f(x) dx$ compared with the composite trapezoid geometric approximation.")
    st.pyplot(fig_integration)

st.markdown("</div>", unsafe_allow_html=True)
