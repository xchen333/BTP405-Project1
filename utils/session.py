import uuid

from sqlalchemy.orm import sessionmaker
from database.models import engine


def create_session():
    session = sessionmaker(bind=engine)
    return session()


def serialize_entity(entity):
    if entity:
        serialized_entity = {}
        for column in entity.__table__.columns:
            value = getattr(entity, column.name)
            # Convert UUID to string if the attribute is of type UUID
            if isinstance(value, uuid.UUID):
                value = str(value)
            serialized_entity[column.name] = value
        return serialized_entity
    return {}


def get_all_entities(model, filters=None):
    session = create_session()
    try:
        entities = session.query(model).filter_by(**filters).all() if filters else session.query(model).all()
        return [serialize_entity(entity) for entity in entities]
    finally:
        session.close()


def get_entity_by_uuid(model, entity_uuid):
    session = create_session()
    try:
        entity = session.query(model).get(entity_uuid)
        return serialize_entity(entity) if entity else None
    finally:
        session.close()


def create_entity(model, data):
    session = create_session()
    try:
        new_entity = model(**data)
        session.add(new_entity)
        session.commit()
        return new_entity
    finally:
        session.close()


def update_entity(model, entity_uuid, data):
    session = create_session()
    try:
        existing_entity = session.query(model).get(entity_uuid)
        if existing_entity:
            for key, value in data.items():
                setattr(existing_entity, key, value)
            session.commit()
        return existing_entity
    finally:
        session.close()


def delete_entity(model, entity_uuid):
    session = create_session()
    try:
        entity_to_delete = session.query(model).get(entity_uuid)
        if entity_to_delete:
            session.delete(entity_to_delete)
            session.commit()
        return entity_to_delete
    finally:
        session.close()
