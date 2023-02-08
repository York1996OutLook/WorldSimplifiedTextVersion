from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import EmailType

Base = declarative_base()

from ..session import session


class PlayerMailRecord(Base):
    """
    用户右键记录表
    """
    __tablename__ = 'player_mail_record'

    id = Column(Integer, primary_key=True)

    send_character_id = Column(Integer, comment="邮件发送人的 character_id。如果是游戏管理员，需要在设置表中指定游戏管理员的ID；")
    received_character_id = Column(Integer, comment="邮件接收人的 character_id")

    give_stuff_id = Column(Integer, comment="赠送物品的id。只有未绑定的物品才可以邮寄给别人。暂定最多赠送一件物品。")

    charge = Column(Integer, comment="收费黄金数量，如果要接受邮件需要付费的数量")
    give = Column(Integer, comment="赠送黄金数量，不仅赠送给人物品，还赠送给别人黄金")

    mail_type = Column(Integer, comment="邮件类型，参考EmailType")

    addition_message = Column(Integer, comment="邮件发送的时候的附加信息，接受放能够看到；")
    send_timestamp = Column(Integer, comment="邮件发送的时间")
