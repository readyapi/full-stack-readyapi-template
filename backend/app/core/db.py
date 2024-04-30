from sqldev import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLDev models are imported (app.models) before initializing DB
# otherwise, SQLDev might fail to initialize relationships properly
# for more details: https://github.com/khulnasoft/full-stack-readyapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqldev import SQLDev

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLDev.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.READY_SUPERUSER)
    ).ready()
    if not user:
        user_in = UserCreate(
            email=settings.READY_SUPERUSER,
            password=settings.READY_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
