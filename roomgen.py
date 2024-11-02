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

    import math

    def get_closest_side_midpoints(self, room1, room2):
        # Get the side midpoints
        room1_sides = room1.get_side_midpoints()
        room2_sides = room2.get_side_midpoints()
        
        # Determine the direction from room1 to room2
        dx = room2.x - room1.x
        dy = room2.y - room1.y

        angle_rad = math.atan2(dy, dx)
        if angle_rad < 0:
            angle_rad += 2 * math.pi

        if 0 <= angle_rad < math.pi / 8:
            return room1_sides["right"], room2_sides["left"]
        
        elif math.pi / 8 <= angle_rad < math.pi / 4:
            return room1_sides["right"], room2_sides["bottom"]
        
        elif math.pi / 4 <= angle_rad < 3 * math.pi / 8:
            return room1_sides["top"], room2_sides["left"]

        elif 3 * math.pi / 8 <= angle_rad < math.pi / 2:
            return room1_sides["top"], room2_sides["bottom"]

        elif math.pi / 2 < angle_rad < 5 * math.pi / 8:
            return room1_sides["top"], room2_sides["bottom"]

        elif 5 * math.pi / 8 <= angle_rad < 3 * math.pi / 4:
            return room1_sides["top"], room2_sides["right"]

        elif 3 * math.pi / 4 <= angle_rad < 7 * math.pi / 8:
            return room1_sides["left"], room2_sides["bottom"]

        elif 7 * math.pi / 8 <= angle_rad < math.pi:
            return room1_sides["left"], room2_sides["right"]

        elif math.pi<= angle_rad <9* math.pi / 8:
            return room1_sides["left"], room2_sides["right"]
        elif 9* math.pi/ 8<= angle_rad <5* math.pi /4 :
            return room1_sides["left"], room2_sides["top"]
        elif 5*math.pi/ 4<= angle_rad <11* math.pi /8 :
            return room1_sides["bottom"], room2_sides["right"]
        elif 11* math.pi/ 8<= angle_rad <6* math.pi /4 :
            return room1_sides["bottom"], room2_sides["top"]
        elif 12* math.pi/ 8<= angle_rad <13* math.pi /8 :
            return room1_sides["bottom"], room2_sides["top"]
        elif 13* math.pi/ 8<= angle_rad <14* math.pi /8 :
            return room1_sides["bottom"], room2_sides["left"]
        elif 14* math.pi/ 8<= angle_rad <15* math.pi /8 :
            return room1_sides["right"], room2_sides["top"]
        elif 15* math.pi/ 8<= angle_rad <16* math.pi /4 :
            return room1_sides["right"], room2_sides["left"]



    def central(self):
        center_left = self.center_x - self.room_length
        center_right = self.center_x + self.room_length
        center_top = self.center_y - self.room_length
        center_bottom = self.center_y + self.room_length
        for i in range(center_left, center_right):
                for j in range(center_top, center_bottom):
                    self.grid[i][j] = "c"


    def initialise_rooms(self):
        self.central()
        centralRoom = Room(self.center_x, self.center_y, self.room_length*2, self.room_width*2)
        self.rooms.append(centralRoom)
        max_attempts = 50  # Limit the number of placement attempts to avoid infinite loops
        for _ in range(self.num_rooms):
            attempts = 0
            while attempts < max_attempts:
                # Get a random position in the ellipse for the new room's center
                x, y = self.get_random_point_in_ellipse(self.size // 8)
                new_room = Room(x, y, self.room_length, self.room_width)
                
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
                    floorTiles = ["a","b","c","d"]
                    random_number = random.randint(0,3)
                    self.grid[i][j] = floorTiles[random_number]
            
    def get_room_centers(self):
        centers=[]
        for room in self.rooms:
            centers.append(room.get_center())
        return centers
            

    def bresenhams(self,node1,node2):
        x1 = node1[0]
        x2  =node2[0]        
        y1 = node1[1]
        y2 = node2[1]
        
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

    # def bresenhams(self, node1, node2):
    #     x1, y1 = node1
    #     x2, y2 = node2
        
    #     if x1 == x2:  # Vertical connection
    #         for y in range(min(y1, y2) - 1, max(y1, y2) + 2):  # Extend range to create a 3x3 vertical path
    #             for x_offset in range(-1, 2):  # Create a 3x3 block
    #                 if 0 <= x1 + x_offset < self.size and 0 <= y < self.size:  # Ensure we are within grid boundaries
    #                     self.grid[x1 + x_offset][y] = "b"
    #     elif y1 == y2:  # Horizontal connection
    #         for x in range(min(x1, x2) - 1, max(x1, x2) + 2):  # Extend range to create a 3x3 horizontal path
    #             for y_offset in range(-1, 2):  # Create a 3x3 block
    #                 if 0 <= x < self.size and 0 <= y1 + y_offset < self.size:  # Ensure we are within grid boundaries
    #                     self.grid[x][y1 + y_offset] = "b"
    #     else:  # L-shaped connection
    #         # Horizontal first
    #         for x in range(x1, x2 + 1) if x1 < x2 else range(x1, x2 - 1, -1):
    #             for y_offset in range(-1, 2):  # Create a 3x3 block
    #                 if 0 <= x < self.size and 0 <= y1 + y_offset < self.size:  # Ensure we are within grid boundaries
    #                     self.grid[x][y1 + y_offset] = "b"
    #         # Then vertical
    #         for y in range(y1, y2 + 1) if y1 < y2 else range(y1, y2 - 1, -1):
    #             for x_offset in range(-1, 2):  # Create a 3x3 block
    #                 if 0 <= x2 + x_offset < self.size and 0 <= y < self.size:  # Ensure we are within grid boundaries
    #                     self.grid[x2 + x_offset][y] = "b"

    def bresenhams(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        if dx > dy:  # If the line is more horizontal than vertical
            err = dx / 2.0
            while x1 != x2 and y1!="a":
                if 0 <= x1 < self.size and 0 <= y1 < self.size:  # Ensure we are within grid boundaries
                    self.grid[x1][y1] = "b"  # Mark the path
                err -= dy
                if err < 0:
                    y1 += sy
                    err += dx
                x1 += sx
            if 0 <= x2 < self.size and 0 <= y2 < self.size:  # Mark the last point
                self.grid[x2][y2] = "b"
        else:  # If the line is more vertical than horizontal
            err = dy / 2.0
            while y1 != y2 and x1!="a":
                if 0 <= x1 < self.size and 0 <= y1 < self.size:  # Ensure we are within grid boundaries
                    self.grid[x1][y1] = "b"  # Mark the path
                err -= dx
                if err < 0:
                    x1 += sx
                    err += dy
                y1 += sy
            if 0 <= x2 < self.size and 0 <= y2 < self.size:  # Mark the last point
                self.grid[x2][y2] = "b"
        
    
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


def generate_map(array_size, num_rooms,room_length, room_width):
    myMap = Map(array_size,num_rooms,room_length,room_width)
    centralRoom = Room(myMap.center_x,myMap.center_y, myMap.size*2, myMap.size*2)
    myMap.initialise_rooms()
    myMap.add_rooms()
    myMap.connect_rooms(myMap.MST())
    return myMap

#Map.generate_map(empty array size, number of rooms, room length, room width)
#Map.generate_map(100,16,8,8) 
