import streamlit as st
import math
import ast
import operator as op

# streamlit_test.py
# Demo calculator Streamlit app
# Run with: streamlit run streamlit_test.py


st.set_page_config(page_title="Demo Calculator", layout="centered")

st.title("Demo Calculator")
st.write("A simple Streamlit calculator with Basic, Scientific and Expression modes.")

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

# --- UI ---
mode = st.sidebar.selectbox("Mode", ["Basic", "Scientific", "Expression"])

if mode == "Basic":
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

elif mode == "Scientific":
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

elif mode == "Expression":
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
st.sidebar.write("Streamlit demo calculator • Use the Expression mode for flexible math expressions.")