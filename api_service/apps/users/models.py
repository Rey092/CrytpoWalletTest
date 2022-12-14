# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api_service.config.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String)
    is_active = Column(Boolean, default=True)
    count_messages = Column(Integer, default=0)

    permission = relationship("Permission", backref="user", uselist=False)
    wallets = relationship("Wallet", backref="user")


class Permission(Base):
    __tablename__ = "permission"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    has_access_chat = Column(Boolean, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
