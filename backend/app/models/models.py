from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Float, Integer, PrimaryKeyConstraint, Table, Text, Uuid, text, Boolean, Double
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
    weekly_allowance: Mapped[int] = mapped_column(Integer, server_default=text('100'))  # or whatever default
    purchased_credits: Mapped[float] = mapped_column(Double, server_default=text('0'))
    unlimited: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
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


# t_tokens = Table(
#     'tokens', Base.metadata,
#     Column('id', Uuid, nullable=False, server_default=text('gen_random_uuid()')),
#     Column('userid', Uuid, nullable=False),
#     Column('key', Text, nullable=False, server_default=text("'''hkdb_tkn_'' || gen_random_uuid()'::text")),
#     Column('dbid', Uuid, nullable=False),
#     Column('created_at', DateTime(True), nullable=True, server_default=text('now()')),
#     Column('name', Text, nullable=True, server_default=text("DB token")),
#     ForeignKeyConstraint(['dbid'], ['databases.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_dbid_fkey'),
#     ForeignKeyConstraint(['userid'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_userid_fkey')
# )

class Tokens(Base):
    __tablename__ = 'tokens'
    __table_args__ = (
        ForeignKeyConstraint(['dbid'], ['databases.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_dbid_fkey'),
        ForeignKeyConstraint(['userid'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='tokens_userid_fkey'),
        PrimaryKeyConstraint('id', name='tokens_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    userid: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    key: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'''hkdb_tkn_'' || gen_random_uuid()'::text"))
    dbid: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), nullable=True, server_default=text('now()'))
    name: Mapped[Optional[str]] = mapped_column(Text, nullable=True, server_default=text("DB token"))



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

# class SDKInstances(Base):

    
class CreditsHistory(Base):
    __tablename__ = 'credits_history'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='credits_history_user_id_fkey'),
        PrimaryKeyConstraint('id', name='credits_history_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    credits_spent: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    
class CLIAuthState(Base):
    __tablename__ = 'cli_auth_states'
    instance_id: Mapped[str] = mapped_column(Text, primary_key=True)
    slack_user_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)