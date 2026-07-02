from .services import UserService
from .models import User

def main():
    service = UserService()
    user = service.register_user(1, 'john_doe', 'john@example.com')
    print('Registered User:', user.username, user.email)
    retrieved = service.get_user(1)
    print('Retrieved User matches registered:', retrieved is user)
if __name__ == '__main__':
    main()
