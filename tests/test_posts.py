import pytest
from app import schemas

#define order of testing 
pytestmark = pytest.mark.order(3)

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauth_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauth_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    #print(res.json())
    post = schemas.PostVoteResponse(**res.json())
    #print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    #print(res.json())
    post = schemas.PostVoteResponse(**res.json())
    #print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/99999999999999")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content", [
    ("new title", "new content"),
    ("another title", "more content")
])
def test_create_post(authorized_client, test_user, test_posts, title, content):
    res = authorized_client.post("/posts/", json={"title": title, "content": content})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner.id == test_user["id"]