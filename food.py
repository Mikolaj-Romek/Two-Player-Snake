import random
import threading
from turtle import Turtle

class Food(Turtle):
    def __init__(self, snake1, snake2, semaphore, lock):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("magenta")
        self.speed("fastest")
        self.snake1 = snake1
        self.snake2 = snake2
        self.semaphore = semaphore
        self.lock = lock
        self.refresh_timer = None  # Timer for refreshing food
        self.refresh()

    def refresh(self):
        #Place food at a new random position not occupied by any snake.
        with self.lock:
            while True:
                new_x = random.randint(-280, 280)
                new_y = random.randint(-280, 280)

                # Ensure the new position is not occupied by any snake segment
                occupied = False
                for segment in self.snake1.segments + self.snake2.segments:
                    if segment.distance(new_x, new_y) < 20:
                        occupied = True
                        break

                if not occupied:
                    break

            self.goto(new_x, new_y)

        # Cancel the previous timer if it exists
        if self.refresh_timer is not None:
            self.refresh_timer.cancel()

        # Create a new timer for refreshing food after 3 seconds
        self.refresh_timer = threading.Timer(3.0, self.refresh)
        self.refresh_timer.start()

    def run(self):
        directionx = random.randint(-1, 1)
        directiony = random.randint(-1, 1)

        new_x = self.xcor() + 20 * directionx
        new_y = self.ycor() + 20 * directiony

        # Ensure the new position is within the screen boundaries
        if new_x > 280:
            new_x = 280
        elif new_x < -280:
            new_x = -280

        if new_y > 280:
            new_y = 280
        elif new_y < -280:
            new_y = -280

        # Check if the new position is not occupied by any snake segment
        occupied = False
        for segment in self.snake1.segments + self.snake2.segments:
            if segment.distance(new_x, new_y) < 10:
                occupied = True
                break

        if not occupied:
            self.goto(new_x, new_y)
        else:
            self.refresh()