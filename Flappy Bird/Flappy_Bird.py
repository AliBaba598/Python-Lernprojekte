import pygame
import math
import random
import time
import os
pygame.font.init()


WIDTH, HEIGHT=600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BG = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "Background.jpeg")), (WIDTH, HEIGHT))

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40

PLAYER_VEL = -40
PLAYER_GRAVITY = 2

PIPE_WIDTH = 100
PIPE_GAP = 200
PIPE_VEL = 2
PIPE_SPAWN_INTERVAL = 3000

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.upper_rect = None
        self.low_rect = None
        self.passed = False

        self.set_height()
    
    def set_height(self):
        min_upper_y = 100
        max_upper_y = HEIGHT - PIPE_GAP - min_upper_y
        
        self.height = random.randint(min_upper_y, max_upper_y)
        
        self.upper_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.lower_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP))

    def move(self):
        self.x -= PIPE_VEL
        self.upper_rect.x = self.x
        self.lower_rect.x = self.x
    
    def draw(self, win):
        pygame.draw.rect(win, "green", self.upper_rect)
        pygame.draw.rect(win, "green", self.lower_rect)
    
    def collide(self, player_rect):
        if player_rect.colliderect(self.upper_rect) or player_rect.colliderect(self.lower_rect):
            return True
        return False

FONT = pygame.font.SysFont("Arial", 30)

def draw(player, pipe_score, pipes):
    WIN.blit(BG, (0, 0))
    
    pipe_score_text = FONT.render(f"Score: {round(pipe_score)}", 1, "black")
    WIN.blit(pipe_score_text, (10, 10))
    
    pygame.draw.rect(WIN, "yellow", player)
    
    for pipe in pipes:
        pipe.draw(WIN)
    
    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(WIDTH//2-PLAYER_WIDTH//2, HEIGHT//2-PLAYER_HEIGHT//2, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    
    space_pressed_this_cycle = False
    
    clock = pygame.time.Clock()
    
    pipes = []
    last_pipe_time = pygame.time.get_ticks()

    pipe_score = 0
    
    hit = False
    
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False   
                break

        player.y += PLAYER_GRAVITY
        if player.y + PLAYER_HEIGHT > HEIGHT:
            player.y = HEIGHT - PLAYER_HEIGHT

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player.y - PLAYER_HEIGHT >= 0:
            if not space_pressed_this_cycle:
                player.y += PLAYER_VEL
                space_pressed_this_cycle = True
        else:
            space_pressed_this_cycle = False

        if player.y < 0:
            player.y = 0
        
        # Pipe_vel
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > PIPE_SPAWN_INTERVAL:
            pipes.append(Pipe(WIDTH))
            last_pipe_time = current_time

        pipes_to_remove = []
        for pipe in pipes:
            pipe.move()

            if pipe.collide(player):
                hit=True
            
            if player.x > pipe.x + PIPE_WIDTH and not pipe.passed:
                pipe_score += 1
                pipe.passed = True
                
            if pipe.x + PIPE_WIDTH < 0:
                pipes_to_remove.append(pipe)
                
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        if hit:
            lost_text = FONT.render("You lost!", 1, "black")
            WIN.blit(lost_text, (WIDTH//2-lost_text.get_width()//2, HEIGHT//2-lost_text.get_width() //2))
            pygame.display.update()
            pygame.time.delay(2000)
            break
        else:
            draw(player, pipe_score, pipes)
         
    pygame.quit()
        

if __name__ == "__main__":
    main()