from reactpy_utils import UID


def test_UID():
    user_ids = [UID(prefix="user") for i in range(1000000)]
    assert user_ids[0].startswith("user-")
    assert len(user_ids) == len(set(user_ids))
