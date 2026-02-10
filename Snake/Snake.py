import pygame
import random
import math
import os
pygame.font.init()

WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "snake.png")
BG = pygame.transform.scale(pygame.image.load(image_path),
                            (WIDTH, HEIGHT))
# BG_TWO = pygame.transform.scale(pygame.image.load("Python\pyGame\Snake\Medien.png"),
#                         (WIDTH, HEIGHT))

SNAKE_SIZE = 10
SNAKE_VEL = 5
SNAKE_FRAMES_PER_MOVE = 6

APPLE_SIZE = 10

class Apple:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.apple = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def set_position(self):
        self.x = random.randint(1, WIDTH//10) * 10
        self.y = random.randint(1, HEIGHT//10) * 10
        
        self.apple = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, win):
        pygame.draw.rect(win, "red", self.apple)
        
    def eaten(self, player_rect):
        if player_rect.colliderect(self.apple):
            return True
        return False
    
class Snake:
    def __init__(self, x, y, segment_size, initial_length = 3):
        self.segment_size = segment_size
        self.body = []
        self.direction = "right"
        
        for i in range(initial_length):
            self.body.insert(0, pygame.Rect(x-i * self.segment_size, y, self.segment_size, self.segment_size))
        
        self.body[0] = pygame.Rect(x, y, segment_size, segment_size)
    
    def move(self):
        head_x, head_y = self.body[0].topleft
        # self.delay = 0
        new_head_x, new_head_y = head_x, head_y
        if self.direction == "up":
            # pygame.time.wait(self.delay)
            new_head_y -= self.segment_size
        elif self.direction == "down":
            # pygame.time.wait(self.delay)
            new_head_y += self.segment_size
        elif self.direction == "left":
            # pygame.time.wait(self.delay)
            new_head_x -= self.segment_size
        elif self.direction == "right":
            # pygame.time.wait(self.delay)
            new_head_x += self.segment_size
            
        new_head_rect = pygame.Rect(new_head_x, new_head_y, self.segment_size, self.segment_size)
        
        self.body.insert(0, new_head_rect)
        
    def change_direction(self, new_direction):
        if (new_direction == "up" and self.direction != "down") or \
           (new_direction == "down" and self.direction != "up") or \
           (new_direction == "left" and self.direction != "right") or \
           (new_direction == "right" and self.direction != "left"):
            self.direction = new_direction
            
    def get_head_rect(self):
        return self.body[0]
        
    def check_collision_wall(self, game_width, game_height):
        head = self.get_head_rect()
        return (head.left < 0 or head.right > game_width or
                head.top < 0 or head.bottom > game_height)
        
    def check_collision_self(self):
        head = self.get_head_rect()
        for segment in self.body[1:]:
            if head.colliderect(segment):
                return True
        return False
    
    def draw(self, win):
        for i, segment in enumerate(self.body):
            if i == 0:
                pygame.draw.rect(win, "darkblue", segment)
            else:
                pygame.draw.rect(win, "blue", segment)
    
FONT = pygame.font.SysFont("Arial", 30)

def draw(snake, current_apple):
    # if apple_score > 10:
    #     WIN.blit(BG_TWO, (0, 0))
    # else:
    WIN.blit(BG, (0, 0))
        
    snake.draw(WIN)
    
    current_apple.draw(WIN)
    
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    
    initial_snake_x = (WIDTH // 2 // SNAKE_SIZE) * SNAKE_SIZE
    initial_snake_y = (HEIGHT // 2 // SNAKE_SIZE) * SNAKE_SIZE
    
    snake = Snake(initial_snake_x, initial_snake_y, SNAKE_SIZE)
    frame_counter = 0

    current_apple = Apple(random.randint(APPLE_SIZE, WIDTH-APPLE_SIZE), random.randint(APPLE_SIZE, WIDTH-APPLE_SIZE),
                              APPLE_SIZE, APPLE_SIZE)
    apple_score = 0
    hit = False
    
    
    while run:
        clock.tick(60)
        frame_counter += 1
        
        if frame_counter >= SNAKE_FRAMES_PER_MOVE:
            frame_counter = 0
            
            snake.move()
                
            if current_apple.eaten(snake.get_head_rect()):
                apple_score += 1
                current_apple.set_position()
            else:
                snake.body.pop()
                
            if snake.check_collision_wall(WIDTH, HEIGHT) or snake.check_collision_self():
                hit = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    snake.change_direction("up")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    snake.change_direction("down")
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    snake.change_direction("left")
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    snake.change_direction("right")

        
        
        if hit:
            lost_text = FONT.render("You lose!", 1, "red")
            WIN.blit(lost_text, (WIDTH//2-lost_text.get_width()//2, HEIGHT//2-lost_text.get_height()//2))
            apple_score = FONT.render(f"Your score: {apple_score}", 1, "red")
            WIN.blit(apple_score, (WIDTH//2-lost_text.get_width()//2, ((HEIGHT//2-lost_text.get_height()//2)) + 30))
            pygame.display.update()
            pygame.time.delay(3000)
            break
        
        if not hit:
            draw(snake, current_apple)
    
    pygame.quit()

if __name__ == "__main__":
    main()   


        
        