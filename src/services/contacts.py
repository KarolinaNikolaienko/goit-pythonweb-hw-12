from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactBase, ContactResponse


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User):
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, user: User):
        return await self.contact_repository.get_contacts(skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def search_contact(self, q: str, skip: int, limit: int, user: User):
        return await self.contact_repository.search_contact(q, skip, limit, user)

    async def update_contact(self, contact_id: int, body: ContactBase, user: User):
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def delete_contact(self, contact_id: int, user: User):
        return await self.contact_repository.delete_contact(contact_id, user)

    async def get_birthdays(self, days: int, skip: int, limit: int, user: User):
        return await self.contact_repository.get_birthdays(days, skip, limit, user)
