from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Boolean

from Enums import MailType,StuffType
from DBHelper.tables.base_table import Basic,Base
from DBHelper.tables.base_table import CustomColumn,Timestamp
from Utils.tools import find_smallest_missing

from DBHelper.session import session


class PlayerMailRecord(Basic,Base):
    """
    用户邮件记录表
    """

    __cn__ = "用户邮件记录表"
    __tablename__ = 'player_mail_record'

    send_character_id = CustomColumn(Integer, cn="发送人ID",comment="邮件发送人的 character_id。如果是游戏管理员,需要在设置表中指定游戏管理员的ID;")
    received_character_id = CustomColumn(Integer, cn="接收人ID",comment="邮件接收人的 character_id")
    mail_position_index = CustomColumn(Integer, cn="邮件索引",comment="邮件所占用位置的索引,从1开始;")

    give_stuff_type = CustomColumn(Integer, cn="赠送物品类型",bind_type=StuffType,comment="赠送物品的id。只有未绑定的物品才可以邮寄给别人。暂定最多赠送一件物品。")
    give_stuff_record_id = CustomColumn(Integer, cn="赠送物品ID",comment="赠送物品的id。只有未绑定的物品才可以邮寄给别人。暂定最多赠送一件物品。")

    charge = CustomColumn(Integer, cn="收费",comment="收费黄金数量,如果要接受邮件需要付费的数量")
    give = CustomColumn(Integer, cn="赠送",comment="赠送黄金数量,不仅赠送给人物品,还赠送给别人黄金")

    mail_type = CustomColumn(Integer, cn="邮件类型",bind_type=MailType,comment="邮件类型,参考MailType")

    is_already_read = CustomColumn(Boolean, cn="是否已读",comment="是否已经打开过了")
    is_already_deleted = CustomColumn(Boolean,cn="是否删除", comment="是否已经打开过了")

    addition_message = CustomColumn(Integer, cn="附言",comment="邮件发送的时候的附加信息,接受放能够看到;")
    send_timestamp = CustomColumn(Timestamp, cn="发送时间",comment="邮件发送的时间")

    @classmethod
    def add_or_update_by_id(cls, *,
                            _id: int,
                            send_character_id: int = None,
                            received_character_id: int = None,
                            mail_position_index: int = None,
                            give_stuff_id: int = None,
                            charge: int = None,
                            give: int = None,
                            mail_type: int = None,
                            is_already_read: bool = None,
                            is_already_deleted: bool = None,
                            addition_message: int = None,
                            send_timestamp: int = None
                            ):
        fields = cls.update_fields_from_signature(func=cls.add_or_update_by_id)
        record = cls._add_or_update_by_id(**fields)
        return record

    # 改
    @classmethod
    def update_read_status(cls, *, _id: int, is_already_read: bool) -> "PlayerMailRecord":
        record=cls.update_kwargs_by_id(_id=_id,is_already_read=is_already_read)
        return record

    @classmethod
    def update_type_by_record_id(cls,*, _id: int, new_mail_type: int):
        record=cls.update_kwargs_by_id(_id=_id,new_mail_type=new_mail_type)
        return record

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
