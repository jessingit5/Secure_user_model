from app.hashing import Hasher
import pytest

def test_hash_password():

    password = "mysecretpassword"
    hashed_password = Hasher.hash_password(password)
    assert hashed_password is not None
    assert hashed_password != password

def test_verify_password():

    password = "mysecretpassword"
    hashed_password = Hasher.hash_password(password)
    assert Hasher.verify_password(password, hashed_password) is True

def test_verify_incorrect_password():

    password = "mysecretpassword"
    hashed_password = Hasher.hash_password(password)
    assert Hasher.verify_password("wrongpassword", hashed_password) is False