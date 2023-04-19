from typing import List, Set, DefaultDict, Dict


class Item:
    def __init__(self, *, index: int, name: str, comment: str = ''):
        self.index = index
        self.name = name
        self.comment = comment


def get_dict(*, items: List[Item]):
    name_index_dict = dict()
    index_name_dict = dict()
    for item in items:
        name_index_dict[item.name] = item.index
        index_name_dict[item.index] = item.name
    return name_index_dict, index_name_dict


# class PassiveBattleStatus:
#     index=0
#     index+=1
#     BLEED=

# class PositiveBattleStatus:

class SkillLevel:
    index = 0

    index += 1
    ONE = Item(index=index, name='1', comment="等级1")
    index += 1
    TWO = Item(index=index, name='2', comment="等级2")
    index += 1
    THREE = Item(index=index, name='3', comment="等级3")
    index += 1
    FOUR = Item(index=index, name='4', comment="等级4")
    index += 1
    FIVE = Item(index=index, name='5', comment="等级5")
    index += 1
    SIX = Item(index=index, name='6', comment="等级6")
    index += 1
    SEVEN = Item(index=index, name='7', comment="等级7")
    index += 1
    EIGHT = Item(index=index, name='8', comment="等级8")
    index += 1
    NINE = Item(index=index, name='9', comment="等级9")
    items = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = NINE


class LearningApproach:
    index = 0
    index += 1
    IN_SKILL_ACADEMY = Item(index=index, name="技能学院", comment="直接可以获得，仅仅消耗技能点，主要是基础技能，不依赖于具体装备")
    index += 1
    EQUIPMENT_ADDITIONAL = Item(index=index, name="装备附加", comment="仅仅可以从装备上获得，和装备名字相关。")

    items = [IN_SKILL_ACADEMY, EQUIPMENT_ADDITIONAL]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = IN_SKILL_ACADEMY


class SkillType:
    # 如果附带状态则收到状态抵抗的影响
    index = 0

    index += 1
    PASSIVE = Item(index=index, name='被动')

    index += 1
    BLESSING = Item(index=index, name='祝福', comment='可以对自己或者对方释放')

    index += 1
    CURSE = Item(index=index, name='诅咒', comment='只能对敌人释放。是否命中受到对方洞察值的影响')

    index += 1
    PHYSICAL_ATTACK = Item(index=index, name='物理攻击', comment="只能对对方释放。是否命中看自身命中和对方闪避值。")

    index += 1
    MAGIT_ATTACK = Item(index=index, name='魔法攻击', comment="只能对对方释放。是否命中看对方的洞察值")

    items = [PASSIVE, BLESSING, CURSE, PHYSICAL_ATTACK, MAGIT_ATTACK]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = PASSIVE


class SkillTarget:
    index = 0

    index += 1
    SELF = Item(index=index, name='自身', comment='自身')

    index += 1
    ENEMY = Item(index=index, name="敌人", comment="敌人")
    items = [SELF, ENEMY]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = SELF


class StatusType:
    index = 0

    index += 1
    PASSIVE = Item(index=index, name='减益', comment='减益')

    index += 1
    POSITIVE = Item(index=index, name="增益", comment="增益")

    index += 1
    NEUTRAL = Item(index=index, name="中立", comment="中立")

    items = [PASSIVE, POSITIVE, NEUTRAL]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = PASSIVE


class AchievementType:
    """
    成就的类型
    """
    CHARGE = 1
    GOLD_NUM = 7  # 黄金数量
    ADDITIONAL_PROPERTY = 0  # 附加属性排行榜
    BASE_PROPERTY = 2  # 基础属性突破
    LEVEL_UP = 3  # 等级提升相关
    KILL_BOSS = 4  # 击败BOSS数量
    BATTLE = 4  # 击败BOSS数量
    FIRST_PK = 5  # PK相关
    PK_Number = 6  # PK相关
    PK_RANK = 6  # PK相关
    PK_RANK_RAISE = 7
    SKILL = 8  # 学习技能的时候会触发
    FIRST_LOTTERY = 9  # 抽奖相关
    LOTTERY = 9  # 抽奖相关
    EQUIPMENT = 10  # 装备穿戴会触发
    SELL_STUFF = 11  # 交易物品相关
    EXP_BOOK = 12  # 经验书相关
    IDENTIFY = 15
    RAISE_STAR = 16
    GEM = 16  # 宝石相关
    ANNIVERSARY_FESTIVAL = 12  # 周年节日


class EquipmentQuality:
    """Enumeration class representing different levels of equipment quality.

    Attributes:
        COMMON (int): Representing common equipment quality. # 普通
        EXCELLENT (int): Representing excellent equipment quality. # 优秀
        RARE (int): Representing rare equipment quality. # 稀有
        EPIC (int): Representing epic equipment quality. # 史诗
        MYTHIC (int): Representing mythic equipment quality. # 传说
        ULTIMATE (int): Representing ultimate equipment quality. # 神话
    """
    COMMON = 1  # 1个属性
    EXCELLENT = 2  # 2个属性
    RARE = 3  # 2个属性
    EPIC = 4  # 3个属性    带技能
    MYTHIC = 5  # 4个属性  带技能
    MYTHOLOGY = 6  # 4个属性   带技能


equipment_cn_quality_dict = {
    "普通": EquipmentQuality.COMMON,
    "优秀": EquipmentQuality.EXCELLENT,
    "稀有": EquipmentQuality.RARE,
    "史诗": EquipmentQuality.EPIC,
    "传说": EquipmentQuality.MYTHIC,
    "神话": EquipmentQuality.MYTHOLOGY,
}


class PartType:
    CLOAK = 1  # "披风"
    NECKLACE = 2  # "项链"
    COSTUME = 3  # "时装"
    AMULET = 4  # "护符"
    MOUNT = 5  # "坐骑"

    HEAD = 6  # "头"
    SHOULDER = 7  # "肩"
    CLOTHES = 8  # "衣"
    WAIST = 9  # "腰"
    HAND = 10  # "手"
    LEG = 11  # "腿"
    FOOT = 12  # "脚"

    WEAPON = 13  # "武器"


part_cn_type_dict = {
    '披风': PartType.CLOAK,
    '护符': PartType.AMULET,
    '项链': PartType.NECKLACE,
    '时装': PartType.COSTUME,
    '坐骑': PartType.MOUNT,

    '头': PartType.HEAD,
    '肩': PartType.SHOULDER,
    '衣': PartType.CLOTHES,
    '腰': PartType.WAIST,
    '手': PartType.HAND,
    '腿': PartType.LEG,
    '足': PartType.FOOT,

    '武器': PartType.WEAPON,
}


class StuffStatus:
    IN_BAG_NOT_SELL = 1  # 在背包中，且未出售
    IN_SHOP = 2  # '在交易所'，且未出售
    DECOMPOSE = 3  # '被分解了'
    DISCARDED = 4  # '被扔掉'


class StuffType:
    """
    物品类型
    """
    EQUIPMENT = 1  # 装备
    BOX = 2  # 箱子   允许一次性使用多个
    GEM = 3  # 宝石
    RAISE_STAR_BOOK = 4  # 升星卷轴 允许一次性使用多个
    IDENTIFY_BOOK = 5  # 鉴定卷轴
    EXP_BOOK = 6  # 经验书  允许一次性使用多个
    SKILL_BOOK = 7  # 技能书 允许一次性使用多个
    POTION = 8  # 药水 使用后可以临时提高某个属性；
    MONSTER = 9  # 怪物，被击败的时候使用；


stuff_cn_type_dict = {
    "装备": StuffType.EQUIPMENT,
    "箱子": StuffType.BOX,
    "宝石": StuffType.GEM,
    "升星卷轴": StuffType.RAISE_STAR_BOOK,
    "鉴定卷轴": StuffType.IDENTIFY_BOOK,
    "经验书": StuffType.EXP_BOOK,
    "技能书": StuffType.SKILL_BOOK,
    "药剂": StuffType.POTION,
    "怪物": StuffType.MONSTER,
}


class BeingType:
    """
    生物类型
    """
    PLAYER = 1  # 游戏玩家
    MONSTER = 2  # 怪物、boss


class AdditionSourceType:
    """
    属性的来源
    """
    index = 0

    index += 1
    INITIAL = Item(index=index, name='初始属性')

    index += 1
    BASE_PROPERTY_POINT = Item(index=index, name='基础属性加点', comment='基础属性加点')

    index += 1
    BASE_ADDITIONAL = Item(index=index, name='基础属性对应附加属性', comment='基础属性如何转换为其它的属性')

    index += 1
    ACHIEVEMENT = Item(index=index, name='称号', comment='称号增加属性')

    index += 1
    SKILL = Item(index=index, name='技能', comment='技能增加属性')

    index += 1
    SKILL_BOOK = Item(index=index, name='技能书', comment='技能书的属性')

    index += 1
    EQUIPMENT_PROTOTYPE = Item(index=index, name='装备原型', comment='装备原型的属性')

    index += 1
    EQUIPMENT_RECORD = Item(index=index, name='装备记录', comment='具体某个装备的属性')

    index += 1
    POTION = Item(index=index, name='药剂', comment='某个药剂增加的属性')

    index += 1
    PLAYER = Item(index=index, name='人物', comment='某个人物的属性')

    index += 1
    MONSTER = Item(index=index, name='怪物', comment='某个怪物的属性')

    index += 1
    STATUS = Item(index=index, name='状态', comment='状态增加属性')

    items = [INITIAL,
             BASE_PROPERTY_POINT, BASE_ADDITIONAL,
             ACHIEVEMENT,
             SKILL, SKILL_BOOK,
             EQUIPMENT_PROTOTYPE, EQUIPMENT_RECORD,
             POTION,
             PLAYER,
             MONSTER,
             STATUS]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = INITIAL


class GemInlayingStatus:
    """
    宝石镶嵌的状态。一般只有装备可以镶嵌宝石；
    """
    NOT_INLAYING = 1  # 还未镶嵌宝石
    INLAYING = 2  # 宝石镶嵌中
    DAMAGED_INLAYING = 3  # 镶嵌破损


class AdditionalPropertyType:
    """
    装备、技能、称号所有可能的属性
    """
    index = 0
    index += 1
    PHYSIQUE = Item(index=index, name="体质", comment="帧率")
    index += 1
    PHYSIQUE_ADD_PERCENT = Item(index=index, name="体质百分比", comment="体质百分比")

    index += 1
    STRENGTH = Item(index=index, name="力量", comment="力量")
    index += 1
    STRENGTH_ADD_PERCENT = Item(index=index, name="力量百分比", comment="力量百分比")

    index += 1
    AGILITY = Item(index=index, name="敏捷", comment="敏捷")
    index += 1
    AGILITY_ADD_PERCENT = Item(index=index, name="敏捷百分比", comment="敏捷百分比")

    index += 1
    INTELLIGENCE = Item(index=index, name="智力", comment="智力")
    index += 1
    INTELLIGENCE_ADD_PERCENT = Item(index=index, name="智力百分比", comment="智力百分比")

    index += 1
    PERCEPTION = Item(index=index, name="感知", comment="感知")
    index += 1
    PERCEPTION_ADD_PERCENT = Item(index=index, name="感知百分比", comment="感知百分比")

    index += 1
    ATTACK_SPEED = Item(index=index, name="出手速度", comment="出手速度")
    index += 1
    ATTACK_SPEED_ADD_PERCENT = Item(index=index, name="出手速度百分比", comment="出手速度百分比")

    index += 1
    PHYSICS_ATTACK = Item(index=index, name="物理攻击力", comment="物理攻击力")
    index += 1
    PHYSICS_ATTACK_ADD_PERCENT = Item(index=index, name="物理攻击力百分比", comment="物理攻击力百分比")

    index += 1
    HEALTH = Item(index=index, name="生命上限", comment="生命上限")
    index += 1
    HEALTH_ADD_PERCENT = Item(index=index, name="生命上限百分比", comment="生命上限百分比")
    # 增加生命上限的通过状态实现；
    index += 1
    HEALTH_RECOVERY = Item(index=index, name="生命恢复", comment="恢复生命")
    index += 1
    HEALTH_RECOVERY_ADD_PERCENT = Item(index=index, name="生命恢复百分比", comment="生命恢复百分比")
    index += 1
    HEALTH_RECOVERY_ALL_PERCENT = Item(index=index, name="恢复百分比生命", comment="恢复百分比生命")

    index += 1
    HEALTH_ABSORPTION = Item(index=index, name="生命吸收", comment="出手速度")
    index += 1
    HEALTH_ABSORPTION_ADD_PERCENT = Item(index=index, name="生命吸收百分比", comment="出手速度百分比")

    index += 1
    MANA = Item(index=index, name="法力上限", comment="法力上限")
    index += 1
    MANA_ADD_PERCENT = Item(index=index, name="法力上限百分比", comment="法力上限百分比")

    index += 1
    MANA_RECOVERY = Item(index=index, name="法力恢复", comment="法力恢复")
    index += 1
    MANA_RECOVERY_ADD_PERCENT = Item(index=index, name="法力恢复百分比", comment="法力恢复百分比")
    index += 1
    MANA_RECOVERY_ALL_PERCENT = Item(index=index, name="回复百分比法力", comment="回复百分比法力")

    index += 1
    MANA_ABSORPTION = Item(index=index, name="法力上限", comment="法力上限")
    index += 1
    MANA_ABSORPTION_ADD_PERCENT = Item(index=index, name="法力上限百分比", comment="法力上限百分比")

    index += 1
    COUNTERATTACK = Item(index=index, name="反击", comment="反击")
    index += 1
    COUNTERATTACK_ADD_PERCENT = Item(index=index, name="反击百分比", comment="反击百分比")

    index += 1
    IGNORE_COUNTERATTACK = Item(index=index, name="无视反击", comment="无视反击")
    index += 1
    IGNORE_COUNTERATTACK_ADD_PERCENT = Item(index=index, name="无视反击百分比", comment="无视反击百分比")

    index += 1
    CRITICAL_POINT = Item(index=index, name="致命点", comment="致命点")
    index += 1
    CRITICAL_POINT_ADD_PERCENT = Item(index=index, name="致命点百分比", comment="致命点百分比")

    index += 1
    STATE_RESISTANCE = Item(index=index, name="状态抵抗", comment="状态抵抗")
    index += 1
    STATE_RESISTANCE_ADD_PERCENT = Item(index=index, name="状态抵抗百分比", comment="状态抵抗百分比")

    index += 1
    IGNORE_STATE_RESISTANCE = Item(index=index, name="无视状态抵抗", comment="无视状态抵抗")
    index += 1
    IGNORE_STATE_RESISTANCE_ADD_PERCENT = Item(index=index, name="无视状态抵抗百分比", comment="无视状态抵抗百分比")

    index += 1
    INSIGHT = Item(index=index, name="洞察", comment="洞察")
    index += 1
    INSIGHT_PERCENT = Item(index=index, name="洞察百分比", comment="洞察百分比")

    index += 1
    IGNORE_INSIGHT = Item(index=index, name="无视洞察", comment="无视洞察")
    index += 1
    IGNORE_INSIGHT_PERCENT = Item(index=index, name="无视洞察百分比", comment="状态抵抗百分比")

    index += 1
    HIT = Item(index=index, name="命中", comment="命中")
    index += 1
    HIT_PERCENT = Item(index=index, name="命中百分比", comment="命中百分比")

    index += 1
    DODGE = Item(index=index, name="闪避", comment="闪避")
    index += 1
    DODGE_PERCENT = Item(index=index, name="闪避百分比", comment="闪避百分比")

    index += 1
    WEAPON_DAMAGE = Item(index=index, name="武器伤害", comment="武器伤害")
    index += 1
    WEAPON_DAMAGE_PERCENT = Item(index=index, name="武器伤害百分比", comment="武器伤害百分比")

    index += 1
    MAGIC_ATTACK = Item(index=index, name="魔法攻击力", comment="魔法攻击力")
    index += 1
    MAGIC_ATTACK_PERCENT = Item(index=index, name="魔法攻击力百分比", comment="魔法攻击力百分比")

    index += 1
    DAMAGE_REDUCTION = Item(index=index, name="伤害减免", comment="伤害减免")
    index += 1
    DAMAGE_REDUCTION_PERCENT = Item(index=index, name="伤害减免百分比", comment="伤害减免百分比")

    index += 1
    IGNORE_DAMAGE_REDUCTION = Item(index=index, name="无视伤害减免", comment="无视伤害减免")
    index += 1
    IGNORE_DAMAGE_REDUCTION_PERCENT = Item(index=index, name="无视伤害减免百分比", comment="无视伤害减免百分比")

    index += 1
    DAMAGE_SHIELD = Item(index=index, name="免伤护盾", comment="无视伤害减免百分比")

    index += 1
    DAMAGE_PERCENT = Item(index=index, name="造成伤害百分比", comment="造成伤害百分比")

    index += 1
    TAKE_DAMAGE_PERCENT = Item(index=index, name="承受伤害百分比", comment="承受伤害百分比")

    index += 1
    EXP_ADD_PERCENT = Item(index=index, name="经验百分比", comment="经验百分比")

    items = [PHYSIQUE, PHYSIQUE_ADD_PERCENT,
             STRENGTH, STRENGTH_ADD_PERCENT,
             AGILITY, AGILITY_ADD_PERCENT,
             INTELLIGENCE, INTELLIGENCE_ADD_PERCENT,
             PERCEPTION, PERCEPTION_ADD_PERCENT,
             ATTACK_SPEED, ATTACK_SPEED_ADD_PERCENT,
             PHYSICS_ATTACK, PHYSICS_ATTACK_ADD_PERCENT,
             HEALTH, HEALTH_ADD_PERCENT,
             HEALTH_RECOVERY, HEALTH_RECOVERY_ADD_PERCENT, HEALTH_RECOVERY_ALL_PERCENT,
             HEALTH_ABSORPTION, HEALTH_ABSORPTION_ADD_PERCENT,
             MANA, MANA_ADD_PERCENT,
             MANA_RECOVERY, MANA_RECOVERY_ADD_PERCENT, MANA_RECOVERY_ALL_PERCENT,
             MANA_ABSORPTION, MANA_ABSORPTION_ADD_PERCENT,
             COUNTERATTACK, COUNTERATTACK_ADD_PERCENT,
             IGNORE_COUNTERATTACK, IGNORE_COUNTERATTACK_ADD_PERCENT,
             CRITICAL_POINT, CRITICAL_POINT_ADD_PERCENT,
             STATE_RESISTANCE, STATE_RESISTANCE_ADD_PERCENT,
             IGNORE_STATE_RESISTANCE, IGNORE_STATE_RESISTANCE_ADD_PERCENT,
             INSIGHT, INSIGHT_PERCENT,
             IGNORE_INSIGHT, IGNORE_INSIGHT_PERCENT,
             HIT, HIT_PERCENT,
             DODGE, DODGE_PERCENT,
             WEAPON_DAMAGE, WEAPON_DAMAGE_PERCENT,
             MAGIC_ATTACK, MAGIC_ATTACK_PERCENT,
             DAMAGE_REDUCTION, DAMAGE_REDUCTION_PERCENT,
             IGNORE_DAMAGE_REDUCTION, IGNORE_DAMAGE_REDUCTION_PERCENT,
             DAMAGE_SHIELD,
             DAMAGE_PERCENT,
             TAKE_DAMAGE_PERCENT,
             EXP_ADD_PERCENT,
             ]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = PHYSIQUE


class BasePropertyType:  # 目前宝石和基础属性公用一套属性。所以宝石的类型也仅仅限于这些类型。
    """
    1 3 5 7 9的原因是为了和附加属性一致
    """
    PHYSIQUE = AdditionalPropertyType.PHYSIQUE
    STRENGTH = AdditionalPropertyType.STRENGTH  # "力量"
    AGILITY = AdditionalPropertyType.AGILITY  # "敏捷"
    INTELLIGENCE = AdditionalPropertyType.INTELLIGENCE  # "智力"
    PERCEPTION = AdditionalPropertyType.PERCEPTION  # "感知"

    items = [PHYSIQUE, STRENGTH, AGILITY, INTELLIGENCE, PERCEPTION]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = PHYSIQUE


class MailType:
    """
    收到的邮件类型
    """
    SEND_TO_OTHER_PLAYER = 1  # 由玩家寄出给别人的，需要指明收费多少；
    SEND_TO_OTHER_PLAYER_GET_REJECT = 2  # 由玩家寄出给别人的，需要指明收费多少；
    RECEIVED_FROM_OTHER_PLAYER = 3  # 由别人寄给玩家的，需要指明收费多少；
    RECEIVED_FROM_GAME_MASTER = 4  # 从游戏管理员那里收到的
    RECEIVED_FROM_EXCHANGE_STORE_SOLD = 5  # 交易所发给自己的邮件（卖出了）；
    RECEIVED_FROM_EXCHANGE_STORE_NOT_SOLD_RETURN = 6  # 交易所发给自己的邮件（时间到了，未售出，退回）；
    RECEIVED_FROM_EXCHANGE_STORE_POSITIVE_RETURN = 7  # 交易所发给自己的邮件（时间未到，但是玩家选择主动退回，不挂售）；


class CalendarType:
    LUNAR = 1  # 农历
    GREGORIAN = 2  # 公历


calendar_cn_type_dict = {
    "农历": CalendarType.LUNAR,
    "公历": CalendarType.GREGORIAN,
}


class EquipmentPropertyAvailability:
    MIN = 1  # 最小属性
    MAX = 2  # 最大属性
    CURRENT = 3  # 当前属性
    IDENTIFY_TEMP = 4  # 鉴定得到的临时属性


class ExpBookType:
    CHARACTER = 1  # 人物


exp_book_cn_type_dict = {
    "人物": ExpBookType.CHARACTER
}


class DateType:
    HOUR_OF_DAY = 1  # 每天的几点会出现；对应的值为0到24
    DAY_OF_WEEK = 2  # 每周几；对应的值为1-7
    DAY_OF_MONTH = 3  # 每周几；对应的值为1-31
    HOLIDAY = 4  # 特殊节日会出现；参考表holiday


date_cn_type_dict = {
    "小时": DateType.HOUR_OF_DAY,
    '周几': DateType.DAY_OF_WEEK,
    '几号': DateType.DAY_OF_MONTH,
    "节日": DateType.HOLIDAY
}


class BattleType:
    WITH_OTHER_PLAYER = 1
    WITH_MONSTER = 2


if __name__ == '__main__':
    print()
