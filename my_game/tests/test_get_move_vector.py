from game import get_move_vector
import pytest



def test__get_move_vector__move_left():
    
    assert get_move_vector(direction='left', speed=5) == (-5, 0)


def test__get_move_vector__move_down():

    assert get_move_vector(direction='down', speed=5) == (0, 5)

def test__get_move_vector__move_up():

    assert get_move_vector(direction='up', speed=5) == (0, -5)

def test__get_move_vector__move_right():

    assert get_move_vector(direction='right', speed=5) == (5, 0)

    

@pytest.mark.parametrize('speed', [5, 10, 15])
def test__get_move_vector__move_use_speed_as_move_distance(speed):
    assert get_move_vector(direction='right', speed=speed) == (speed, 0)