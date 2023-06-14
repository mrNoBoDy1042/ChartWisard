from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from app.config import settings


cookie = SessionCookie(
    cookie_name=f'{settings.app_name}_cookie',
    identifier='general_verifier',
    auto_error=True,
    secret_key=settings.cookie_secret_key,
    cookie_params=CookieParameters(),
)