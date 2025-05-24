from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Table, Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    slack_access_token: Mapped[str] = mapped_column(Text)
    slack_user_id : Mapped[str] = mapped_column(Text)
    username: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    quota: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('100'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    databases: Mapped[List['Databases']] = relationship('Databases', back_populates='users')


class Databases(Base):
    __tablename__ = 'databases'
    __table_args__ = (
        ForeignKeyConstraint(['owner'], ['users.id'], ondelete='CASCADE', name='databases_owner_fkey'),
        PrimaryKeyConstraint('id', name='databases_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    owner: Mapped[uuid.UUID] = mapped_column(Uuid)
    name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    users: Mapped['Users'] = relationship('Users', back_populates='databases')
    usertables: Mapped[List['Usertables']] = relationship('Usertables', back_populates='databases')


t_tokens = Table(
    'tokens', Base.metadata,
    Column('id', Uuid, nullable=False, server_default=text('gen_random_uuid()')),
    Column('userid', Uuid, nullable=False),
    Column('key', Text, nullable=False, server_default=text("'''hkdb_tkn_'' || gen_random_uuid()'::text")),
    Column('dbid', Uuid, nullable=False),
    Column('created_at', DateTime(True), nullable=True, server_default=text('now()')),
    Column('name', Text, nullable=True, server_default=text("DB token")),
    ForeignKeyConstraint(['dbid'], ['databases.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_dbid_fkey'),
    ForeignKeyConstraint(['userid'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_userid_fkey')
)


class Usertables(Base):
    __tablename__ = 'usertables'
    __table_args__ = (
        ForeignKeyConstraint(['db'], ['databases.id'], ondelete='CASCADE', name='usertables_db_fkey'),
        PrimaryKeyConstraint('id', name='usertables_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(Text)
    db: Mapped[uuid.UUID] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    databases: Mapped['Databases'] = relationship('Databases', back_populates='usertables')
