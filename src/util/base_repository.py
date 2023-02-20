from typing import List
from sqlalchemy.orm import Session


class BaseRepository:
    entityModel: any

    def find_all(self, db: Session) -> List[any]:
        return db.query(self.entityModel).all()

    def save(self, db: Session, entity: any) -> any:
        if entity.id:
            db.merge(entity)
        else:
            db.add(entity)
        db.commit()
        return entity

    def update(self, db: Session, entityUpdated: any, columnName: str, matchValue: any) -> any:

        query_result = self.find_by_custom_column_value(db, columnName=columnName, matchValue=matchValue)
        if query_result.first() is not None:
            fields_to_update = vars(entityUpdated).pop("_sa_instance_state")
            query_result.update(fields_to_update.dict)
            db.flush()
            db.commit()
            return query_result.first()

        return None

    def find_by_custom_column_value(self, db: Session, columnName: str, matchValue: any) -> any:

        if hasattr(self.entityModel, columnName):
            return db.query(self.entityModel).filter(vars(self.entityModel)[columnName] == matchValue)

        return None




    def find_by_id(self, db: Session, id: int) -> any:
        return db.query(self.entityModel).filter(self.entityModel.id == id).first()

    def exists_by_id(self, db: Session, id: int) -> bool:
        return db.query(self.entityModel).filter(self.entityModel.id == id).first() is not None

    def delete_by_id(self, db: Session, id: int) -> None:
        entity = db.query(self.entityModel).filter(self.entityModel.id == id).first()
        if entity is not None:
            db.delete(entity)
            db.commit()
