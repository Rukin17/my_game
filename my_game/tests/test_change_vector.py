import pygame
from unittest import mock
from game import change_vector_upon_collision, compose_context


screen = pygame.display.set_mode((640, 480))
context = compose_context(screen)


def test__change_vector():
    with mock.patch('random.choice') as choice_mock:
        choice_mock.return_value = 'right'
        assert change_vector_upon_collision(context=context, old_topleft=(80, 40), speed=5) == (5, 0)