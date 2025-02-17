from datetime import date
from typing import List

import sqlalchemy
from sqlalchemy import select, or_, extract, func, Integer, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.sqltypes import Date, DateTime

from src.database.models import Contact, User
from src.schemas.contacts import ContactBase, ContactResponse


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int, user: User) -> List[Contact]:
        stmt = select(Contact).filter_by(user=user).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def search_contact(self, q: str, skip: int, limit: int, user: User):
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .filter(
                or_(
                    Contact.name.ilike(f"%{q}%"),
                    Contact.surname.ilike(f"%{q}%"),
                    Contact.email.ilike(f"%{q}%"),
                    Contact.phone.ilike(f"%{q}%"),
                )
            )
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_birthdays(
        self, days: int, skip: int, limit: int, user: User
    ) -> List[Contact]:
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .where(
                (
                    func.make_date(
                        date.today().year,
                        cast(func.extract("month", Contact.birthday), Integer),
                        cast(func.extract("day", Contact.birthday), Integer),
                    )
                    - date.today()
                )
                <= days
            )
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id, user)

    async def delete_contact(self, contact_id: int, user: User) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactBase, user: User
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact
