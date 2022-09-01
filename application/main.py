from turtle import left
import matplotlib.pyplot as plt
import numpy as np

class linear_function():
    def __init__(self, m, b):
        self.m = m
        self.b = b
    
    def compute_y(self, x: np.array) -> np.array:
        return self.m*x+self.b
    
    def plof_lf(self, x):
        y = self.compute_y(x)
        plt.plot(x, y, label="y="+str(self.m)+"x"+str(self.b))
        # TODO: Adjust the right inequality conditon for space filling
        plt.fill_between(
                    x=x,
                    y1=y,
                    y2=np.max(x),
                    color="red",
                    alpha=0.3,
                    hatch="/"
                )

def get_params(text: str):
    # e.g. text: -1*x+3
    ineqs = ["<", ">", "<=", ">="]
    kind = ""
    for s in ineqs:
        if s in text:
            kind = s
            
    _, right_side = text.split(kind)
    slope = float(right_side.split("*")[0])
    intercept = float(right_side.split("x")[1])
    
    return slope, intercept

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
    nb1 = input("Enter Nebenbedingung 1 solved for y (e.g. y<=-2*x+4): ")
    # nb2 = input("Enter Nebenbedingung 2 solved for y (e.g. y<=-1/2*x+4): ")
    # nb3 = input("Enter Nebenbedingung 3 solved for y (e.g. y<=-1/2*x+4): ")
    lf1 = linear_function(*get_params(nb1))
    # lf2 = linear_function(*get_params(nb2))
    # lf3 = linear_function(*get_params(nb3))
    X = np.linspace(-10, 10, 10)
    
    ax, fig = create_fig()
    lf1.plof_lf(X)
    plt.grid()
    plt.gca().set_aspect("equal")
    plt.legend(loc="upper left")
    plt.show()


    
    

    
    
    
    
if __name__ == "__main__":
    main()