from django.contrib.auth import get_user_model


def _user_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "last_login": user.last_login.strftime("%m/%d/%Y %I:%M:%S %p"),
    }


def update_user_information(user_id: int, updates: dict) -> str:
    """
    Update a user's name and/or email address.

    This function updates the user identified by the given user ID. The `updates` dictionary
    may contain either or both of the following keys: 'name' and 'email'. Fields not included
    in the dictionary will remain unchanged.

    Args:
        user_id (int): The unique ID of the user to update.
        updates (dict): A dictionary containing one or more of the fields to update.
                        Allowed keys are 'name' and/or 'email'.

    Returns:
        str: A message indicating whether the update was successful or if the user does not exist.
    """
    try:
        get_user_model().objects.filter(id=user_id).update(**updates)
        return f'User\'s information has been updated.'
    except get_user_model().DoesNotExist as e:
        return f'Error: User does not exist.'


def get_user_information(user_id: int) -> dict:
    """
    Retrieve user information by user ID.

    This function fetches a user from the database using the given user ID
    and returns their information as a dictionary. If no user is found,
    an empty dictionary is returned.

    Args:
        user_id (int): The unique ID of the user to retrieve.

    Returns:
        dict: A dictionary containing the user's information if found;
              otherwise, an empty dictionary.
    """
    try:
        user = get_user_model().objects.get(id=user_id)
        return _user_dict(user)
    except get_user_model().DoesNotExist:
        return {}
