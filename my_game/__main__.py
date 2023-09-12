import random

import pygame
from pygame.sprite import Group, spritecollide

from game import GameObject
from labirinth_template import gameboard



class Player(GameObject):
    sprite_filename = "player"


class Walls(GameObject):
    sprite_filename = "walls"


class Skeleton(GameObject):
    sprite_filename = "skeleton"


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
        ])

    return walls_coordinates


def create_labyrinth_coordinates(screen, width, height):
    """ Функция задает координаты для лабиринта из шаблона 'labirinth_template.gameboard' """
    list_1 = []
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i - 1])):
            if gameboard[i][j] == 1:
                x = j * width
                y = i * height
                list_1.extend([(x, y)])

    return list_1


def compose_context(screen):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Walls.width, Walls.height)
    
    obj =  {
        "player": Player(screen.get_width() // 2, screen.get_height() // 2),
        "walls": Group(*[Walls(x, y) for (x, y) in walls_coordinates]),
        "skeleton": Skeleton(40, 40),
    }
    lst = create_labyrinth_coordinates(screen, Walls.width, Walls.height)    # добавляет список координатов для стен лабиринта
    for i in lst:
        obj[f'walls{lst.index(i)}'] = Walls(*i)
    return obj


def draw_whole_screen(screen, context):
    screen.fill("purple")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["skeleton"].draw(screen)
    
    for i in range(len(context) - 3):      # рисует стены лабиринта
        context[f'walls{i}'].draw(screen)
    




def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5

    context = compose_context(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
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

        for i in range(len(context) - 3):
            if context["player"].is_collided_with(context[f"walls{i}"]):
                # обрабатываем столкновения с препятствиями
                context["player"].rect.topleft = old_player_topleft

        if context["player"].is_collided_with(context["skeleton"]):
            context["skeleton"].rect.topleft = (
                random.randint(Walls.width, screen.get_width() - Walls.width * 2),
                random.randint(Walls.height, screen.get_height() - Walls.height * 2),
            )

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()