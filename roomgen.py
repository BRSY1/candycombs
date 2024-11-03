import random
import math
from scipy.spatial import Delaunay
import numpy
import networkx

class Room:
    def __init__(self,x,y,length,width,type):
        self.x = x
        self.y = y
        self.length = length
        self.width = width 
        self.right = self.x + self.length//2
        self.left = self.x - (self.length//2)
        self.top = self.y - (self.width//2)
        self.bottom = self.y + self.width//2
        self.type = type
    
    
    def get_center(self):
        return(self.x, self.y)        
    
    def get_side_midpoints(self):
        return {
            "top": (self.x, self.top),
            "bottom": (self.x, self.bottom),
            "left": (self.left, self.y),
            "right": (self.right, self.y),
        }
        
    def updateBoundaries(self):
        self.right = self.x + self.length // 2
        self.left = self.x - (self.length // 2)
        self.top = self.y - (self.width // 2)
        self.bottom = self.y + self.width // 2

    
    def updateCentre(self):
        self.x = (self.right + self.left)//2
        self.y = (self.top +self.bottom) //2


    def intersects(self, other_room):    
        return not (self.right <= other_room.left -3 or
                    self.left >= other_room.right +3 or
                    self.bottom <= other_room.top -3 or
                    self.top >= other_room.bottom +3)

    def separate(self, other_room):
        if self.intersects(other_room):
            dx = self.x - other_room.x
            dy = self.y - other_room.y

            if abs(dx) > abs(dy):  # Push more horizontally
                if dx > 0:
                    self.x += abs(self.right - other_room.left)+1
                else:
                    other_room.x += abs(self.left - other_room.right)+1
            else:  # Push more vertically
                if dy > 0:
                    self.y += abs(self.bottom - other_room.top)+1
                else:
                    other_room.y += abs(self.top - other_room.bottom)+1

            # Update boundaries after separation
            self.updateBoundaries()
            other_room.updateBoundaries()



class Map:
    def __init__(self, size, num_rooms, room_length, room_width):
        self.size = size
        self.num_rooms = num_rooms
        self.room_length =  room_length
        self.room_width = room_width
        self.grid = [["." for i in range(self.size)] for j in range(self.size)]
        self.rooms=[]
        self.center_x = self.size//2
        self.center_y = self.size//2
        self.treasure_count = 20
        self.floorTiles = ["a","b","c","d"]

    def print_grid(self):
        for row in self.grid:
            print("".join(row))
        
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
    
    def mark_no_path_zones(self):
        for room in self.rooms:
            for i in range(room.left - 1, room.right + 2):
                if 0 <= i < self.size:
                    if 0 <= room.top - 1 < self.size:
                        self.grid[i][room.top - 1] = "#"  # Mark above top edge
                    if 0 <= room.bottom + 1 < self.size:
                        self.grid[i][room.bottom + 1] = "#"  # Mark below bottom edge
            for j in range(room.top - 1, room.bottom + 2):
                if 0 <= j < self.size:
                    if 0 <= room.left - 1 < self.size:
                        self.grid[room.left - 1][j] = "#"  # Mark left of left edge
                    if 0 <= room.right + 1 < self.size:
                        self.grid[room.right + 1][j] = "#"  # Mark right of right edge



    def get_room_centers(self):
        centers=[]
        for room in self.rooms:
            centers.append(room.get_center())
        return centers

    def get_random_point_in_ellipse(self, ellipse_height):
        angle = random.uniform(0, 2*math.pi)
        x_distance = (self.size//2-self.room_length) * math.sqrt(random.uniform(0,1))
        y_distance = (self.size//2-ellipse_height) * math.sqrt(random.uniform(0,1))

        x=x_distance*math.cos(angle)
        y=y_distance*math.sin(angle)
        
        return (int(x + (self.size//2)),int(y + self.size//2))        


        
    def get_closest_side_midpoints(self, room1, room2):
        # Get the midpoints of each side for both rooms
        room1_sides = room1.get_side_midpoints()
        room2_sides = room2.get_side_midpoints()
        
        # Initialize variables to keep track of the closest pair of midpoints
        min_distance = float('inf')
        closest_midpoints = (None, None)
        
        # Iterate over each side midpoint of room1 and room2
        for side1, midpoint1 in room1_sides.items():
            for side2, midpoint2 in room2_sides.items():
                # Calculate the distance between the midpoints
                distance = math.dist(midpoint1, midpoint2)
                
                # Update the closest pair if the current distance is shorter
                if distance < min_distance:
                    min_distance = distance
                    closest_midpoints = (midpoint1, midpoint2)
        
        # Return the pair of midpoints with the shortest distance
        return closest_midpoints
    
        


    def central(self):
        center_left = self.center_x - self.room_length
        center_right = self.center_x + self.room_length
        center_top = self.center_y - self.room_length
        center_bottom = self.center_y + self.room_length
        for i in range(center_left, center_right):
                for j in range(center_top, center_bottom):
                    self.grid[i][j] = "c"


    def initialise_rooms(self):
        roomTypes = [1,1,1,1,2,2,3]
        self.central()
        centralRoom = Room(self.center_x, self.center_y, self.room_length*2, self.room_width*2,0)
        self.rooms.append(centralRoom)
        max_attempts = 50  # Limit the number of placement attempts to avoid infinite loops
        for i in range(self.num_rooms):
            attempts = 0
            while attempts < max_attempts:
                # Get a random position in the ellipse for the new room's center
                x, y = self.get_random_point_in_ellipse(self.size // 8)
                if i < 7:
                    new_room = Room(x, y, self.room_length, self.room_width, roomTypes[i])
                else:
                    new_room = Room(x, y, self.room_length, self.room_width, 0)
                
                # Check if the new room overlaps any existing room
                overlap = False
                for room in self.rooms:
                    if new_room.intersects(room):
                        overlap = True
                        break
                
                # If no overlap is found, add the room to the list and exit the loop
                if not overlap:
                    self.rooms.append(new_room)
                    break
                
                # Increment attempts if there was an overlap
                attempts += 1
                if attempts == max_attempts:
                    print("Failed to place a room without overlap. Consider increasing map size or reducing room count.")
        
        self.check_room_boundaries()    
        
    
    def add_rooms(self):
        for room in self.rooms:
            for i in range(room.left, room.right):
                for j in range(room.top, room.bottom):
                    random_number = random.randint(0,3)
                    self.grid[i][j] = self.floorTiles[random_number]
            if room.type == 0: # Chest / Atrium
                self.grid[room.x][room.y] = "t"
            elif room.type == 1: # TOT
                self.grid[room.x][room.y] = "t"
                self.grid[room.x-1][room.y] = "l"
                self.grid[room.x-1][room.y-1] = 'l'
                self.grid[room.x][room.y-1] = 'l'

                #horizontal parts
                for i in range(0,6):
                    self.grid[room.x-3][room.y-3+i] = 'l'
                    self.grid[room.x+2][room.y-3+i] = 'l'

                #vertical parts
                for i in range(0,4):
                    self.grid[room.x-2+i][room.y-3] = 'l'
                    self.grid[room.x-2+i][room.y+2] = 'l'
                
                i = random.randint(1,4)
                j = random.randint(1,4)
                if i == 1:
                    self.grid[room.x-3][room.y-3+j] = 'a'
                elif i == 2:
                    self.grid[room.x-3+j][room.y+2] = 'a'
                elif i == 3:
                    self.grid[room.x+2][room.y-3+j] = 'a'
                elif i == 4:
                    self.grid[room.x-3+j][room.y-3] = 'a'
            elif room.type == 2: # TT
                self.grid[room.x][room.y-2] = 'e'
                self.grid[room.x][room.y] = 'm'
                self.grid[room.x][room.y+2] = 'h'
            elif room.type == 3: # GG
                self.grid[room.x-1][room.y-1] = '1'
                self.grid[room.x-1][room.y] = '2'
                self.grid[room.x][room.y-1] = '3'
                self.grid[room.x][room.y] = '4'
            
    def get_room_centers(self):
        centers=[]
        for room in self.rooms:
            centers.append(room.get_center())
        return centers
            

    
    
    def bresenhams(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        if dx > dy:  # If the line is more horizontal than vertical
            err = dx / 2.0
            while x1 != x2:
                for i in range(2):  # Create a 2x2 block
                    for j in range(2):
                        if 0 <= x1 + i < self.size and 0 <= y1 + j < self.size:  # Ensure we are within grid boundaries
                            self.grid[x1 + i][y1 + j] = "p"  # Mark the path
                err -= dy
                if err < 0:
                    y1 += sy
                    err += dx
                x1 += sx

        else:  # If the line is more vertical than horizontal
            err = dy / 2.0
            while y1 != y2:
                for i in range(2):  # Create a 2x2 block
                    for j in range(2):
                        if 0 <= x1 + i < self.size and 0 <= y1 + j < self.size:  # Ensure we are within grid boundaries
                            self.grid[x1 + i][y1 + j] = "p"  # Mark the path
                err -= dx
                if err < 0:
                    x1 += sx
                    err += dy
                y1 += sy
        
        # Mark the last point with a 2x2 block
        for i in range(2):
            for j in range(2):
                if 0 <= x2 + i < self.size and 0 <= y2 + j < self.size:  # Ensure we are within grid boundaries
                    self.grid[x2 + i][y2 + j] = "p"  # Mark the path
    
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

    
    def connect_rooms(self,points):
        for pair in points:
            coords1 = pair[0]
            coords2 = pair[1]
            for room in self.rooms:
                if room.x == coords1[0] and room.y == coords1[1]:
                    node1 = room
                elif room.x == coords2[0] and room.y == coords2[1]:
                    node2 = room


            midpoint1, midpoint2 = self.get_closest_side_midpoints(node1, node2)

            if midpoint1[0] < midpoint2[0]:  # Rightward connection
                mid_x = midpoint1[0] + (midpoint2[0] - midpoint1[0]) // 2  # Midpoint in x
            else:  # Leftward connection
                mid_x = midpoint1[0] - (midpoint1[0] - midpoint2[0]) // 2 
            self.bresenhams(midpoint1, (mid_x, midpoint1[1]))  # Horizontal to mid_x
            self.bresenhams((mid_x, midpoint1[1]), (mid_x, midpoint2[1]))  # Vertical down/up to mid_y
            self.bresenhams((mid_x, midpoint2[1]), midpoint2)  # Horizontal to midpoint2

    def add_decor(self):
        safe=["a","b","c","d"]
        decors = ["u","v","w","x","y","z"]
        
        for room in self.rooms:
            for i in range(3):
                i = random.randint(room.left,room.right)
                j = random.randint(room.top,room.bottom)
                if self.grid[i][j] in safe:
                    self.grid[i][j] = random.choice(decors)
                    


def generate_map(array_size, num_rooms,room_length, room_width):
    myMap = Map(array_size,num_rooms,room_length,room_width)
    centralRoom = Room(myMap.center_x,myMap.center_y, myMap.size*2, myMap.size*2, 0)
    myMap.initialise_rooms()
    myMap.connect_rooms(myMap.MST())
    myMap.add_rooms()
    myMap.add_decor()
    #myMap.print_grid()
    
    return myMap

#Map.generate_map(empty array size, number of rooms, room length, room width)
generate_map(100,16,8,8) 