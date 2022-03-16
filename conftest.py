import pytest
from src.classes.user import User
from src.classes.search import Search


@pytest.fixture(scope="session")
def global_user1():
    user1 = User()
    user1.set_user('johndoe', '1234', 'john', 'doe')
    return user1


@pytest.fixture(scope="session")
def global_user2():
    user2 = User()
    user2.set_user('tombrown', '6789', 'tom', 'brown')
    return user2

@pytest.fixture(scope="session")
def global_search():
    user = User()
    user.set_user('johndoe', '1234', 'john', 'doe')
    search = Search()
    search.set_search(user.username, 'IAH', 'WAS', '2/22/2022', 2)
    return search