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
    res = authorized_client.get("/posts/99999999999999")
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

def test_unauth_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "some title", "content": "some content"})
    assert res.status_code == 401

def test_unauth_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    validate_delete = authorized_client.get("/posts/")
    assert len(validate_delete.json()) == len(test_posts)-1

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/9999999999999")
    assert res.status_code == 404
    validate_delete = authorized_client.get("/posts/")
    assert len(validate_delete.json()) == len(test_posts)

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    validate_delete = authorized_client.get("/posts/")
    assert len(validate_delete.json()) == len(test_posts)


@pytest.mark.parametrize("title, content, published, status_code", [
    ("some updated title", "some updated content", True, 200),
    ("another updated title", "more updated content", False, 200),
    (None, "more updates", True, 422),
    ("updating", None, True, 422),
])
def test_update_post(authorized_client, test_user, test_posts, title, content, published, status_code):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title": title, "content": content, "published": published})
    assert res.status_code == status_code
    validate_update = authorized_client.get(f"/posts/{test_posts[0].id}")
    if published is not False:
        updated_post = schemas.PostVoteResponse(**validate_update.json())
        if status_code != 422:
            assert updated_post.Post.title == title
            assert updated_post.Post.content == content
            assert updated_post.Post.published == published
        else:
            assert updated_post.Post.title == test_posts[0].title
            assert updated_post.Post.content == test_posts[0].content
            assert updated_post.Post.published == test_posts[0].published
    else:
        assert validate_update.status_code == 404