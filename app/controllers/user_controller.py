from app.dtos.user_create import UserCreateDTO
from app.dtos.user_response import UserResponseDTO
from app.dtos.user_update import UserUpdateDTO
from app.models.user_model import UserModel
from app.services.user_service import UserService


class UserController:
    """Controller component responsible for handling HTTP-level request parsing and response formatting.

    Attributes:
        _service (UserService): Service instance providing core user management business logic.
    """

    def __init__(self, service: UserService) -> None:
        """Initializes the controller with a user service instance.

        Args:
            service (UserService): The service layer dependency for user operations.
        """
        self._service = service

    def create_user(self, data: UserCreateDTO) -> UserResponseDTO:
        """Handles the HTTP request to create a new user.

        Args:
            data (UserCreateDTO): Data transfer object containing creation payload.

        Returns:
            UserResponseDTO: Validated response DTO representing the newly created user.
        """
        user = self._service.create_user(data)
        return UserResponseDTO.model_validate(user)

    def list_users(self) -> list[UserResponseDTO]:
        """Handles the HTTP request to list all existing users.

        Returns:
            list[UserResponseDTO]: A list of response DTOs for all registered users.
        """
        users = self._service.list_users()
        return [UserResponseDTO.model_validate(user) for user in users]

    def get_user(
        self,
        user_id: int,
        current_user: UserModel,
    ) -> UserResponseDTO:
        """Retrieves a user by ID and converts the entity to a response DTO.

        Args:
            user_id (int): The unique identifier of the target user to retrieve.
            current_user (UserModel): The currently authenticated user making the request.

        Returns:
            UserResponseDTO: Data transfer object containing the user details.
        """
        user = self._service.get_user(user_id, current_user)
        return UserResponseDTO.model_validate(user)

    def update_user(
        self,
        user_id: int,
        data: UserUpdateDTO,
        current_user: UserModel,
    ) -> UserResponseDTO:
        """Handles the request to update an existing user's attributes.

        Args:
            user_id (int): The unique identifier of the user to update.
            data (UserUpdateDTO): Data transfer object containing fields to update.
            current_user (UserModel): The currently authenticated user making the request.

        Returns:
            UserResponseDTO: Validated response DTO representing the updated user.
        """
        user = self._service.update_user(user_id, data, current_user)
        return UserResponseDTO.model_validate(user)

    def delete_user(
        self,
        user_id: int,
        current_user: UserModel,
    ) -> None:
        """Handles the request to delete a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user to delete.
            current_user (UserModel): The currently authenticated user making the request.
        """
        self._service.delete_user(user_id, current_user)
