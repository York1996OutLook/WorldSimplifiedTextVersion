class BattleType:
    """
    战斗类型
    """
    WITH_OTHER_PLAYER = 1  # 和其他玩家
    WITH_MONSTER = 2  # 和怪物Boss等
    WITH_SELF = 3  # 和自己战斗？？


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
    KILL_BOSS = 3  # 击败BOSS
    PK = 4  # PK相关
    GOLD_NUM_INCREASE = 5  # 黄金数量
    SKILL = 6  # 技能相关
    LOTTERY = 7  # 抽奖相关
    EQUIPMENT = 8  # 装备穿戴相关
    SELL_STUFF = 9  # 交易物品相关
    EXP_BOOK = 10  # 经验书相关


class EquipmentQuality:
    """Enumeration class representing different levels of equipment quality.

    Attributes:
        COMMON (int): Representing common equipment quality. # 普通
        EXCELLENT (int): Representing excellent equipment quality. # 优秀
        RARE (int): Representing rare equipment quality. # 稀有
        LEGENDARY (int): Representing legendary equipment quality. # 极品
        EPIC (int): Representing epic equipment quality. # 史诗
        MYTHIC (int): Representing mythic equipment quality. # 传说
        ULTIMATE (int): Representing ultimate equipment quality. # 终极
        ETERNAL (int): Representing eternal equipment quality. # 永恒
    """
    COMMON = 1  # 1个属性
    EXCELLENT = 2  # 1个属性
    RARE = 3  # 2个属性
    LEGENDARY = 4  # 2个属性
    EPIC = 5  # 3个属性
    MYTHIC = 6  # 3个属性
    ULTIMATE = 7  # 4个属性
    ETERNAL = 8  # 4个属性


class Part:
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

    weapon = 13  # "武器"


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
    ACHIEVEMENT = 1  # 成就称号
    SKILL = 2  # 技能
    EQUIPMENT = 3  # 装备


class AdditionalPropertyType:
    """
    装备、技能、称号所有可能的属性
    """
    PHYSIQUE = 1  # "体质"
    PHYSIQUE_ADD_PERCENT = 2  # "体质"

    STRENGTH = 3  # "力量"
    STRENGTH_ADD_PERCENT = 4  # "力量"

    AGILITY = 5  # "敏捷"
    AGILITY_ADD_PERCENT = 6  # "敏捷"

    INTELLIGENCE = 7  # "智力"
    INTELLIGENCE_ADD_PERCENT = 8  # "智力"

    PERCEPTION = 9  # "感知"
    PERCEPTION_ADD_PERCENT = 10  # "感知"

    ATTACK_SPEED = 11  # 攻击速度
    ATTACK_SPEED_ADD_PERCENT = 12  # 攻击速度增加百分比

    ATTACK = 13  # 攻击力
    ATTACK_ADD_PERCENT = 14  # 攻击力增加百分比

    HEALTH = 15  # 生命值
    HEALTH_ADD_PERCENT = 16  # 生命值增加百分比

    HEALTH_RECOVERY = 17  # 生命值回复
    HEALTH_RECOVERY_ADD_PERCENT = 18  # 生命值回复增加百分比

    HEALTH_ABSORPTION = 19  # 生命吸收
    HEALTH_ABSORPTION_ADD_PERCENT = 20  # 生命吸收增加百分比

    MANA = 21  # 法力值
    MANA_ADD_PERCENT = 22  # 法力值增加百分比

    MANA_RECOVERY = 23  # 法力值回复
    MANA_RECOVERY_ADD_PERCENT = 24  # 法力值回复百分比

    MANA_ABSORPTION = 25  # 法力值吸收
    MANA_ABSORPTION_ADD_PERCENT = 26  # 法力值吸收增加百分比

    COUNTERATTACK = 27  # 反击值
    COUNTERATTACK_ADD_PERCENT = 28  # 反击值增加百分比
    IGNORE_COUNTERATTACK = 29  # 无视反击值
    IGNORE_COUNTERATTACK_ADD_PERCENT = 30  # 无视反击值增加百分比

    CRITICAL_POINT = 31  # 致命点
    CRITICAL_POINT_ADD_PERCENT = 32  # 致命点增加百分比

    DAMAGE_SHIELD = 33  # 免伤护盾

    min_num = 1
    max_num = 33


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


if __name__ == '__main__':
    var = AdditionalPropertyType.DAMAGE_SHIELD
    print()
