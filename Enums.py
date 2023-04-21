from typing import List, Set, DefaultDict, Dict

class ItemList:
    def __init__(self):
        self.items = []
        self.name_index_dict_ = dict()
        self.index_name_dict = dict()

    def clear(self):
        self.items = []

    def get_items(self):
        return self.items

    def get_name_by_index(self, *, index: int):
        return self.index_name_dict[index]

    def get_index_by_name(self, *, name: str):
        return self.name_index_dict_[name]


class Item:
    def __init__(self, *, name: str, comment: str = '', item_list: ItemList):
        counter = len(item_list.items) + 1
        self.index = counter
        self.name = name
        self.comment = comment

        item_list.items.append(self)

        item_list.name_index_dict_[name] = counter
        item_list.index_name_dict[counter] = name

    def __repr__(self):
        return f'Item({self.index}: {self.name}, {self.comment})'


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
    name = "技能等级"
    item_list=ItemList()
    ONE = Item(name='1', comment="等级1",item_list=item_list)
    TWO = Item(name='2', comment="等级2",)
    THREE = Item(name='3', comment="等级3")
    FOUR = Item(name='4', comment="等级4")
    FIVE = Item(name='5', comment="等级5")
    SIX = Item(name='6', comment="等级6")
    SEVEN = Item(name='7', comment="等级7")
    EIGHT = Item(name='8', comment="等级8")
    NINE = Item(name='9', comment="等级9")

    items = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = NINE


class LearningApproach:
    name = "学习途径"
    Item.clear()

    IN_SKILL_ACADEMY = Item(name="技能学院", comment="直接可以获得，仅仅消耗技能点，主要是基础技能，不依赖于具体装备")
    EQUIPMENT_ADDITIONAL = Item(name="装备附加", comment="仅仅可以从装备上获得，和装备名字相关。")

    items = [IN_SKILL_ACADEMY, EQUIPMENT_ADDITIONAL]

    name_index_dict, index_name_dict = get_dict(items=items)
    default = IN_SKILL_ACADEMY


class SkillType:
    name = "技能类型"

    # 如果附带状态则收到状态抵抗的影响
    Item.clear()

    PASSIVE = Item(name='被动', comment="")
    BLESSING = Item(name='祝福', comment='可以对自己或者对方释放')
    CURSE = Item(name='诅咒', comment='只能对敌人释放。是否命中受到对方洞察值的影响')
    PHYSICAL_ATTACK = Item(name='物理攻击', comment="只能对对方释放。是否命中看自身命中和对方闪避值。")
    MAGIT_ATTACK = Item(name='魔法攻击', comment="只能对对方释放。是否命中看对方的洞察值")

    items = [PASSIVE, BLESSING, CURSE, PHYSICAL_ATTACK, MAGIT_ATTACK]
    name_index_dict, index_name_dict = get_dict(items=items)
    default = PASSIVE


class SkillTarget:
    name = "作用目标"
    Item.clear()

    SELF = Item(name='自身', comment='自身')
    ENEMY = Item(name="敌人", comment="敌人")

    name_index_dict, index_name_dict = get_dict(items=Item)
    default = SELF


class StatusType:
    name = '状态类型'
    Item.clear()

    PASSIVE = Item(name='减益', comment='减益')
    POSITIVE = Item(name="增益", comment="增益")
    NEUTRAL = Item(name="中立", comment="中立")

    items = [PASSIVE, POSITIVE, NEUTRAL]

    name_index_dict, index_name_dict = get_dict(items=items)

    default = PASSIVE


class AchievementPropertyType:
    name = '成就达成属性'
    Item.clear()

    VIP_LEVEL = Item(name='VIP等級', comment="充值动作完成后会触发")
    CHARGE = Item(name='充值数量', comment="充值动作完成后会触发")
    GOLD_NUM = Item(name="黄金数量", comment="黄金数量增加后可能会触发")
    PHYSIQUE = Item(name="体质", comment="基础属性变化的时候会触发")
    STRENGTH = Item(name="力量", comment="基础属性变化的时候会触发")
    AGILITY = Item(name="敏捷", comment="基础属性变化的时候会触发")
    INTELLIGENCE = Item(name="智力", comment="基础属性变化的时候会触发")
    LEVEL = Item(name="等级", comment="升级的时候会触发")
    KILL_BOSS_NUM = Item(name="击杀怪物数量", comment="击杀成功的时候可能会触发")
    KILL_BOSS_SUCCESS = Item(name="某个特定怪物的ID", comment="击杀成功的时候可能会触发，比如说是屠龙勇士")
    KILL_BOSS_FAILED = Item(name="被怪物打败次数", comment="击杀失败的时候可能会触发")
    PK_NUMBER = Item(name="PK胜利次数", comment="PK胜利的时候会触发")
    PK_RANK = Item(name="PK排行榜名次", comment="PK胜利的时候会触发")
    PK_RANK_RAISE = Item(name="PK排行榜名次提升数量", comment="PK胜利的时候会触发")
    SKILL = Item(name="学习技能数量", comment="学习技能的时候会触发")
    ANY_SKILL_LEVEL = Item(name="某个技能的技能等级", comment="学习技能的时候会触发")
    ALL_SKILL_LEVEL = Item(name="所有技能的技能等级和", comment="学习技能的时候会触发")
    ALL_SKILL_LEVEL_BIGGER_THAN = Item(name="所有技能中的最低等级", comment="学习技能的时候会触发")
    LOTTERY_NUM = Item(name="抽奖次数", comment="抽奖的时候可能会触发")
    WIN_LOTTERY_NUMBER = Item(name="中奖次数", comment="中奖的时候可能会触发")
    ALL_EQUIPMENT_QUALITY = Item(name="所有装备最低品质", comment="穿戴装备的时候可能会触发")
    BUY_STUFF = Item(name="购买物品", comment="从交易所购买物品的时候可能会触发")
    SELL_STUFF = Item(name="卖出物品", comment="卖出物品的时候可能会触发")
    EXP_BOOK_NUM = Item(name="使用经验书次数", comment="使用经验书的时候可能会触发")
    IDENTIFY_NUM = Item(name="鉴定次数", comment="使用鉴定卷轴的时候（包括装备鉴定卷轴，装备技能鉴定卷轴）可能会触发")
    RAISE_STAR_NUM = Item(name="第一次升星成功", comment="装备升星的时候可能会触发")
    ANY_RAISE_STAR_NUM = Item(name="某个穿戴装备升星数量", comment="装备升星的时候可能会触发")
    SUM_RAISE_STAR_NUM = Item(name="所有穿戴装备累计升星数量", comment="装备升星的时候可能会触发")
    ANY_GEM_NUM = Item(name="某件穿戴装备宝石数量", comment="镶嵌宝石、更换装备的时候可能会触发")
    SUM_GEM_NUM = Item(name="全身穿戴装备宝石数量", comment="镶嵌宝石、更换装备的时候可能会触发")

    ANNIVERSARY_FESTIVAL = Item(name="周年节日", comment="周年节日对应的称号。通过称号卷轴获得。")
    items = [VIP_LEVEL, CHARGE, GOLD_NUM,
             PHYSIQUE, STRENGTH, AGILITY, INTELLIGENCE,
             LEVEL,
             KILL_BOSS_NUM, KILL_BOSS_SUCCESS, KILL_BOSS_FAILED,
             PK_NUMBER, PK_RANK, PK_RANK_RAISE,
             SKILL, ANY_SKILL_LEVEL, ALL_SKILL_LEVEL, ALL_SKILL_LEVEL_BIGGER_THAN,
             LOTTERY_NUM, WIN_LOTTERY_NUMBER,
             ALL_EQUIPMENT_QUALITY,
             BUY_STUFF, SELL_STUFF,
             EXP_BOOK_NUM, IDENTIFY_NUM,
             RAISE_STAR_NUM, ANY_RAISE_STAR_NUM, SUM_RAISE_STAR_NUM,
             ANY_GEM_NUM, SUM_GEM_NUM,
             ANNIVERSARY_FESTIVAL,
             ]
    name_index_dict, index_name_dict = get_dict(items=items)
    default = CHARGE


class AchievementType:
    """
    成就的类型
    """
    name = '成就类型'
    Item.clear()

    VIP = Item(name='VIP称号', comment="充值动作完成后会触发")
    CHARGE = Item(name='充值', comment="充值动作完成后会触发")
    GOLD_NUM = Item(name="黄金数量", comment="黄金数量增加后可能会触发")
    BASE_PROPERTY_TYPE = Item(name="基础属性突破", comment="黄金数量增加后可能会触发")
    LEVEL = Item(name="等级", comment="升级的时候会触发")
    KILL_BOSS_SUCCESS = Item(name="击杀怪物", comment="击杀成功的时候可能会触发")
    KILL_BOSS_FAILED = Item(name="被怪物打败", comment="击杀失败的时候可能会触发")
    PK_NUMBER = Item(name="PK胜利次数", comment="PK胜利的时候会触发")
    PK_RANK = Item(name="PK排行榜名次", comment="PK胜利的时候会触发")
    PK_RANK_RAISE = Item(name="PK排行榜名次提升", comment="PK胜利的时候会触发")
    SKILL = Item(name="学习技能", comment="学习技能的时候会触发")
    LOTTERY = Item(name="抽奖", comment="抽奖的时候可能会触发")
    EQUIPMENT = Item(name="装备", comment="穿戴装备的时候可能会触发")
    BUY_STUFF = Item(name="购买物品", comment="从交易所购买物品的时候可能会触发")
    SELL_STUFF = Item(name="卖出物品", comment="卖出物品的时候可能会触发")
    EXP_BOOK = Item(name="经验书", comment="使用经验书的时候可能会触发")
    IDENTIFY = Item(name="鉴定", comment="使用鉴定卷轴的时候（包括装备鉴定卷轴，装备技能鉴定卷轴）可能会触发")
    RAISE_STAR = Item(name="装备升星强化", comment="装备升星的时候可能会触发")
    GEM = Item(name="全身宝石", comment="镶嵌宝石的时候可能会触发")

    ANNIVERSARY_FESTIVAL = Item(name="周年节日", comment="周年节日对应的称号。通过称号卷轴获得。")
    items = [VIP, CHARGE, GOLD_NUM,
             BASE_PROPERTY_TYPE,
             LEVEL,
             KILL_BOSS_FAILED,
             PK_NUMBER, PK_RANK_RAISE,
             SKILL,
             LOTTERY,
             EQUIPMENT,
             SELL_STUFF, ]

    name_index_dict, index_name_dict = get_dict(items=items)
    default = CHARGE


class EquipmentQuality:
    name = '装备品质'

    Item.clear()

    COMMON = Item(name='普通', comment="1个属性")
    EXCELLENT = Item(name='优秀', comment="2个属性")
    RARE = Item(name='稀有', comment="3个属性")
    EPIC = Item(name='史诗', comment="3个属性，可能带技能")
    MYTHIC = Item(name='传说', comment="4个属性，可能带技能")
    MYTHOLOGY = Item(name='神话', comment="4个属性")


class PartType:
    name = '装备品质'

    Item.clear()
    CLOAK = Item(name='披风', comment="1个属性")
    NECKLACE = Item(name='项链', comment="1个属性")
    COSTUME = Item(name='时装', comment="1个属性")
    AMULET = Item(name='护符', comment="1个属性")
    MOUNT = Item(name='坐骑', comment="1个属性")

    HEAD = Item(name='头部', comment="1个属性")
    SHOULDER = Item(name='护肩', comment="1个属性")
    CLOTHES = Item(name='衣服', comment="1个属性")
    WAIST = Item(name='腰', comment="1个属性")
    HAND = Item(name='手', comment="1个属性")
    LEG = Item(name='腿', comment="1个属性")
    FOOT = Item(name='足', comment="1个属性")

    WEAPON = Item(name='武器', comment="1个属性")


class StuffStatus:
    name = '物品状态'
    Item.clear()

    EQUIPMENT = Item(name='装备中', comment="参考PartType")
    IN_BAG = Item(name='在背包中', comment="在背包中放着呢")
    IN_REPOSITORY = Item(name='在仓库中', comment="在仓库中放着呢")
    IN_MAIL = Item(name='在邮件中', comment="在发给别人的邮件中。不能给系统发送带装备的邮件。发送邮件要有间隔")
    IN_SHOP = Item(name='在交易所', comment="1个属性")
    DECOMPOSE = Item(name='被分解了', comment="1个属性")
    DISCARDED = Item(name='被丢弃了', comment="1个属性")


class StuffType:
    name="物品类型"

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
    Item.clear()

    INITIAL = Item(name='初始属性')

    BASE_PROPERTY_POINT = Item(name='基础属性加点', comment='基础属性加点')

    BASE_ADDITIONAL = Item(name='基础属性对应附加属性', comment='基础属性如何转换为其它的属性')

    ACHIEVEMENT = Item(name='称号', comment='称号增加属性')

    SKILL = Item(name='技能', comment='技能增加属性')

    SKILL_BOOK = Item(name='技能书', comment='技能书的属性')

    EQUIPMENT_PROTOTYPE = Item(name='装备原型', comment='装备原型的属性')

    EQUIPMENT_RECORD = Item(name='装备记录', comment='具体某个装备的属性')

    POTION = Item(name='药剂', comment='某个药剂增加的属性')

    PLAYER = Item(name='人物', comment='某个人物的属性')

    MONSTER = Item(name='怪物', comment='某个怪物的属性')

    STATUS = Item(name='状态', comment='状态增加属性')

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
    Item.clear()

    PHYSIQUE = Item(name="体质", comment="帧率")

    PHYSIQUE_ADD_PERCENT = Item(name="体质百分比", comment="体质百分比")

    STRENGTH = Item(name="力量", comment="力量")

    STRENGTH_ADD_PERCENT = Item(name="力量百分比", comment="力量百分比")

    AGILITY = Item(name="敏捷", comment="敏捷")

    AGILITY_ADD_PERCENT = Item(name="敏捷百分比", comment="敏捷百分比")

    INTELLIGENCE = Item(name="智力", comment="智力")

    INTELLIGENCE_ADD_PERCENT = Item(name="智力百分比", comment="智力百分比")

    PERCEPTION = Item(name="感知", comment="感知")

    PERCEPTION_ADD_PERCENT = Item(name="感知百分比", comment="感知百分比")

    MANA_SHIELD = Item(name="法力护盾", comment="出手速度")

    MANA_SHIELD_ADD_PERCENT = Item(name="法力护盾百分比", comment="出手速度百分比")

    ATTACK_SPEED = Item(name="出手速度", comment="出手速度")

    ATTACK_SPEED_ADD_PERCENT = Item(name="出手速度百分比", comment="出手速度百分比")

    PHYSICS_ATTACK = Item(name="物理攻击力", comment="物理攻击力")

    PHYSICS_ATTACK_ADD_PERCENT = Item(name="物理攻击力百分比", comment="物理攻击力百分比")

    HEALTH = Item(name="生命上限", comment="生命上限")

    HEALTH_ADD_PERCENT = Item(name="生命上限百分比", comment="生命上限百分比")
    # 增加生命上限的通过状态实现；

    HEALTH_RECOVERY = Item(name="生命恢复", comment="恢复生命")

    HEALTH_RECOVERY_ADD_PERCENT = Item(name="生命恢复百分比", comment="生命恢复百分比")

    HEALTH_RECOVERY_ALL_PERCENT = Item(name="恢复百分比生命", comment="恢复百分比生命")

    HEALTH_ABSORPTION = Item(name="生命吸收", comment="出手速度")

    HEALTH_ABSORPTION_ADD_PERCENT = Item(name="生命吸收百分比", comment="出手速度百分比")

    MANA = Item(name="法力上限", comment="法力上限")

    MANA_ADD_PERCENT = Item(name="法力上限百分比", comment="法力上限百分比")

    MANA_RECOVERY = Item(name="法力恢复", comment="法力恢复")

    MANA_RECOVERY_ADD_PERCENT = Item(name="法力恢复百分比", comment="法力恢复百分比")

    MANA_RECOVERY_ALL_PERCENT = Item(name="回复百分比法力", comment="回复百分比法力")

    MANA_ABSORPTION = Item(name="法力上限", comment="法力上限")

    MANA_ABSORPTION_ADD_PERCENT = Item(name="法力上限百分比", comment="法力上限百分比")

    COUNTERATTACK = Item(name="反击", comment="反击")

    COUNTERATTACK_ADD_PERCENT = Item(name="反击百分比", comment="反击百分比")

    IGNORE_COUNTERATTACK = Item(name="无视反击", comment="无视反击")

    IGNORE_COUNTERATTACK_ADD_PERCENT = Item(name="无视反击百分比", comment="无视反击百分比")

    CRITICAL_POINT = Item(name="致命点", comment="致命点")

    CRITICAL_POINT_ADD_PERCENT = Item(name="致命点百分比", comment="致命点百分比")

    STATE_RESISTANCE = Item(name="状态抵抗", comment="状态抵抗")

    STATE_RESISTANCE_ADD_PERCENT = Item(name="状态抵抗百分比", comment="状态抵抗百分比")

    IGNORE_STATE_RESISTANCE = Item(name="无视状态抵抗", comment="无视状态抵抗")

    IGNORE_STATE_RESISTANCE_ADD_PERCENT = Item(name="无视状态抵抗百分比", comment="无视状态抵抗百分比")

    INSIGHT = Item(name="洞察", comment="洞察")

    INSIGHT_PERCENT = Item(name="洞察百分比", comment="洞察百分比")

    IGNORE_INSIGHT = Item(name="无视洞察", comment="无视洞察")

    IGNORE_INSIGHT_PERCENT = Item(name="无视洞察百分比", comment="状态抵抗百分比")

    HIT = Item(name="命中", comment="命中")

    HIT_PERCENT = Item(name="命中百分比", comment="命中百分比")

    DODGE = Item(name="闪避", comment="闪避")

    DODGE_PERCENT = Item(name="闪避百分比", comment="闪避百分比")

    WEAPON_DAMAGE = Item(name="武器伤害", comment="武器伤害")

    WEAPON_DAMAGE_PERCENT = Item(name="武器伤害百分比", comment="武器伤害百分比")

    MAGIC_ATTACK = Item(name="魔法攻击力", comment="魔法攻击力")

    MAGIC_ATTACK_PERCENT = Item(name="魔法攻击力百分比", comment="魔法攻击力百分比")

    DAMAGE_REDUCTION = Item(name="伤害减免", comment="伤害减免")

    DAMAGE_REDUCTION_PERCENT = Item(name="伤害减免百分比", comment="伤害减免百分比")

    IGNORE_DAMAGE_REDUCTION = Item(name="无视伤害减免", comment="无视伤害减免")

    IGNORE_DAMAGE_REDUCTION_PERCENT = Item(name="无视伤害减免百分比", comment="无视伤害减免百分比")

    DAMAGE_SHIELD = Item(name="免伤护盾", comment="无视伤害减免百分比")

    DAMAGE_PERCENT = Item(name="造成伤害百分比", comment="造成伤害百分比")

    TAKE_DAMAGE_PERCENT = Item(name="承受伤害百分比", comment="承受伤害百分比")

    EXP_ADD_PERCENT = Item(name="经验百分比", comment="经验百分比")

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
             MANA_SHIELD, MANA_SHIELD_ADD_PERCENT,
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
