import pytest
from app import schemas, models

#define order of testing 
pytestmark = pytest.mark.order(4)

def test_up_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert res.status_code == 201

#fixture to create vote
@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_up_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == 409