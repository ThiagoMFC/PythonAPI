import pytest

#define order of testing 
pytestmark = pytest.mark.order(3)

def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts")
    assert res.status_code == 200