from reactpy_utils.static_counter import ID


def test_static_counter():
    assert ID() == 1
    assert ID() == 2
    assert ID() == 3
    assert ID() == 4
