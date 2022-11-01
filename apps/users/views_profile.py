# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.users.dependencies import get_db, get_user_manager
from apps.users.manager import UserManager
from apps.users.models import User
from apps.users.schemas import UserUpdate
from apps.users.user import get_current_user

profile_router = APIRouter()


@profile_router.get("/get")
async def get_profile(
    user=Depends(get_current_user),
):
    return user


@profile_router.put("/update")
async def update_profile(
    user_data: UserUpdate = Depends(UserUpdate.as_form),
    user: User = Depends(get_current_user),
    user_manager: UserManager = Depends(get_user_manager),
    db: Session = Depends(get_db),
):
    result = await user_manager.update(
        user.id,
        user_data,
        db,
    )
    # file = user_image.file.read()
    #
    # client.put_object(Bucket='cryptowallet',
    #                   Key='test4.png',
    #                   Body=file,
    #                   ACL='public-read',
    #                   Metadata={
    #                       'Content-Type': user_image.content_type
    #                   }
    #                   )
    #
    # client.delete_object(Bucket='cryptowallet',
    #                      Key='Без названия.png')

    # client.upload_fileobj(
    #     file, 'cryptowallet', 'test3.png',
    #     ExtraArgs={'Metadata': {'mykey': 'myvalue'}}
    # )

    # url = client.generate_presigned_url(ClientMethod='get_object',
    #                                     Params={'Bucket': 'cryptowallet',
    #                                             'Key': 'Без названия.png'},
    #                                     ExpiresIn=300)

    # print(url)

    return result
