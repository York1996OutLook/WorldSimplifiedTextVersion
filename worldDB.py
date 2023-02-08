"""
2023年2月6日 数据库新建
"""
from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.tables.achievement import Achievement
from DBHelper.tables.base_property_add_record import BasePropertyAddRecord
from DBHelper.tables.base_property_additional_property import BasePropertyAdditionalProperty
from DBHelper.tables.battle_record import BattleRecord
from DBHelper.tables.battle_status import BattleStatus
from DBHelper.tables.gem import Gem
from DBHelper.tables.monster import Monster
from DBHelper.tables.open_decompose_or_drop_stuffs import OpenDecomposeOrDropStuffs
from DBHelper.tables.player import Player
from DBHelper.tables.player_achievement_record import PlayerAchievementRecord
from DBHelper.tables.player_level_exp import PlayerLevelExp
from DBHelper.tables.player_monster_additional_property_record import PlayerMonsterAdditionalPropertyRecord
from DBHelper.tables.player_sell_store_record import PlayerSellStoreRecord
from DBHelper.tables.player_stuff_record import PlayerStuffRecord
from DBHelper.tables.player_skill_record import PlayerSkillRecord
from DBHelper.tables.raise_star_prob import RaiseStarProb
from DBHelper.tables.setting import Setting
from DBHelper.tables.skill import Skill
from DBHelper.tables.skill_achievement_equipment_etc_properties import SkillAchievementEquipmentEtcProperties
from DBHelper.tables.skill_book import SkillBook
from DBHelper.tables.skill_point import SkillPoint
from DBHelper.tables.stuff_property import StuffProperty

Base = declarative_base()

table_classes = [Achievement, PlayerMonsterAdditionalPropertyRecord, BasePropertyAddRecord,
                 BasePropertyAdditionalProperty,
                 BattleRecord, BattleStatus, Gem, Monster, OpenDecomposeOrDropStuffs, Player, PlayerAchievementRecord,
                 PlayerLevelExp, PlayerSellStoreRecord, PlayerStuffRecord, PlayerSkillRecord, RaiseStarProb, Setting,
                 Skill, SkillAchievementEquipmentEtcProperties, SkillBook, SkillPoint, StuffProperty
                 ]

# 全局设置
engine = create_engine('sqlite:///worldSTV.db')
Base.metadata.create_all(engine)

# 创建所有表格
for cls in table_classes:
    Base.metadata.create_all(engine, [cls.__table__], checkfirst=True)
