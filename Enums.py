from typing import List, Set, DefaultDict, Dict


class ItemList:
    def __init__(self):
        Item.item_list = self

        self.items = []
        self.name_index_dict = dict()
        self.index_name_dict = dict()
        self.counter = 0

    def clear(self):
        self.items = []

    def get_items(self)->List["Item"]:
        return self.items

    def get_names(self) -> List[str]:
        names = [item.name for item in self.items]
        return names

    def get_name_by_index(self, *, index: int)->str:
        if index not in self.index_name_dict:
            return None
        return self.index_name_dict[index]

    def get_index_by_name(self, *, name: str)->int:
        if name not in self.name_index_dict:
            return None
        return self.name_index_dict[name]


class Item:
    item_list = None

    def __init__(self, *, name: str, comment: str = '', index=None):
        if index:
            self.index = index
        else:
            self.index = len(self.item_list.items) + 1

        self.name = name
        self.comment = comment

        self.item_list.items.append(self)

        if self.name in self.item_list.name_index_dict:
            raise ValueError(f"name:{self.name} is already exists!")
        if self.name in self.item_list.name_index_dict:
            raise ValueError(f"index:{self.index} is already exists!")

        self.item_list.name_index_dict[self.name] = self.index
        self.item_list.index_name_dict[self.index] = self.name

    def __repr__(self)->str:
        return f'Item({self.index}: {self.name}, {self.comment})'


def get_dict(*, items: List[Item]):
    name_index_dict = dict()
    index_name_dict = dict()
    for item in items:
        name_index_dict[item.name] = item.index
        index_name_dict[item.index] = item.name
    return name_index_dict, index_name_dict


class SkillLevel:
    name = "技能等级"
    item_list = ItemList()

    ONE = Item(name='1', comment="等级1", )
    TWO = Item(name='2', comment="等级2", )
    THREE = Item(name='3', comment="等级3")
    FOUR = Item(name='4', comment="等级4")
    FIVE = Item(name='5', comment="等级5")
    SIX = Item(name='6', comment="等级6")
    SEVEN = Item(name='7', comment="等级7")
    EIGHT = Item(name='8', comment="等级8")
    NINE = Item(name='9', comment="等级9")

    default = NINE


class DataType:
    name = "数据类型"
    item_list = ItemList()

    TIMESTAMP = Item(name="时间戳类型", comment="本质还是整数类型，为了显示的时候可以显示陈哥时间格式")
    INTEGER = Item(name="整数类型", comment="整数类型")
    BOOL = Item(name="布尔类型", comment="整数类型")
    STRING = Item(name="字符串", comment="整数类型")
    TEXT = Item(name="文本", comment="整数类型")
    default = INTEGER


class LearningApproach:
    name = "学习途径"
    item_list = ItemList()

    IN_SKILL_ACADEMY = Item(name="技能学院", comment="直接可以获得，仅仅消耗技能点，主要是基础技能，不依赖于具体装备")
    EQUIPMENT_ADDITIONAL = Item(name="装备附加", comment="仅仅可以从装备上获得，和装备名字相关。")

    default = IN_SKILL_ACADEMY


class SkillType:
    name = "技能类型"

    item_list = ItemList()

    PASSIVE = Item(name='被动', comment="")
    BLESSING = Item(name='祝福', comment='可以对自己或者对方释放')
    CURSE = Item(name='诅咒', comment='只能对敌人释放。是否命中受到对方洞察值的影响')
    PHYSICAL_ATTACK = Item(name='物理攻击', comment="只能对对方释放。是否命中看自身命中和对方闪避值。")
    MAGIT_ATTACK = Item(name='魔法攻击', comment="只能对对方释放。是否命中看对方的洞察值")

    default = PASSIVE


class SkillTarget:
    name = "作用目标"

    item_list = ItemList()

    SELF = Item(name='自身', comment='自身')
    ENEMY = Item(name="敌人", comment="敌人")

    default = SELF


class StatusType:
    name = '状态类型'
    item_list = ItemList()

    PASSIVE = Item(name='减益', comment='减益')
    POSITIVE = Item(name="增益", comment="增益")
    NEUTRAL = Item(name="中立", comment="中立")

    default = PASSIVE


class BindType:
    name = '绑定类型'

    long_string = 2


class AchievementPropertyType:
    name = '成就达成属性'
    item_list = ItemList()

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

    default = CHARGE


class AchievementType:
    """
    成就的类型
    """
    name = '成就类型'

    item_list = ItemList()

    VIP = Item(name='VIP称号', comment="开通vip后会触发")
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

    default = CHARGE


class EquipmentQuality:
    name = '装备品质'

    item_list = ItemList()

    COMMON = Item(name='普通', comment="1个属性")
    EXCELLENT = Item(name='优秀', comment="2个属性")
    RARE = Item(name='稀有', comment="3个属性")
    EPIC = Item(name='史诗', comment="3个属性，可能带技能")
    MYTHIC = Item(name='传说', comment="4个属性，可能带技能")
    MYTHOLOGY = Item(name='神话', comment="4个属性")

    default = COMMON


class PartType:
    name = '装备品质'

    item_list = ItemList()

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

    default = CLOAK


class StuffStatus:
    name = '物品状态'

    item_list = ItemList()

    EQUIPMENT = Item(name='装备中', comment="参考PartType")
    IN_BAG = Item(name='在背包中', comment="在背包中放着呢")
    IN_REPOSITORY = Item(name='在仓库中', comment="在仓库中放着呢")
    IN_MAIL = Item(name='在邮件中', comment="在发给别人的邮件中。不能给系统发送带装备的邮件。发送邮件要有间隔")
    IN_SHOP = Item(name='在交易所', comment="1个属性")
    DECOMPOSE = Item(name='被分解了', comment="1个属性")
    DISCARDED = Item(name='被丢弃了', comment="1个属性")

    default = EQUIPMENT


class StuffType:
    name = "物品类型"

    item_list = ItemList()
    EQUIPMENT = Item(name='装备', comment="装备，包含武器、装备、坐骑")
    BOX = Item(name='箱子', comment="允许一次性使用多个")
    GEM = Item(name='宝石', comment="加不同属性的宝石。不能一次镶嵌多个")
    RAISE_STAR_BOOK = Item(name='升星卷轴', comment="可以一次性使用多个")
    IDENTIFY_BOOK = Item(name='装备属性鉴定卷轴', comment="1个属性，不可以一次性使用多个")
    SKILL_IDENTIFY_BOOK = Item(name='装备技能鉴定卷轴', comment="1个属性")
    EXP_BOOK = Item(name='经验卷轴', comment="为人物增加经验")
    SKILL_BOOK = Item(name='人物技能卷轴', comment="技能书")
    SKILL_SLOT = Item(name='人物技能槽', comment="技能书")
    POTION = Item(name='药水', comment="药剂，一般是临时的")
    DUST = Item(name='装备粉尘', comment="装备分解获得，计划用来鉴定装备的时候用")
    ACHIEVEMENT_TITLE_BOOK = Item(name='成就称号', comment="称号，使用后可以获得某个称号。部分称号为自动获得，不一定要通过使用成就称号来获得。")
    MONSTER = Item(name='怪物', comment="暂时不清楚后续是否会用到")
    WorldHeroMedal = Item(name='世界英雄勋章', comment="暂时不清楚后续是否会用到")

    default = EQUIPMENT


multiple_use_stuffs = {
    StuffType.BOX,
    StuffType.RAISE_STAR_BOOK,
    StuffType.EXP_BOOK,
    StuffType.SKILL_BOOK,
}


class BeingType:
    name = "生物类型"
    item_list = ItemList()

    PLAYER = Item(name='玩家', comment="")
    MONSTER = Item(name='怪物', comment="")

    default = PLAYER


class AdditionSourceType:
    name = '属性来源'

    item_list = ItemList()

    INITIAL = Item(name='初始属性')
    BASE_PROPERTY_POINT = Item(name='基础属性加点', comment='基础属性加点')
    BASE_ADDITIONAL = Item(name='基础属性对应附加属性', comment='基础属性如何转换为其它的属性')
    ACHIEVEMENT_TITLE = Item(name='称号', comment='称号增加属性')
    SKILL = Item(name='技能', comment='技能增加属性')
    SKILL_BOOK = Item(name='技能书', comment='技能书的属性')
    EQUIPMENT_PROTOTYPE = Item(name='装备原型', comment='装备原型的属性')
    EQUIPMENT_RECORD = Item(name='装备记录', comment='具体某个装备的属性')
    POTION = Item(name='药剂', comment='某个药剂增加的属性')
    PLAYER = Item(name='人物', comment='某个人物的属性')
    MONSTER = Item(name='怪物', comment='某个怪物的属性')
    STATUS = Item(name='状态', comment='状态增加属性')

    default = INITIAL


class GemInlayingStatus:
    """
    一般只有装备可以镶嵌宝石；
    """
    name = '宝石镶嵌状态'
    item_list = ItemList()

    NOT_INLAYING = Item(name='未镶嵌宝石', comment='状态增加属性')
    INLAYING = Item(name='未破损', comment='状态增加属性')
    DAMAGED_INLAYING = Item(name='镶嵌破损', comment='状态增加属性')

    default = NOT_INLAYING


class AdditionalPropertyType:
    """
    装备、技能、称号所有可能的属性
    """
    name = '所有属性'
    item_list = ItemList()

    PHYSIQUE = Item(name="体质", comment="体质")
    PHYSIQUE_PERCENT = Item(name="体质百分比", comment="体质百分比")

    STRENGTH = Item(name="力量", comment="力量")
    STRENGTH_PERCENT = Item(name="力量百分比", comment="力量百分比")

    AGILITY = Item(name="敏捷", comment="敏捷")
    AGILITY_PERCENT = Item(name="敏捷百分比", comment="敏捷百分比")

    INTELLIGENCE = Item(name="智力", comment="智力")
    INTELLIGENCE_PERCENT = Item(name="智力百分比", comment="智力百分比")

    PERCEPTION = Item(name="感知", comment="感知")
    PERCEPTION_PERCENT = Item(name="感知百分比", comment="感知百分比")

    MANA_SHIELD = Item(name="法力护盾", comment="法力护盾")
    MANA_SHIELD_PERCENT = Item(name="法力护盾百分比", comment="出手速度百分比")

    DEDUCT_MANA_SHIELD = Item(name="扣除法力护盾", comment="")
    DEDUCT_MANA_SHIELD_PERCENT = Item(name="扣除当前法力护盾百分比", comment="")
    DEDUCT_MANA_SHIELD_UPPER_LIMIT_PERCENT = Item(name="扣除法力护盾上限百分比", comment="")

    ATTACK_SPEED = Item(name="出手速度", comment="出手速度")
    ATTACK_SPEED_PERCENT = Item(name="出手速度百分比", comment="出手速度百分比")

    DEDUCT_ATTACK_SPEED = Item(name="扣除出手速度", comment="")
    DEDUCT_ATTACK_SPEED_PERCENT = Item(name="扣除当前出手速度百分比", comment="")
    DEDUCT_ATTACK_SPEED_UPPER_LIMIT_PERCENT = Item(name="扣除出手速度上限百分比", comment="")

    PHYSICS_ATTACK = Item(name="物理攻击力", comment="物理攻击力")
    PHYSICS_ATTACK_PERCENT = Item(name="物理攻击力百分比", comment="物理攻击力百分比")

    HEALTH = Item(name="生命上限", comment="生命上限")
    HEALTH_PERCENT = Item(name="生命上限百分比", comment="生命上限百分比")

    DEDUCT_HEALTH = Item(name="扣除生命值", comment="")
    DEDUCT_HEALTH_PERCENT = Item(name="扣除当前生命值百分比", comment="")
    DEDUCT_HEALTH_UPPER_LIMIT_PERCENT = Item(name="扣除生命上限百分比", comment="")

    HEALTH_RECOVERY = Item(name="生命恢复", comment="恢复生命")
    HEALTH_RECOVERY_PERCENT = Item(name="生命恢复百分比", comment="生命恢复百分比")
    HEALTH_RECOVERY_UPPER_LIMIT_PERCENT = Item(name="恢复百分比生命", comment="恢复百分比生命")

    HEALTH_ABSORPTION = Item(name="生命吸收", comment="出手速度")
    HEALTH_ABSORPTION_PERCENT = Item(name="生命吸收百分比", comment="生命吸收百分比")

    MANA = Item(name="法力上限", comment="法力上限")
    MANA_PERCENT = Item(name="法力上限百分比", comment="法力上限百分比")

    DEDUCT_MANA = Item(name="扣除法力值", comment="")
    DEDUCT_MANA_PERCENT = Item(name="扣除当前法力值百分比", comment="")
    DEDUCT_MANA_UPPER_LIMIT_PERCENT = Item(name="扣除法力值上限百分比", comment="")

    MANA_RECOVERY = Item(name="法力恢复", comment="法力恢复")
    MANA_RECOVERY_PERCENT = Item(name="法力恢复百分比", comment="法力恢复百分比")
    MANA_RECOVERY_UPPER_LIMIT_PERCENT = Item(name="回复百分比法力", comment="回复百分比法力")

    MANA_ABSORPTION = Item(name="法力吸收", comment="法力吸收")
    MANA_ABSORPTION_PERCENT = Item(name="法力吸收百分比", comment="法力吸收百分比")

    COUNTERATTACK = Item(name="反击", comment="反击")
    COUNTERATTACK_PERCENT = Item(name="反击百分比", comment="反击百分比")

    IGNORE_COUNTERATTACK = Item(name="无视反击", comment="无视反击")
    IGNORE_COUNTERATTACK_PERCENT = Item(name="无视反击百分比", comment="无视反击百分比")

    DEDUCT_COUNTERATTACK = Item(name="扣除反击值", comment="")
    DEDUCT_COUNTERATTACK_PERCENT = Item(name="扣除当前反击值百分比", comment="")
    DEDUCT_COUNTERATTACK_UPPER_LIMIT_PERCENT = Item(name="扣除反击值上限百分比", comment="")

    CRITICAL_POINT = Item(name="致命点", comment="致命点")
    CRITICAL_POINT_PERCENT = Item(name="致命点百分比", comment="致命点百分比")

    STATE_RESISTANCE = Item(name="状态抵抗", comment="状态抵抗")
    STATE_RESISTANCE_PERCENT = Item(name="状态抵抗百分比", comment="状态抵抗百分比")
    IGNORE_STATE_RESISTANCE = Item(name="无视状态抵抗", comment="无视状态抵抗")
    IGNORE_STATE_RESISTANCE_PERCENT = Item(name="无视状态抵抗百分比", comment="无视状态抵抗百分比")

    DEDUCT_STATE_RESISTANCE = Item(name="扣除状态抵抗", comment="")
    DEDUCT_STATE_RESISTANCE_PERCENT = Item(name="扣除当前状态抵抗百分比", comment="")
    DEDUCT_STATE_RESISTANCE_UPPER_PERCENT = Item(name="扣除状态抵抗上限百分比", comment="")

    INSIGHT = Item(name="洞察", comment="洞察")
    INSIGHT_PERCENT = Item(name="洞察百分比", comment="洞察百分比")
    IGNORE_INSIGHT = Item(name="无视洞察", comment="无视洞察")
    IGNORE_INSIGHT_PERCENT = Item(name="无视洞察百分比", comment="无视洞察百分比")

    DEDUCT_INSIGHT = Item(name="扣除洞察", comment="")
    DEDUCT_INSIGHT_PERCENT = Item(name="扣除当前洞察百分比", comment="")
    DEDUCT_INSIGHT_UPPER_LIMIT_PERCENT = Item(name="扣除洞察上限百分比", comment="")

    HIT = Item(name="命中", comment="命中")
    FORCED_HIT = Item(name="强制命中率", comment="100为满，先根据强制命中率计算是否命中，如果不命中，则根据命中计算；")
    HIT_PERCENT = Item(name="命中百分比", comment="命中百分比")

    DEDUCT_HIT = Item(name="扣除命中", comment="")
    DEDUCT_HIT_PERCENT = Item(name="扣除当前命中百分比", comment="")
    DEDUCT_HIT_UPPER_LIMIT_PERCENT = Item(name="扣除命中上限百分比", comment="")

    DODGE = Item(name="闪避", comment="闪避")
    DODGE_PERCENT = Item(name="闪避百分比", comment="闪避百分比")

    DEDUCT_DODGE = Item(name="扣除闪避", comment="")
    DEDUCT_DODGE_PERCENT = Item(name="扣除当前闪避百分比", comment="")
    DEDUCT_DODGE_UPPER_LIMIT_PERCENT = Item(name="扣除闪避上限百分比", comment="")

    WEAPON_DAMAGE = Item(name="武器伤害", comment="武器伤害")
    WEAPON_DAMAGE_PERCENT = Item(name="武器伤害百分比", comment="武器伤害百分比")

    MAGIC_ATTACK = Item(name="魔法攻击力", comment="魔法攻击力")
    MAGIC_ATTACK_PERCENT = Item(name="魔法攻击力百分比", comment="魔法攻击力百分比")

    DAMAGE_REDUCTION = Item(name="伤害减免", comment="伤害减免")
    DAMAGE_REDUCTION_PERCENT = Item(name="伤害减免百分比", comment="伤害减免百分比")
    IGNORE_DAMAGE_REDUCTION = Item(name="无视伤害减免", comment="无视伤害减免")
    IGNORE_DAMAGE_REDUCTION_PERCENT = Item(name="无视伤害减免百分比", comment="无视伤害减免百分比")

    DEDUCT_DAMAGE_REDUCTION = Item(name="扣除伤害减免", comment="")
    DEDUCT_DAMAGE_REDUCTION_PERCENT = Item(name="扣除当前伤害减免百分比", comment="")
    DEDUCT_DAMAGE_REDUCTION_UPPER_LIMIT_PERCENT = Item(name="扣除伤害减免上限百分比", comment="")

    DAMAGE_SHIELD = Item(name="免伤护盾", comment="免伤护盾")

    DAMAGE_PERCENT = Item(name="造成伤害百分比", comment="造成伤害百分比，状态用到")
    TAKE_DAMAGE_PERCENT = Item(name="承受伤害百分比", comment="承受伤害百分比，状态用到")

    EXP_PERCENT = Item(name="经验百分比", comment="经验百分比")

    default = PHYSIQUE


class BasePropertyType:  # 目前宝石和基础属性公用一套属性。所以宝石的类型也仅仅限于这些类型。
    """
    为了和附加属性一致，因为其存储在一个表上；
    """
    name = '基础属性'
    item_list = ItemList()

    PHYSIQUE = Item(name="体质", comment="体质", index=AdditionalPropertyType.PHYSIQUE.index)
    STRENGTH = Item(name="力量", comment="力量", index=AdditionalPropertyType.STRENGTH.index)
    AGILITY = Item(name='敏捷', comment="敏捷", index=AdditionalPropertyType.AGILITY.index)
    INTELLIGENCE = Item(name="智力", comment="智力", index=AdditionalPropertyType.INTELLIGENCE.index)
    PERCEPTION = Item(name="感知", comment="感知", index=AdditionalPropertyType.PERCEPTION.index)

    default = PHYSIQUE


class MailReadStatus:
    name = "邮件阅读状态"


class MailType:
    name = '邮件类型'
    item_list = ItemList()

    SEND_TO_OTHER_PLAYER = Item(name="寄给其他玩家", comment="由玩家寄出给别人的，需要指明收费多少；")
    SEND_TO_OTHER_PLAYER_GET_REJECT = Item(name="被其他玩家退回", comment="由玩家寄出给别人的，然后被退回了，需要指明收费多少；")
    SEND_TO_GAME_MASTER = Item(name="寄给游戏管理员", comment="寄给游戏管理员的")

    RECEIVED_FROM_TEAM_AWARD = Item(name="组队时击杀奖励邮件", comment="组队的时候击杀boss奖励的邮件，不直接到玩家背包中，而是到邮件中，因为背包可能已经满了。")

    RECEIVED_FROM_OTHER_PLAYER = Item(name="其他玩家发来的邮件", comment="由其他玩家寄给当前玩家的，需要指明收费多少")
    RECEIVED_FROM_GAME_MASTER = Item(name="从管理员发来的邮件", comment="从游戏管理员那里收到的。包含奖励邮件、充值邮件、管理员回复邮件")

    RECEIVED_FROM_EXCHANGE_STORE_SOLD = Item(name="卖出物品的邮件", comment="交易所发给自己的邮件（卖出了）；")
    RECEIVED_FROM_EXCHANGE_STORE_NOT_SOLD_RETURN = Item(name="交易所到期邮件", comment="交易所发给自己的邮件（时间到了，未售出，退回）；")
    RECEIVED_FROM_EXCHANGE_STORE_POSITIVE_RETURN = Item(name="玩家主动从交易所撤销销售的邮件",
                                                        comment="交易所发给自己的邮件（时间未到，但是玩家选择主动退回，不挂售）")

    default = SEND_TO_OTHER_PLAYER


class CalendarType:
    name = '日期类型'
    item_list = ItemList()

    LUNAR = Item(name="农历", comment="")
    GREGORIAN = Item(name="公历", comment="")

    default = LUNAR


class PropertyAvailability:
    name = '属性可用类型'
    item_list = ItemList()
    CURRENT = Item(name="当前属性", comment="")

    MIN = Item(name="最小属性", comment="")
    MAX = Item(name="最大属性", comment="")
    IDENTIFY_TEMP = Item(name="鉴定得到的临时属性", comment="")

    default = CURRENT


class ExpBookType:
    name = '经验卷轴的类型'
    item_list = ItemList()

    CHARACTER = Item(name="人物", comment="目前仅仅有人物类型的经验卷轴")

    default = CHARACTER


class MonsterTypes:
    name = "怪物类型"
    comment = '怪物的可能类型，可能有多个'
    item_list = ItemList()

    DESERT = Item(name="荒漠", comment="戈壁，沙漠，神殿，沙土，土地")
    ICE_SNOW = Item(name="冰雪", comment="冰河，冰川，雪山，南北极，雪地，雪原")
    GRASS = Item(name="草原", comment="草地，植被，灌木丛")
    FOREST = Item(name="森林", comment="深林，雨林，树林")
    MOUNTAIN = Item(name="山峦", comment="峡谷，岩石，火山，雪山峡谷，山峰，山地，丘陵")
    OCEAN = Item(name='海洋', comment="湖泊，河流，深海，沼泽，海底遗迹，岛屿")
    EAST_PALACE = Item(name='东方宫殿', comment="村舍、围城，四合院，紫禁城，皇宫，府邸，山水画水墨画庙宇")
    WEST_PALACE = Item(name='西方宫殿', comment="城邦、教堂、城堡，要塞，花园，泳池，油画浮雕雕刻")
    CITY = Item(name="都市", comment="楼宇，高楼，建筑物")
    WAR = Item(name="战场", comment="战场，战地，阵地，战区，攻城，军事，战争")
    SKY = Item(name="天空", comment="大气层，鸟类栖息地，翱翔，云层，虚空")
    HELL = Item(name="地狱", comment="炼狱，地下，地底，阴曹地府")
    HEAVEN = Item(name='天堂', comment="天堂，天国，西天，极乐之地，诸神")
    ALIEN = Item(name='外星', comment="外星人，外星球，不明飞行物")
    MICROORGANISM = Item(name="微生物", comment="缩小体积，病毒，细菌，蛋白质，癌细胞，坏死细胞")
    VIRTUAL = Item(name='虚拟', comment="虚拟的，模拟的，虚构的，网络，电子，元宇宙，病毒，意识，代码，信号")

    OTHER = Item(name="其他", comment="其他不便于分类的怪物类型或者较少的类型")

    default = OTHER


class DateType:
    name = "日期类型"
    item_list = ItemList()

    HOUR_OF_DAY = Item(name="几点", comment="每天的几点会出现；对应的值为0到24")
    DAY_OF_WEEK = Item(name="周几", comment="每周几；对应的值为1-7")
    DAY_OF_MONTH = Item(name="几号", comment="每周几；对应的值为1-31")
    WEEK_OF_YEAR = Item(name="第几周", comment="每年的第几周会出现")
    HOLIDAY = Item(name="节日", comment="特殊节日会出现；参考表holiday")

    default = HOUR_OF_DAY


class BattleType:
    name = "战斗类型"

    item_list = ItemList()

    WITH_OTHER_PLAYER = Item(name="与其它玩家")
    WITH_MONSTER = Item(name='与怪物')

    default = WITH_OTHER_PLAYER


if __name__ == '__main__':
    print()
