from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db")
Session = sessionmaker(bind=engine)
session = Session()


class EquipmentQuality(Base):
    """
    装备品质
    """
    __tablename__ = 'equipment_quality'

    id = Column(Integer, primary_key=True)
    quality = Column(String, comment="品质")
    bonus = Column(Float, comment="对应加成（比例）")


# 增
def add_equipment_quality(quality: str, bonus: float):
    """
    Add a new equipment quality record to the database

    :param quality: string, name of the equipment quality
    :param bonus: integer, bonus percentage for the equipment quality
    :return: None
    """

    new_record = EquipmentQuality(quality=quality, bonus=bonus)
    session.add(new_record)
    session.commit()
    session.close()


# 删
def delete_equipment_quality(id: int):
    """
    删除装备品质记录
    :param id: 记录的id
    :return: None
    """
    equipment_quality = session.query(EquipmentQuality).filter_by(id=id).first()
    if equipment_quality:
        session.delete(equipment_quality)
        session.commit()


# 改
def update_equipment_quality(id: int, quality: int = None, bonus=None):
    """
    修改装备品质记录

    :param id: 记录的id
    :param quality: 新的品质
    :param bonus: 新的对应加成（比例）
    :return: 修改后的装备品质记录
    """
    equipment_quality = session.query(EquipmentQuality).get(id)
    if not equipment_quality:
        return None

    if quality:
        equipment_quality.quality = quality
    if bonus:
        equipment_quality.bonus = bonus

    session.commit()
    return equipment_quality


# 查
def get_equipment_quality_by_id(session, equipment_quality_id):
    """
    获取品质
    """
    return session.query(EquipmentQuality).filter_by(id=equipment_quality_id).first()
