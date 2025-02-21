import bcrypt

def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    pwd_hasshed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return pwd_hasshed.decode('utf-8')

def verify_password(password: str, password_hash: str):
    pwd_bytes = password.encode('utf-8')
    pwd_hash_bytes = password_hash.encode('utf-8')
    pwd_valid = bcrypt.checkpw(pwd_bytes, pwd_hash_bytes)
    return pwd_valid