import pygame 
import os 
import random
pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHT_GREY = (211,211,211)
ORANGE = (255,165,0)
RED = (255,0,0)

FPS = 60
VEL = 10
H_MOVE = ["RIGHT", "LEFT"]
V_MOVE = ["UP", "DOWN"]
SMALL_FOOD_EVENT = pygame.USEREVENT + 0
BIG_FOOD_EVENT = pygame.USEREVENT + 1
CRASH = pygame.USEREVENT + 2

FOOD_EAT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Food_eating.mp3'))
BIG_FOOD_EAT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Sanke_collide_with_body.mp3'))
HEAD_CRASH = pygame.mixer.Sound(os.path.join('Assets','BIG_FOOD_EAT.wav'))
SCORE = pygame.font.SysFont('pluto', 40)
GAME_OVER = pygame.font.SysFont('pluto', 100)

def draw_window(HEAD, SNAKE_LENGTH, FOOD_LIST, SCORE_NO):
    WIN.fill(LIGHT_GREY)
    for food in range(0,len(FOOD_LIST) - 1):
        pygame.draw.rect(WIN, BLACK, FOOD_LIST[food])
    pygame.draw.rect(WIN, ORANGE, HEAD)
    Score_text = SCORE.render("SCORE: " + str(SCORE_NO[0]), 1, WHITE)
    WIN.blit(Score_text, (10,10))
    for Body in range(1,len(SNAKE_LENGTH)):
        pygame.draw.rect(WIN, ORANGE, SNAKE_LENGTH[Body][0])
    pygame.display.update()

def food_eating(HEAD, SNAKE_LENGTH, MOVE, SMALL_FOOD, FOOD_LIST, SCORE_NO):
   
    if HEAD.colliderect(FOOD_LIST[0]):
        FOOD_EAT_SOUND.play()
        Body = Snake(SNAKE_LENGTH[len(SNAKE_LENGTH)-1][4], SNAKE_LENGTH[len(SNAKE_LENGTH)-1][5], SNAKE_LENGTH[len(SNAKE_LENGTH)-1][6])
        SNAKE_LENGTH.append(Body)
        
        FOOD_LIST.pop(0)
        snake_food(SNAKE_LENGTH, FOOD_LIST)
        SCORE_NO[0] += 10
        if type(FOOD_LIST[1]) == int:
            FOOD_LIST[1] += 1
            if FOOD_LIST[1] >= 10:
                snake_food(SNAKE_LENGTH, FOOD_LIST, 12,12)
                pygame.time.set_timer(BIG_FOOD_EVENT, 5000)

    if len(FOOD_LIST) >= 3:
        if HEAD.colliderect(FOOD_LIST[1]):
            BIG_FOOD_EAT_SOUND.play()
            SCORE_NO[0] += 50
            FOOD_LIST[2] = 0
            FOOD_LIST.pop(1)



def snake_movement(HEAD, SNAKE_LENGTH, MOVE, SMALL_FOOD, FOOD_LIST, SCORE_NO):
    if MOVE == "RIGHT":
        HEAD.x += VEL
        if HEAD.x >= 1280:
            HEAD.x = - HEAD.width
    if MOVE == "LEFT":
        HEAD.x -= VEL
        if HEAD.x + HEAD.width <= 0:
            HEAD.x = WIDTH
    if MOVE == "UP":
        HEAD.y -= VEL
        if HEAD.y + HEAD.height <= 0:
            HEAD.y = HEIGHT
    if MOVE == "DOWN":
        HEAD.y += VEL
        if HEAD.y >= HEIGHT:
            HEAD.y = - HEAD.height

    SNAKE_LENGTH[0][4], SNAKE_LENGTH[0][5], SNAKE_LENGTH[0][6] = SNAKE_LENGTH[0][1], SNAKE_LENGTH[0][2], SNAKE_LENGTH[0][3]
    SNAKE_LENGTH[0][1], SNAKE_LENGTH[0][2], SNAKE_LENGTH[0][3] = HEAD.x, HEAD.y, MOVE 

    if len(SNAKE_LENGTH) >=2:
        for i in range(1,len(SNAKE_LENGTH)):
            SNAKE_LENGTH[i][4], SNAKE_LENGTH[i][5], SNAKE_LENGTH[i][6] = SNAKE_LENGTH[i][1], SNAKE_LENGTH[i][2], SNAKE_LENGTH[i][3]
            SNAKE_LENGTH[i][1], SNAKE_LENGTH[i][2], SNAKE_LENGTH[i][2] = SNAKE_LENGTH[i-1][4], SNAKE_LENGTH[i-1][5], SNAKE_LENGTH[i-1][5] 
            SNAKE_LENGTH[i][0].x, SNAKE_LENGTH[i][0].y = SNAKE_LENGTH[i][1], SNAKE_LENGTH[i][2]
    for Body in range(1,len(SNAKE_LENGTH)):
        rest_body = SNAKE_LENGTH[Body][0]
        if HEAD.colliderect(rest_body):
            HEAD_CRASH.play()
            pygame.event.post(pygame.event.Event(CRASH))  

    food_eating(HEAD, SNAKE_LENGTH, MOVE, SMALL_FOOD, FOOD_LIST, SCORE_NO)

def checkFoodCollide(SNAKE_LENGTH, FOOD_LIST, food_position, x, y):
    VALID1, VALID2 = False, False
    for Body in SNAKE_LENGTH:
        if food_position.colliderect(Body[0]):
            VALID = True

    if (x == 12) and (y == 12):
        Food = FOOD_LIST[0]
        if food_position.colliderect(Food):
            VALID2 = True
    return (VALID1 or VALID2)

def snake_food(SNAKE_LENGTH, FOOD_LIST, x = 8, y = 8): 
    food_x = random.randrange(0,WIDTH - x)
    food_y = random.randrange(0, HEIGHT - y)
    food_position = pygame.Rect(food_x, food_y, x, y)
    if (x == 8) and (y == 8):
        while(checkFoodCollide(SNAKE_LENGTH, FOOD_LIST, food_position, x, y)):
            food_position.x = random.randrange(1,WIDTH-x)
            food_position.y = random.randrange(1,HEIGHT-y)
        FOOD_LIST.insert(0,food_position)

    if (x == 12) and (y == 12):
        while(checkFoodCollide(SNAKE_LENGTH,FOOD_LIST, food_position, x, y)):
            food_position.x = random.randrange(1,WIDTH-x)
            food_position.y = random.randrange(0,HEIGHT-y)
        FOOD_LIST.insert(1,food_position)

def gameOver():
    draw_text = GAME_OVER.render("GAME OVER", 1, RED)
    WIN.blit(draw_text, ((WIDTH - draw_text.get_width())//2, (HEIGHT - draw_text.get_height())//2))
    pygame.display.update()
    pygame.time.delay(5000)

def Snake(x1, y1, move1, x2=None, y2=None, move2=None):
    Square = pygame.Rect(x1,y1,10,10)
    Body = [Square,x1,y1,move1,x2,y2,move2]
    return Body

def main():
    clock = pygame.time.Clock()
    run = True

    H_MOVE = ["LEFT", "RIGHT"]
    V_MOVE = ["UP", "DOWN"]
    MOVE = "RIGHT"
    PREVIOUS_MOVE = MOVE
    SCORE_NO = [0]

    SNAKE_LENGTH = []
    HEAD = Snake(WIDTH//2, HEIGHT//2,MOVE,(WIDTH//2)-10,HEIGHT//2,MOVE)
    SNAKE_LENGTH.append(HEAD)
 
    FOOD_LIST = []
    snake_food(SNAKE_LENGTH, FOOD_LIST)
    FOOD_LIST.append(0)
    SMALL_FOOD = FOOD_LIST[0]

    time, time_step = 0, 50

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    MOVE = "UP"
                if event.key == pygame.K_DOWN:
                    MOVE = "DOWN"
                if event.key == pygame.K_LEFT:
                    MOVE = "LEFT"
                if event.key == pygame.K_RIGHT:
                    MOVE = "RIGHT"

            if event.type == BIG_FOOD_EVENT:
                if (len(FOOD_LIST) >= 2) and (type(FOOD_LIST[1]) != int):
                    FOOD_LIST[2] = 0
                    FOOD_LIST.pop(1)

            if event.type == CRASH:
                gameOver()
                run = False
                pygame.quit()

        if ((MOVE in H_MOVE) and (PREVIOUS_MOVE in H_MOVE)) or ((MOVE in V_MOVE) and (PREVIOUS_MOVE in V_MOVE)):
            MOVE = PREVIOUS_MOVE
        else:
            PREVIOUS_MOVE = MOVE
        time_now = pygame.time.get_ticks()
        
        if time_now - time > time_step:
            time = time_now
            snake_movement(SNAKE_LENGTH[0][0],SNAKE_LENGTH, MOVE, SMALL_FOOD, FOOD_LIST, SCORE_NO)
        draw_window(SNAKE_LENGTH[0][0],SNAKE_LENGTH, FOOD_LIST, SCORE_NO)
    main()

if __name__ == "__main__":
    main()