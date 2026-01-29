import json
import os
from datetime import datetime
from typing import Dict
from app.models.user import UserStatus

class UserService:
    """
    Простой сервис для трекинга пользователей (в памяти/файле для MVP).
    В продакшене тут была бы БД User(device_id, is_premium, ...).
    """
    def __init__(self):
        self.db_path = "backend/users.json"
        self.users: Dict[str, dict] = self._load_db()
        self.DAILY_LIMIT = 3

    def _load_db(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except: 
                return {}
        return {}

    def _save_db(self):
        with open(self.db_path, "w") as f:
            json.dump(self.users, f, indent=2)

    def get_user_status(self, device_id: str) -> UserStatus:
        user = self.users.get(device_id, {
            "is_premium": False,
            "daily_count": 0,
            "last_date": datetime.now().strftime("%Y-%m-%d")
        })
        
        # Reset counter if new day
        today = datetime.now().strftime("%Y-%m-%d")
        if user["last_date"] != today:
            user["daily_count"] = 0
            user["last_date"] = today
            self.users[device_id] = user
            self._save_db()
            
        limit = 999 if user["is_premium"] else self.DAILY_LIMIT
        
        return UserStatus(
            device_id=device_id,
            is_premium=user["is_premium"],
            daily_count=user["daily_count"],
            limit=limit
        )

    def increment_usage(self, device_id: str):
        if device_id not in self.users:
            self.get_user_status(device_id) # Init user
            
        self.users[device_id]["daily_count"] += 1
        self._save_db()

    def upgrade_user(self, device_id: str):
        if device_id not in self.users:
            self.get_user_status(device_id)
            
        self.users[device_id]["is_premium"] = True
        self._save_db()
