from typing import List, Set, DefaultDict, Dict


class Base:
    def __init__(self, *, index: int, name: str, comment: str = ''):
        self.index = index
        self.name = name


class SkillType:
    # 如果附带状态则收到状态抵抗的影响
    PASSIVE = Base(index=1, name='被动')
    BLESSING = Base(index=2, name='祝福，可以对自己或者对方释放；')
    CURSE = Base(index=3, name='诅咒', comment='只能对敌人释放。是否命中受到对方洞察值的影响')
    PHYSICAL_ATTACK = Base(index=4, name='物理攻击', comment="只能对对方释放。是否命中看自身命中和对方闪避值。")
    MAGIT_ATTACK = Base(index=5, name='物理攻击', comment="只能对对方释放。是否命中看对方的洞察值")


class SkillTarget:
    SELF = Base(index=2, name='自身', comment='自身')
    ENEMY = Base(index=2, name="敌人", comment="敌人")


class AchievementType:
    """
    成就的类型
    """
    ENTER_THE_GAME = 1  # 第一次进入游戏
    BASE_PROPERTY = 2  # 基础属性突破
    LEVEL_UP = 3  # 等级提升相关
    KILL_BOSS = 4  # 击败BOSS数量
    BATTLE = 4  # 击败BOSS数量
    FIRST_PK = 5  # PK相关
    PK_RANK = 6  # PK相关
    PK_RANK_RAISE=7
    GOLD_NUM = 7  # 黄金数量
    SKILL = 8  # 学习技能的时候会触发
    FIRST_LOTTERY = 9  # 抽奖相关
    LOTTERY = 9  # 抽奖相关
    EQUIPMENT = 10  # 装备穿戴会触发
    FIRST_SELL_STUFF = 11  # 交易物品相关
    FIRST_EXP_BOOK = 12  # 经验书相关
    FIRST_IDENTIFY = 15
    FIRST_RAISE_STAR = 16
    SINGLE_RAISE_STAR = 17
    ALL_RAISE_STAR = 18


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
    INITIAL = 1  # 初始属性
    BASE_PROPERTY_POINT = 2  # 基础属性加点
    ACHIEVEMENT = 3  # 成就称号
    SKILL = 4  # 技能
    SKILL_BOOK = 5  # 技能书
    EQUIPMENT_PROTOTYPE = 6  # 装备原型
    EQUIPMENT_RECORD = 7  # 装备记录
    POTION = 8  # 临时药剂
    PLAYER = 9  # player
    MONSTER = 10  # monster
    BASE_ADDITIONAL = 11  # 基础属性其它属性值；


addition_source_type_cn_dict = {
    AdditionSourceType.INITIAL: "初始",
    AdditionSourceType.BASE_PROPERTY_POINT: "基础属性加点",
    AdditionSourceType.ACHIEVEMENT: "成就称号",
    AdditionSourceType.SKILL: "技能",
    AdditionSourceType.SKILL_BOOK: "技能书",
    AdditionSourceType.EQUIPMENT_PROTOTYPE: "装备原型",
    AdditionSourceType.EQUIPMENT_RECORD: "装备记录",
    AdditionSourceType.POTION: "临时药剂",
    AdditionSourceType.PLAYER: "用户",
    AdditionSourceType.MONSTER: "怪物",
    AdditionSourceType.BASE_ADDITIONAL: "基础属性其它属性值",
}


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
    PHYSIQUE = 1  # "体质"
    PHYSIQUE_ADD_PERCENT = 2  # "体质百分比"

    STRENGTH = 3  # "力量"
    STRENGTH_ADD_PERCENT = 4  # "力量百分比"

    AGILITY = 5  # "敏捷"
    AGILITY_ADD_PERCENT = 6  # "敏捷百分比"

    INTELLIGENCE = 7  # "智力"
    INTELLIGENCE_ADD_PERCENT = 8  # "智力百分比"

    PERCEPTION = 9  # "感知"
    PERCEPTION_ADD_PERCENT = 10  # "感知百分比"

    ATTACK_SPEED = 11  # 出手速度
    ATTACK_SPEED_ADD_PERCENT = 12  # 出手速度百分比

    PHYSICS_ATTACK = 13  # 攻击力
    PHYSICS_ATTACK_ADD_PERCENT = 14  # 攻击力百分比

    HEALTH = 15  # 生命上限
    HEALTH_ADD_PERCENT = 16  # 生命上限百分比

    HEALTH_RECOVERY = 17  # 生命恢复(每回合)
    HEALTH_RECOVERY_ADD_PERCENT = 18  # 生命恢复百分比

    HEALTH_ABSORPTION = 19  # 生命吸收
    HEALTH_ABSORPTION_ADD_PERCENT = 20  # 生命吸收百分比

    MANA = 21  # 法力
    MANA_ADD_PERCENT = 22  # 法力百分比(每回合)

    MANA_RECOVERY = 23  # 法力恢复
    MANA_RECOVERY_ADD_PERCENT = 24  # 法力恢复百分比

    MANA_ABSORPTION = 25  # 法力吸收
    MANA_ABSORPTION_ADD_PERCENT = 26  # 法力吸收百分比

    COUNTERATTACK = 27  # 反击
    COUNTERATTACK_ADD_PERCENT = 28  # 反击百分比
    IGNORE_COUNTERATTACK = 29  # 无视反击
    IGNORE_COUNTERATTACK_ADD_PERCENT = 30  # 无视反击百分比

    CRITICAL_POINT = 35  # 致命点
    CRITICAL_POINT_ADD_PERCENT = 36  # 致命点百分比

    STATE_RESISTANCE = 37  # 状态抵抗
    STATE_RESISTANCE_ADD_PERCENT = 38  # 状态抵抗百分比

    IGNORE_STATE_RESISTANCE = 39  # 状态抵抗百分比
    IGNORE_STATE_RESISTANCE_ADD_PERCENT = 40  # 状态抵抗百分比

    INSIGHT = 41  # 洞察
    INSIGHT_PERCENT = 42  # 洞察百分比
    IGNORE_INSIGHT = 43  # 无视洞察
    IGNORE_INSIGHT_PERCENT = 44  # 无视洞察百分比

    HIT = 45  # 命中
    HIT_PERCENT = 46  # 命中百分比
    DODGE = 47  # 闪避
    DODGE_PERCENT = 48  # 闪避百分比

    WEAPON_DAMAGE = 49  # 武器伤害  为真实伤害
    WEAPON_DAMAGE_PERCENT = 50  # 武器伤害百分比

    MAGIC_ATTACK = 51  # 魔法攻击力
    MAGIC_ATTACK_PERCENT = 52  # 魔法攻击力百分比

    DAMAGE_REDUCTION = 54  #
    DAMAGE_REDUCTION_PERCENT = 55  #

    IGNORE_DAMAGE_REDUCTION = 56  #
    IGNORE_DAMAGE_REDUCTION_PERCENT = 57  #

    DAMAGE_SHIELD = 58  # 免伤护盾

    EXP_ADD_PERCENT = 59  # 经验百分比，有些装备可以经验获得

    @classmethod
    def all(cls) -> List[int]:
        return [
            cls.PHYSIQUE,
            cls.PHYSIQUE_ADD_PERCENT,

            cls.STRENGTH,
            cls.STRENGTH_ADD_PERCENT,

            cls.AGILITY,
            cls.AGILITY_ADD_PERCENT,

            cls.INTELLIGENCE,
            cls.INTELLIGENCE_ADD_PERCENT,

            cls.PERCEPTION,
            cls.PERCEPTION_ADD_PERCENT,

            cls.ATTACK_SPEED,
            cls.ATTACK_SPEED_ADD_PERCENT,

            cls.PHYSICS_ATTACK,
            cls.PHYSICS_ATTACK_ADD_PERCENT,

            cls.HEALTH,
            cls.HEALTH_ADD_PERCENT,

            cls.HEALTH_RECOVERY,
            cls.HEALTH_RECOVERY_ADD_PERCENT,

            cls.HEALTH_ABSORPTION,
            cls.HEALTH_ABSORPTION_ADD_PERCENT,

            cls.MANA,
            cls.MANA_ADD_PERCENT,

            cls.MANA_RECOVERY,
            cls.MANA_RECOVERY_ADD_PERCENT,

            cls.MANA_ABSORPTION,
            cls.MANA_ABSORPTION_ADD_PERCENT,

            cls.COUNTERATTACK,
            cls.COUNTERATTACK_ADD_PERCENT,
            cls.IGNORE_COUNTERATTACK,
            cls.IGNORE_COUNTERATTACK_ADD_PERCENT,

            cls.CRITICAL_POINT,
            cls.CRITICAL_POINT_ADD_PERCENT,

            cls.STATE_RESISTANCE,  # 状态抵抗
            cls.STATE_RESISTANCE_ADD_PERCENT,  # 状态抵抗百分比

            cls.IGNORE_STATE_RESISTANCE,  # 状态抵抗百分比
            cls.IGNORE_STATE_RESISTANCE_ADD_PERCENT,  # 状态抵抗百分比

            cls.INSIGHT,  # 洞察
            cls.INSIGHT_PERCENT,  # 洞察百分比
            cls.IGNORE_INSIGHT,  # 无视洞察
            cls.IGNORE_INSIGHT_PERCENT,  # 无视洞察百分比

            cls.HIT,  # 命中
            cls.HIT_PERCENT,  # 命中百分比
            cls.DODGE,  # 闪避
            cls.DODGE_PERCENT,  # 闪避百分比

            cls.WEAPON_DAMAGE,  # 武器伤害
            cls.WEAPON_DAMAGE_PERCENT,  # 武器伤害百分比

            cls.MAGIC_ATTACK,  # 魔法攻击力
            cls.MAGIC_ATTACK_PERCENT,  # 魔法攻击力百分比

            cls.DAMAGE_REDUCTION,  # 伤害减免
            cls.DAMAGE_REDUCTION_PERCENT,  # 伤害减免百分比

            cls.IGNORE_DAMAGE_REDUCTION,  # 无视伤害减免
            cls.IGNORE_DAMAGE_REDUCTION_PERCENT,  # 无视伤害减免百分比

            cls.DAMAGE_SHIELD,

            cls.EXP_ADD_PERCENT,
        ]


property_type_cn_dict = {
    AdditionalPropertyType.PHYSIQUE: "体质",
    AdditionalPropertyType.PHYSIQUE_ADD_PERCENT: "体质百分比",

    AdditionalPropertyType.STRENGTH: "力量",
    AdditionalPropertyType.STRENGTH_ADD_PERCENT: "力量百分比",

    AdditionalPropertyType.AGILITY: "敏捷",
    AdditionalPropertyType.AGILITY_ADD_PERCENT: "敏捷百分比",

    AdditionalPropertyType.INTELLIGENCE: "智力",
    AdditionalPropertyType.INTELLIGENCE_ADD_PERCENT: "智力百分比",

    AdditionalPropertyType.PERCEPTION: "感知",
    AdditionalPropertyType.PERCEPTION_ADD_PERCENT: "感知百分比",

    AdditionalPropertyType.ATTACK_SPEED: "出手速度",
    AdditionalPropertyType.ATTACK_SPEED_ADD_PERCENT: "出手速度百分比",

    AdditionalPropertyType.PHYSICS_ATTACK: "物理攻击力",
    AdditionalPropertyType.PHYSICS_ATTACK_ADD_PERCENT: "物理攻击力百分比",

    AdditionalPropertyType.HEALTH: "生命上限",
    AdditionalPropertyType.HEALTH_ADD_PERCENT: "生命上限百分比",

    AdditionalPropertyType.HEALTH_RECOVERY: "生命恢复",
    AdditionalPropertyType.HEALTH_RECOVERY_ADD_PERCENT: "生命恢复百分比",

    AdditionalPropertyType.HEALTH_ABSORPTION: "生命吸收",
    AdditionalPropertyType.HEALTH_ABSORPTION_ADD_PERCENT: "生命吸收百分比",

    AdditionalPropertyType.MANA: "法力",
    AdditionalPropertyType.MANA_ADD_PERCENT: "法力百分比",

    AdditionalPropertyType.MANA_RECOVERY: "法力恢复",
    AdditionalPropertyType.MANA_RECOVERY_ADD_PERCENT: "法力恢复百分比",

    AdditionalPropertyType.MANA_ABSORPTION: "法力吸收",
    AdditionalPropertyType.MANA_ABSORPTION_ADD_PERCENT: "法力吸收百分比",

    AdditionalPropertyType.COUNTERATTACK: "反击",
    AdditionalPropertyType.COUNTERATTACK_ADD_PERCENT: "反击百分比",
    AdditionalPropertyType.IGNORE_COUNTERATTACK: "无视反击",
    AdditionalPropertyType.IGNORE_COUNTERATTACK_ADD_PERCENT: "无视反击百分比",

    AdditionalPropertyType.CRITICAL_POINT: "致命点",
    AdditionalPropertyType.CRITICAL_POINT_ADD_PERCENT: "致命点百分比",

    AdditionalPropertyType.STATE_RESISTANCE: "状态抵抗",  # 状态抵抗
    AdditionalPropertyType.STATE_RESISTANCE_ADD_PERCENT: "状态抵抗百分比",  # 状态抵抗百分比

    AdditionalPropertyType.IGNORE_STATE_RESISTANCE: "无视状态抵抗",  # 状态抵抗百分比
    AdditionalPropertyType.IGNORE_STATE_RESISTANCE_ADD_PERCENT: "五十状态抵抗百分比",  # 状态抵抗百分比

    AdditionalPropertyType.INSIGHT: "洞察",  # 洞察
    AdditionalPropertyType.INSIGHT_PERCENT: "洞察百分比",  # 洞察百分比
    AdditionalPropertyType.IGNORE_INSIGHT: "无视洞察",  # 无视洞察
    AdditionalPropertyType.IGNORE_INSIGHT_PERCENT: "无视洞察百分比",  # 无视洞察百分比

    AdditionalPropertyType.HIT: "命中",  # 命中
    AdditionalPropertyType.HIT_PERCENT: "命中百分比",  # 命中百分比
    AdditionalPropertyType.DODGE: "闪避",  # 闪避
    AdditionalPropertyType.DODGE_PERCENT: "闪避百分比",  # 闪避百分比

    AdditionalPropertyType.WEAPON_DAMAGE: "武器伤害",  # 武器伤害
    AdditionalPropertyType.WEAPON_DAMAGE_PERCENT: "武器伤害百分比",  # 武器伤害百分比

    AdditionalPropertyType.DAMAGE_REDUCTION: "伤害减免",  # 武器伤害百分比
    AdditionalPropertyType.DAMAGE_REDUCTION_PERCENT: "伤害减免百分比",  # 武器伤害百分比
    AdditionalPropertyType.IGNORE_DAMAGE_REDUCTION: "无视伤害减免",  # 武器伤害百分比
    AdditionalPropertyType.IGNORE_DAMAGE_REDUCTION_PERCENT: "无视伤害减免百分比",  # 武器伤害百分比

    AdditionalPropertyType.MAGIC_ATTACK: "魔法攻击力",  # 魔法攻击力
    AdditionalPropertyType.MAGIC_ATTACK_PERCENT: "魔法攻击力百分比",  # 魔法攻击力百分比

    AdditionalPropertyType.DAMAGE_SHIELD: "免伤护盾",

    AdditionalPropertyType.EXP_ADD_PERCENT: "经验百分比"
    # ，有些装备可以经验获得,
}


class BasePropertyType:  # 目前宝石和基础属性公用一套属性。所以宝石的类型也仅仅限于这些类型。
    """
    1 3 5 7 9的原因是为了和附加属性一致
    """
    PHYSIQUE = AdditionalPropertyType.PHYSIQUE
    STRENGTH = AdditionalPropertyType.STRENGTH  # "力量"
    AGILITY = AdditionalPropertyType.AGILITY  # "敏捷"
    INTELLIGENCE = AdditionalPropertyType.INTELLIGENCE  # "智力"
    PERCEPTION = AdditionalPropertyType.PERCEPTION  # "感知"


property_cn_type_dict = {property_type_cn_dict[key]: key for key in property_type_cn_dict}
base_property_cn_type_dict = {key: property_cn_type_dict[key] for key in property_cn_type_dict if
                              key in {"体质", "力量", "敏捷", "智力", "感知", }}


class BattlePropertyType:
    """
    战斗需要的属性
    """
    ATTACK_SPEED = 11  # 出手速度
    ATTACK = 13  # 攻击力

    HEALTH = 15  # 生命上限
    HEALTH_RECOVERY = 17  # 生命恢复(每回合)
    HEALTH_ABSORPTION = 19  # 生命吸收

    MANA = 21  # 法力
    MANA_RECOVERY = 23  # 法力恢复
    MANA_ABSORPTION = 25  # 法力吸收

    COUNTERATTACK = 27  # 反击
    IGNORE_COUNTERATTACK = 29  # 无视反击

    CRITICAL_POINT = 31  # 致命点

    DAMAGE_SHIELD = 33  # 免伤护盾

    @classmethod
    def all(cls) -> List[int]:
        return [
            cls.ATTACK_SPEED,
            cls.ATTACK,

            cls.HEALTH,
            cls.HEALTH_RECOVERY,
            cls.HEALTH_ABSORPTION,

            cls.MANA,
            cls.MANA_RECOVERY,
            cls.MANA_ABSORPTION,

            cls.COUNTERATTACK,
            cls.IGNORE_COUNTERATTACK,

            cls.CRITICAL_POINT,

            cls.DAMAGE_SHIELD,
        ]


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
