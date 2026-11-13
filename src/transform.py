import pandas as pd

def transform_users(users: list[dict]) -> pd.DataFrame:
    """
    Transforms a list of user dictionaries into a pandas DataFrame.

    Args:
        users (list[dict]): A list of user dictionaries.

    Returns:
        pd.DataFrame: A DataFrame containing the transformed user data.
    """

    df = pd.json_normalize(users)

    df = df[
        [
            "id",
            "name",
            "username",
            "email",
            "address.city",
            "company.name",
        ]
    ].copy()

    df.columns = [
        "user_id",
        "name",
        "username",
        "email",
        "city",
        "company",
    ]

    df["email"] = df["email"].str.lower().str.strip()
    df["name"] = df["name"].str.strip()

    df = df.dropna(subset=["user_id", "email"])
    df = df.drop_duplicates(subset=["user_id"])    

    
    return df