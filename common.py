from DBHelper.db import *
from Enums import StuffType


def get_stuff_id_by_stuff_type_and_name(*, stuff_type: StuffType, stuff_name: str, stuff_level: int = None):
    if stuff_type == StuffType.BOX:
        one_stuff = box.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.GEM:
        one_stuff = gem.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.EXP_BOOK:
        one_stuff = exp_book.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.POTION:
        one_stuff = potion.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.RAISE_STAR_BOOK:
        one_stuff = raise_star_book.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.EQUIPMENT:
        one_stuff = equipment.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.IDENTIFY_BOOK:
        one_stuff = identify_book.get_by_name(name=stuff_name)
    elif stuff_type == StuffType.SKILL_BOOK:
        if stuff_level not in range:
            raise ValueError(f"stuff_level {stuff_level} 不能是{None}")
        one_skill = skill.get_skill_by_name(name=stuff_name)
        one_stuff = skill_book.get_by_skill_id_skill_level(skill_id=one_skill.id, level=stuff_level).id
    else:
        raise ValueError('类型处理函数未定义')
    return one_stuff.id


def get_stuff_by_stuff_type_and_id(*,
                                         stuff_type: StuffType,
                                         stuff_id: int
                                         ) -> box.Box or gem.Gem or exp_book.ExpBook or potion.Potion or \
                                              raise_star_book.RaiseStarBook or equipment.Equipment or \
                                              identify_book.IdentifyBook or skill_book.SkillBook:
    if stuff_type == StuffType.BOX:
        one_stuff = box.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.GEM:
        one_stuff = gem.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.EXP_BOOK:
        one_stuff = exp_book.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.POTION:
        one_stuff = potion.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.RAISE_STAR_BOOK:
        one_stuff = raise_star_book.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.EQUIPMENT:
        one_stuff = equipment.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.IDENTIFY_BOOK:
        one_stuff = identify_book.get_by_id(_id=stuff_id)
    elif stuff_type == StuffType.SKILL_BOOK:
        one_stuff = skill_book.get_by_id(_id=stuff_id)
    else:
        raise ValueError('类型处理函数未定义')
    return one_stuff
