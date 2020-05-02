import math

class path:
    def __init__(self):
        self.G = 0
        self.cost = 0
        self.visited = set()
        self.route = list()
        self.goal_reached = False
        
    def __str__(self):
        return f"Cost: {self.cost}\nVisited: {self.visited}"
        

class priorityQueue:
    
    def __init__(self, initial_size=10):
        self.cbt = [None for _ in range(initial_size)]  # initialize arrays
        self.next_index = 0  # denotes next index where new element should go

    def insert(self, path):
        # insert element at the next index
        self.cbt[self.next_index] = path

        # heapify
        self._up_heapify()

        # increase index by 1
        self.next_index += 1

        # double the array and copy elements if next_index goes out of array bounds
        if self.next_index >= len(self.cbt):
            temp = self.cbt
            self.cbt = [None for _ in range(2 * len(self.cbt))]

            for index in range(self.next_index):
                self.cbt[index] = temp[index]

    def remove(self):
        if self.size() == 0:
            return None
        self.next_index -= 1

        to_remove = self.cbt[0]
        last_element = self.cbt[self.next_index]

        # place last element of the cbt at the root
        self.cbt[0] = last_element

        # we do not remove the elementm, rather we allow next `insert` operation to overwrite it
        self.cbt[self.next_index] = to_remove
        self._down_heapify()
        return to_remove

    def size(self):
        return self.next_index 

    def is_empty(self):
        return self.size() == 0

    def _up_heapify(self):
        # print("inside heapify")
        child_index = self.next_index

        while child_index >= 1:
            parent_index = (child_index - 1) // 2
            parent_element = self.cbt[parent_index]
            child_element = self.cbt[child_index]

            if parent_element.cost > child_element.cost:
                self.cbt[parent_index] = child_element
                self.cbt[child_index] = parent_element

                child_index = parent_index
            else:
                break

    def _down_heapify(self):
        parent_index = 0

        while parent_index < self.next_index:
            left_child_index = 2 * parent_index + 1
            right_child_index = 2 * parent_index + 2

            parent = self.cbt[parent_index]
            left_child = None
            right_child = None
            
            min_element = parent

            # check if left child exists
            if left_child_index < self.next_index:
                left_child = self.cbt[left_child_index]

            # check if right child exists
            if right_child_index < self.next_index:
                right_child = self.cbt[right_child_index]

            # compare with left child
            if left_child is not None:
                if parent.cost < left_child.cost:
                    min_element = parent
                else:
                    min_element = left_child

            # compare with right child
            if right_child is not None:
                if min_element.cost > right_child.cost:
                    min_element = right_child

            # check if parent is rightly placed
            if min_element.cost == parent.cost:
                return

            if min_element.cost == left_child.cost:
                self.cbt[left_child_index] = parent
                self.cbt[parent_index] = min_element
                parent_index = left_child_index

            elif min_element.cost == right_child.cost:
                self.cbt[right_child_index] = parent
                self.cbt[parent_index] = min_element
                parent_index = right_child_index

    def get_minimum(self):
        # Returns the minimum element present in the heap
        if self.size() == 0:
            return None
        return self.cbt[0]

    
def get_distance(M, node1,node2):
    #Using Euclidean distance to calculate gcost and hcost
    
    coords1 = M.intersections[node1]
    coords2 = M.intersections[node2]
    
    deltax = (coords2[0] - coords1[0])**2
    deltay = (coords2[1] - coords1[1])**2
    
    return math.sqrt(deltax + deltay)



def shortest_path(M,start,goal):
    
    #frontiers dictionary to keep track of the explored paths
    frontiers = dict()
    
    #priority queue using heap data structure to store path & their costs
    priority = priorityQueue(10)
    
    if start == goal:
        return [start]
    
    while True:
        
        if not priority.is_empty():
            bestPath = priority.remove()
            frontier = bestPath.route[-1]
            if bestPath.goal_reached:
                return bestPath.route
        else:
            frontier = start
        
        for road in M.roads[frontier]:
            g_cost = get_distance(M, frontier, road)
            
            #Small Heuristic to increase short path precision
            h_cost = get_distance(M,road,goal)
            if frontier != start:
                
                if road in bestPath.visited:
                    continue
                
                newPath = path()
                newPath.G = g_cost + bestPath.G
                newPath.cost = newPath.G + h_cost
                newPath.visited = set(bestPath.visited)
                newPath.visited.add(road)
                newPath.route = bestPath.route[:]
                newPath.route.append(road)
                
                if road == goal:
                    newPath.goal_reached = True
                
                if frontiers.get(road):
                    if frontiers[road].cost <= newPath.cost:
                        continue

            else:
                newPath = path()
                newPath.G = g_cost
                newPath.cost = h_cost + g_cost
                newPath.visited.add(start)
                newPath.visited.add(road)
                newPath.route.append(start)
                newPath.route.append(road)
            
            frontiers[road] = newPath
            priority.insert(newPath)