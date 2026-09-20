from core.security import verify_password, hash_password

def test_hash_password():
    password = "testpassword"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password

def test_verify_password():
    password = "testpassword"
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password) 
    assert not verify_password("wrongpassword", hashed_password) 