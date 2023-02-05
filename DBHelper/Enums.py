from enum import Enum


class BasePropertyEnum(Enum):
    physique = "体质"
    strength = "力量"
    agility = "敏捷"
    intelligence = "智力"
    perception = "感知"

class Part(Enum):
    Cloak = "披风"
    Necklace = "项链"
    Costume = "时装"
    Amulet = "护符"
    Mount = "坐骑"
    Head = "头"
    Shoulder = "肩"
    Clothes = "衣服"
    Waist = "腰"
    Hand = "手"
    Leg = "腿"
    Foot = "脚"
    Weapon = "武器"

class StuffStatus(Enum):
    IN_BAG_NOT_SELL = 1  # 在背包中，且未出售
    IN_SHOP = 2  # '在交易所'，且未出售
    DECOMPOSE = 3  # '被分解了'
    DISCARDED = 4  # '被扔掉'
