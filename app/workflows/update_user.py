from app.dtos.user_update import UserUpdateDTO
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class UpdateUserWorkflow:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, user_id: int, data: UserUpdateDTO) -> UserModel:
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        if data.email is not None:
            existing_user = self._repository.find_by_email(data.email)

            if existing_user is not None and existing_user.id != user.id:
                raise ValueError("Email already exists")

            user.email = data.email

        if data.name is not None:
            user.name = data.name

        return self._repository.update(user)