from ast import parse
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
        print(res)
        foo = res.args[1].args[1]
        c = foo.as_coeff_Add()
        self.m = float(c[1].args[0])
        self.b = float(c[0])
        self.kind = str(type(res.args[1]))
    
    
    def compute_y(self, x: np.array) -> np.array:
        return self.m*x+self.b
    
    def plot(self, X: np.array):
        y = self.compute_y(X)
        if self.kind == "<class 'sympy.core.relational.GreaterThan'>":
            y2 = np.min(X)
        else:
            y2 = np.max(X)
        
        plt.plot(X, y, label="y="+str(self.m)+"x+"+str(self.b))
        plt.fill_between(
                    x=X,
                    y1=y,
                    y2=y2,
                    color="red",
                    alpha=0.3,
                    hatch="/"
                )
    
def create_fig():
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
    
    return ax, fig

def main():
    print("--- Welcome to the LP Visualizer ---")
    # zf = input("Enter Zielfunktion (e.g. maximize 3x+4y): ")
    iq_strs = ["1*x1+2*x2 <= 2", "-1*x1-1*x2 <= 0", "-1*x1+2*x2 <= -6" ]
    
    # for i in range(3):
    #     iq_strs.append(input("Enter Nebenbedingung: "))
    
    ax, fig = create_fig()
    X = np.linspace(-10, 10, 10)
    for iq_str in iq_strs: 
        lf = linear_function(iq_str)
        lf.solve_raw_input()
        lf.plot(X)
        
    plt.grid()
    plt.gca().set_aspect("equal")
    plt.legend(loc="upper left")
    plt.show()
    
    """
    1*x1+4*x2 <= 20
    1*x1+0*x2 <= 4
    1*x1-2*x2 <= -2
    """
    
    

    
    
    
    
if __name__ == "__main__":
    main()
    