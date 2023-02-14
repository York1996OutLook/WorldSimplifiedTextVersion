class BasePropertyType:  # 目前宝石和基础属性公用一套属性。所以宝石的类型也仅仅限于这些类型。
    """
    1 3 5 7 9的原因是为了和附加属性一致
    """
    PHYSIQUE = 1  # "体质"
    STRENGTH = 3  # "力量"
    AGILITY = 5  # "敏捷"
    INTELLIGENCE = 7  # "智力"
    PERCEPTION = 9  # "感知"

    items = [PHYSIQUE, STRENGTH, AGILITY, INTELLIGENCE, PERCEPTION]


class AchievementType:
    """
    成就的类型
    """
    ENTER_THE_GAME = 1  # 第一次进入游戏
    BASE_PROPERTY = 2  # 基础属性突破
    LEVEL_UP = 3  # 等级提升相关
    KILL_BOSS = 4  # 击败BOSS
    PK = 5  # PK相关
    GOLD_NUM_INCREASE = 6  # 黄金数量
    SKILL = 7  # 技能相关
    LOTTERY = 8  # 抽奖相关
    EQUIPMENT = 9  # 装备穿戴相关
    SELL_STUFF = 10  # 交易物品相关
    EXP_BOOK = 11  # 经验书相关


class EquipmentQuality:
    """Enumeration class representing different levels of equipment quality.

    Attributes:
        COMMON (int): Representing common equipment quality. # 普通
        EXCELLENT (int): Representing excellent equipment quality. # 优秀
        RARE (int): Representing rare equipment quality. # 稀有
        LEGENDARY (int): Representing legendary equipment quality. # 极品
        EPIC (int): Representing epic equipment quality. # 史诗
        MYTHIC (int): Representing mythic equipment quality. # 传说
        ULTIMATE (int): Representing ultimate equipment quality. # 神话
    """
    COMMON = 1  # 1个属性
    EXCELLENT = 2  # 1个属性
    RARE = 3  # 2个属性
    LEGENDARY = 4  # 2个属性
    EPIC = 5  # 3个属性
    MYTHIC = 6  # 3个属性
    MYTHOLOGY = 7  # 4个属性


class PartType:
    CLOAK = 1  # "披风"
    NECKLACE = 2  # "项链"
    COSTUME = 3  # "时装"
    AMULET = 4  # "护符"
    MOUNT = 5  # "坐骑"

    HEAD = 6  # "头"
    SHOULDER = 7  # "肩"
    CLOTHES = 8  # "衣服"
    WAIST = 9  # "腰"
    HAND = 10  # "手"
    LEG = 11  # "腿"
    FOOT = 12  # "脚"

    WEAPON = 13  # "武器"


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
    Potion = 8  # 药水 使用后可以临时提高某个属性；


class BeingType:
    """
    生物类型
    """
    PLAYER = 1  # 游戏玩家
    MONSTER = 2  # 怪物、boss


class AdditionSourceType:
    """
    增加属性的来源
    """
    INITIAL = 1  # 初始属性
    BASE_PROPERTY_POINT = 2  # 基础属性加点
    ACHIEVEMENT = 3  # 成就称号
    SKILL = 4  # 技能
    EQUIPMENT_PROTOTYPE = 5  # 装备原型
    EQUIPMENT_RECORD = 6  # 装备记录
    POTION = 7  # 临时药剂


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
    PHYSIQUE_ADD_PERCENT = 2  # "体质增加百分比"

    STRENGTH = 3  # "力量"
    STRENGTH_ADD_PERCENT = 4  # "力量增加百分比"

    AGILITY = 5  # "敏捷"
    AGILITY_ADD_PERCENT = 6  # "敏捷增加百分比"

    INTELLIGENCE = 7  # "智力"
    INTELLIGENCE_ADD_PERCENT = 8  # "智力增加百分比"

    PERCEPTION = 9  # "感知"
    PERCEPTION_ADD_PERCENT = 10  # "感知增加百分比"

    ATTACK_SPEED = 11  # 出手速度
    ATTACK_SPEED_ADD_PERCENT = 12  # 出手速度增加百分比

    ATTACK = 13  # 攻击力
    ATTACK_ADD_PERCENT = 14  # 攻击力增加百分比

    HEALTH = 15  # 生命值
    HEALTH_ADD_PERCENT = 16  # 生命值增加百分比

    HEALTH_RECOVERY = 17  # 生命值恢复(每回合)
    HEALTH_RECOVERY_ADD_PERCENT = 18  # 生命值恢复增加百分比

    HEALTH_ABSORPTION = 19  # 生命吸收
    HEALTH_ABSORPTION_ADD_PERCENT = 20  # 生命吸收增加百分比

    MANA = 21  # 法力值
    MANA_ADD_PERCENT = 22  # 法力值增加百分比(每回合)

    MANA_RECOVERY = 23  # 法力值恢复
    MANA_RECOVERY_ADD_PERCENT = 24  # 法力值恢复百分比

    MANA_ABSORPTION = 25  # 法力值吸收
    MANA_ABSORPTION_ADD_PERCENT = 26  # 法力值吸收增加百分比

    COUNTERATTACK = 27  # 反击值
    COUNTERATTACK_ADD_PERCENT = 28  # 反击值增加百分比
    IGNORE_COUNTERATTACK = 29  # 无视反击值
    IGNORE_COUNTERATTACK_ADD_PERCENT = 30  # 无视反击值增加百分比

    CRITICAL_POINT = 31  # 致命点
    CRITICAL_POINT_ADD_PERCENT = 32  # 致命点增加百分比

    DAMAGE_SHIELD = 33  # 免伤护盾

    EXP_ADD_PERCENT = 34  # 经验增加百分比，有些装备可以增加经验值获得

    min_num = 1
    max_num = 34


property_type_cn_dict = {
    AdditionalPropertyType.PHYSIQUE: "体质",
    AdditionalPropertyType.PHYSIQUE_ADD_PERCENT: "体质增加百分比",

    AdditionalPropertyType.STRENGTH: "力量",
    AdditionalPropertyType.STRENGTH_ADD_PERCENT: "力量增加百分比",

    AdditionalPropertyType.AGILITY: "敏捷",
    AdditionalPropertyType.AGILITY_ADD_PERCENT: "敏捷增加百分比",

    AdditionalPropertyType.INTELLIGENCE: "智力",
    AdditionalPropertyType.INTELLIGENCE_ADD_PERCENT: "智力增加百分比",

    AdditionalPropertyType.PERCEPTION: "感知",
    AdditionalPropertyType.PERCEPTION_ADD_PERCENT: "感知增加百分比",

    AdditionalPropertyType.ATTACK_SPEED: "出手速度",
    AdditionalPropertyType.ATTACK_SPEED_ADD_PERCENT: "出手速度增加百分比",

    AdditionalPropertyType.ATTACK: "攻击力",
    AdditionalPropertyType.ATTACK_ADD_PERCENT: "攻击力增加百分比",

    AdditionalPropertyType.HEALTH: "生命值",
    AdditionalPropertyType.HEALTH_ADD_PERCENT: "生命值增加百分比",

    AdditionalPropertyType.HEALTH_RECOVERY: "生命值恢复(每回合)",
    AdditionalPropertyType.HEALTH_RECOVERY_ADD_PERCENT: "生命值恢复增加百分比",

    AdditionalPropertyType.HEALTH_ABSORPTION: "生命吸收",
    AdditionalPropertyType.HEALTH_ABSORPTION_ADD_PERCENT: "生命吸收增加百分比",

    AdditionalPropertyType.MANA: "法力值",
    AdditionalPropertyType.MANA_ADD_PERCENT: "法力值增加百分比(每回合)",

    AdditionalPropertyType.MANA_RECOVERY: "法力值恢复",
    AdditionalPropertyType.MANA_RECOVERY_ADD_PERCENT: "法力值恢复百分比",

    AdditionalPropertyType.MANA_ABSORPTION: "法力值吸收",
    AdditionalPropertyType.MANA_ABSORPTION_ADD_PERCENT: "法力值吸收增加百分比",

    AdditionalPropertyType.COUNTERATTACK: "反击值",
    AdditionalPropertyType.COUNTERATTACK_ADD_PERCENT: "反击值增加百分比",
    AdditionalPropertyType.IGNORE_COUNTERATTACK: "无视反击值",
    AdditionalPropertyType.IGNORE_COUNTERATTACK_ADD_PERCENT: "无视反击值增加百分比",

    AdditionalPropertyType.CRITICAL_POINT: "致命点",
    AdditionalPropertyType.CRITICAL_POINT_ADD_PERCENT: "致命点增加百分比",

    AdditionalPropertyType.DAMAGE_SHIELD: "免伤护盾",

    AdditionalPropertyType.EXP_ADD_PERCENT: "经验增加百分比"
    # ，有些装备可以增加经验值获得,
}
property_cn_type_dict = {property_type_cn_dict[key]: key for key in property_type_cn_dict}
base_property_cn_type_dict = {key:property_cn_type_dict[key] for key in property_cn_type_dict if
                              key in {"体质", "力量", "敏捷", "智力", "感知", }}


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


class EquipmentPropertyAvailability:
    MIN = 1  # 最小属性
    MAX = 2  # 最大属性
    CURRENT = 3  # 当前属性
    IDENTIFY_TEMP = 4  # 鉴定得到的临时属性


class ExpBookType:
    CHARACTER = 1  # 角色


class DateType:
    HOUR_OF_DAY = 1  # 每天的几点会出现；对应的值为0到24
    DAY_OF_WEEK = 2  # 每周几；对应的值为1-7
    DAY_OF_MONTH = 3  # 每周几；对应的值为1-31
    HOLIDAY = 4  # 特殊节日会出现；参考表holiday


class BattleType:
    WITH_OTHER_PLAYER = 1
    WITH_MONSTER = 2


if __name__ == '__main__':
    print()
