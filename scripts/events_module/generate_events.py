#!/usr/bin/env python3
# -*- coding: ascii -*-
import random

import ujson

from scripts.game_structure.game_essentials import game
from scripts.utility import filter_relationship_type, get_living_clan_cat_count,get_alive_status_cats

resource_directory = "resources/dicts/events/"


# ---------------------------------------------------------------------------- #
#                Tagging Guidelines can be found at the bottom                 #
# ---------------------------------------------------------------------------- #

class GenerateEvents:
    loaded_events = {}

    INJURY_DISTRIBUTION = None
    with open(f"resources/dicts/conditions/event_injuries_distribution.json", 'r') as read_file:
        INJURY_DISTRIBUTION = ujson.loads(read_file.read())

    INJURIES = None
    with open(f"resources/dicts/conditions/injuries.json", 'r') as read_file:
        INJURIES = ujson.loads(read_file.read())

    @staticmethod
    def get_short_event_dicts(file_path):
        try:
            with open(
                    file_path,
                    "r",
            ) as read_file:
                events = ujson.loads(read_file.read())
        except:
            print(f"ERROR: Unable to load {file_path}.")
            return None

        return events

    @staticmethod
    def get_ongoing_event_dicts(file_path):
        events = None
        try:
            with open(
                    file_path,
                    "r",
            ) as read_file:
                events = ujson.loads(read_file.read())
        except:
            print(f"ERROR: Unable to load events from biome {file_path}.")

        return events

    @staticmethod
    def get_death_reaction_dicts(family_relation, rel_value):
        try:
            file_path = f"{resource_directory}/death/death_reactions/{family_relation}/{family_relation}_{rel_value}.json"
            with open(
                    file_path,
                    "r",
            ) as read_file:
                events = ujson.loads(read_file.read())
        except:
            events = None
            print(f"ERROR: Unable to load death reaction events for {family_relation}_{rel_value}.")
        return events

    @staticmethod
    def clear_loaded_events():
        GenerateEvents.loaded_events = {}

    @staticmethod
    def generate_short_events(event_triggered, biome):

        file_path = f"{resource_directory}{event_triggered}/{biome}.json"

        try:
            if file_path in GenerateEvents.loaded_events:
                return GenerateEvents.loaded_events[file_path]
            else:
                events_dict = GenerateEvents.get_short_event_dicts(file_path)

                event_list = []
                if not events_dict:
                    return event_list
                for event in events_dict:
                    event_text = event["event_text"] if "event_text" in event else None
                    if not event_text:
                        event_text = event["death_text"] if "death_text" in event else None

                    if not event_text:
                        print(f"WARNING: some events resources which are used in generate_events. Have no 'event_text'.")
                    event = ShortEvent(
                        event_id=event["event_id"] if "event_id" in event else "",
                        biome=event["biome"] if "biome" in event else ["any"],
                        camp=event["camp"] if "camp" in event else ["any"],
                        season=event["season"] if "season" in event else ["any"],
                        sub_type=event["sub_type"] if "sub_type" in event else [],
                        tags=event["tags"] if "tags" in event else [],
                        weight=event["weight"] if "weight" in event else 20,
                        event_text=event_text,
                        new_accessory=event["new_accessory"] if "new_accessory" in event else [],
                        m_c=event["m_c"] if "m_c" in event else {},
                        r_c=event["r_c"] if "r_c" in event else {},
                        new_cat=event["new_cat"] if "new_cat" in event else [],
                        injury=event["injury"] if "injury" in event else [],
                        history=event["history"] if "history" in event else [],
                        relationships=event["relationships"] if "relationships" in event else [],
                        outsider=event["outsider"] if "outsider" in event else {},
                        other_clan=event["other_clan"] if "other_clan" in event else {}
                    )
                    event_list.append(event)

                # Add to loaded events.
                GenerateEvents.loaded_events[file_path] = event_list
                return event_list
        except:
            print(f"WARNING: {file_path} was not found, check short event generation")

    @staticmethod
    def generate_ongoing_events(event_type, biome, specific_event=None):

        file_path = f"resources/dicts/events/{event_type}/{biome}.json"

        if file_path in GenerateEvents.loaded_events:
            return GenerateEvents.loaded_events[file_path]
        else:
            events_dict = GenerateEvents.get_ongoing_event_dicts(file_path)

            if not specific_event:
                event_list = []
                for event in events_dict:
                    event = OngoingEvent(
                        event=event["event"],
                        camp=event["camp"],
                        season=event["season"],
                        tags=event["tags"],
                        priority=event["priority"],
                        duration=event["duration"],
                        current_duration=0,
                        rarity=event["rarity"],
                        trigger_events=event["trigger_events"],
                        progress_events=event["progress_events"],
                        conclusion_events=event["conclusion_events"],
                        secondary_disasters=event["secondary_disasters"],
                        collateral_damage=event["collateral_damage"]
                    )
                    event_list.append(event)
                return event_list
            else:
                event = None
                for event in events_dict:
                    if event["event"] != specific_event:
                        # print(event["event"], 'is not', specific_event)
                        continue
                    # print(event["event"], "is", specific_event)
                    event = OngoingEvent(
                        event=event["event"],
                        camp=event["camp"],
                        season=event["season"],
                        tags=event["tags"],
                        priority=event["priority"],
                        duration=event["duration"],
                        current_duration=0,
                        progress_events=event["progress_events"],
                        conclusion_events=event["conclusion_events"],
                        collateral_damage=event["collateral_damage"]
                    )
                    break
                return event

    @staticmethod
    def possible_short_events(event_type=None):
        event_list = []

        # skip the rest of the loading if there is an unrecognised biome
        if game.clan.biome not in game.clan.BIOME_TYPES:
            print(
                f"WARNING: unrecognised biome {game.clan.biome} in generate_events. Have you added it to BIOME_TYPES "
                f"in clan.py?")

        biome = game.clan.biome.lower()

        # biome specific events
        event_list.extend(
            GenerateEvents.generate_short_events(event_type, biome))

        # any biome events
        event_list.extend(
            GenerateEvents.generate_short_events(event_type, "general"))

        return event_list

    @staticmethod
    def filter_possible_short_events(Cat_class, possible_events, cat, random_cat, other_clan, freshkill_active, freshkill_trigger_factor, sub_types=None, ):
        final_events = []

        # TODO: put the injury severity code back?
        minor = []
        major = []
        severe = []

        # Chance to bypass the skill or trait requirements. 
        trait_skill_bypass = 15

        # check if generated event should be a war event
        if "war" in sub_types and random.randint(1, 10) != 1:
            war_event = True
        else:  # otherwise, take all war events out
            war_event = False
            if "war" in sub_types:
                sub_types.remove("war")

        for event in possible_events:
            # check for event sub_type
            wrong_type = False
            for sub in sub_types:
                if sub not in event.sub_type:
                    wrong_type = True
                    continue
            for sub in event.sub_type:
                if sub not in sub_types:
                    wrong_type = True
                    continue
            if wrong_type:
                continue

            # check biome
            if game.clan.biome.lower() not in event.biome and "any" not in event.biome:
                continue
            # check camp
            if game.clan.camp_bg.lower() not in event.camp and "any" not in event.camp:
                continue
            # check season
            if game.clan.current_season.lower() not in event.season and "any" not in event.season:
                continue

            # check tags
            prevent_bypass = "skill_trait_required" in event.tags

            # some events are classic only
            if game.clan.game_mode in ["expanded", "cruel season"] and "classic" in event.tags:
                continue
            # cruel season only events
            if game.clan.game_mode in ["classic", "expanded"] and "cruel_season" in event.tags:
                continue

            # make complete leader death less likely until the leader is over 150 moons
            if "all_lives" in event.tags:
                if int(cat.moons) < 150 and int(random.random() * 5):
                    continue

            leader_lives = game.clan.leader_lives

            # make sure that 'some lives' and "lives_remain" events don't show up if the leader doesn't have multiple
            # lives to spare
            if "some_lives" in event.tags and leader_lives <= 3:
                continue
            if "lives_remain" in event.tags and leader_lives < 2:
                continue

            # check leader life count
            if "high_lives" in event.tags and leader_lives not in [7, 8, 9]:
                continue
            elif "mid_lives" in event.tags and leader_lives not in [4, 5, 6]:
                continue
            elif "low_lives" in event.tags and leader_lives not in [1, 2, 3]:
                continue

            # check if Clan has kits
            if "clan_kits" in event.tags and not get_alive_status_cats(Cat_class, ["kitten"]):
                continue

            # check if Clan has apps
            if "clan_apps" in event.tags and not get_alive_status_cats(Cat_class, ["apprentice", "medicine cat apprentice", "mediator apprentice"]):
                continue

            # check if Clan has newborns
            if "clan_newborns" in event.tags and not get_alive_status_cats(Cat_class, ["newborn"]):
                continue

            # If the cat or any of their mates have "no kits" toggled, forgo the adoption event.
            if "adoption" in event.sub_type:
                if cat.no_kits:
                    continue
                if any(cat.fetch_cat(i).no_kits for i in cat.mate):
                    continue

            # check for old age
            if "old_age" in event.sub_type and cat.moons < game.config["death_related"]["old_age_death_start"]:
                continue
            # remove some non-old age events to encourage elders to die of old age more often
            if "old_age" not in event.sub_type and cat.moons > game.config["death_related"]["old_age_death_start"] \
                    and int(random.random() * 3):
                continue

            # if the event is marked as changing romantic interest, check that the cats are allowed to be romantic
            if random_cat:
                if "romance" in event.sub_type and not random_cat.is_potential_mate(cat):
                    continue

            if event.m_c:
                if cat.age not in event.m_c["age"] and "any" not in event.m_c["age"]:
                    continue
                if cat.status not in event.m_c["status"] and "any" not in event.m_c["status"]:
                    continue
                if event.m_c["relationship_status"]:
                    if not filter_relationship_type(group=[cat, random_cat],
                                                    filter_types=event.m_c["relationship_status"],
                                                    event_id=event.event_id):
                        continue

                # check cat trait and skill
                has_trait = False
                if event.m_c["trait"]:
                    if cat.personality.trait in event.m_c["trait"]:
                        has_trait = True

                has_skill = False
                if event.m_c["skill"]:
                    for _skill in event.m_c["skill"]:
                        split = _skill.split(",")

                        if len(split) < 2:
                            print("Cat skill incorrectly formatted", _skill)
                            continue

                        if cat.skills.meets_skill_requirement(split[0], int(split[1])):
                            has_skill = True
                            break

                if event.m_c["trait"] and event.m_c["skill"]:
                    if not (has_trait or has_skill) and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue
                elif event.m_c["trait"]:
                    if not has_trait and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue
                elif event.m_c["skill"]:
                    if not has_skill and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue

                # check cat negate trait and skill
                has_trait = False
                if event.m_c["not_trait"]:
                    if cat.personality.trait in event.m_c["not_trait"]:
                        has_trait = True

                has_skill = False
                if event.m_c["not_skill"]:
                    for _skill in event.m_c["not_skill"]:
                        split = _skill.split(",")

                        if len(split) < 2:
                            print("Cat skill incorrectly formatted", _skill)
                            continue

                        if cat.skills.meets_skill_requirement(split[0], int(split[1])):
                            has_skill = True
                            break

                # There is a small chance to bypass the skill or trait requirements.
                if (has_trait or has_skill) and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                    continue

                # check backstory
                if event.m_c["backstory"]:
                    if cat.backstory not in event.m_c["backstory"]:
                        continue

            # check that a random_cat is available to use for r_c
            if event.r_c and random_cat:
                if random_cat.age not in event.r_c["age"] and "any" not in event.r_c["age"]:
                    continue
                if random_cat.status not in event.r_c["status"] and "any" not in event.r_c["status"]:
                    continue
                if event.r_c["relationship_status"]:
                    if not filter_relationship_type(group=[cat, random_cat],
                                                    filter_types=event.r_c["relationship_status"],
                                                    event_id=event.event_id):
                        continue

                # check random_cat trait and skill
                has_trait = False
                if event.r_c["trait"]:
                    if random_cat.personality.trait in event.r_c["trait"]:
                        has_trait = True

                has_skill = False
                if event.r_c["skill"]:
                    for _skill in event.r_c["skill"]:
                        split = _skill.split(",")

                        if len(split) < 2:
                            print("random_cat skill incorrectly formatted", _skill)
                            continue

                        if random_cat.skills.meets_skill_requirement(split[0], int(split[1])):
                            has_skill = True
                            break

                if event.r_c["trait"] and event.r_c["skill"]:
                    if not (has_trait or has_skill) and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue
                elif event.r_c["trait"]:
                    if not has_trait and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue
                elif event.r_c["skill"]:
                    if not has_skill and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                        continue

                # check random_cat negate trait and skill
                has_trait = False
                if event.r_c["not_trait"]:
                    if random_cat.personality.trait in event.r_c["not_trait"]:
                        has_trait = True

                has_skill = False
                if event.r_c["not_skill"]:
                    for _skill in event.r_c["not_skill"]:
                        split = _skill.split(",")

                        if len(split) < 2:
                            print("random_cat skill incorrectly formatted", _skill)
                            continue

                        if random_cat.skills.meets_skill_requirement(split[0], int(split[1])):
                            has_skill = True
                            break

                # There is a small chance to bypass the skill or trait requirements.
                if (has_trait or has_skill) and (prevent_bypass or int(random.random() * trait_skill_bypass)):
                    continue

                # check backstory
                if event.r_c["backstory"]:
                    if random_cat.backstory not in event.r_c["backstory"]:
                        continue

            # check that injury is possible
            if event.injury:
                # determine which injury severity list will be used
                allowed_severity = None
                discard = False
                if cat.status in GenerateEvents.INJURY_DISTRIBUTION:
                    minor_chance = GenerateEvents.INJURY_DISTRIBUTION[cat.status]['minor']
                    major_chance = GenerateEvents.INJURY_DISTRIBUTION[cat.status]['major']
                    severe_chance = GenerateEvents.INJURY_DISTRIBUTION[cat.status]['severe']
                    severity_chosen = random.choices(["minor", "major", "severe"],
                                                     [minor_chance, major_chance, severe_chance], k=1)
                    if severity_chosen[0] == 'minor':
                        allowed_severity = "minor"
                    elif severity_chosen[0] == 'major':
                        allowed_severity = "major"
                    else:
                        allowed_severity = "severe"

                for block in event.injury:
                    for injury in block["injuries"]:
                        if injury in GenerateEvents.INJURIES:
                            if GenerateEvents.INJURIES[injury]["severity"] != allowed_severity:
                                discard = True
                                break

                            if "m_c" in block["cats"]:
                                if injury == 'mangled tail' and (
                                        'NOTAIL' in cat.pelt.scars or 'HALFTAIL' in cat.pelt.scars):
                                    continue

                                if injury == 'torn ear' and 'NOEAR' in cat.pelt.scars:
                                    continue
                            if "r_c" in block["cats"]:
                                if injury == 'mangled tail' and (
                                        'NOTAIL' in random_cat.pelt.scars or 'HALFTAIL' in random_cat.pelt.scars):
                                    continue

                                if injury == 'torn ear' and 'NOEAR' in random_cat.pelt.scars:
                                    continue

                if discard:
                    continue

            # check if outsider event is allowed
            if event.outsider:
                # don't waste time checking rep if any rep is allowed
                if "any" not in event.outsider["current_rep"]:
                    # hostile
                    if 1 <= game.clan.reputation <= 30 and "hostile" not in event.outsider["current_rep"]:
                        continue
                    # neutral
                    elif 31 <= game.clan.reputation <= 70 and "neutral" not in event.outsider["current_rep"]:
                        continue
                    # welcoming
                    elif 71 <= game.clan.reputation <= 100 and "welcoming" not in event.outsider["current_rep"]:
                        continue

            # other Clan related checks
            if event.other_clan:
                if not other_clan:
                    continue
                # don't waste time checking rep if any rep is allowed
                if "any" not in event.other_clan["current_rep"]:
                    # ally
                    if "ally" in event.other_clan["current_rep"] and int(other_clan.relations) < 17:
                        continue
                    # neutral
                    elif "neutral" in event.other_clan["current_rep"] and (
                            int(other_clan.relations) <= 7 or int(other_clan.relations) >= 17):
                        continue
                    # hostile
                    elif "hostile" in event.other_clan["current_rep"] and int(other_clan.relations) > 7:
                        continue

            # clans below a certain age can't have their supplies messed with
            if game.clan.age < 5 and event.supplies:
                continue
            elif event.supplies:
                clan_size = get_living_clan_cat_count(Cat_class)
                for supply in event.supplies:
                    trigger = supply["trigger"]
                    supply_type = supply["type"]
                    if supply_type == "freshkill":
                        # classic mode doesn't do freshkill
                        # TODO: consider if events could still be allowed as "flavor" rather than actual supply changes
                        if game.clan.game_mode == "classic":
                            continue

                        discard = True
                        pile = game.clan.freshkill_pile
                        needed_amount = pile.amount_food_needed()
                        if not freshkill_active:
                            continue

                        # "low" means total_amount must be less than half what is needed
                        if "low" in trigger:
                            if needed_amount / 2 > pile.total_amount:
                                discard = False

                        # "adequate" means total_amount must be greater than half needed,
                        # but not greater than 1 moons worth of food
                        if "adequate" in trigger:
                            if needed_amount / 2 < pile.total_amount < needed_amount:
                                discard = False

                        # now do the math to find how much is too much prey
                        trigger_factor = freshkill_trigger_factor
                        divider = 35 if game.clan.game_mode == "expanded" else 20
                        trigger_factor = trigger_factor - round(pow((clan_size / divider), 2))
                        if trigger_factor < 2 and game.clan.game_mode == "expanded":
                            trigger_factor = 2
                        if trigger_factor < 1.2 and game.clan.game_mode == "cruel season":
                            trigger_factor = 1.2

                        trigger_value = round(trigger_factor * needed_amount, 2)
                        print(
                            f" -- FRESHKILL: trigger amount {trigger_value}. current amount (after feed, before moon gathering) {pile.total_amount}")

                        # "full" means total_amount is enough for 1 moons worth, but is not over the multiplier
                        if "full" in trigger:
                            # check this quick to see if we can skip the math
                            if needed_amount < pile.total_amount < trigger_value:
                                discard = False

                        # "excess" means total_amount is over the multiplier and there's too much food!
                        if "excess" in trigger:
                            if pile.total_amount > trigger_value:
                                discard = False

                        if discard:
                            continue

                    else:  # if supply type wasn't freshkill, then it must be an herb type
                        herbs = game.clan.herbs
                        needed_amount = int(clan_size * 3)
                        discard = True

                        if supply_type == "all_herb":
                            if "low" in trigger:
                                for herb in herbs:
                                    if herbs[herb] < needed_amount / 2:
                                        discard = False
                                    else:
                                        discard = True
                                        break
                            if "adequate" in trigger:
                                for herb in herbs:
                                    if needed_amount / 2 < herbs[herb] < needed_amount:
                                        discard = False
                                    else:
                                        discard = True
                                        break
                            if "full" in trigger:
                                for herb in herbs:
                                    if needed_amount < herbs[herb] < needed_amount * 2:
                                        discard = False
                                    else:
                                        discard = True
                                        break
                            if "excess" in trigger:
                                for herb in herbs:
                                    if needed_amount * 2 < herbs[herb]:
                                        discard = False
                                    else:
                                        discard = True
                                        break
                        else:
                            if supply_type == "any_herb":
                                chosen_herb = random.choice(herbs.keys)
                            else:
                                chosen_herb = supply_type

                            if "low" in trigger:
                                if chosen_herb < needed_amount / 2:
                                    discard = False
                            if "adequate" in trigger:
                                if needed_amount / 2 < chosen_herb < needed_amount:
                                    discard = False
                            if "full" in trigger:
                                if needed_amount < chosen_herb < needed_amount * 2:
                                    discard = False
                            if "excess" in trigger:
                                if needed_amount * 2 < chosen_herb:
                                    discard = False

                        if discard:
                            continue

            final_events.append(event)

        return final_events

    @staticmethod
    def possible_ongoing_events(event_type=None, specific_event=None):
        event_list = []

        if game.clan.biome not in game.clan.BIOME_TYPES:
            print(
                f"WARNING: unrecognised biome {game.clan.biome} in generate_events. Have you added it to BIOME_TYPES in clan.py?")

        else:
            biome = game.clan.biome.lower()
            if not specific_event:
                event_list.extend(
                    GenerateEvents.generate_ongoing_events(event_type, biome)
                )
                """event_list.extend(
                    GenerateEvents.generate_ongoing_events(event_type, "general", specific_event)
                )"""
                return event_list
            else:
                # print(specific_event)
                event = (
                    GenerateEvents.generate_ongoing_events(event_type, biome, specific_event)
                )
                return event

    @staticmethod
    def possible_death_reactions(family_relation, rel_value, trait, body_status):
        possible_events = []
        # grab general events first, since they'll always exist
        events = GenerateEvents.get_death_reaction_dicts("general", rel_value)
        possible_events.extend(events["general"][body_status])
        if trait in events:
            possible_events.extend(events[trait][body_status])

        # grab family events if they're needed. Family events should not be romantic. 
        if family_relation != 'general' and rel_value != "romantic":
            events = GenerateEvents.get_death_reaction_dicts(family_relation, rel_value)
            possible_events.extend(events["general"][body_status])
            if trait in events:
                possible_events.extend(events[trait][body_status])

        # print(possible_events)

        return possible_events


class ShortEvent:
    """
    A moon event that only affects the moon it was triggered on.  Can involve two cats directly and be restricted by various constraints.
    - full documentation available on github wiki
    """

    def __init__(
            self,
            event_id="",
            biome=None,
            camp=None,
            season=None,
            sub_type=None,
            tags=None,
            weight=0,
            event_text="",
            new_accessory=None,
            m_c=None,
            r_c=None,
            new_cat=None,
            injury=None,
            history=None,
            relationships=None,
            outsider=None,
            other_clan=None,
            supplies=None
    ):
        if not event_id:
            print("WARNING: moon event has no event_id")
        self.event_id = event_id
        self.biome = biome if biome else ["any"]
        self.camp = camp if camp else ["any"]
        self.season = season if season else ["any"]
        self.sub_type = sub_type if sub_type else []
        self.tags = tags if tags else []
        self.weight = weight
        self.event_text = event_text
        self.new_accessory = new_accessory
        self.m_c = m_c if m_c else {
            "age": ["any"]
        }
        if self.m_c:
            if "age" not in self.m_c:
                self.m_c["age"] = ["any"]
            if "status" not in self.m_c:
                self.m_c["status"] = ["any"]
            if "relationship_status" not in self.m_c:
                self.m_c["relationship_status"] = []
            if "skill" not in self.m_c:
                self.m_c["skill"] = []
            if "not_skill" not in self.m_c:
                self.m_c["not_skill"] = []
            if "trait" not in self.m_c:
                self.m_c["trait"] = []
            if "not_trait" not in self.m_c:
                self.m_c["not_trait"] = []
            if "age" not in self.m_c:
                self.m_c["age"] = []
            if "backstory" not in self.m_c:
                self.m_c["backstory"] = []
            if "dies" not in self.m_c:
                self.m_c["dies"] = False

        self.r_c = r_c if r_c else {}
        if self.r_c:
            if "age" not in self.r_c:
                self.r_c["age"] = []
            if "status" not in self.r_c:
                self.r_c["status"] = []
            if "relationship_status" not in self.r_c:
                self.r_c["relationship_status"] = []
            if "skill" not in self.r_c:
                self.r_c["skill"] = []
            if "not_skill" not in self.r_c:
                self.r_c["not_skill"] = []
            if "trait" not in self.r_c:
                self.r_c["trait"] = []
            if "not_trait" not in self.r_c:
                self.r_c["not_trait"] = []
            if "age" not in self.r_c:
                self.r_c["age"] = []
            if "backstory" not in self.r_c:
                self.r_c["backstory"] = []
            if "dies" not in self.r_c:
                self.r_c["dies"] = False

        self.new_cat = new_cat if new_cat else []
        self.injury = injury if injury else []
        self.history = history if history else []
        self.relationships = relationships if relationships else []
        self.outsider = outsider if outsider else {}
        if self.outsider:
            if "current_rep" not in self.outsider:
                self.outsider["current_rep"] = []
            if "changed" not in self.outsider:
                self.outsider["changed"] = 0
        self.other_clan = other_clan if other_clan else {}
        if self.other_clan:
            if "current_rep" not in self.other_clan:
                self.other_clan["current_rep"] = []
            if "changed" not in self.other_clan:
                self.other_clan["changed"] = 0
        self.supplies = supplies if supplies else []


class OngoingEvent:
    def __init__(self,
                 event=None,
                 camp=None,
                 season=None,
                 tags=None,
                 priority='secondary',
                 duration=None,
                 current_duration=0,
                 rarity=0,
                 trigger_events=None,
                 progress_events=None,
                 conclusion_events=None,
                 secondary_disasters=None,
                 collateral_damage=None
                 ):
        self.event = event
        self.camp = camp
        self.season = season
        self.tags = tags
        self.priority = priority
        self.duration = duration
        self.current_duration = current_duration
        self.rarity = rarity
        self.trigger_events = trigger_events
        self.progress_events = progress_events
        self.conclusion_events = conclusion_events
        self.secondary_disasters = secondary_disasters
        self.collateral_damage = collateral_damage
