from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas.users import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Get a User by its id.

        Args:
            user_id: The id of the User to retrieve.

        Returns:
            The User with the specified id, or None if no such User exists.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Get a User by its username.

        Args:
            username: The username of the User to retrieve.

        Returns:
            The User with the specified username, or None if no such User exists.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get a User by its email.

        Args:
            email: The username of the User to retrieve.

        Returns:
            The User with the specified email, or None if no such User exists.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new User with the given attributes.

        Args:
            body: A UserCreate with the attributes to assign to the User.
            avatar: Generated avatar image in str format.

        Returns:
            A User with the assigned attributes.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Sets User's 'confirmed' attribute to True.

        Args:
            email: Email of the User

        Returns:
            None
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()
