# -*- coding: utf-8 -*-
from api_service.config.settings import settings

SQLALCHEMY_DATABASE_URL = str(settings.test_db_url)

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base.metadata.create_all(bind=engine)
#
#
# def override_get_db():
#     connection = engine.connect()
#
#     # begin a non-ORM transaction
#     transaction = connection.begin()
#
#     # bind an individual Session to the connection
#     db = TestingSessionLocal(bind=connection)
#     # db = Session(engine)
#
#     yield db
#
#     db.close()
#     transaction.rollback()
#     connection.close()
#
#
# app.dependency_overrides[get_db] = override_get_db
