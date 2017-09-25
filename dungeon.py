from random import randrange
#Dungeon internal model
class layout:
    def genMap(self, rows, cols, attempts):
        self.xLim = cols
        self.yLim = rows #2d array size
        print self.yLim
        self.roomAttempts = attempts
        #init this to "#" for all walls to begin with
        self.cMap = [['#' for y in range(cols)] for x in range(rows)]
        #Create random starting room in the middle of the map
        l,w = self.sizeRoom()
        self.fillRect(self.xLim // 2, self.yLim // 2, l, w, '.')

        #loop until limit of rooms tried is reached
        while (self.roomAttempts > 0):
            x_wall,y_wall,direction = self.pickWall()
            l,w = self.selectRoom()
            valid_room = self.isValid(x_wall, y_wall, w, l, direction)
            if valid_room:
                self.placeRoom(x_wall, y_wall, w, l, direction)
            self.roomAttempts -= 1

    #Fills a rectangle x by y with specified starting location
    # traveling from upper left corner
    def fillRect(self, x_pos, y_pos, x_size, y_size, char):
        for y in range(y_size):
            for x in range(x_size):
                self.cMap[y_pos + y][x_pos + x] = char

    #randomly sizes a room within hardcoded limits
    def sizeRoom(self):
        length = randrange(2, 7)
        width = randrange(2, 5) #36 tiles upper limit
        return length, width

    #randomly chooses points until one is a wall (adj. to floor)
    # return coordinates of successful point and direction of wall(1-4, N-W)
    def pickWall(self):
        while True:
            x_rand = randrange(1, self.xLim - 1)
            y_rand = randrange(1, self.yLim - 1)
            if self.cMap[y_rand][x_rand] == '#':
                if self.cMap[y_rand - 1][x_rand] == '.':
                    return x_rand, y_rand, 3 #south
                elif self.cMap[y_rand +1][x_rand] == '.':
                    return x_rand, y_rand, 1 #north
                elif self.cMap[y_rand][x_rand -1] == '.':
                    return x_rand, y_rand, 2 #east
                elif self.cMap[y_rand][x_rand + 1] == '.':
                    return x_rand, y_rand, 4 #west

    #Choose size and type of room to build next at weighted random odds
    #(currently 33% room, 33% vertical hallway, 33% horizontal hallway)
    def selectRoom(self):
        rand_type = randrange(3)
        if rand_type == 0: #build room
            l, w = self.sizeRoom()
            return l, w
        elif rand_type == 1: #build hori hall (width = 1)
            w = 1
            l = randrange(3, 10)
            return l,w
        else: #build vert hall (length = 1)
            l = 1
            w = randrange(3, 8)
            return l, w

    #Check if there is room to add the selected room in the space
    #scanning outward from wall location, if not, cancel
    def isValid(self, x_wall, y_wall, x_scan, y_scan, direction):
        #Note: check extra one tile further to ensure a wall in between rooms
        if direction == 1: #north wall scans -y +x
            for y in range(y_scan + 1):
                for x in range(x_scan + 1):
                    if (y_wall - y < 1 or x_wall + x >= self.xLim
                        or self.cMap[y_wall - y][x_wall + x] == '.'):
                        return False
        elif direction == 2: #east wall scans +x +y
            for y in range(y_scan + 1):
                for x in range(x_scan + 1):
                    if (y_wall + y + 1>= self.yLim or x_wall + x >= self.xLim 
                        or self.cMap[y_wall + y][x_wall + x] == '.'):
                        return False
        elif direction == 3: #south wall scans +y -x
            for y in range(y_scan + 1):
                for x in range(x_scan + 1):
                    if (y_wall + y + 1>= self.yLim or x_wall - x < 1
                        or self.cMap[y_wall + y][x_wall - x] == '.'):
                        return False
        elif direction == 4: #west wall scans -x -y
            for y in range(y_scan + 1):
                for x in range(x_scan + 1):
                    if (y_wall - y < 1 or x_wall - x < 1 
                        or self.cMap[y_wall - y][x_wall - x] == '.'):
                        return False
        return True

    #Modifies the layout to include the new room
    def placeRoom(self, x_wall, y_wall, x_size, y_size, direction):
        self.cMap[y_wall][x_wall] = '+' #+ for door
        if direction == 1:
            self.fillRect(x_wall, y_wall - y_size, x_size, y_size, '.')
        elif direction == 2:
            self.fillRect(x_wall + 1, y_wall, x_size, y_size, '.')
        elif direction == 3:
            self.fillRect(x_wall - x_size + 1, y_wall + 1, x_size, y_size, '.')
        elif direction == 4:
            self.fillRect(x_wall - x_size, y_wall - y_size + 1, x_size, y_size, '.')

#Main
def main():
    init_x = 80
    init_y = 50
    roomAttempts = 100
    dungeon = layout()
    dungeon.genMap(init_y, init_x, roomAttempts)
    for y in range(init_y):
        line = ""
        for x in range(init_x):
            if dungeon.cMap[y][x] == '#':
                if y == 0 or y == dungeon.yLim - 1 or x == 0 or x == dungeon.xLim -1:
                    line += '#'
                elif (dungeon.cMap[y-1][x] == '#' and dungeon.cMap[y+1][x] == '#' 
                      and dungeon.cMap[y][x-1] == '#' and dungeon.cMap[y][x+1] == '#'
                      and dungeon.cMap[y-1][x-1] == '#' and dungeon.cMap[y-1][x+1] == '#'
                      and dungeon.cMap[y+1][x-1] == '#' and dungeon.cMap[y+1][x+1] == '#'):
                    line += ' '
                else:
                    line += '#'
            else:
                line += dungeon.cMap[y][x]
        print (line)

if __name__ == "__main__":
    main()
