from __future__ import annotations

from typing import List
from datetime import date, time

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship


Base = declarative_base()
base_metadata = Base.metadata

class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # 1:M, у комнаты может не быть слотов
    slots: Mapped[List[Slot]] = relationship(back_populates="room",
                                             cascade="all, delete",
                                             passive_deletes=True)


class Slot(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    start_time: Mapped[time] = mapped_column(nullable=False)
    end_time: Mapped[time] = mapped_column(nullable=False)
    slot_date: Mapped[date] = mapped_column(nullable=False)
    # M:1, у слота всегда есть родитель-комната
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    room: Mapped[Room] = relationship(back_populates="slots")
    # 1:1, у слота может не быть резерваций
    reservations: Mapped[Reservation] = relationship(back_populates="slot",
                                                     cascade="all, delete",
                                                     passive_deletes=True)

    # Слоты могут начинаться и заканчиваться только в пределах одного дня - проверка не учитывает дату
    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_slot_times'),
    )

class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates="reservations")
    # M:1, у резервации всегда есть родитель-слот, на один слот может быть только одна резервация
    slot_id: Mapped[int] = mapped_column(ForeignKey("slot.id", ondelete="CASCADE"), nullable=False, unique=True)
    slot: Mapped[Slot] = relationship(back_populates="reservations")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    # Делаем bool, потому что на данный момент роли всего две - потом можно расширить, изменив поле на таблицу ролей
    is_admin: Mapped[bool] = mapped_column(nullable=False)
    # 1:M, у пользователя может не быть резерваций
    reservations: Mapped[List[Reservation]] = relationship(back_populates="user",
                                                           cascade="all, delete",
                                                           passive_deletes=True)