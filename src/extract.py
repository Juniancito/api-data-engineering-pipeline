import requests

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def create_http_session() -> Session:
    """
        Create an HTTP session with retry configuration for handling transient errors.
    """

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1,
        backoff_jitter=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def extract_users(api_url: str)-> list[dict]:
    """
        Extract users from an external API with automatic retries
    """

    with create_http_session() as session:

        try:
            response = session.get(
                api_url,
                timeout=(5, 30)
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise ValueError(
                    "Expected a list of users from the API response"
                )

            return data

        except requests.RequestException as exc:
            raise RuntimeError(
                f"Failed to extract users from API: {exc}"
            ) from exc
