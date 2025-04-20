from django.contrib.auth.models import User

from finance.logger import logger


def check_if_user_exists(username: str) -> bool:
    """
    Check if a user with the given username exists in the database.

    Args:
        username (str): The username to check.

    Returns:
        bool: If the user exists
    """
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


@logger.catch
def create_user(username: str, email: str) -> User | None:
    """
    Create a new user.

    Args:
        username (str): username of the user
        email (str): email of the user

    Returns:
        User | None: The created user object
    """
    try:
        user = User.objects.create_user(
            username=username,
            email=email
        )
        return user
    except Exception:
        return None
