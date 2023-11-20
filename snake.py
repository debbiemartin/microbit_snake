from microbit import * 
import random

class Snake(object):
    BRIGHTNESS = 5
    
    def __init__(self):
        self.coordinates = [(1, 2), (2, 2)]
        self.direction = (1, 0)        

    def turn_clockwise(self):
        # Clockwise: (1,0) -> (0,1) -> (-1,0) -> (0,-1)
        self.direction = (-1 * self.direction[1], self.direction[0])
    
    def turn_anticlockwise(self):
        # Anticlockwise: (1,0) -> (0,-1) -> (-1,0) -> (0,1)
        self.direction = (self.direction[1], -1 * self.direction[0])

    def plot(self):
        display.clear()
        for coordinate in self.coordinates:
            display.set_pixel(coordinate[0], coordinate[1], self.BRIGHTNESS)

    def next(self):
        if button_a.was_pressed():
            self.turn_clockwise()
        elif button_b.was_pressed():
            self.turn_anticlockwise()

        head = self.coordinates[-1]
        next = ((head[0] + self.direction[0]) % 5, (head[1] + self.direction[1]) % 5)
        return next
    
    def alive(self):
        return len(set(self.coordinates)) == len(self.coordinates)
            
    def grow(self, next):
        self.coordinates.append(next)

    def move(self, next):
        self.coordinates.append(next)
        self.coordinates.pop(0)

    def get_coordinates(self):
        return self.coordinates

class FoodManager(object):
    def __init__(self):
        self.food = None
        self.iterations_since_food = 0

    def manage_food(self, coordinates):
        """
        If there is already food present, don't create another. 
        If it has been 3 turns since either the start of the game
        or the last food eaten, create one at a pseudo-random location
        which does not coincide with any of the coordinates given in the
        argument.

        Arguments:
          coordinates: Coordinates at which food must not be plotted.
        """
        self.iterations_since_food += 1
        if self.food:
            return

        if self.iterations_since_food == 3:
            # Can't make a food which is in the snake's body
            food = None
            while not food or food in coordinates:
                food = (random.randint(0, 4), random.randint(0, 4))
                print(food)

            self.food = food

    def reset(self):
        self.food = None
        self.iterations_since_food = 0

    def plot(self):
        if not self.food:
            return
        display.set_pixel(self.food[0], self.food[1], 9)
    
score = 0
snake = Snake()
snake.plot()
food_mgr = FoodManager()

while snake.alive():
    next = snake.next()

    if food_mgr.food and food_mgr.food == next:
        snake.grow(next)
        food_mgr.reset()
        score += 1
    else:
        snake.move(next)

    food_mgr.manage_food(snake.get_coordinates())

    snake.plot()
    food_mgr.plot()

    sleep(1000) 

sleep(1000)
display.scroll("SCORE:")
display.scroll(score)
