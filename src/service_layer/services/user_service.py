from src.service_layer.unit_of_work import AbstractUnitOfWork

from src.adapters.orm.models import User, UserStorage
from src.adapters.storage_client import AbstractStorageClient, get_storage_client

from api.schemas import UserCreate, UserResponse

from src.utils import hash_password

from minio import S3Error


async def create_user(
    uow: AbstractUnitOfWork,
    user_data: UserCreate,
    storage_client: AbstractStorageClient,
):
    password_hash = hash_password(user_data.password)

    async with uow:
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )

        await uow.repo.add(user)

    try:
        storage_client.client.make_bucket(str(user.id))
    except S3Error as err:
        print(f"Failed to create bucket: {err}")

    async with uow:
        user_storage = UserStorage(
            user_fk=user.id, bucket_name=f"{user.username}-bucket"
        )

        await uow.repo.add(user_storage)

    UserResponse.model_validate(
        {
            "username": user.username,
            "email": user.email,
        }
    )
