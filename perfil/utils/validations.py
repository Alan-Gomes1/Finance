import re

from django.core.exceptions import ValidationError


def clean_username(username: str) -> None | ValueError:
    """Valida o nome de usuário

    Args:
        username (str): nome do usuário

    Raises:
        ValidationError: O nome de usuário deve ter pelo menos 4 caracteres

    Returns:
        None | ValueError: None
    """
    if len(username) < 4:
        raise ValidationError(
            "O nome de usuário deve ter pelo menos 4 caracteres"
        )


def clean_password(password: str) -> None | ValueError:
    """Valida a senha do usuário

    Args:
        password (str): senha

    Raises:
        ValidationError: A senha deve ter pelo menos 8 caracteres
        ValidationError: A senha deve conter pelo menos um número
        ValidationError: A senha deve conter pelo menos uma letra maiúscula

    Returns:
        None | ValueError: None
    """
    if len(password) < 8:
        raise ValidationError(
            "A senha deve ter pelo menos 8 caracteres"
        )

    if not re.search(r"\d", password):
        raise ValidationError(
            "A senha deve conter pelo menos um número"
        )

    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            "A senha deve conter pelo menos uma letra maiúscula"
        )


def clean_email(email: str) -> None | ValueError:
    """Valida o email

    Args:
        email (str): email

    Raises:
        ValidationError: O email deve ter pelo menos 5 caracteres
        ValidationError: Formato de email inválido

    Returns:
        None | ValueError: None
    """
    if len(email) < 5:
        raise ValidationError(
            "O email deve ter pelo menos 5 caracteres"
        )

    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, email):
        raise ValidationError(
            "Formato de email inválido"
        )
