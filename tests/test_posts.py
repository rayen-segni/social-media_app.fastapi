import pytest
from fastapi import status

from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    for post in res.json():
        schemas.PostResponse(**post["Post"]) # Because the endpoint return joined data between post and user infos sow e extract only posts

    assert res.status_code == status.HTTP_200_OK

def test_unautorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_unautorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_one_not_exist_post(authorized_client):
    res = authorized_client.get("/posts/1")
    
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    
    posts = res.json()["Post"]
    
    schemas.PostResponse(**posts)
    assert posts["id"] == test_posts[0].id
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(["title", "content", "published"], [
    ("Awesome New Title", "Awesome new content", True),
    ("Favorite Pizza", "I love pepperoni", False),
    ("Tallest Man", "From Netherlands", True),
])
def test_create_post(
    authorized_client,
    title, content, published
):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published
        })
    
    created_post = schemas.PostResponse(**res.json())
    
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(authorized_client):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": "title",
            "content": "content"
        })
    
    created_post = schemas.PostResponse(**res.json())
    
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True


def test_unautorized_create_post(client):
    res = client.post(
        "/posts/",
        json={
            "title": "title",
            "content": "content",
            "published": True
        })
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_user_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_none_exist_post(authorized_client):
    res = authorized_client.delete("/posts/1")

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_not_owned_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}") # This post is owned by the user 2
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "updated title",
            "content": "updated content",
            "id": test_posts[0].id
        })
    
    updated_post = schemas.PostResponse(**res.json())
    
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == "updated title"
    assert updated_post.content == "updated content"


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    # test_posts[3] is owned by test_user2, but authorized_client is authenticated as test_user
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json={
            "title": "updated title",
            "content": "updated content",
            "id": test_posts[0].id
        }
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED

