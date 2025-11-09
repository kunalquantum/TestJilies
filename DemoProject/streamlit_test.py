import streamlit as st
import math
import ast
import operator as op
import plotly.graph_objects as go

# streamlit_test.py
# Demo calculator Streamlit app
# Run with: streamlit run streamlit_test.py


st.set_page_config(page_title="Advanced Calculator", layout="wide")

st.title("Advanced Calculator")
st.write("A multi-mode calculator with Basic, Scientific, Financial, and Expression modes.")

# --- Safe expression evaluator ---
# Based on a whitelist approach using ast
ALLOWED_NAMES = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
ALLOWED_NAMES.update({"abs": abs, "round": round, "pow": pow})

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.FloorDiv: op.floordiv,
}


def safe_eval(expr: str):
    """
    Evaluate a numeric Python expression safely using ast.
    Supports numbers, parentheses, unary/binary ops and whitelisted math functions.
    """
    try:
        node = ast.parse(expr, mode="eval")
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):  # < Py3.8
            return node.n
        if hasattr(ast, "Constant") and isinstance(node, ast.Constant):  # Py3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Unsupported constant type")
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Operator {op_type} not allowed")
            return ALLOWED_OPERATORS[op_type](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Unary operator {op_type} not allowed")
            return ALLOWED_OPERATORS[op_type](_eval(node.operand))
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls allowed")
            func_name = node.func.id
            if func_name not in ALLOWED_NAMES:
                raise ValueError(f"Function {func_name} not allowed")
            args = [_eval(arg) for arg in node.args]
            return ALLOWED_NAMES[func_name](*args)
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_NAMES:
                return ALLOWED_NAMES[node.id]
            raise ValueError(f"Name {node.id} is not allowed")
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    return _eval(node)


# --- Session state for history ---
if "history" not in st.session_state:
    st.session_state.history = []

def render_basic_calculator():
    st.subheader("Basic calculator")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("First number", value=0.0, format="%-0.8g")
    with col2:
        b = st.number_input("Second number", value=0.0, format="%-0.8g")

    op = st.selectbox("Operation", ["Add (+)", "Subtract (-)", "Multiply (*)", "Divide (/)"])
    if st.button("Compute"):
        try:
            if op.startswith("Add"):
                res = a + b
            elif op.startswith("Subtract"):
                res = a - b
            elif op.startswith("Multiply"):
                res = a * b
            elif op.startswith("Divide"):
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                res = a / b
            else:
                res = "Unknown operation"
            st.success(f"Result: {res}")
            st.session_state.history.append(f"{a} {op} {b} = {res}")
        except Exception as e:
            st.error(f"Error: {e}")

def render_scientific_calculator():
    st.subheader("Scientific calculator")
    func = st.selectbox(
        "Function",
        [
            "sin", "cos", "tan",
            "asin", "acos", "atan",
            "sqrt", "log", "log10",
            "exp", "factorial", "pow"
        ],
    )
    if func == "pow":
        x = st.number_input("Base", value=2.0, format="%-0.8g")
        y = st.number_input("Exponent", value=3.0, format="%-0.8g")
    elif func == "factorial":
        n = st.number_input("Integer", value=5, step=1)
    else:
        x = st.number_input("Input", value=1.0, format="%-0.8g")

    if st.button("Compute"):
        try:
            if func in ("sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "log", "log10", "exp"):
                result = getattr(math, func)(x)
                st.success(f"{func}({x}) = {result}")
                st.session_state.history.append(f"{func}({x}) = {result}")
            elif func == "factorial":
                val = int(n)
                if val < 0:
                    raise ValueError("factorial() not defined for negative values")
                result = math.factorial(val)
                st.success(f"factorial({val}) = {result}")
                st.session_state.history.append(f"factorial({val}) = {result}")
            elif func == "pow":
                result = math.pow(x, y)
                st.success(f"pow({x}, {y}) = {result}")
                st.session_state.history.append(f"pow({x}, {y}) = {result}")
            else:
                st.error("Unsupported function")
        except Exception as e:
            st.error(f"Error: {e}")


def render_expression_evaluator():
    st.subheader("Expression evaluator (safe)")
    expr = st.text_input("Enter expression", value="2 * sin(pi / 4) + sqrt(16)")
    st.caption("Allowed: numbers, arithmetic operators, math functions (sin, cos, sqrt, etc.), abs, round, pow.")
    if st.button("Evaluate"):
        try:
            res = safe_eval(expr)
            st.success(f"{expr} = {res}")
            st.session_state.history.append(f"{expr} = {res}")
        except Exception as e:
            st.error(f"Error: {e}")

def render_financial_calculator():
    st.subheader("Financial Calculator")

    tab1, tab2, tab3 = st.tabs(["Loan Payment", "Compound Interest", "Savings Goal"])

    with tab1:
        st.header("Loan Payment Calculator")
        loan_amount = st.number_input("Loan Amount", min_value=0.0, value=10000.0, step=1000.0)
        interest_rate = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        loan_term = st.slider("Loan Term (Years)", min_value=1, max_value=30, value=5, step=1)

        if st.button("Calculate Loan Payment"):
            try:
                monthly_rate = (interest_rate / 100) / 12
                num_payments = loan_term * 12
                if monthly_rate > 0:
                    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
                else:
                    monthly_payment = loan_amount / num_payments

                total_paid = monthly_payment * num_payments
                total_interest = total_paid - loan_amount

                st.success(f"Monthly Payment: ${monthly_payment:,.2f}")
                st.info(f"Total Paid: ${total_paid:,.2f}")
                st.warning(f"Total Interest: ${total_interest:,.2f}")

                # Pie chart for principal vs interest
                fig = go.Figure(data=[go.Pie(labels=['Principal', 'Interest'], values=[loan_amount, total_interest], hole=.3)])
                fig.update_layout(title_text='Principal vs. Interest')
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.header("Compound Interest Calculator")
        principal = st.number_input("Principal Amount", min_value=0.0, value=1000.0, step=100.0)
        ci_interest_rate = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1, key="ci_rate")
        years = st.slider("Number of Years", min_value=1, max_value=50, value=10, step=1)
        compounding_freq = st.selectbox("Compounding Frequency", ["Annually", "Semi-Annually", "Quarterly", "Monthly"])

        if st.button("Calculate Compound Interest"):
            try:
                freq_map = {"Annually": 1, "Semi-Annually": 2, "Quarterly": 4, "Monthly": 12}
                n = freq_map[compounding_freq]
                r = ci_interest_rate / 100

                future_value = principal * (1 + r / n)**(n * years)

                st.success(f"Future Value: ${future_value:,.2f}")

                # Line chart for investment growth
                time_periods = list(range(years + 1))
                values = [principal * (1 + r / n)**(n * t) for t in time_periods]
                fig = go.Figure(data=go.Scatter(x=time_periods, y=values, mode='lines+markers'))
                fig.update_layout(title='Investment Growth Over Time', xaxis_title='Years', yaxis_title='Future Value ($)')
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error: {e}")

    with tab3:
        st.header("Savings Goal Calculator")
        goal_amount = st.number_input("Goal Amount", min_value=0.0, value=20000.0, step=1000.0)
        sg_interest_rate = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=20.0, value=4.0, step=0.1, key="sg_rate")
        sg_years = st.slider("Number of Years to Save", min_value=1, max_value=50, value=5, step=1)

        if st.button("Calculate Savings Needed"):
            try:
                r = sg_interest_rate / 100 / 12
                n = sg_years * 12
                if r > 0:
                    monthly_saving = goal_amount * (r / ((1 + r)**n - 1))
                else:
                    monthly_saving = goal_amount / n

                st.success(f"You need to save ${monthly_saving:,.2f} per month to reach your goal.")

            except Exception as e:
                st.error(f"Error: {e}")


# --- UI ---
MODES = {
    "Basic": render_basic_calculator,
    "Scientific": render_scientific_calculator,
    "Financial": render_financial_calculator,
    "Expression": render_expression_evaluator,
}

mode = st.sidebar.selectbox("Mode", list(MODES.keys()))

# Render the selected mode
if mode in MODES:
    MODES[mode]()

# --- History and controls ---
st.sidebar.markdown("### History")
if st.session_state.history:
    for h in reversed(st.session_state.history[-10:]):
        st.sidebar.write(h)
else:
    st.sidebar.write("No history yet")

if st.sidebar.button("Clear history"):
    st.session_state.history = []
    st.sidebar.success("History cleared")

st.sidebar.markdown("---")
st.sidebar.info("Developed by Advanced Streamlit App")
