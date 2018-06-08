import hashlib

USER_DATA= {
    'name':'Al-python',
    'password':hashlib.md5('123'.encode()).hexdigest(),
}



def authenticate(username,password):
    '''密码验证'''
    if username and password:
        hash_pw =hashlib.md5(password.encode()).hexdigest()
        if username == USER_DATA['name'] and hash_pw == USER_DATA['password']:
            return True


    return False


