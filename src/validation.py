from pydantic import ValidationError
from src.schemas import UserSchema

def validate_users(users: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Validate user records individually.

    Returns:
        tuple:
            - Validated user records.
            - Rejected records with validation errors.
    """

    valid_users = []
    rejected_users = []

    for index, user in enumerate(users):

        try:
            validated_user = UserSchema.model_validate(user)

            valid_users.append(
                validated_user.model_dump(mode="json")
            )

        except ValidationError as exc:
            rejected_users.append({
                "record_index": index,
                "record_data": user,
                "errors": exc.errors(include_url=False)
            })
    return valid_users, rejected_users


