import bcrypt
from app.models.user import User

def hash_pw(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Seed user roles aligned with Phase 7.2 RBAC Role Matrix
MOCK_USERS = {
    "admin": {
        "id": "usr-1",
        "username": "admin",
        "email": "admin@intelliicu.org",
        "hashed_password": hash_pw("admin123"),
        "role": "HospitalAdmin",
        "is_active": True
    },
    "reyes": {
        "id": "usr-2",
        "username": "reyes",
        "email": "reyes@intelliicu.org",
        "hashed_password": hash_pw("intensivist123"),
        "role": "ICUManager",
        "is_active": True
    },
    "miller": {
        "id": "usr-3",
        "username": "miller",
        "email": "miller@intelliicu.org",
        "hashed_password": hash_pw("miller123"),
        "role": "Doctor",
        "is_active": True
    }
}

class UserRepository:
    @staticmethod
    def get_by_username(username: str) -> User | None:
        user_dict = MOCK_USERS.get(username.lower())
        if not user_dict:
            return None
        return User(**user_dict)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        user_dict = next(
            (u for u in MOCK_USERS.values() if u["email"].lower() == email.lower()),
            None
        )
        if not user_dict:
            return None
        return User(**user_dict)

    @staticmethod
    def get_by_id(user_id: str) -> User | None:
        user_dict = next(
            (u for u in MOCK_USERS.values() if u["id"] == user_id),
            None
        )
        if not user_dict:
            return None
        return User(**user_dict)
