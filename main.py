import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define display dimensions and create the display
dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('SlotPY')
clock = pygame.time.Clock()

snake_block = 10 # Dimension of a block (snake AND orb)
initial_snake_speed = 15
snake_speed_increase_rate = 0.11

# Load custom fonts
font_style = pygame.font.Font(None, 25)
score_font = pygame.font.Font(None, 35)

def Your_score(score,glowing=False):
    if glowing:
        value = score_font.render("Your Score: " + str(score), True, random.choice([red, black]))
    else:
        value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def endGameAnimation(snake_List, length_of_snake):
    # # Gradually turn the snake blocks red one-by-one
    # for block in snake_List:
    #     dis.fill(blue)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()

    #     pygame.draw.rect(dis, red, [block[0], block[1], snake_block, snake_block])
    #     Your_score(length_of_snake - 1)
    #     pygame.display.update()
    #     time.sleep(0.1)  # Adjust the speed of the animation

    # red_color = pygame.Color('red')
    # black_color = pygame.Color('black')
    # color_increment = 255 // length_of_snake

    # for i, block in enumerate(snake_List):
    #     dis.fill(blue)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()

    #     color = red_color.lerp(black_color, i / length_of_snake)
    #     pygame.draw.rect(dis, color, [block[0], block[1], snake_block, snake_block])
    #     Your_score(length_of_snake - 1)
    #     pygame.display.update()
    #     time.sleep(0.1)  # Adjust the speed of the animation

    fade_out_speed = 8  # Adjust the speed of the fade-out effect

    for alpha in range(255, 0, -fade_out_speed):
        dis.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for i, block in enumerate(snake_List):
            color = pygame.Color('red')
            color.a = alpha  # Set the alpha channel (opacity) of the color
            pygame.draw.rect(dis, color, [block[0], block[1], snake_block, snake_block])

        Your_score(length_of_snake - 1)
        pygame.display.update()
        clock.tick(60)  # Adjust the frame rate

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    eat_animation = False
    eat_animation_frames = 1

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press 'C' to Play Again or 'Q' To Quit The Game", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Implement the functionality for the snake to appear on the opposite side
        x1 = (x1 + x1_change) % dis_width
        y1 = (y1 + y1_change) % dis_height

        snake_speed = initial_snake_speed + snake_speed_increase_rate * (Length_of_snake-1)

        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
            # Trigger the end game animation and freeze the game
                endGameAnimation(snake_List, Length_of_snake)
                # message("You Lost! Press 'C' to Play Again or 'Q' To Quit The Game", red)

                # pygame.time.wait(2000)
                # Your_score(Length_of_snake - 1)
                # pygame.display.update()
                time.sleep(2)  # Freeze the game for 2 seconds before allowing restart

                # Restart the game
                # gameLoop()

        our_snake(snake_block, snake_List)

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            eat_animation = True
            
            # Show the glowing effect on the score for a brief moment
            Your_score(Length_of_snake - 1, glowing=True)
            pygame.display.update()
            time.sleep(0.15)  # Adjust the duration of the glow
        
        if eat_animation:
            for _ in range(eat_animation_frames):
                x1 += x1_change
                y1 += y1_change
                dis.fill(blue)
                pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
                our_snake(snake_block, snake_List)
                Your_score(Length_of_snake - 1)
                pygame.display.update()

                clock.tick(snake_speed)

            eat_animation = False

        Your_score(Length_of_snake - 1)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
