"""
2023年2月6日 数据库新建
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.tables.achievement import Achievement
from DBHelper.tables.base_property_additional_property import BasePropertyAdditionalProperty
from DBHelper.tables.battle_status import BattleStatus
from DBHelper.tables.box import Box
from DBHelper.tables.equipment import Equipment
from DBHelper.tables.equipment_gem_record import EquipmentGemRecord
from DBHelper.tables.exp_book import ExpBook
from DBHelper.tables.gem import Gem
from DBHelper.tables.holiday import Holiday
from DBHelper.tables.identify_book import IdentifyBook
from DBHelper.tables.monster import Monster
from DBHelper.tables.monster_show_up_record import MonsterShowUpRecord
from DBHelper.tables.monster_skill_record import MonsterSkillRecord
from DBHelper.tables.open_decompose_or_drop_stuffs import OpenDecomposeOrDropStuffsRecord
from DBHelper.tables.player import Player
from DBHelper.tables.player_achievement_record import PlayerAchievementRecord
from DBHelper.tables.player_battle_record import PlayerBattleRecord
from DBHelper.tables.player_level_exp_skill_point import PlayerLevelExpSkillPoint
from DBHelper.tables.player_lottery_record import PlayerLotteryRecord
from DBHelper.tables.player_mail_record import PlayerMailRecord
from DBHelper.tables.player_monster_additional_property_record import PlayerMonsterAdditionalPropertyRecord
from DBHelper.tables.player_sell_store_record import PlayerSellStoreRecord
from DBHelper.tables.player_or_monster_skill_setting import PlayerOrMonsterSkillSetting
from DBHelper.tables.player_potion_record import PlayerPotionRecord
from DBHelper.tables.player_skill_record import PlayerSkillRecord
from DBHelper.tables.player_stuff_record import PlayerStuffRecord
from DBHelper.tables.potion import Potion
from DBHelper.tables.raise_star_book import RaiseStarBook
from DBHelper.tables.raise_star_prob import RaiseStarProb
from DBHelper.tables.setting import Setting
from DBHelper.tables.skill import Skill
from DBHelper.tables.skill_book import SkillBook
from DBHelper.tables.initial_skill_achievement_equipment_potion_etc_properties import \
    InitialSkillAchievementEquipmentPotionEtcPropertiesRecord
from DBHelper.tables.skill_cost_mana import PositiveSkillCostMana
from DBHelper.tables.skill_cost_point import SkillCostPoint
from DBHelper.tables.tips import Tips

Base = declarative_base()

table_classes = [Achievement,
                 BasePropertyAdditionalProperty, BattleStatus, Box,
                 Equipment, EquipmentGemRecord, ExpBook,
                 Gem,
                 Holiday,
                 IdentifyBook, InitialSkillAchievementEquipmentPotionEtcPropertiesRecord,
                 Monster, MonsterShowUpRecord, MonsterSkillRecord,
                 OpenDecomposeOrDropStuffsRecord,
                 Player, PlayerAchievementRecord, PlayerBattleRecord, PlayerLevelExpSkillPoint,
                 PlayerLotteryRecord, PlayerMailRecord, PlayerMonsterAdditionalPropertyRecord,
                 PlayerOrMonsterSkillSetting, PlayerPotionRecord,
                 PlayerSellStoreRecord, PlayerSkillRecord,
                 PlayerStuffRecord, PositiveSkillCostMana, Potion,
                 RaiseStarBook, RaiseStarProb,
                 Setting, Skill, SkillBook, SkillCostPoint,
                 Tips,
                 ]

# 全局设置
engine = create_engine('sqlite:///F:\Python-code\WorldSimplifiedTextVersion\DBHelper\worldSTV.db')
Base.metadata.create_all(engine)

# 创建所有表格
for cls in table_classes:
    Base.metadata.create_all(engine, [cls.__table__], checkfirst=True)
