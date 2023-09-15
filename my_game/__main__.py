import random

import pygame
from pygame.sprite import Group, spritecollide
from labirinth_template import gameboard
from game import get_move_vector, draw_whole_screen, compose_context, change_vector, Walls


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5
    enemy_speed = 5

    context = compose_context(screen)
    
    next_move = (0, -5)
      
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
        old_skeleton_topleft = context['skeleton'].rect.topleft
      
        if keys[pygame.K_w]:
            context["player"].rect = context["player"].rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context["player"].rect = context["player"].rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context["player"].rect = context["player"].rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context["player"].rect = context["player"].rect.move(player_speed, 0)

        if spritecollide(context["player"], context["walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft


        context["skeleton"].rect = context["skeleton"].rect.move(*next_move)
       

        if spritecollide(context["skeleton"], context["walls"], dokill=False):
            # Смена направления движения врага после столкновения со стенами периметра
            next_move = change_vector(context, old_skeleton_topleft, enemy_speed)
        

        for i in range(len(context) - 3):
            if context["skeleton"].is_collided_with(context[f"walls{i}"]):
                # Смена направления движения врага после столкновения со стенами лабиринта
                next_move = change_vector(context, old_skeleton_topleft, enemy_speed)

        for i in range(len(context) - 3):
            if context["player"].is_collided_with(context[f"walls{i}"]):
                # обрабатываем столкновения игрока с препятствиями
                context["player"].rect.topleft = old_player_topleft
        

        
        if context["player"].is_collided_with(context["skeleton"]):
            # TODO Обработать в этом месте GameOver и рестарт игры через нажатие пробела

            context["skeleton"].rect.topleft = (
                random.randint(Walls.width, screen.get_width() - Walls.width * 2),
                random.randint(Walls.height, screen.get_height() - Walls.height * 2),
            )
            
            

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()