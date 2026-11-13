import pandas as pd

OUTPUT_COLUMNS = [

    "user_id",
    "name",
    "username",
    "email",
    "city",
    "company",

]

SOURCE_COLUMNS = [

    "id",
    "name",
    "username",
    "email",
    "address.city",
    "company.name",

]


def transform_users(users: list[dict]) -> pd.DataFrame:
    """
    Normalize and clean user records.

    Returns:
        pd.DataFrame: Cleaned users with a consistent schema.
    """

    if not users:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    df = pd.json_normalize(users)

    df = df.reindex(columns=SOURCE_COLUMNS)

    df.columns = OUTPUT_COLUMNS

    # Normalize text fields.
    df["name"] = df["name"].astype("string").str.strip()
    df["email"] = (
        df["email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Remove records without a valid user ID or email
    df = df.dropna(subset=["user_id", "email"])
    df = df[df["email"].ne("")]

    # Keep only the first occurrence of each user ID
    df = df.drop_duplicates(subset=["user_id"], keep="first")

    return df.reset_index(drop=True)