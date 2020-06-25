from math import floor, sqrt
import sdl2
import sdl2.ext as sdl

SIZE = 20

def initiation(algorithm, data):
    '''initiate and return a window and renderer from the name of algorithm and maze data'''
    w = sdl.Window("%s simulation" %algorithm, (len(data[0]) * SIZE, len(data) * SIZE))
    r = sdl.Renderer(w)
    return w, r

class Simulation:
    white = sdl.Color(255, 255, 255, 0)
    black = sdl.Color(0, 0, 0, 0)
    red = sdl.Color(255, 0, 0, 0)

    def __init__(self, renderer, x, y, data):
        self.data = data
        self.widy = len(self.data[0])
        self.widx = len(self.data)
        self.r = renderer
        self.__y = x * SIZE
        self.__x = y * SIZE
    
    def __draw_square(self, x, y):
        '''draw a sqaure at given points'''
        for i in range(y, y + SIZE):
            self.r.draw_line((x, i, x + SIZE, i))

    def __rendercircle(self, xc, yc, r = int(SIZE / 2 - SIZE / 5)):
        '''function to draw circle of radius and XY coordinates'''
        xc, yc = int(xc), int(yc)
        for x in range(r): 
            y = floor(sqrt(r ** 2 - x ** 2))
            self.r.draw_line((xc + x, yc + y, xc + x, yc - y))
            self.r.draw_line((xc - x, yc + y, xc - x, yc - y))

    def __rendersprite(self):
        '''render a sprite which travels in the maze according to the path
        does not present the rendered sprite on window'''
        self.r.color = self.red
        self.__rendercircle(self.__x + SIZE / 2, self.__y + SIZE / 2)

    def build_maze(self):
        '''build maze in window
        does not present the rendered maze on window'''
        self.r.color = self.black
        for i in range(self.widx):
            for j in range(self.widy):
                if self.data[i][j] == 1:
                    self.__draw_square(j * SIZE, i * SIZE)
    
    # pylint: disable=no-self-argument, protected-access, not-callable 
    def renderfirst(fun):
        '''takes a yielding function which performs a certain rendering of
        the sprite in a direction and returns a wrapper over it
        which takes care of things like rendering maze, handling mouse click events,
        clearing and rendering the content of window etc'''
        def fullfun(self):
            self.__clear()
            for _ in fun(self):
                i = sdl2.SDL_GetTicks()
                self.build_maze()
                self.__rendersprite()
                events = sdl.get_events()
                for e in events:
                    if e.type == sdl2.SDL_QUIT:
                        return False
                self.__present()
                self.__clear()
                i = sdl2.SDL_GetTicks() - i
                if i < (1000 // 500):
                    sdl2.SDL_Delay(1000 // 500 - i)
            return True
        return fullfun

    @renderfirst
    def move_up(self):
        '''move the sprite up'''
        for _ in range(SIZE // 2):
            self.__y -= 2
            yield

    @renderfirst
    def move_down(self):
        '''move the sprite down'''
        for _ in range(SIZE // 2):
            self.__y += 2
            yield

    @renderfirst
    def move_right(self):
        '''move the sprite right'''
        for _ in range(SIZE // 2):
            self.__x += 2
            yield

    @renderfirst
    def move_left(self):
        '''move the sprite left'''
        for _ in range(SIZE // 2):
            self.__x -= 2
            yield

    def __clear(self):
        self.r.clear(self.white)

    def __present(self):
        self.r.present()

ACTION = {
    'up': Simulation.move_up,
    'down': Simulation.move_down,
    'right': Simulation.move_right,
    'left': Simulation.move_left
} 

def run_simulation(name, path, maze, continuous = False):
    '''run a simulation of sprite going through the maze 
    parameters:
    name :          name of the algorithm to be displayed on window
    path :          the path returned by the algorithm
    startstate :    the starting state of the maze
    data :          the maze matrix (containing 0s and 1s)
    continuos :     True if click is not necessary for next move else False'''
    startstate, data = maze.startstate, maze.data
    w, r = initiation(name, data)
    run = True
    way = iter(path)
    w.show()
    s = Simulation(r, *startstate, data)
    nextitem = True
    while True:
        events = sdl.get_events()
        for e in events:
            if e.type == sdl2.SDL_QUIT:
                run = False
                break
            elif e.type == sdl2.SDL_MOUSEBUTTONDOWN or e.type == sdl2.SDL_KEYDOWN:
                nextitem = True
        if not run:
            break
        if nextitem:
            try:
                direction = next(way)
            except StopIteration:
                run = False
                break
            if direction == "end":
                nextitem = False
            elif direction == "start":
                pass
            else:
                run = ACTION[direction](s)
        if not continuous:
            nextitem = False
    w.hide()
