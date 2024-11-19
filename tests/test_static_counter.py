from reactpy_utils.static_counter import id


def test_static_counter():
    assert id() == 1
    assert id() == 2
    assert id() == 3
    assert id() == 4
