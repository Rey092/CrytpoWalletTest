# # -*- coding: utf-8 -*-
# """
# FastAPI Users database adapter for Tortoise ORM.
# """
# import random
# from typing import Optional, Tuple, Type, TypeVar
#
# from fastapi_users.db import BaseUserDatabase
# from pydantic import UUID4
# from tortoise.models import Model
#
# from apps.users.models import NewPasswordToken, User
#
# UD = TypeVar("UD")
#
#
# class TortoiseUserDatabase(BaseUserDatabase):
#     """
#     Database adapter for Tortoise ORM.
#
#     :param user_model: Tortoise ORM model.
#     :param oauth_account_model: Optional Tortoise ORM model of a OAuth account.
#
#     """
#
#     schema: Type[UD]
#     model: Type[User]
#     oauth_account_model: Optional[Type[Model]]
#
#     def __init__(
#         self,
#         user_model: Type[User],
#         oauth_account_model: Optional[Type[Model]] = None,
#         new_password_token_model: NewPasswordToken = NewPasswordToken,
#     ):
#         self.model = user_model
#         self.oauth_account_model = oauth_account_model
#         self.new_password_token_model = new_password_token_model
#
#     async def get(self, id: UUID4) -> User:
#         return await self.model.get(id=id)
#
#     async def get_by_email(self, email: str) -> Optional[UD]:
#         query = self.model.filter(email__iexact=email).first()
#
#         if self.oauth_account_model is not None:
#             query = query.prefetch_related("oauth_accounts")
#
#         user = await query
#
#         return user
#
#     async def create(self, user_dict: UD) -> UD:
#         user = self.model(**user_dict)
#         await user.save()
#
#         return user
#
#     async def generate_nickname_number(self, nickname: str) -> str:
#         query = self.model.filter(nickname__iexact=nickname).values("nickname_number")
#         nickname_numbers = list(await query)
#         while True:
#             nickname_number = random.randint(0, 9999)
#             if nickname_number not in nickname_numbers:
#                 break
#         return str(nickname_number).zfill(4)
#
#     async def update(self, user: UD) -> UD:
#         raise NotImplementedError
#         # user_dict = user.dict()
#         # user_dict.pop("id")  # Tortoise complains if we pass the PK again
#         # oauth_accounts = user_dict.pop("oauth_accounts", None)
#         #
#         # model = await self.model.get(id=user.id)
#         # for field in user_dict:
#         #     setattr(model, field, user_dict[field])
#         # await model.save()
#         #
#         # if oauth_accounts and self.oauth_account_model:
#         #     await model.oauth_accounts.all().delete()  # type: ignore
#         #     oauth_account_objects = []
#         #     for oauth_account in oauth_accounts:
#         #         oauth_account_objects.append(
#         #             self.oauth_account_model(user=model, **oauth_account),
#         #         )
#         #     await self.oauth_account_model.bulk_create(oauth_account_objects)
#         #
#         # return user
#
#     async def delete(self, user: UD) -> None:
#         await self.model.filter(id=user.id).delete()
#
#     async def request_new_password(self, email: str, token_hash: str, new_password: str) -> str:
#         new_password_token, created = await self.new_password_token_model.request_new_password(
#             email=email,
#             token_hash=token_hash,
#             new_password=new_password,
#         )
#         return new_password_token.new_password
#
#     async def get_confirm_new_password_user(self, token_hash: str) -> Tuple[Optional[User], Optional[str]]:
#         query = self.new_password_token_model.filter(token_hash=token_hash)
#         new_password_token = await query.first()
#
#         if new_password_token:
#             email = new_password_token.email
#             user = await self.model.filter(email=email).first()
#             await new_password_token.delete()
#             return user, new_password_token.new_password
#
#         else:
#             return None, None
#
#     @staticmethod
#     async def set_new_password(user: User, new_password: str) -> None:
#         user.hashed_password = new_password
#         await user.save()
