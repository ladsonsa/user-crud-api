from app.dtos.user_create import UserCreateDTO
from app.dtos.user_update import UserUpdateDTO
from app.models.user_model import UserModel
from app.workflows.create_user import CreateUserWorkflow
from app.workflows.delete_user import DeleteUserWorkflow
from app.workflows.get_user import GetUserWorkflow
from app.workflows.list_users import ListUsersWorkflow
from app.workflows.update_user import UpdateUserWorkflow


class UserService:
    """Service layer coordinating execution of user-related workflows.

    Attributes:
        _create_workflow (CreateUserWorkflow): Workflow for creating new users.
        _list_workflow (ListUsersWorkflow): Workflow for retrieving all users.
        _get_workflow (GetUserWorkflow): Workflow for fetching a single user.
        _update_workflow (UpdateUserWorkflow): Workflow for updating an existing user.
        _delete_workflow (DeleteUserWorkflow): Workflow for removing a user.
    """

    def __init__(
        self,
        create_workflow: CreateUserWorkflow,
        list_workflow: ListUsersWorkflow,
        get_workflow: GetUserWorkflow,
        update_workflow: UpdateUserWorkflow,
        delete_workflow: DeleteUserWorkflow,
    ) -> None:
        """Initializes the service with required user management workflows.

        Args:
            create_workflow (CreateUserWorkflow): Workflow instance for user creation.
            list_workflow (ListUsersWorkflow): Workflow instance for listing users.
            get_workflow (GetUserWorkflow): Workflow instance for fetching a user.
            update_workflow (UpdateUserWorkflow): Workflow instance for user updates.
            delete_workflow (DeleteUserWorkflow): Workflow instance for user deletion.
        """
        self._create_workflow = create_workflow
        self._list_workflow = list_workflow
        self._get_workflow = get_workflow
        self._update_workflow = update_workflow
        self._delete_workflow = delete_workflow

    def create_user(self, data: UserCreateDTO) -> UserModel:
        """Delegates the user creation process to the create workflow.

        Args:
            data (UserCreateDTO): Data transfer object containing new user details.

        Returns:
            UserModel: The newly created user model instance.
        """
        return self._create_workflow.execute(data)

    def list_users(self) -> list[UserModel]:
        """Delegates the retrieval of all users to the list workflow.

        Returns:
            list[UserModel]: A list containing all user model instances.
        """
        return self._list_workflow.execute()

    def get_user(self, user_id: int) -> UserModel:
        """Delegates fetching a single user by ID to the get workflow.

        Args:
            user_id (int): Unique identifier of the user to retrieve.

        Returns:
            UserModel: The corresponding user model instance.
        """
        return self._get_workflow.execute(user_id)

    def update_user(self, user_id: int, data: UserUpdateDTO) -> UserModel:
        """Delegates the user update process to the update workflow.

        Args:
            user_id (int): Unique identifier of the user to update.
            data (UserUpdateDTO): Data transfer object containing fields to update.

        Returns:
            UserModel: The updated user model instance.
        """
        return self._update_workflow.execute(user_id, data)

    def delete_user(self, user_id: int) -> None:
        """Delegates the user deletion process to the delete workflow.

        Args:
            user_id (int): Unique identifier of the user to delete.
        """
        self._delete_workflow.execute(user_id)
