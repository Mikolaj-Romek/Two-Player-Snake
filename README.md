Snake

The project presents a simplified version of the Snake game in a multiplayer mode using threads, mutexes, and semaphores for learning purposes. The game involves controlling two snakes, each controlled by a different player, with the goal of earning as many points as possible by eating the food that appears on the screen. The movements of the snakes and their interactions are managed concurrently using threads, and critical sections are protected by synchronization mechanisms to ensure correct game state management.


Use of Threads:

snake1/2_thread: Threads responsible for moving the snakes.
collisions_thread: Checks for collisions between snakes, screen boundaries, food, and themselves; resets snakes after a collision.
food_thread: Generates new food on the screen and randomly moves the food around.
Critical Sections:

Mutex screen_update_lock: Only one thread at a time can update the game board by drawing new snake positions.
Mutex food_lock: Only one thread at a time can create new food on the board.
Semaphore food_semaphore: Only one snake at a time can eat a food pellet and grow longer.
