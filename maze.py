import sys

class Laser:
    '''A laser has the following properties: 
    curr_loc: current location
    curr_dirc: current direction
    maze: the maze the laser is traversing in
    '''
    def __init__(self, curr_loc, curr_dirc, maze):
        '''initiate a laser object with respective location, direction and maze'''
        self.curr_dirc = curr_dirc
        self.curr_loc = curr_loc
        self.maze = maze

    def newLaserDirection(self, mirror_position):
        '''identify the new laser direction based on mirror position and current laser direction'''
        
        if self.curr_dirc == "N":
            if mirror_position == "/":
                self.curr_dirc = "E"
            else:
                self.curr_dirc = "W"
        elif self.curr_dirc == "S":
            if mirror_position == "/":
                self.curr_dirc = "W"
            else:
                self.curr_dirc = "E"
        elif self.curr_dirc == "E":
            if mirror_position == "/":
                self.curr_dirc = "N"
            else:
                self.curr_dirc = "S"
        elif self.curr_dirc == "W":
            if mirror_position == "/":
                self.curr_dirc = "S"
            else:
                self.curr_dirc = "N"

    def findClosestMirror(self):
        '''find the closest mirror based on laser location and direction, plus potential mirrors in the maze'''

        next_mirror = []

        #if the laser is moving North, check all mirrors share the same x but have bigger y as the current position
        if self.curr_dirc == "N":
            potential_mirrors = [mirror for mirror in self.maze.mirrors if mirror[0] == self.curr_loc[0] and mirror[1] > self.curr_loc[1]]
            if potential_mirrors != []:
                min_y = min([mirror[1] for mirror in potential_mirrors])
                next_mirror = list([mirror for mirror in potential_mirrors if mirror[1] == min_y][0])

        #if the laser is moving South, check all mirrors share the same x but have smaller y as the current position
        elif self.curr_dirc == "S":
            potential_mirrors = [mirror for mirror in self.maze.mirrors if mirror[0] == self.curr_loc[0] and mirror[1] < self.curr_loc[1]]
            if potential_mirrors != []:
                max_y = max([mirror[1] for mirror in potential_mirrors])
                next_mirror = list([mirror for mirror in potential_mirrors if mirror[1] == max_y][0])

        #if the laser is moving East, check all mirrors share the same y but have bigger x as the current position    
        elif self.curr_dirc == "E":
            potential_mirrors = [mirror for mirror in self.maze.mirrors if mirror[1] == self.curr_loc[1] and mirror[0] > self.curr_loc[0]]
            if potential_mirrors != []:
                min_x = min([mirror[0] for mirror in potential_mirrors])
                next_mirror = list([mirror for mirror in potential_mirrors if mirror[0] == min_x][0])

        #if the laser is moving West, check all mirrors share the same y but have smaller x as the current position
        elif self.curr_dirc == "W":
            potential_mirrors = [mirror for mirror in self.maze.mirrors if mirror[1] == self.curr_loc[1] and mirror[0] < self.curr_loc[0]]
            if potential_mirrors != []:
                max_x = max([mirror[0] for mirror in potential_mirrors])
                next_mirror = list([mirror for mirror in potential_mirrors if mirror[0] == max_x][0])
        return next_mirror

    def findFinalLocation(self):
        '''If no mirrors are identified in the laser direction, find the final locaiton on the wall'''
        if self.curr_dirc == "N":
            return [self.curr_loc[0], self.maze.height - 1]
        elif self.curr_dirc == "S":
            return [self.curr_loc[0], 0]
        elif self.curr_dirc == "E":
            return [self.maze.width - 1, self.curr_loc[1]]
        elif self.curr_dirc == "W":
            return [0, self.curr_loc[1]] 

class Maze:
    '''An maze has the following properties:
    width: the width of the maze
    height: the height of the maze
    mirrors: if any mirrors exisit, it stores their locaiton and facing position
    '''
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mirrors = []

    def setDimension(self, dimension):
        self.width = dimension[0]
        self.height = dimension[1]

    def addMirror(self, mirror):
        self.mirrors.append(mirror)

def parseInput(infile):
    '''parse the informaiton from the input text, including maze dimension, laser intial informaiton (locaiton and direction), mirror informaiton'''
    input_file = open(infile, "r")

    maze = Maze()

    for line in input_file:
        elements = line.strip().split()
        if len(elements) == 2:
            maze.setDimension(list(map(int,elements)))
        elif len(elements) == 3:
            if elements[2] in ['W','E','S','N']:
                laser = Laser(list(map(int,elements[:2])), elements[2], maze)
            else:
                mirror = list(map(int,elements[:2]))
                mirror.extend(elements[2])
                maze.addMirror(mirror)

    input_file.close()

    return maze, laser

def traverseMaze(maze, laser):
    '''calcaulted the number of squares the laser traversed and find the last location of the laser if it hits a wall'''
    
    sq_traversed = 0
    
    #store all mirrors visited
    mirrors_visited = {}

    next_mirror = laser.findClosestMirror()

    #print(next_mirror)

    while next_mirror != []:

        previous_location = laser.curr_loc

        #if the laser visits the same mirror in the same direction, it indicates the laser has been travelling in a loop.
        #return -1 for the squares traversed count and break out of the loop
        next_mirror.append(laser.curr_dirc)

        if tuple(next_mirror) in mirrors_visited:
            sq_traversed = -1
            break
        else:
            mirrors_visited[tuple(next_mirror)] = 1
        
        laser.curr_loc = next_mirror[:2]

        laser.newLaserDirection(next_mirror[2])

        sq_traversed += abs(sum([a_i - b_i for a_i, b_i in zip(previous_location, laser.curr_loc)]))

        next_mirror = laser.findClosestMirror()

    if sq_traversed != -1:

        #add the last segment of squares laser traveled
        final_location = laser.findFinalLocation()

        #print(final_location,laser.curr_loc)
        sq_traversed += abs(sum([a_i - b_i for a_i, b_i in zip(laser.curr_loc, final_location)]))
        
        return sq_traversed, final_location

    else:
        return sq_traversed, "NA"
        
    #if needed, one can also return all mirrors visited by simply print out mirrors_visited
    #alternatively, if one wants to record the path of the laser, one can use a list of lists to record the mirrors visited instead of a dictionary.


def main():
    
    maze, laser = parseInput(sys.argv[1])

    #output the number of the mirrors travsered and last location (it will be NA if the laser is trapped in a loop)
    sq_traversed, final_location = traverseMaze(maze, laser)

    output_file = open(sys.argv[2],"w")

    output_file.write(str(sq_traversed)+"\n")

    if sq_traversed > 0:
        output_file.write(" ".join(map(str, final_location)))
        output_file.close()


if __name__ == '__main__':
    main()
