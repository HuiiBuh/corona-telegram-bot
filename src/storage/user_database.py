from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import field
from typing import Dict, Union, List

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from helpers.singleton import Singleton


@dataclass
class User:
    id: int
    districts: List[int] = field(default_factory=lambda: [])
    notification_active: bool = True


class UserDict(BaseModel):
    __root__: Dict[int, User] = Field({})

    def all(self) -> Dict[int, User]:
        return deepcopy(self.__root__)

    def set(self, user: User):
        self.__root__[user.id] = user

    def get(self, user_id: int) -> User:
        return self.__root__[user_id]

    def delete(self, user_id: int) -> None:
        del self.__root__[user_id]

    def has(self, user_id: int) -> bool:
        return user_id in self.__root__


class UserDatabase(metaclass=Singleton):

    def __init__(self, file_name: str):
        self._data: UserDict = UserDict()
        self.file_name: str = file_name

    def load(self, create_if_not_exist=True) -> None:
        if not os.path.exists(self.file_name):
            if create_if_not_exist:
                with open(self.file_name, "w") as file:
                    file.write("{}")
            else:
                raise Exception("Could not load from file")

        with open(self.file_name, "r") as file:
            self._data = UserDict(__root__=json.loads(file.read()))

    def save(self) -> None:
        with open(self.file_name, "w") as file:
            file.write(self._data.json())

    def add_user(self, user_id: int, districts=None, notification_active=True) -> None:
        if self._data.has(user_id):
            raise Exception("User is already in the database")

        if districts is None:
            districts = []

        self._data.set(User(user_id, districts, notification_active))
        self.save()

    def create_if_not_exist(self, user_id: int):
        if not self._data.has(user_id):
            self._data.set(User(user_id))
            self.save()

    def delete_user(self, user_id: int):
        self._data.delete(user_id)
        self.save()

    def edit_user(self, user_id: int, districts=None, notification_active=None) -> None:
        if not self._data.has(user_id):
            raise Exception("User is not in the database")

        user: User = self._data.get(user_id)

        if districts is not None:
            user.districts = districts

        if notification_active is not None:
            user.notification_active = notification_active

        self.save()

    def get_user(self, user_id: int) -> Union[User, None]:
        if not self._data.has(user_id):
            self.add_user(user_id)
        return self._data.get(user_id)

    def get_all_users(self) -> Dict[int, User]:
        return self._data.all()

    @staticmethod
    def create() -> UserDatabase:
        return UserDatabase("database/user_db.json")
