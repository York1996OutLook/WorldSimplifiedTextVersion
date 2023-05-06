"""
2023年2月6日 数据库新建
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from DBHelper.tables.achievement import Achievement
from DBHelper.tables.achievement_title_book import AchievementTitleBook
from DBHelper.tables.battle_status import BattleStatus
from DBHelper.tables.box import Box
from DBHelper.tables.dust import Dust
from DBHelper.tables.equipment import Equipment
from DBHelper.tables.equipment_gem_record import EquipmentGemRecord
from DBHelper.tables.equipment_quality_dust_num import EquipmentQualityDustNum
from DBHelper.tables.equipment_star_record import EquipmentStarRecord
from DBHelper.tables.exp_book import ExpBook
from DBHelper.tables.gem import Gem
from DBHelper.tables.holiday import Holiday
from DBHelper.tables.identify_book import IdentifyBook
from DBHelper.tables.initial_skill_achievement_equipment_potion_etc_properties import \
    InitialSkillAchievementEquipmentPotionEtcPropertiesRecord
from DBHelper.tables.monster import Monster
from DBHelper.tables.monster_show_up_record import MonsterShowUpRecord
from DBHelper.tables.open_decompose_or_drop_stuffs import OpenDecomposeOrDropStuffsRecord
from DBHelper.tables.pk_rank import PK_Rank
from DBHelper.tables.player import Player
from DBHelper.tables.player_achievement_record import PlayerAchievementRecord
from DBHelper.tables.player_battle_record import PlayerBattleRecord
from DBHelper.tables.player_level_exp_skill_point import PlayerLevelExpSkillPoint
from DBHelper.tables.player_lottery_record import PlayerLotteryRecord
from DBHelper.tables.player_mail_record import PlayerMailRecord
from DBHelper.tables.player_or_monster_skill_setting import PlayerOrMonsterSkillSetting
from DBHelper.tables.player_potion_record import PlayerPotionRecord
from DBHelper.tables.player_sell_store_record import PlayerSellStoreRecord
from DBHelper.tables.player_skill_record import PlayerSkillRecord
from DBHelper.tables.player_stuff_record import PlayerStuffRecord
from DBHelper.tables.player_use_book_record import PlayerUseStuffRecord
from DBHelper.tables.potion import Potion
from DBHelper.tables.raise_star_book import RaiseStarBook
from DBHelper.tables.raise_star_prob import RaiseStarProb
from DBHelper.tables.setting import Setting
from DBHelper.tables.skill import Skill
from DBHelper.tables.skill_book import SkillBook
from DBHelper.tables.skill_cost_point import SkillCostPoint
from DBHelper.tables.skill_slot import SkillSlot
from DBHelper.tables.tips import Tips
from DBHelper.tables.world_hero_medal import WorldHeroMedal

import local_setting

Base = declarative_base()

table_classes = [Achievement, AchievementTitleBook,
                 BattleStatus, Box,
                 Dust,
                 Equipment, EquipmentGemRecord, EquipmentQualityDustNum,EquipmentStarRecord,
                 ExpBook,
                 Gem,
                 Holiday,
                 IdentifyBook, InitialSkillAchievementEquipmentPotionEtcPropertiesRecord,
                 Monster, MonsterShowUpRecord,
                 OpenDecomposeOrDropStuffsRecord,
                 PK_Rank,
                 Player, PlayerAchievementRecord, PlayerBattleRecord, PlayerLevelExpSkillPoint,PlayerUseStuffRecord,
                 PlayerLotteryRecord, PlayerMailRecord,
                 PlayerOrMonsterSkillSetting, PlayerPotionRecord,
                 PlayerSellStoreRecord, PlayerSkillRecord,
                 PlayerStuffRecord, Potion,
                 RaiseStarBook, RaiseStarProb,
                 Setting, Skill, SkillBook, SkillCostPoint, SkillSlot,
                 Tips,
                 WorldHeroMedal,
                 ]

# 全局设置
engine = create_engine(local_setting.db_connection_str)
Base.metadata.create_all(engine)

# 创建所有表格
for cls in table_classes:
    Base.metadata.create_all(engine, [cls.__table__], checkfirst=True)
