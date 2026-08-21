from app.dtos.user_create import UserCreateDTO
from app.dtos.user_response import UserResponseDTO
from app.dtos.user_update import UserUpdateDTO
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

    def get_user(self, user_id: int) -> UserResponseDTO:
        """Handles the HTTP request to fetch a specific user by identifier.

        Args:
            user_id (int): Unique identifier of the user to retrieve.

        Returns:
            UserResponseDTO: Response DTO containing the requested user's details.
        """
        user = self._service.get_user(user_id)
        return UserResponseDTO.model_validate(user)

    def update_user(
        self,
        user_id: int,
        data: UserUpdateDTO,
    ) -> UserResponseDTO:
        """Handles the HTTP request to update an existing user's details.

        Args:
            user_id (int): Unique identifier of the user to update.
            data (UserUpdateDTO): Data transfer object containing updated fields.

        Returns:
            UserResponseDTO: Response DTO representing the updated user state.
        """
        user = self._service.update_user(user_id, data)
        return UserResponseDTO.model_validate(user)

    def delete_user(self, user_id: int) -> None:
        """Handles the HTTP request to remove a user from the system.

        Args:
            user_id (int): Unique identifier of the user to delete.
        """
        self._service.delete_user(user_id)
