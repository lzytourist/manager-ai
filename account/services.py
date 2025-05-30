from django.contrib.auth import get_user_model


def get_user_fullname(user_id: int) -> str:
    """
    Gets user full name from user id.
    :param user_id: int
    :return: str
    """
    try:
        user = get_user_model().objects.get(id=user_id)
        return user.name
    except get_user_model().DoesNotExist as e:
        print('error', str(e))
        return f'Error: could not get user fullname'


def update_user_fullname(user_id: int, name: str) -> str:
    """
    Updates full name of user.
    :param user_id: int
    :param name: str
    :returns: full name
    """
    try:
        print('Updating name')
        get_user_model().objects.filter(id=user_id).update(name=name)
        return f'User\'s name has been updated.'
    except get_user_model().DoesNotExist as e:
        print('error', str(e))
        return f'Error: User does not exist: {name}.'
