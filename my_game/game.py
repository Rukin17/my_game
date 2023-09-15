import random
from pygame.sprite import Group
from game_objects import GameObject
from labirinth_template import gameboard


class Player(GameObject):
    sprite_filename = "player"


class Walls(GameObject):
    sprite_filename = "walls"


class Skeleton(GameObject):
    sprite_filename = "skeleton"



def draw_whole_screen(screen, context):
    screen.fill("purple")
    context["player"].draw(screen)
    context["walls"].draw(screen)
    context["skeleton"].draw(screen)
    
    for i in range(len(context) - 3): 
        # рисует стены лабиринта     
        context[f'walls{i}'].draw(screen)


def compose_context(screen):
    # TODO Написать тесты

    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Walls.width, Walls.height)
    
    obj =  {
        "player": Player(screen.get_width() // 2, screen.get_height() // 2),
        "walls": Group(*[Walls(x, y) for (x, y) in walls_coordinates]),
        "skeleton": Skeleton(80, 80),
    }
    lst = create_labyrinth_coordinates(Walls.width, Walls.height)    # добавляет список координатов для стен лабиринта
    for i in lst:
        obj[f'walls{lst.index(i)}'] = Walls(*i)
    return obj


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    """ Функция создает стены по периметру игрового окна """
    # TODO Написать тесты

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



def create_labyrinth_coordinates(width, height):
    """ Функция задает координаты для лабиринта из шаблона 'labirinth_template.gameboard' """
    list_1 = []
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i - 1])):
            if gameboard[i][j] == 1:
                x = j * width
                y = i * height
                list_1.extend([(x, y)])

    return list_1


def get_move_vector(direction: str, speed: int) -> tuple[int, int]:
    
    vectors = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }
    dx, dy = vectors[direction]
    return dx * speed, dy * speed


def change_vector(context: dict[str, str], old_topleft: tuple[int, int], speed) -> tuple[int, int]:
    """ Функция осуществляет остановку врага и задает новые координаты для движения"""

    context["skeleton"].rect.topleft = old_topleft
    value = random.choice(['right', 'left', 'up', 'down'])
    next_move = get_move_vector(value, speed)
    return next_move
