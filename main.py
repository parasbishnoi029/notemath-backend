from fastapi import FastAPI
from pydantic import BaseModel
from sympy import symbols, integrate
from sympy.parsing.latex import parse_latex

app = FastAPI()
x = symbols("x")

class Input(BaseModel):
    latex: str

@app.get("/")
def root():
    return {"status": "NoteMath backend running"}

@app.post("/solve")
def solve(data: Input):
    try:
        # Expect input like: \int x^2 dx
        cleaned = data.latex.replace("\\int", "").replace("dx", "").strip()
        expr = parse_latex(cleaned)
        result = integrate(expr, x)

        return {
            "steps": [
                f"Given the integral {data.latex}",
                "Increase the power of x by 1",
                "Divide by the new power",
                "Add constant of integration C"
            ],
            "answer": f"{result} + C"
        }
    except:
        return {"error": "Invalid expression"}
