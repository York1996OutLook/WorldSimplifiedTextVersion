from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 属性

class BaseProperty(Base):
    """
    基础属性名称: 体质、力量、敏捷、感知、智力
    """

    __tablename__ = 'base_property'
    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名字")


class PropertyRecord(Base):
    """人物、怪物常见属性表，后期可能会更新"""
    __tablename__ = 'property_record'

    id = Column(Integer, primary_key=True)

    attack_speed = Column(Integer, comment='出手速度')

    attack = Column(Integer, comment='攻击力')

    health = Column(Integer, comment='生命值')
    health_recovery = Column(Integer, comment='生命恢复')
    health_absorption = Column(Integer, comment='生命吸收')

    mana = Column(Integer, comment='法力值')
    mana_recovery = Column(Integer, comment='法力恢复')
    mana_absorption = Column(Integer, comment='法力吸收')

    counterattack = Column(Integer, comment='反击值')
    ignore_counterattack = Column(Integer, comment='无视反击值')

    critical_point = Column(Integer, comment='致命点')  # 致命伤害

    damage_shield = Column(Integer, comment='免伤护盾')


class Skill(Base):
    """
    人物可学习或者怪物的技能
    """
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)

    skill_name = Column(String, comment="技能名称")
    is_positive = Column(Boolean, comment="是否是主动技能，如果是主动技能则需要设置何时释放")
    effect_expression = Column(String, comment="效果说明")


# 人物相关

class Player(Base):
    """
    人物属性表
    """
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, comment='ID')
    nickname = Column(String(50), comment='昵称（QQ昵称）')
    current_level = Column(Integer, comment='当前等级')
    current_experience = Column(Integer, comment='当前经验值，为当前经验值')
    attack_property = Column(Integer, comment="参考攻击属性表")
    game_sign = Column(String, comment="游戏中的签名，可以被其他玩家查看到属性")


class PlayerLevelExp(Base):
    """
    升级所需经验
    """
    __tablename__ = "player_level_exp"

    id = Column(Integer, primary_key=True)

    level = Column(Integer, comment="等级")
    required_exp = Column(Float, comment="所需经验。非叠加；")


class BasePropertyAddRecord(Base):
    """
    基础属性会带来的附加属性提升
    """
    __tablename__ = "base_property_add_record"

    id = Column(Integer, primary_key=True, comment="ID")

    player_id = Column(Integer, "参考用户表")

    attribute = Column(String, comment="参考基础属性表：体质 力量 敏捷 智力 感知")

    power_increase = Column(Float, comment="攻击力增加")
    hp_increase = Column(Float, comment="生命值增加")
    mp_increase = Column(Float, comment="法力值增加")
    speed_increase = Column(Float, comment="出手速度增加")


class LearnedSkillRecord(Base):
    """
    已学习技能表
    """
    __tablename__ = 'learned_skill_record'

    id = Column(Integer, primary_key=True)

    player_id = Column(Integer, comment="玩家ID，qq号")

    skill_id = Column(Integer, comment="技能ID")  # ForeignKey(Skill.id)

    skill_level_id = Column(Integer, comment="已经学习的技能等级")
    learning_time_id = Column(Integer, comment="学习的时间")


# 成就系统
class Achievement(Base):
    """
    有哪些成就可以达成
    """
    __tablename__ = "achievement"

    id = Column(Integer, primary_key=True, comment="成就ID")
    name = Column(String, comment="成就名称")
    condition = Column(String, comment="达成条件")


class AchievementRecord(Base):
    """
    将玩家获得的成就记录下来
    """
    __tablename__ = "achievement_record"

    id = Column(Integer, primary_key=True, comment="成就记录ID")

    achievement_id = Column(Integer, comment="成就ID")  # ForeignKey(Achievement.id)
    character_id = Column(Integer, comment="成就达成人物ID")  # ForeignKey(CharacterProperty.id),
    achieve_time = Column(Integer, comment="成就达成时间")


# 战斗

class BattleStatus(Base):
    """
    战斗中的属性，比如中毒，火烧等等；
    """
    __tablename__ = "BattleStatus"

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="名称")
    effect = Column(String, comment="效果")


class BattleRecord(Base):
    """
    战斗中的属性
    """
    __tablename__ = "battle_record"
    id = Column(Integer, primary_key=True)
    battle_type = Column(Integer, comment="战斗类型")

    positive_id = Column(Integer, comment="主动攻击玩家ID")
    passive_id = Column(Integer, comment="被动攻击玩家ID")

    positive_won = Column(Boolean, comment="主动攻击人是否胜利")
    battle_text = Column(String, comment="战斗产生的文字说明")


# 怪物
class Monster(Base):
    """
    怪物
    """
    tablename = 'monster'

    id = Column(Integer, primary_key=True, comment='ID')
    difficulty = Column(Integer, comment='难度值')
    name = Column(Integer, comment='名称')
    exp_value = Column(Integer, comment='被击败后掉落的经验值')

    attack_property_id = Column(Integer, comment="参考攻击属性")

    active_skill_id = Column(Integer, comment='主动技能名称')

    description = Column(String, comment='怪物说明或者背景')
    drop_stuffs = Column(String, comment='可以掉落的物品')  # 格式为【物品id,概率】的文字列表；


# 装备物品

class EquipmentQuality(Base):
    """
    装备品质
    """
    __tablename__ = 'equipment_quality'

    id = Column(Integer, primary_key=True)
    quality = Column(String, comment="品质")
    bonus = Column(Integer, comment="对应加成（比例）")


class Part(Base):
    """
    Enum("披风", "项链", "时装", "护符", "坐骑", "头", "肩", "衣服", "腰", "手", "腿", "脚", "武器")
    Enum("披", "项", "装", "符", "骑", "头", "肩", "衣", "腰", "手", "腿", "脚", "武")
    """
    __tablename__ = 'part'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    one_char_name = Column(String, comment="单字名字")


class StuffPrototype(Base):
    """
    装备、物品等的属性
    """
    __tablename__ = 'stuff_prototype'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    part = Column(Integer, comment="所属位置")
    is_bound = Column(Integer, comment="是否已经绑定")
    decompose_get_stuffs = Column(String, comment="分解可以获得的物品列表")

    quality = Column(Integer, comment="参考品质表")  # 枚举类型

    complete_property1 = Column(Integer, comment="属性1")  # 为属性id的列表.满鉴定属性
    complete_property2 = Column(Integer, comment="属性2")  # 为属性id的列表.满鉴定属性
    complete_property3 = Column(Integer, comment="属性3")  # 为属性id的列表.满鉴定属性
    complete_property4 = Column(Integer, comment="属性4")  # 为属性id的列表.满鉴定属性

    property1 = Column(Integer, comment="属性1")  # 为属性id的列表.当前属性；
    property2 = Column(Integer, comment="属性2")  # 为属性id的列表.当前属性；
    property3 = Column(Integer, comment="属性3")  # 为属性id的列表.当前属性；
    property4 = Column(Integer, comment="属性4")  # 为属性id的列表.当前属性；
    introduction = Column(String, comment="说明")


class Gem(Base):
    __tablename__ = 'gem'

    id = Column(Integer, primary_key=True)
    base_property_id = Column(Integer, comment="参考基础属性表，暂时不考虑加入其它属性的宝石")
    increase = Column(Integer, comment="+1还是+2，3，4，5等")


class SkillBook(Base):
    """
    技能书的列表
    """
    __tablename__ = 'skill_book'
    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, comment="参考技能表")
    level = Column(Integer, comment="技能书的等级，高等级技能书可以学习低等级技能，但是反过来不行")


class SkillPoint(Base):
    """
    升级技能需要的技能点
    """
    __tablename__ = 'skill_point'
    id = Column(Integer, primary_key=True)
    level = Column(Integer, comment="等级")
    need_point = Column(Integer, comment="所需技能点")


class StuffStatus(Base):
    """
    物品状态
    """
    __tablename__ = 'item_status'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, comment='所属用户')
    status = Column(String, comment='物品状态')  # 枚举类型，未出售在背包中，在交易所，被分解了，被扔掉

    # 在背包中
    IN_BAG_NOT_SELL = 1  # 在背包中，且未出售
    # 在交易所
    IN_SHOP = 2  # '在交易所'，且未出售
    # 被分解了
    DECOMPOSE = 3  # '被分解了'
    # 被扔掉
    DISCARDED = 4  # '被扔掉'


# 交易所记录
class ExchangeRecord(Base):
    __tablename__ = 'exchange_record'

    id = Column(Integer, primary_key=True)

    owner_player_id = Column(Integer, comment="参考")

    stuff_name = Column(String, comment='物品名称')
    stuff_count = Column(Integer, comment="物品个数。如果不可叠加则数量是1，如果可叠加，则数量可以不是1")

    original_price = Column(int, comment='原始售价')
    initial_sell_time = Column(Integer, comment='初始挂售时间')

    is_sold = Column(Boolean, comment="是否被购买")
    deal_time = Column(Integer, comment='交易成交时间')

    tax_rate = Column(Float, comment='税率')
    taxed_price = Column(Float, comment='加税后价格；不足1则按照1进行计算')


# 全局设置

class Setting(Base):
    """
    比如：
    一个人最多可以学习多少个技能，10

    交易所税率 3%
    充值比例  200%
    挂售退回时间  2day

    每日可以挑战次数 # 10
    致命伤害的加成：2.5

    """
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True)
    name = Column(String, comment="设置的名称")
    value = Column(String, comment="设置的值，如果是数字，则将字符串转换为数字；")


engine = create_engine('sqlite:///worldSTV.db')
Base.metadata.create_all(engine)
