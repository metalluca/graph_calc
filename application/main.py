from ast import parse
from cProfile import label
from code import interact
from turtle import left
import matplotlib.pyplot as plt
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers import solve
from sympy import symbols
from sympy import Lt, Gt
from sympy.plotting import plot 
from sympy.plotting import plot_implicit
from sympy import Rel

class linear_function():
    
    _expr = None
    m = None
    b = None
    kind = None
    
    def __init__(self, string):
        self._expr = string
    
    def solve_raw_input(self):
        x1, x2 = symbols('x1 x2')
        lhs, rhs = parse_expr(self._expr).args
        eq = Rel(lhs, rhs, "<=")
        res = solve(eq, x2)
        foo = res.args[1].args[1]
        c = foo.as_coeff_Add()
        if c[1].args:
            self.m = float(c[1].args[0])
            self.b = float(c[0])
            self.kind = str(type(res.args[1]))
        else:
            self.kind = "vertical"
            self.m = res.args[0].args[1] # the value for x vertical line
    
    def compute_y(self, x: np.array) -> np.array:
        return self.m*x+self.b
    
    def plot(self, X: np.array):
        
        if self.kind == "vertical":
            plt.axvline(self.m, color="black", label=f"y <= {self.m}")
            plt.axvspan(self.m, np.max(X), alpha=0.3, color="red", hatch="/", label="forbidden space")
         
        else:
            y = self.compute_y(X)
            if self.kind == "<class 'sympy.core.relational.GreaterThan'>":
                y2 = np.min(X)
            else:
                y2 = np.max(X)
            
            plt.plot(X, y, label="y <="+str(self.m)+"x+"+str(self.b))
            plt.fill_between(
                        x=X,
                        y1=y,
                        y2=y2,
                        color="red",
                        alpha=0.3,
                        hatch="/"
                    )

def plot_zf(zf_expr: str, ax):
    eq = parse_expr(zf_expr)
    zf_xx = eq.args[1].args[0]
    zf_yy = eq.args[0].args[0]
    ax.arrow(0, 0, int(zf_xx), int(zf_yy), width=0.1, 
             length_includes_head=True, label="Zielfunktionsvektor",
             color="green")

def create_figure(iq_strs: list, zf: str):
    X = np.linspace(-10, 10, 10)
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.set_xticks(np.arange(-10, 10))
    ax.set_yticks(np.arange(-10, 10))
    ax.set_ylim([-10, 10])
 
    plot_zf(zf, ax)
    for iq_str in iq_strs: 
        lf = linear_function(iq_str)
        lf.solve_raw_input()
        lf.plot(X)
        
    plt.grid()
    plt.gca().set_aspect("equal")
    plt.legend(loc="upper left")
    plt.show()
    
def main():
    
    print("--- Welcome to the LP Visualizer ---")
    no_iq = int(input("How many constraints do you want to visualize?: "))
    # zf = input("Enter Zielfunktion (e.g. maximize 3x+4y): ")
    zf = "2*x1 -1*x2"
    # ! TESTS
    # iq_strs = ["1*x1+2*x2 <= 2", "-1*x1-1*x2 <= 0", "-1*x1+2*x2 <= -6" ]
    iq_strs = ["1*x1+4*x2 <= 20", "1*x1+0*x2 <= 4", "1*x1-2*x2 <= -2", "-5*x1+2*x2 <= 10"]
    # iq_strs = ["1*x1+0*x2 <= 4"]
    # iq_strs = []
    # for i in range(no_iq):
    #     iq_strs.append(input("Enter Nebenbedingung: "))
    create_figure(iq_strs, zf)

if __name__ == "__main__":
    main()
    