import re

import ujson

from scripts.game_structure.game_essentials import game
from scripts.utility import (
    get_alive_status_cats,
    filter_relationship_type,
)

def event_for_location(locations: list) -> bool:
    """
    checks if the clan is within the given locations
    """
    if "any" in locations:
        return True

    for place in locations:
        if ":" in place:
            info = place.split(":")
            req_biome = info[0]
            req_camps = info[1].split("_")
        else:
            req_biome = place
            req_camps = ["any"]

        if req_biome == game.clan.biome.lower():
            if "any" in req_camps or game.clan.camp_bg in req_camps:
                return True
        return False


def event_for_season(seasons: list) -> bool:
    """
        checks if the clan is within the given seasons
        """
    if "any" in seasons or game.clan.current_season.lower() in seasons:
        return True

    return False


def event_for_tags(tags: list, cat, other_cat=None) -> bool:
    """
        checks if current tags disqualify the event
        """
    if not tags:
        return True

    # some events are mode specific
    mode = game.clan.game_mode
    possible_modes = ["classic", "expanded", "cruel_season"]
    for _poss in possible_modes:
        if _poss in tags and mode != _poss:
            return False

    # check leader life tags
    if cat.status == "leader":
        leader_lives = game.clan.leader_lives

        life_lookup = {
            "some_lives": 4,
            "lives_remain": 2,
            "high_lives": 7,
            "mid_lives": 4,
            "low_lives": 1
        }

        for _con, _val in life_lookup.items():
            if _con in tags and leader_lives < _val:
                return False

    # check for required ranks within the clan
    for _tag in tags:
        rank_match = re.match(r"clan:(.+)", _tag)
        if not rank_match:
            continue
        ranks = [x for x in rank_match.group(1).split(",")]

        for rank in ranks:
            if rank == "apps":
                if not get_alive_status_cats(
                        cat,
                        ["apprentice", "medicine cat apprentice", "mediator apprentice"]):
                    return False
                else:
                    continue

            if rank in ["leader", "deputy"] and not get_alive_status_cats(cat, [rank]):
                return False

            if not len(get_alive_status_cats(cat, [rank])) >= 2:
                return False

    # check if main cat will allow for adoption
    if "adoption" in tags:
        if cat.no_kits:
            return False
        if cat.moons <= 14 + cat.age_moons["kitten"][1]:
            return False
        if any(cat.fetch_cat(i).no_kits for i in cat.mate):
            return False

    if other_cat and "romantic" in tags and not other_cat.is_potential_mate(cat):
        return False

    return True


def event_for_reputation(required_rep: list) -> bool:
    """
        checks if the clan has reputation matching required_rep
        """
    if "any" in required_rep:
        return True

    clan_rep = game.clan.reputation

    if "hostile" in required_rep and 0 <= clan_rep <= 30:
        return True
    elif "neutral" in required_rep and 31 <= clan_rep <= 70:
        return True
    elif "welcoming" in required_rep and 71 <= clan_rep:
        return True

    return False


def event_for_clan_relations(required_rel: list, other_clan) -> bool:
    """
        checks if the clan has clan relations matching required_rel
        """
    if "any" in required_rel:
        return True

    current_rel = other_clan.relations

    if "hostile" in required_rel and 0 <= current_rel <= 6:
        return True
    elif "neutral" in required_rel and 7 <= current_rel <= 17:
        return True
    elif "ally" in required_rel and 18 <= current_rel:
        return True

    return False


def event_for_freshkill_supply(pile, trigger, factor, clan_size) -> bool:
    """
        checks if clan has the correct amount of freshkill for event
        """
    if game.clan.game_mode == "classic":
        return False

    needed_amount = pile.amount_food_needed()
    half_amount = needed_amount / 2
    clan_supply = pile.total_amount

    if "always" in trigger:
        return True
    if "low" in trigger and half_amount > clan_supply:
        return True
    if "adequate" in trigger and half_amount < clan_supply < needed_amount:
        return True

    # find how much is too much freshkill
    # it would probably be good to move this section of finding trigger_value to the freshkill class
    divider = 35 if game.clan.game_mode == "expanded" else 20
    factor = factor - round(
        pow((clan_size / divider), 2)
    )
    if factor < 2 and game.clan.game_mode == "expanded":
        factor = 2

    trigger_value = round(factor * needed_amount, 2)

    if "full" in trigger and needed_amount < clan_supply < trigger_value:
        return True
    if "excess" in trigger and clan_supply > trigger_value:
        return True

    # if it hasn't returned by now, it doesn't qualify
    return False


def event_for_herb_supply(trigger, supply_type, clan_size) -> bool:
    """
    checks if clan's herb supply qualifies for event
    """
    if "always" in trigger:
        return True

    herb_supply = game.clan.herbs.copy()
    possible_herbs = HERBS
    num_of_herbs = len(possible_herbs)

    if not herb_supply and "low" in trigger:
        return True

    for herb in possible_herbs:
        if herb not in herb_supply:
            herb_supply[herb] = 0

    needed_amount = clan_size * 2
    half_amount = needed_amount / 2

    if supply_type == "all_herb":
        if "low" in trigger and len([x for x in herb_supply if herb_supply[x] < half_amount]) == num_of_herbs:
            return True
        elif "adequate" in trigger and len(
                [x for x in herb_supply if half_amount < herb_supply[x] <= needed_amount]) == num_of_herbs:
            return True
        elif "full" in trigger and len(
                [x for x in herb_supply if needed_amount < herb_supply[x] <= needed_amount * 2]) == num_of_herbs:
            return True
        elif "excess" in trigger and len(
                [x for x in herb_supply if needed_amount * 2 < herb_supply[x]]) == num_of_herbs:
            return True

        return False

    if supply_type == "any_herb":
        if "low" in trigger and [x for x in herb_supply if herb_supply[x] < half_amount]:
            return True
        elif "adequate" in trigger and [x for x in herb_supply if half_amount < herb_supply[x] <= needed_amount]:
            return True
        elif "full" in trigger and [x for x in herb_supply if needed_amount < herb_supply[x] <= needed_amount * 2]:
            return True
        elif "excess" in trigger and [x for x in herb_supply if needed_amount * 2 < herb_supply[x]]:
            return True

        return False

    else:
        chosen_herb = supply_type
        if chosen_herb not in possible_herbs:
            print(f"WARNING: possible typo in supply constraint: {chosen_herb}")
            return False
        if "low" in trigger and herb_supply[chosen_herb] < half_amount:
            return True
        elif "adequate" in trigger and half_amount < herb_supply[chosen_herb] <= needed_amount:
            return True
        elif "full" in trigger and needed_amount < herb_supply[chosen_herb] <= needed_amount * 2:
            return True
        elif "excess" in trigger and needed_amount * 2 < herb_supply[chosen_herb]:
            return True

        return False


def event_for_cat(cat_info: dict, cat, cat_group: list = None, event_id: str = None, p_l=None) -> bool:
    """
        checks if a cat is suitable for the event
        :param cat_info: cat's dict of constraints
        :param cat: the cat object of the cat being checked
        :param cat_group: the group of cats being included within the event
        :param event_id: if event comes with an id, include it here
        :param p_l: if event is a patrol, include patrol leader object here
        """

    func_lookup = {
        "age": _check_cat_age(cat, cat_info.get("age", [])),
        "status": _check_cat_status(cat, cat_info.get("status", [])),
        "trait": _check_cat_trait(cat, cat_info.get("trait", []), cat_info.get("not_trait", [])),
        "skills": _check_cat_skills(cat, cat_info.get("skill", []), cat_info.get("not_skill", [])),
        "backstory": _check_cat_backstory(cat, cat_info.get("backstory", [])),
        "gender": _check_cat_gender(cat, cat_info.get("gender", []))
    }

    for func in func_lookup:
        if not func_lookup[func]:
            return False

    if cat_info.get("relationship_status", []):
        if not filter_relationship_type(
                group=cat_group,
                filter_types=cat_info["relationship_status"],
                event_id=event_id,
                patrol_leader=p_l
        ):
            return False

    return True


def _check_cat_age(cat, ages: list) -> bool:
    """
        checks if a cat's age is within ages list
        """
    if "any" in ages or not ages:
        return True

    return cat.age.value in ages


def _check_cat_status(cat, statuses: list) -> bool:
    """
        checks if cat's status is within statuses list
        """
    if "any" in statuses or not statuses:
        return True

    if cat.status in statuses:
        return True

    return False


def _check_cat_trait(cat, traits: list, not_traits: list) -> bool:
    """
    checks if cat has the correct traits for traits and not_traits lists
    """
    if not traits and not not_traits:
        return True

    cat_trait = cat.personality.trait
    allowed = False

    if traits and cat_trait not in traits:
        return False
    if not_traits and cat_trait in not_traits:
        return False
    return True


def _check_cat_skills(cat, skills: list, not_skills: list) -> bool:
    """
        checks if the cat has the correct skills for skills and not skills lists
        """
    if not skills and not not_skills:
        return True

    has_good_skill = False
    has_bad_skill = False

    for _skill in skills:
        skill_info = _skill.split(",")

        if len(skill_info) < 2:
            print("Cat skill incorrectly formatted", _skill)
            continue

        if cat.skills.meets_skill_requirement(
                skill_info[0], int(skill_info[1])
        ):
            has_good_skill = True
            break

    for _skill in not_skills:
        skill_info = _skill.split(",")

        if len(skill_info) < 2:
            print("Cat skill incorrectly formatted", _skill)
            continue

        if cat.skills.meets_skill_requirement(
                skill_info[0], int(skill_info[1])
        ):
            has_bad_skill = True
            break

    if has_good_skill and not has_bad_skill:
        return True

    return False


def _check_cat_backstory(cat, backstories: list) -> bool:
    """
        checks if cat has the correct backstory
        """
    if not backstories:
        return True

    if cat.backstory in backstories:
        return True

    return False


def _check_cat_gender(cat, genders: list) -> bool:
    """
        checks if cat has the correct gender
        """
    if not genders:
        return True

    if cat.gender in genders:
        return True

    return False


# until we make a herbs class, this will have to live here too to avoid a circular import. i am screaming.
with open("resources/dicts/herbs.json", "r", encoding="utf-8") as read_file:
    HERBS = ujson.loads(read_file.read())