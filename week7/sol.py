import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
def yfunc(x):
    return x**2 + np.sin(8*x)

## function for Problem 1 
def find_min(func, bestx, decayrate, T):
    # bestx=starting_point
    best_cost=100000
    bestx_lst=[]
    steps=100
    # rangemin, rangemax = -2, 2 
    xbase = np.linspace(-2, 2, 100)
    ybase = func(xbase)

    fig, ax = plt.subplots()
    ax.plot(xbase, ybase)
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro')
    lngood, = ax.plot([], [], 'go', markersize=10)
    def onestep(frame):
        nonlocal best_cost, bestx, decayrate, T
    # Generate a random value \in -2, +2
        dx = (np.random.random_sample() - 0.5) * T
        x = bestx + dx
        # print(f"Old x = {x}, delta = {dx}")
        y = func(x)
        if y < best_cost:
            # print(f"Improved from {bestcost} at {bestx} to {y} at {x}")
            best_cost = y
            bestx = x
            lngood.set_data(x, y)
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(y-best_cost)/T):
                best_cost = y
                bestx = x
                lngood.set_data(x, y)
            # print(f"New cost {y} worse than best so far: {bestcost}")
            pass
        T = T * decayrate
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)
        # return lngood,

    # print('yes')
    ani= FuncAnimation(fig, onestep, frames=range(1000), interval=100, repeat=False)
    plt.show()
    return bestx,best_cost
bestx,best_cost=find_min(yfunc,-2,0.91,3)
print(f'minima occurs at {bestx} and value is {best_cost}')

# function for reading of file 
def readfile(file):
    with open(file,'r')as f:
        lines=f.read().splitlines()
        total_cities=float(lines[0].split()[0])
        # print(total_cities)
        lst=[]
        for i in range(1,int(total_cities+1)):
            lst.append((float(lines[i].split()[0]),float(lines[i].split()[1])))
        lst=np.array(lst)
        return int(total_cities),lst
    

    # Function for Problem 2
def find_min_cost_tsp(file):
    no_of_cities,cities=readfile(file)  #Reading file
    nodes={}
    x_cities=[]
    y_cities=[]
    for i in range(len(cities)):
        nodes.update({i:cities[i]})
        x_cities.append(cities[i][0])
        y_cities.append(cities[i][1])
    x_cities=np.array(x_cities)
    y_cities=np.array(y_cities)
    T = 100.0
    decayrate = 0.99
    bestcost = 100000

    best_array=[i for i in range(len(cities))]
    # print(best_array)
    def onestep(frame):
        # print(frame)
        # print(bestcost)
        nonlocal bestcost, best_array, decayrate, T
        # print(best_array)
        new_lst=[ele for ele in best_array]
        ran_no1=np.random.randint(0,100)
        ran_no2=np.random.randint(0,100)
        while(ran_no1==ran_no2):
            ran_no1=np.random.randint(0,len(best_array))
            ran_no2=np.random.randint(0,len(best_array))
        new_lst=new_lst[:min(ran_no1,ran_no2)]+new_lst[min(ran_no1,ran_no2):max(ran_no1,ran_no2)][::-1]+new_lst[max(ran_no1,ran_no2):]
        # np.random.shuffle(new_lst)
        y=0
        for i in range(1,len(new_lst)):
            y+=np.sqrt(np.square(nodes[new_lst[i]][0]-nodes[new_lst[i-1]][0])+np.square(nodes[new_lst[i]][1]-nodes[new_lst[i-1]][1]))
        y+=np.sqrt(np.square(nodes[new_lst[len(new_lst)-1]][0]-nodes[new_lst[0]][0])+np.square(nodes[new_lst[len(new_lst)-1]][1]-nodes[new_lst[0]][1]))
        
        if y < bestcost:
            # print(f"Improved from {bestcost} at {bestx} to {y} at {x}")
            bestcost = y
            best_array=new_lst
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(y-bestcost)/T):
                bestcost = y
                best_array=new_lst
            # print(f"New cost {y} worse than best so far: {bestcost}")
            pass
        T = T * decayrate

    for i in range(50000):
        onestep(i)
    
    best_array.append(best_array[0])

    xplot = x_cities[best_array] 
    yplot = y_cities[best_array]
    # xplot = np.append(xplot, xplot[0])
    # yplot = np.append(yplot, yplot[0])
    plt.plot(xplot, yplot, 'o-')
    f1=file.split('/')
    plt.title(f'Cities traversed path for dataset : {f1[len(f1)-1]}')

    name=[]
    for i in range (len(x_cities)):
        name.append(f'A{i+1}')
    for i in range(len(x_cities)):
        plt.annotate(name[i],xy=(xplot[i],yplot[i]))
    
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()
    
    return bestcost,best_array
    print(bestcost)
    print(best_array)

best_cost10,best_array10=find_min_cost_tsp('/Users/amankumar/Documents/semester4/Applied Programming Lab(APL)/week7/tsp_10.txt')
best_cost100,best_array100=find_min_cost_tsp('/Users/amankumar/Documents/semester4/Applied Programming Lab(APL)/week7/tsp_100.txt')

print(f'The minimum total distance covered to visit all cities for tsp_10.txt dataset is : {best_cost10}')
print(f'The cities travelled in the order : {best_array10}')
print()
print(f'The minimum total distance covered to visit all cities for tsp_100.txt dataset is : {best_cost100}')
print(f'The cities travelled in the order for dataset tsp_100.txt: {best_array100}')
#array[:i]+array[i:j][::-1]+array[j+1:]

