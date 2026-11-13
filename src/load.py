import pandas as pd
from sqlalchemy import create_engine, text

def load_users(df: pd.DataFrame, database_url: str) -> int:

    engine = create_engine(database_url)

    create_table = text("""
        CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        name VARCHAR(150),
        username VARCHAR(100),
        email VARCHAR(200),
        city VARCHAR(100),
        company VARCHAR(150)
        );
    """)

    upsert = text("""
        INSERT INTO users (
        user_id, name, username, email, city, company
        ) VALUES (
            :user_id, :name, :username, :email, :city, :company
        )
        ON CONFLICT (user_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            username = EXCLUDED.username,
            email = EXCLUDED.email,
            city = EXCLUDED.city,
            company = EXCLUDED.company;
    """)

    records = df.to_dict(orient="records")

    with engine.begin() as connection:

        connection.execute(create_table)

        if records:
            connection.execute(upsert, records)

    engine.dispose()

    return len(records)
