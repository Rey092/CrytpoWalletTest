# -*- coding: utf-8 -*-

from boto3 import Session
from fastapi import UploadFile


class SqlAlchemyStorage:
    def __init__(
        self,
        client: Session,
    ):
        self.client = client

    async def get_image(self, image: UploadFile):
        print(image.file.read())
        return None


#
# class Json(TypeDecorator):
#     impl = Unicode
#
#     def process_bind_param(self, value, engine):
#         return json.dumps(value)
#
#     def process_result_value(self, value, engine):
#         if value is None:
#             return None
#
#         return json.loads(value)
#
#
# class ProfileImage(Image):
#     __pre_processors__ = [
#         ImageAnalyzer(),
#         ImageValidator(
#             minimum=(80, 80),
#             maximum=(800, 600),
#             min_aspect_ratio=1.2,
#             content_types=['image/jpeg', 'image/png']
#         ),
#         ImageProcessor(
#             fmt='jpeg',
#             width=120,
#             crop=dict(
#                 left='10%',
#                 top='10%',
#                 width='80%',
#                 height='80%',
#             )
#         )
#     ]
#
#
# # class Person(Base):
# #     __tablename__ = 'person'
# #
# #     id = Column(Integer, primary_key=True)
# #     name = Column(Unicode(100))
# #     image = Column(ProfileImage.as_mutable(Json))
# #
# #     def __repr__(self):
# #         return "<%s id=%s>" % (self.name, self.id)
#
#
# if __name__ == '__main__':
#     session = session_factory()
#
#     with StoreManager(session):
#         person1 = Person()
#         person1.image = ProfileImage.create_from('https://www.python.org/static/img/python-logo@2x.png')
#         session.add(person1)
#         session.commit()
#
#         print('Content type:', person1.image.content_type)
#         print('Extension:', person1.image.extension)
#         print('Length:', person1.image.length)
#         print('Original filename:', person1.image.original_filename)
#
#         thumbnail = person1.image.get_thumbnail(width=32, auto_generate=True)
#         print(thumbnail.height)
#         assert exists(join(TEMP_PATH, thumbnail.path))
#
#         thumbnail = person1.image.get_thumbnail(ratio=.3, auto_generate=True)
#         print(thumbnail.width, thumbnail.height)
#         assert exists(join(TEMP_PATH, thumbnail.path))
#
#         person1.image.attach('https://www.python.org/static/img/python-logo.png')
#         session.commit()
#
#         print('Content type:', person1.image.content_type)
#         print('Extension:', person1.image.extension)
#         print('Length:', person1.image.length)
#         print('Original filename:', person1.image.original_filename)
#
#     with StoreManager(session, delete_orphan=True):
#         deleted_filename = join(TEMP_PATH, person1.image.path)
#         person1.image = None
#         session.commit()
#
#         assert not exists(deleted_filename)
#
#         person1.image = ProfileImage.create_from('https://www.python.org/static/img/python-logo.png')
#         session.commit()
#
#         print('Content type:', person1.image.content_type)
#         print('Extension:', person1.image.extension)
#         print('Length:', person1.image.length)
#         print('Original filename:', person1.image.original_filename)
