import random
import math
from scipy.spatial import Delaunay
import numpy
import networkx

class Room:
    def __init__(self,x,y,length,width):
        self.x = x
        self.y = y
        self.length = length
        self.width = width 
        self.right = self.x + self.length//2
        self.left = self.x - (self.length//2)
        self.top = self.y - (self.width//2)
        self.bottom = self.y + self.width//2
    
    
    def updateBoundaries(self):
        self.right = self.x + self.length // 2
        self.left = self.x - (self.length // 2)
        self.top = self.y - (self.width // 2)
        self.bottom = self.y + self.width // 2

    
    def updateCentre(self):
        self.x = (self.right + self.left)//2
        self.y = (self.top +self.bottom) //2


    def intersects(self, other_room):    
        return not (self.right <= other_room.left or
                    self.left >= other_room.right or
                    self.bottom <= other_room.top or
                    self.top >= other_room.bottom)

    def separate(self, other_room):
        if self.intersects(other_room):
            dx = self.x - other_room.x
            dy = self.y - other_room.y

            if abs(dx) > abs(dy):  # Push more horizontally
                if dx > 0:
                    self.x += abs(self.right - other_room.left)
                else:
                    other_room.x += abs(self.left - other_room.right)
            else:  # Push more vertically
                if dy > 0:
                    self.y += abs(self.bottom - other_room.top)
                else:
                    other_room.y += abs(self.top - other_room.bottom)

            # Update boundaries after separation
            self.updateBoundaries()
            other_room.updateBoundaries()

    def get_center(self):
        return(self.x, self.y)        


class Map:
    def __init__(self, size, num_rooms, room_length, room_width):
        self.size = size
        self.num_rooms = num_rooms
        self.room_length =  room_length
        self.room_width = room_width
        self.grid = [["." for i in range(self.size)] for j in range(self.size)]
        self.rooms=[]

    def print_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.grid[j][i], end='')
            print()      
    def get_random_point_in_ellipse(self, ellipse_height):
        angle = 2*math.pi*random.uniform(0, 2*math.pi)
        x_distance = (self.size//2-self.room_length) * math.sqrt(random.uniform(0,1))
        y_distance = (self.size//2-ellipse_height) * math.sqrt(random.uniform(0,1))

        x=x_distance*math.cos(angle)
        y=y_distance*math.sin(angle)
        
        return (int(x + (self.size//2)),int(y + self.size//2))        
    
    def check_room_boundaries(self):
        for room in self.rooms:
            if room.right > self.size - 1:
                room.x -= room.right - (self.size - 1)
            if room.bottom > self.size - 1:
                room.y -= room.bottom - (self.size - 1)
            if room.left < 0:
                room.x += abs(room.left)
            if room.top < 0:
                room.y += abs(room.top)
            room.updateBoundaries()
            room.updateCentre()


    def initialise_rooms(self):    
        for i in range(self.num_rooms):
            x,y=self.get_random_point_in_ellipse(self.size//8)
            
            
            newRoom = Room(x,y,self.room_length,self.room_width)    
            for room in self.rooms:
                newRoom.separate(room)

            self.rooms.append(newRoom)
        self.check_room_boundaries()   
    def add_rooms(self):
        for room in self.rooms:
            for i in range(room.left, room.right):
                for j in range(room.top, room.bottom):
                    self.grid[i][j] = "a"
            
    def get_room_centers(self):
        centers=[]
        for room in self.rooms:
            centers.append(room.get_center())
        return centers
    
    def MST(self):
        centers = self.get_room_centers()
        triangles = Delaunay(centers)
        graph = networkx.Graph(data=True)
        
        for node in triangles.simplices:
            for i in range(3):
                room1=node[i]
                room2=node[(i+1)%3]
                distance = math.dist(centers[room1],centers[room2])
                graph.add_edge(room1,room2, weight = distance)
        
        
        mst = networkx.minimum_spanning_tree(graph ,weight='weight')
        points = [[[int(centers[u][0]),int(centers[u][1])],[int(centers[v][0]),int(centers[v][1])]] for u, v in mst.edges]
        return points

    def bresenhams(self,node1,node2):
        x1 = node1[0]
        x2  =node2[0]        
        y1 = node1[1]
        y2 = node2[1]
        
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1


        while y1 != y2:
            if self.grid[x1][y1]==".": 
                self.grid[x1][y1] = "b"
            if self.grid[x1+1][y1]==".":
                self.grid[x1+1][y1] = "b"
            if self.grid[x1+2][y1]==".":
                self.grid[x1+2][y1] = "b"
            y1 += sy
        while x1 != x2:
            if self.grid[x1][y1]==".":
                self.grid[x1][y1] = "b"
            if self.grid[x1][y1+1]==".":    
                self.grid[x1][y1+1] = "b"
            if self.grid[x1][y1+2]==".":
                self.grid[x1][y1+2] = "b"
            x1 += sx
    def connect_rooms(self,points):
        for pair in points:
            node1 = pair[0]
            node2 = pair[1]
            self.bresenhams(node1,node2)


def generate_map(array_size, num_rooms,room_length, room_width):
    myMap = Map(array_size,num_rooms,room_length,room_width)
    myMap.initialise_rooms()
    myMap.add_rooms()
    myMap.connect_rooms(myMap.MST())
    # myMap.print_grid()
    return myMap

#Map.generate_map(empty array size, number of rooms, room length, room width)
# Map.generate_map(100,16,8,8) 