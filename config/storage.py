# -*- coding: utf-8 -*-
import io
import uuid
from typing import List, Tuple, Union

from fastapi import UploadFile
from fastapi_helper import DefaultHTTPException
from PIL import Image, UnidentifiedImageError
from starlette import status


class ValidateFormatException(DefaultHTTPException):
    code = "format_error"
    type = "VALIDATE_IMAGE"
    message = "Format is not valid"
    status_code = status.HTTP_400_BAD_REQUEST


class StorageException(DefaultHTTPException):
    code = "storage_error"
    type = "DISCONNECTED_STORAGE"
    message = "An error occurred while trying to connect to the DO Spaces"
    status_code = status.HTTP_400_BAD_REQUEST


class SqlAlchemyStorage:
    def __init__(
        self,
        client,
        bucket: str,
    ):
        self.client = client
        self.bucket = bucket

    async def upload(
        self,
        file: UploadFile,
        upload_to: str,
        sizes: Union[Tuple[int, int], None],
        content_types: List[str],
    ) -> str:
        try:
            image = Image.open(file.file)
        except UnidentifiedImageError:
            raise ValidateFormatException(
                message=f"The uploaded file must be in the format {content_types}",
            )

        await self.validate_image(image, content_types)
        image_bytes = await self.image_processor(image, sizes)
        key = f"{upload_to}/image_{uuid.uuid4()}.png"
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=image_bytes,
                ACL="public-read",
                Metadata={
                    "Content-Type": "image/png",
                },
            )
            return key
        except Exception:
            raise StorageException()

    async def delete(self, key: str):
        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=key,
            )
        except Exception:
            raise StorageException()

    @staticmethod
    async def validate_image(image: Image, content_types: List[str]):
        if image.format.lower() not in content_types:
            raise ValidateFormatException(
                message=f"The uploaded file must be in the format {content_types}",
            )

    @staticmethod
    async def image_processor(
        image: Image,
        sizes: Tuple[int, int],
    ) -> bytes:
        if sizes:
            image = image.resize(sizes)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
