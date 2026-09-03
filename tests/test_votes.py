from fastapi import status
import pytest

from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[3].id, "vote_dir": True}
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json().get("message") == "Vote added with success"


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[3].id, "vote_dir": True}
    )
    assert res.status_code == status.HTTP_409_CONFLICT


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[3].id, "vote_dir": False}
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json().get("message") == "Vote removed with success"


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[3].id, "vote_dir": False}
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={"post_id": 88888, "vote_dir": True}
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/votes/",
        json={"post_id": test_posts[3].id, "vote_dir": True}
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
