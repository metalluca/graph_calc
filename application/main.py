import matplotlib.pyplot as plt
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers import solve
from sympy import symbols
from sympy import Rel
"""

TODO: 1. Scale axes automatically to input size
TODO: 2. Scale X to input size


Returns:
    _type_: _description_
"""
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
        foo = res.args[1].args[1] # stores the actual unequation
        c = foo.as_coeff_Add() 
        if c[1].args:
            self.m = float(c[1].args[0])
            self.b = float(c[0])
            self.kind = str(type(res.args[1]))
        else: # if empty the constraint is either larger or smaller than x
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
                y2 = np.min(X) # boundary for filling area: either smaller or greater than function
            else:
                y2 = np.max(X)
            plt.plot(X, y, label="y <="+str(self.m)+"x+"+str(self.b))
            plt.fill_between(
                        x=X,
                        y1=y,
                        y2=y2,
                        color="red",
                        alpha=0.15,
                        hatch="/")

def plot_zf(zf_expr: str, ax):
    eq = parse_expr(zf_expr)
    zf_xx = eq.args[1].args[0]
    zf_yy = eq.args[0].args[0]
    ax.arrow(0, 0, int(zf_xx), int(zf_yy), width=0.1, 
             length_includes_head=True, label="Target-function-vector",
             color="green")

def create_figure(iq_strs: list, zf: str):
    
    X = np.linspace(-100, 100, 100)
    ax_lim = 10
    for iq_str in iq_strs: 
        lf = linear_function(iq_str)
        lf.solve_raw_input()
        if lf.b > ax_lim:
            ax_lim = lf.b
        lf.plot(X)
        
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    step = int(ax_lim/10)
    ax_range = [ax_lim*-1, ax_lim]
    ax_square_ticks = np.arange(ax_lim*-1, ax_lim)
    ax.set_xticks(ax_square_ticks[::step])
    ax.set_yticks(ax_square_ticks[::step])
    
    ax.set_ylim(ax_range)
    ax.set_xlim(ax_range)
    plot_zf(zf, ax)
    plt.grid()
    plt.gca().set_aspect("equal")
    # plt.legend(loc="upper left")
    plt.show()
    
def main():
    
    print("--- Welcome to the LP Visualizer ---")
    # no_iq = int(input("How many constraints do you want to visualize?: "))
    # zf = input("Enter Zielfunktion (e.g. maximize 3x+4y): ")
    zf = "600*x1+2000*x2"
    iq_strs = ["1*x1+1*x2 <= 60", "2000*x1+1000*x2 <= 100000", "10*x1+20*x2 <= 900" ]
    # iq_strs = ["1*x1+2*x2 <= 2", "-1*x1-1*x2 <= 0", "-1*x1+2*x2 <= -6" ]
    # iq_strs = ["1*x1+4*x2 <= 20", "1*x1+0*x2 <= 4", "1*x1-2*x2 <= -2", "-5*x1+2*x2 <= 10"]
    # iq_strs = ["1*x1+0*x2 <= 4"]
    
    # iq_strs = []
    # for i in range(no_iq):
    #     iq_strs.append(input("Enter Nebenbedingung: "))
    create_figure(iq_strs, zf)

if __name__ == "__main__":
    main()
    