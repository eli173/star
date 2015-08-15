

class User:
    def __init__(self,username,password):
        self.is_authenticated = False
        self.username = username
        self.password = password
