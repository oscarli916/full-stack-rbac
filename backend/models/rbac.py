import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    user_has_role = relationship("UserHasRole", back_populates="user_id")
    group_has_user = relationship("GroupHasUser", back_populates="user_id")


class UserHasRole(Base):
    __tablename__ = "user_has_role"

    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    role_id = Column(UUID, ForeignKey("role.id"), nullable=False)


class Role(Base):
    __tablename__ = "role"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    user_has_role = relationship("UserHasRole", back_populates="role_id")
    role_has_permission = relationship("RoleHasPermission", back_populates="role_id")


class RoleHasPermission(Base):
    __tablename__ = "role_has_permission"

    role_id = Column(UUID, ForeignKey("role.id"), nullable=False)
    permission_id = Column(UUID, ForeignKey("permission.id"), nullable=False)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    role_has_permission = relationship(
        "RoleHasPermission", back_populates="permission_id"
    )


class Group(Base):
    __tablename__ = "group"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    role_id = relationship("Role")
    group_has_user = relationship("GroupHasUser", back_populates="group_id")


class GroupHasUser(Base):
    __tablename__ = "group_has_user"

    group_id = Column(UUID, ForeignKey("group.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
