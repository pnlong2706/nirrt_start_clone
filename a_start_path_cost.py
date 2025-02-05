# path = "data/random_2d/train/astar_paths/0_0.txt"

import numpy as np

def a_star_cost(path):
    a = np.genfromtxt(path, delimiter=',')
    
    cost = 0
    for i in range(len(a)-1):
        lenn = np.sqrt( (a[i][0] - a[i+1][0])*(a[i][0] - a[i+1][0]) + (a[i][1] - a[i+1][1])*(a[i][1] - a[i+1][1]) )
        cost = cost + lenn

    return cost