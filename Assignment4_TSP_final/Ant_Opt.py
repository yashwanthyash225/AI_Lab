import sys
import math as m
import random 
import datetime
from itertools import combinations

start = datetime.datetime.now()

class best:
    def __init__(self,cost,path):
        self.cost = cost
        self.path = path





class node:
    def __init__(self,x,y,discov,adj_index):
        self.x = x
        self.y = y
        self.discov = discov
        self.adj_index = adj_index

    def display(self):
        print("x",self.x," y",self.y," discov",self.discov)

# ----------------------------------------------------------
def choose_random_neighbour(nodelist): #choose random neighbour with probability = 1/N
    n = len(nodelist)
    while(1):
        neighbour = nodelist[int(random.randrange(0,N))]
        if neighbour.discov == 0:
            return neighbour


def cost(c,n,adj):
    return adj[c.adj_index][n.adj_index]
def pheromone(c,n,Tau_Matrix):
    return Tau_Matrix[c.adj_index][n.adj_index]


def probab(current,neighbour,nodelist,adj,Tau_Matrix):  #return probability of (current,neighbour) by the given formula
    
   
    sum_Tau_Eta = 0
    alpha = 14
    beta = 15
    Tau_ = pheromone(current,neighbour,Tau_Matrix) ** alpha
    Eta_ = 1/(cost(current,neighbour,adj)) ** beta
    
    for i in range(0,len(nodelist)):
        if nodelist[i].discov == 0 :
            sum_Tau_Eta += (pheromone(current,nodelist[i],Tau_Matrix)**alpha) * (   (1/(cost(current,nodelist[i],adj)))**beta    )
    #print(sum_Tau_Eta ," ", Tau ," ", Eta)
    if sum_Tau_Eta == 0:
        return 1
    p = (  Tau_* Eta_   )/(   sum_Tau_Eta      )
    return  p




def path_cost(path,adj):    #cost of the tour path including return to start city
    cost_p = 0
    for i in range(0,len(path)-1):
        cost_p += cost(path[i],path[i+1],adj)
    return cost_p + cost(path[len(path)-1],path[0],adj)


def update_path_pheromones(path_list,Tau_Matrix,adj):    #after an ant has toured update the city/nodes with pheromones by given formula
        Rho = 0.2 ##evaporation coefficient
        Q = 1 #costant
        # full_path_list.sort(key=lambda x: path_cost(x,adj))
        # path_list = full_path_list[0:20]
        for i in range(0,len(Tau_Matrix)):
            for j in range(0,len(Tau_Matrix)):
                    Tau_Matrix[i][j] = (1 - Rho) * Tau_Matrix[i][j] + 0

        #calc sum of the deposits of m_ants for a single segment 
        # 1st,last for each path
        for path in path_list:
            Tau_Matrix[path[len(path)-1].adj_index][path[0].adj_index] += Q/path_cost(path,adj)
        # now consecutives of each path
        for path in path_list:
            for i in range(0,len(path)-1):
                Tau_Matrix[path[i].adj_index][path[i+1].adj_index] += Q/path_cost(path,adj)

        

def make_tour(nodelist,adj,Tau_Matrix): #make a tour for an ant
    for node in nodelist:
        node.discov = 0
    discov_count = 0
    current = choose_random_neighbour(nodelist) #choose random start city for kth ant
    current.discov = 1
    path = [current] #path of kth Ant
    while(discov_count <= len(nodelist)-2): #while nodes left
        if int((datetime.datetime.now()-start).seconds) >= 294:
            return -1
        neighbour = choose_random_neighbour(nodelist)
        probability = probab(current,neighbour,nodelist,adj,Tau_Matrix)
        # print("Pro",probability)

        if random.uniform(0,1) <= probability : #move with probabilty
            neighbour.discov = 1
            discov_count += 1
            path.append(neighbour)
            current = neighbour
    return path
    






def Ant_Opt(nodelist,adj,Tau_Matrix,m_ants,epochs):    #get the best tour after all ants exhausted
    best_path = best(float('inf'),[None]*len(nodelist))

    kth_path = []
    path_list = [[None]*len(nodelist)]*m_ants
    for iterat in range(0,epochs):
        #print("------------iter",iterat)
        for i in range (0,m_ants):
            #print("ant",i)
            kth_path = make_tour(nodelist,adj,Tau_Matrix)   #make tour for kth ant
            
            if kth_path == -1: #timeout 
                #print("Time",int((datetime.datetime.now()-start).seconds))
                return best_path

            path_list[i] = kth_path                         #update kth path in list of paths for m_ants
            if path_cost(kth_path,adj) < best_path.cost:    #update best path
                best_path.cost = path_cost(kth_path,adj)
                best_path.path = kth_path

        update_path_pheromones(path_list,Tau_Matrix,adj)    # Update pheromones for all edges that the batch of m_ants travelled in this iteration 
    
    return best_path















f = open(sys.argv[1],"r")

dist_type = f.readline().rstrip()
N = int(f.readline())

# print(dist_type,N)

coords = [[None]*2]*N
adj = [[None]*N]*N
Tau_Matrix = [[1]*N]*N #Pheromone depositite inititially with 1


for i in range(0,N):
    coords[i] = list(map(lambda x: float(x), list(f.readline().rstrip().split(" "))))
for i in range(0,N):
    adj[i] = list(map(lambda x: float(x), list(f.readline().rstrip().split(" "))))

# for i in range(0,N):
#     print(coords[i])

# for i in range(0,N):
#     print(adj[i])

nodelist = [None]*N
for i in range(0,N): #making list of nodes/cities
    temp = node(coords[i][0],coords[i][1],0,i)
    nodelist[i] = temp

m_ants = 25
epochs = 10000
b = Ant_Opt(nodelist,adj,Tau_Matrix,m_ants,epochs)

# b.path = nodelist                        #testing
# b.cost = path_cost(nodelist,adj)
t_path = b.path[:]
li  = list(combinations(t_path,2))


i = len(li)-1
while(i>=0):                              #Lin - Kernigan modified Lambda = 2
    if int((datetime.datetime.now()-start).seconds) >= 298:     #timeout
        break
    #print(path_cost(t_path,adj))
    i0 = t_path.index(li[i][0])     #swap
    i1 = t_path.index(li[i][1])
    t_path[i0],t_path[i1] = li[i][1],li[i][0]
    pc = path_cost(t_path,adj)
    if pc < b.cost:                 #update
        b.path = t_path
        b.cost = pc
        li  = list(combinations(b.path,2))  #reshuffle
        i = len(li)-1

    t_path = b.path[:]
    i = i - 1



#print("Time-------",int((datetime.datetime.now()-start).seconds))
# print(b.cost)




for i in b.path:
    print(i.adj_index,end=" ")
# print("\n",len(b.path))
# print(path_cost(nodelist,adj))


print()




