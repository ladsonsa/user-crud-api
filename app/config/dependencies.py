from sqlalchemy.orm import Session

from app.controllers.user_controller import UserController
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.workflows.create_user import CreateUserWorkflow
from app.workflows.delete_user import DeleteUserWorkflow
from app.workflows.get_user import GetUserWorkflow
from app.workflows.list_users import ListUsersWorkflow
from app.workflows.update_user import UpdateUserWorkflow


def get_user_controller(session: Session) -> UserController:
    """Assembles and injects dependencies required to instantiate a UserController.

    Constructs the repository, workflows, and service instances using the provided
    SQLAlchemy database session.

    Args:
        session (Session): The active database session used for transaction management.

    Returns:
        UserController: A fully configured controller instance with injected dependencies.
    """
    repository = SQLAlchemyUserRepository(session)

    service = UserService(
        create_workflow=CreateUserWorkflow(repository),
        list_workflow=ListUsersWorkflow(repository),
        get_workflow=GetUserWorkflow(repository),
        update_workflow=UpdateUserWorkflow(repository),
        delete_workflow=DeleteUserWorkflow(repository),
    )

    return UserController(service)
