import json
import matplotlib.pyplot as plt
import numpy as np
from contextlib import redirect_stdout
import os

if __name__ == '__main__':
    x = np.linspace(-15,5,1000)
    y = 100*np.sqrt(abs(1-0.01*x**2))+0.01*abs(x+10)
    plt.axis([-15,5,0,120])
    plt.plot(x,y)
    plt.show()

    if 'results' not in os.listdir():
        os.makedirs(os.path.join(os.getcwd(), 'results'))

    with open("results/results.json", "w", encoding="utf-8") as file:
        file.write('{\n    ')
        file.writelines(f'"x":{[x[i] for i in range(len(x))]},\n    ')
        file.writelines(f'"y":{[y[i] for i in range(len(y))]}\n')
        file.write('}')