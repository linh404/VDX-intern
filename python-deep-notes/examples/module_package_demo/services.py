from .models import User

class UserService:

    def __init__(self):
        self.users = {}

    def register_user(self, user_id, username, email):
        user = User(user_id, username, email)
        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)
