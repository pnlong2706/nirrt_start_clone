import numpy as np
import matplotlib.pyplot as plt

## Corespond first_iter
def visual_first_iter():
    a = np.genfromtxt("stat/first_iter_list_irrt_star_2d.txt")
    b = np.genfromtxt("stat/first_iter_list_nirrt_star_png_c_2d.txt")
    
    la = []
    lb = []
    
    for i in range(len(a)):
        if a[i] != -1 and b[i] != -1:
            la.append(a[i])
            lb.append(b[i])

    # plt.scatter([2500, 2500], [10, 70], c = "black")
    plt.scatter(la, lb)
    plt.plot([0,2500], [0,2500], c = "red")
    plt.xlabel("IRRT*")
    plt.ylabel("NIRRT*")
    plt.show()
    
def visual_c_best():
    a = np.genfromtxt("stat/c_best_list_irrt_star_2d.txt")
    b = np.genfromtxt("stat/c_best_list_nirrt_star_png_c_2d.txt")
    
    la = []
    lb = []
    
    for i in range(len(a)):
        if a[i] != -1 and b[i] != -1:
            la.append(a[i])
            lb.append(b[i])
    
    # plt.scatter([2500, 2500], [10, 70], c = "black")
    plt.scatter(la, lb)
    plt.plot([70,380], [70,380], c = "red")
    plt.xlabel("IRRT*")
    plt.ylabel("NIRRT*")
    plt.show()
    
def visual_time():
    a = np.genfromtxt("stat/time_list_irrt_star_2d.txt")
    b = np.genfromtxt("stat/time_list_nirrt_star_png_c_2d.txt")
    
    la = []
    lb = []
    
    for i in range(len(a)):
        if a[i] != -1 and b[i] != -1:
            la.append(a[i])
            lb.append(b[i])
    
    # plt.scatter([2500, 2500], [10, 70], c = "black")
    plt.scatter(la, lb)
    plt.plot([0,130], [0,130], c = "red")
    plt.xlabel("IRRT*")
    plt.ylabel("NIRRT*")
    plt.show()
    
def visual_cost_first_iter():
    ca = np.genfromtxt("stat/c_best_list_irrt_star_2d.txt")
    cb = np.genfromtxt("stat/c_best_list_nirrt_star_png_c_2d.txt")
    
    c = zip(ca, cb)
    
    fa = np.genfromtxt("stat/first_iter_list_irrt_star_2d.txt")
    fb = np.genfromtxt("stat/first_iter_list_nirrt_star_png_c_2d.txt")
    
    fca = []
    fcb = []
    
    ffa = []
    ffb = []
    
    for i in range(len(ca)):
        if fa[i]!=-1 and fb[i]!=-1:
            ffa.append([ca[i], fa[i]])
            ffb.append([cb[i], fb[i]])
    
    ffa.sort()
    ffb.sort()
    
    ffa = np.array(ffa)
    ffb = np.array(ffb)
    
    plt.plot(ffa[:,0], ffa[:,1], c = "red")
    plt.plot(ffb[:,0], ffb[:,1])
    plt.show()
    

# visual_first_iter()
# visual_c_best()
# visual_time()
# visual_cost_first_iter()