from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean

from Enums import MailType
from Utils.tools import find_smallest_missing

Base = declarative_base()

from DBHelper.session import session


class PlayerMailRecord(Base):
    """
    用户邮件记录表
    """
    __tablename__ = 'player_mail_record'

    id = Column(Integer, primary_key=True)

    send_character_id = Column(Integer, comment="邮件发送人的 character_id。如果是游戏管理员，需要在设置表中指定游戏管理员的ID；")
    received_character_id = Column(Integer, comment="邮件接收人的 character_id")
    mail_position_index = Column(Integer, comment="邮件所占用位置的索引，从1开始；")

    give_stuff_record_id = Column(Integer, comment="赠送物品的id。只有未绑定的物品才可以邮寄给别人。暂定最多赠送一件物品。")

    charge = Column(Integer, comment="收费黄金数量，如果要接受邮件需要付费的数量")
    give = Column(Integer, comment="赠送黄金数量，不仅赠送给人物品，还赠送给别人黄金")

    mail_type = Column(Integer, comment="邮件类型，参考MailType")

    is_already_read = Column(Boolean, comment="是否已经打开过了")

    addition_message = Column(Integer, comment="邮件发送的时候的附加信息，接受放能够看到；")
    send_timestamp = Column(Integer, comment="邮件发送的时间")


# 增
def add(*,
        send_character_id: int,
        received_character_id: int,
        mail_position_index: int,
        give_stuff_id: int,
        charge: int,
        give: int,
        mail_type: int,
        is_already_read: bool,
        addition_message: int,
        send_timestamp: int
        ):
    """
    增加一条邮件记录
    :param send_character_id: 邮件发送人的 character_id
    :param received_character_id: 邮件接收人的 character_id
    :param mail_position_index: 邮件的位置
    :param give_stuff_id: 赠送物品的id
    :param charge: 收费黄金数量
    :param give: 赠送黄金数量
    :param mail_type: 邮件类型
    :param is_already_read: 是否已经读过了
    :param addition_message: 邮件发送的时候的附加信息
    :param send_timestamp: 邮件发送的时间
    """
    new_record = PlayerMailRecord(
        send_character_id=send_character_id,
        received_character_id=received_character_id,
        mail_position_index=mail_position_index,
        give_stuff_id=give_stuff_id,
        charge=charge,
        give=give,
        mail_type=mail_type,
        is_already_read=is_already_read,
        addition_message=addition_message,
        send_timestamp=send_timestamp
    )
    session.add(new_record)
    session.commit()


# 删
def delete_by_mail_id(*, record_id: int):
    """
    删除指定的邮件记录
    :param record_id: 邮件记录的ID
    """
    session.query(PlayerMailRecord).filter(PlayerMailRecord.id == record_id).delete()
    session.commit()


# 改
def update_read_status(*, mail_id: int, is_read: bool) -> PlayerMailRecord:
    """
    修改某个邮件的已读状态
    :param mail_id: 邮件id
    :param is_read: 是否已读，True/False
    :return: None
    """
    mail = session.query(PlayerMailRecord).filter(PlayerMailRecord.id == mail_id).first()
    mail.is_already_read = is_read
    session.commit()
    session.refresh(mail)
    return mail


def update_type_by_record_id(*, mail_record_id: int, new_mail_type: MailType):
    """
    修改某个邮件的类型
    :param mail_record_id: 邮件id
    :param new_mail_type: 新的邮件类型
    :return: None
    """
    mail = session.query(PlayerMailRecord).filter(PlayerMailRecord.id == mail_record_id).first()
    mail.mail_type = new_mail_type
    session.commit()
    session.refresh(mail)
    return mail


# 查
def get_all_for_character(*, character_id: int) -> List[PlayerMailRecord]:
    """
    获取某个人所有可见的邮件，包括发送的（一直可见），接受的（收到邮件后选择了拒收，则后续将看不到这个邮件）
    :param character_id:
    :return:
    """
    return session.query(PlayerMailRecord).filter(
        (
                PlayerMailRecord.received_character_id == character_id and PlayerMailRecord.mail_type != MailType.SEND_TO_OTHER_PLAYER_GET_REJECT)
        |
        (PlayerMailRecord.send_character_id == character_id)).all()


def get_all_by_character_id(*, character_id: int) -> PlayerMailRecord:
    """
    根据玩家邮件记录来查询
    :param character_id:
    :return:
    """
    return session.query(PlayerMailRecord).filter(PlayerMailRecord.send_character_id == character_id).all()


def get_by_record_id(*, record_id: int) -> PlayerMailRecord:
    """
    根据玩家邮件记录来查询
    :param record_id:
    :return:
    """
    return session.query(PlayerMailRecord).filter(PlayerMailRecord.id == record_id).first()


# other
# 获得当前邮箱没有占用的位置的最小位置


def get_min_unused_mail_position(character_id: int):
    """
    获取某个角色未用的邮箱位置
    """
    mails = get_all_for_character(character_id=character_id)

    positions = []
    for mail in mails:
        positions.append(mail.mail_position_index)

    available_position = find_smallest_missing(positions=positions)
    return available_position


def insert_to_available_position(*,
                                 send_character_id: int,
                                 received_character_id: int,
                                 give_stuff_id: int,
                                 charge: int,
                                 give: int,
                                 mail_type: int,
                                 is_already_read: bool,
                                 addition_message: int,
                                 send_timestamp: int):
    available_position = get_min_unused_mail_position(
        character_id=received_character_id
    )
    add(send_character_id=send_character_id,
        received_character_id=received_character_id,
        mail_position_index=available_position,
        give_stuff_id=give_stuff_id,
        charge=charge,
        give=give,
        mail_type=mail_type,
        is_already_read=is_already_read,
        addition_message=addition_message,
        send_timestamp=send_timestamp
        )
