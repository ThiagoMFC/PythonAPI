import pytest
from app import schemas, models

#define order of testing 
pytestmark = pytest.mark.order(4)

def test_up_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert res.status_code == 201

def test_up_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == 409

def test_down_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 0})
    assert res.status_code == 201

def test_down_vote_not_voted(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 0})
    assert res.status_code == 404

def test_up_vote_unauth(client, test_posts, test_vote):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == 401

def test_down_vote_unauth(client, test_posts, test_vote):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 0})
    assert res.status_code == 401

def test_up_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 99999999999, "direction": 1})
    assert res.status_code == 404

def test_down_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 99999999999, "direction": 0})
    assert res.status_code == 404