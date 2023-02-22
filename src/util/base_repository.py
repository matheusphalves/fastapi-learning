#    MIT License
#
#    Copyright (c) 2023 Matheus Phelipe Alves Pinto
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

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

    def update(self, db: Session, entityUpdated: any) -> any:

        query_result = db.query(self.entityModel).filter(self.entityModel.id == entityUpdated.id)

        if query_result is not None:
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

    def related_fk_exists(self, db: Session, entityRelatedModel: any, fkId: int) -> bool:
        return db.query(entityRelatedModel).filter(entityRelatedModel.id == fkId).first() is not None

    def related_relationship_exists(self, db: Session, entityRelatedModel: any, pkId: int, fkId: int) -> bool:

        child_entity = self.find_by_id(db, pkId)

        if child_entity is not None:
            return db.query(entityRelatedModel).filter(entityRelatedModel.id == fkId).first() is not None

        return False
