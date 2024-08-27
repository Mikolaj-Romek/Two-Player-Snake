import time
import threading
from turtle import Screen
from snake import Snake
from food import Food
import random

def random_central_start_position():

    return random.randint(-100, 100), random.randint(-100, 100)

# Initialize screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# Initialize snakes in central positions
snake1 = Snake(random_central_start_position(), colour="red")
snake2 = Snake(random_central_start_position(), colour="blue")

screen.listen()
screen.onkey(snake1.up, "Up")
screen.onkey(snake1.down, "Down")
screen.onkey(snake1.left, "Left")
screen.onkey(snake1.right, "Right")

screen.onkey(snake2.up, "w")
screen.onkey(snake2.down, "s")
screen.onkey(snake2.left, "a")
screen.onkey(snake2.right, "d")

# Mutexes and Semaphores
screen_update_lock = threading.Lock()
food_lock = threading.Lock()
food_semaphore = threading.Semaphore(1)  # Only one snake can eat the food at a time

# Create initial food
food = Food(snake1, snake2, food_semaphore, food_lock)
food1 = Food(snake1, snake2, food_semaphore, food_lock)

# Global game state variable
game_is_on = True

# Functions to handle snake movement in separate threads
def snake1_movement():
    while game_is_on:
        screen_update_lock.acquire()
        snake1.move()
        screen_update_lock.release()
        time.sleep(0.1)

def snake2_movement():
    while game_is_on:
        screen_update_lock.acquire()
        snake2.move()
        screen_update_lock.release()
        time.sleep(0.1)


def check_collisions():
    global game_is_on

    def check_wall_collision(snake):
        return (
            snake.head.xcor() > 280
            or snake.head.xcor() < -280
            or snake.head.ycor() > 280
            or snake.head.ycor() < -280
        )

    def check_tail_collision(snake):
        return any(snake.head.distance(segment) < 10 for segment in snake.segments[1:])

    def reset_snakes():
        snake1.reset()
        snake2.reset()

    while game_is_on:
        screen_update_lock.acquire()
        screen.update()

        with food_semaphore:
            if snake1.head.distance(food) < 20:
                food.refresh()
                snake1.extend()

            if snake2.head.distance(food) < 20:
                food.refresh()
                snake2.extend()

        with food_semaphore:
            if snake1.head.distance(food1) < 20:
                food1.refresh()
                snake1.extend()

            if snake2.head.distance(food1) < 20:
                food1.refresh()
                snake2.extend()

        # Check for wall collisions
        if check_wall_collision(snake1) or check_tail_collision(snake1):
            snake1.reset()

        if check_wall_collision(snake2) or check_tail_collision(snake2):
            snake2.reset()

        # Check for head-to-head collision
        if snake1.head.distance(snake2.head) < 10:
            reset_snakes()

        # Check for snake1 colliding with snake2's body
        if any(snake1.head.distance(segment) < 10 for segment in snake2.segments[1:]):
            snake1.reset()

        # Check for snake2 colliding with snake1's body
        if any(snake2.head.distance(segment) < 10 for segment in snake1.segments[1:]):
            snake2.reset()

        screen_update_lock.release()
        time.sleep(0.1)

# Function to create new food every 0.5 seconds and refresh every 3 seconds
def create_new_food():
    global game_is_on
    food.refresh_timer = threading.Timer(3.0, food.refresh)
    food.refresh_timer.start()
    while game_is_on:
        time.sleep(0.5)
        with food_lock:
            food1.run()


# Start the threads
collision_thread = threading.Thread(target=check_collisions)
food_thread = threading.Thread(target=create_new_food)
snake1_thread = threading.Thread(target=snake1_movement)
snake2_thread = threading.Thread(target=snake2_movement)

collision_thread.start()
food_thread.start()
snake1_thread.start()
snake2_thread.start()

screen.exitonclick()