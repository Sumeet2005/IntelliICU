import bcrypt
import uuid
from app.models.user import User

def hash_pw(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Seed users with department fields added
MOCK_USERS = {
    "admin": {
        "id": "usr-1",
        "username": "admin",
        "email": "admin@intelliicu.org",
        "hashed_password": hash_pw("admin123"),
        "role": "HospitalAdmin",
        "department": "Administration",
        "is_active": True
    },
    "reyes": {
        "id": "usr-2",
        "username": "reyes",
        "email": "reyes@intelliicu.org",
        "hashed_password": hash_pw("intensivist123"),
        "role": "ICUManager",
        "department": "Medical ICU",
        "is_active": True
    },
    "miller": {
        "id": "usr-3",
        "username": "miller",
        "email": "miller@intelliicu.org",
        "hashed_password": hash_pw("miller123"),
        "role": "Doctor",
        "department": "Medical ICU",
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

    @staticmethod
    def list_users(search: str = None, role: str = None, department: str = None, page: int = 1, size: int = 10) -> tuple[list[User], int]:
        filtered = list(MOCK_USERS.values())
        
        if search:
            term = search.lower()
            filtered = [
                u for u in filtered
                if term in u["username"].lower() or term in u["email"].lower()
            ]
        if role and role.lower() != "all":
            filtered = [u for u in filtered if u["role"].lower() == role.lower()]
        if department and department.lower() != "all":
            filtered = [
                u for u in filtered
                if u.get("department") and u["department"].lower() == department.lower()
            ]
            
        total = len(filtered)
        
        start = (page - 1) * size
        end = start + size
        users = [User(**u) for u in filtered[start:end]]
        return users, total

    @staticmethod
    def create_user(user_data: dict) -> User:
        username = user_data["username"]
        email = user_data["email"]
        
        if username.lower() in MOCK_USERS:
            raise ValueError("Username already exists")
        if any(u["email"].lower() == email.lower() for u in MOCK_USERS.values()):
            raise ValueError("Email already exists")
            
        uid = f"usr-{str(uuid.uuid4())[:8]}"
        user_dict = {
            "id": uid,
            "username": username,
            "email": email,
            "hashed_password": user_data["hashed_password"],
            "role": user_data["role"],
            "department": user_data.get("department"),
            "is_active": True
        }
        MOCK_USERS[username.lower()] = user_dict
        return User(**user_dict)

    @staticmethod
    def update_user(user_id: str, update_data: dict) -> User | None:
        user_dict = next((u for u in MOCK_USERS.values() if u["id"] == user_id), None)
        if not user_dict:
            return None
            
        email = update_data.get("email")
        if email and email.lower() != user_dict["email"].lower():
            if any(u["email"].lower() == email.lower() and u["id"] != user_id for u in MOCK_USERS.values()):
                raise ValueError("Email already exists")
                
        user_dict["email"] = update_data.get("email", user_dict["email"])
        user_dict["role"] = update_data.get("role", user_dict["role"])
        user_dict["department"] = update_data.get("department", user_dict.get("department"))
        if "is_active" in update_data:
            user_dict["is_active"] = update_data["is_active"]
            
        # Update entry in MOCK_USERS dictionary keys if username changes (though username is static in this CRUD step)
        return User(**user_dict)

    @staticmethod
    def set_password(user_id: str, hashed_password: str) -> bool:
        user_dict = next((u for u in MOCK_USERS.values() if u["id"] == user_id), None)
        if not user_dict:
            return False
        user_dict["hashed_password"] = hashed_password
        return True
