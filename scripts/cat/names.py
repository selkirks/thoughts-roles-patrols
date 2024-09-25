"""
Module that handles the name generation for all cats.
"""
import os
import random

import ujson

from scripts.game_structure.game_essentials import game
from scripts.housekeeping.datadir import get_save_dir
from .alt_namer import Namer


class Name:
    """
    Stores & handles name generation.
    """

    if os.path.exists('resources/dicts/names/alt_prefixes.json'):
        with open('resources/dicts/names/alt_prefixes.json') as read_file:
            mod_prefixes = ujson.loads(read_file.read())
    if os.path.exists('resources/dicts/names/names.json'):
        with open('resources/dicts/names/names.json') as read_file:
            names_dict = ujson.loads(read_file.read())

        if os.path.exists(get_save_dir() + '/prefixlist.txt'):
            with open(get_save_dir() + '/prefixlist.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            while new_name[1:] in names_dict["normal_prefixes"]:
                                names_dict["normal_prefixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_prefixes"].append(new_name)

        if os.path.exists(get_save_dir() + '/suffixlist.txt'):
            with open(get_save_dir() + '/suffixlist.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            while new_name[1:] in names_dict["normal_suffixes"]:
                                names_dict["normal_suffixes"].remove(new_name[1:])
                        else:
                            names_dict["normal_suffixes"].append(new_name)

        if os.path.exists(get_save_dir() + '/specialsuffixes.txt'):
            with open(get_save_dir() + '/specialsuffixes.txt', 'r') as read_file:
                name_list = read_file.read()
                if_names = len(name_list)
            if if_names > 0:
                new_names = name_list.split('\n')
                for new_name in new_names:
                    if new_name != '':
                        if new_name.startswith('-'):
                            del names_dict["special_suffixes"][new_name[1:]]
                        elif ':' in new_name:
                            _tmp = new_name.split(':')
                            names_dict["special_suffixes"][_tmp[0]] = _tmp[1]

    def __init__(self,
                 Cat=None,
                 status="warrior",
                 genotype=None,
                 phenotype=None,
                 chimpheno=None,
                 moons=0,
                 prefix=None,
                 suffix=None,
                 pelt=None,
                 tortiepattern=None,
                 biome=None,
                 specsuffix_hidden=False,
                 load_existing_name=False
                 ):
        self.status = status
        self.moons = moons
        self.genotype = genotype
        self.phenotype = phenotype
        self.chimpheno = chimpheno
        self.prefix = prefix
        self.suffix = suffix
        self.specsuffix_hidden = specsuffix_hidden

        name_fixpref = False
        # Set prefix
        if prefix is None:
            self.give_prefix(Cat, biome, no_suffix=True if suffix == "" else False)
            # needed for random dice when we're changing the Prefix
            name_fixpref = True

        # Set suffix
        if self.suffix is None:
            self.give_suffix(pelt, biome, tortiepattern)
            if name_fixpref and self.prefix is None:
                # needed for random dice when we're changing the Prefix
                name_fixpref = False

        if self.suffix and not load_existing_name:
            # Prevent triple letter names from joining prefix and suffix from occurring (ex. Beeeye)
            triple_letter = False
            possible_three_letter = (self.prefix[-2:] + self.suffix[0], self.prefix[-1] + self.suffix[:2])
            if all(i == possible_three_letter[0][0] for i in possible_three_letter[0]) or \
                    all(i == possible_three_letter[1][0] for i in possible_three_letter[1]):
                triple_letter = True
            # Prevent double animal names (ex. Spiderfalcon)
            double_animal = False
            if self.prefix in self.names_dict["animal_prefixes"] and self.suffix in self.names_dict["animal_suffixes"]:
                double_animal = True
            # Prevent the inappropriate names
            nono_name = self.prefix + self.suffix
            # Prevent double names (ex. Iceice)
            # Prevent suffixes containing the prefix (ex. Butterflyfly)

            i = 0
            while nono_name.lower() in self.names_dict["inappropriate_names"] or triple_letter or double_animal or \
                    (self.prefix.lower() in self.suffix.lower() and not str(self.prefix) == '') or (
                    self.suffix.lower() in self.prefix.lower() and not str(self.suffix) == ''):

                # check if random die was for prefix
                if name_fixpref:
                    self.give_prefix(Cat, biome)
                else:
                    self.give_suffix(pelt, biome, tortiepattern)

                nono_name = self.prefix + self.suffix
                possible_three_letter = (self.prefix[-2:] + self.suffix[0], self.prefix[-1] + self.suffix[:2])
                if not (all(i == possible_three_letter[0][0] for i in possible_three_letter[0]) or
                        all(i == possible_three_letter[1][0] for i in possible_three_letter[1])):
                    triple_letter = False
                if not (self.prefix in self.names_dict["animal_prefixes"]
                        and self.suffix in self.names_dict["animal_suffixes"]):
                    double_animal = False
                i += 1

    def filter(self, all, used):
        return [x for x in all if x not in used]

    # Generate possible prefix
    def give_prefix(self, Cat, biome, no_suffix=False):
        try:
            used_prefixes = [cat.name.prefix for cat in Cat.all_cats.values() if not cat.dead and not cat.status in ['kittypet', 'loner', 'rogue', 'former Clancat']]
        except:
            used_prefixes = []

        namer = Namer(used_prefixes, self.mod_prefixes, self.moons)
        if not game.clan or game.clan.clan_settings['new prefixes']:
            self.prefix = namer.start(self.genotype, self.phenotype, self.chimpheno)
            print(self.prefix)
            if no_suffix:
                if self.prefix == "Striped":
                    self.prefix = "Stripe"
                elif self.prefix == "Spotted":
                    self.prefix = "Spot"
            return
            

        # decided in game config: cat_name_controls
        if game.config["cat_name_controls"]["always_name_after_appearance"]:
            named_after_appearance = True
        else:
            named_after_appearance = not random.getrandbits(2)  # Chance for True is '1/4'

        named_after_biome_ = not random.getrandbits(3)  # chance for True is 1/8

        colour_mappings = {
            "black" : ["BLACK"],
            "blue" : ["GREY", "DARKGREY"],
            "chocolate" : ["BROWN", "GOLDEN-BROWN", "DARKBROWN", "CHOCOLATE"],
            "lilac" : ["PALEGREY", "SILVER", "LILAC"],
            "cinnamon" : ["SIENNA", "DARKGINGER", "GOLDEN-BROWN"],
            "fawn" : ["LIGHTBROWN"],
            "red" : ["GINGER", "DARKGINGER"],
            "cream" : ["CREAM", "PALEGINGER"],
            "white" : ["WHITE"],
            "silver shaded" : ["WHITE"]
        }
        
        params = namer.parse_chimera() if self.genotype.chimera else namer.get_categories(self.genotype, self.phenotype)

        colours = colour_mappings[params[0]]
        if params[2]['type'] == 'silver' and params[0] not in ['ginger', 'cream']:
            colours.append('PALEGREY')
            colours.append('SILVER')
        if params[2]['type'] == 'dark' and params[0] == "black":
            colours.append('GHOST')
        if params[2]['type'] == 'golden' and params[0] not in ['ginger', 'cream']:
            colours.append('GOLDEN')
        if self.genotype.ruftype == 'rufoused' and params[0] == 'ginger':
            colours.append('DARKGINGER')
        if self.genotype.ruftype == 'low' and params[0] == 'ginger':
            colours.append('PALEGINGER')
        if params[2]['pattern'] != '' and params[2]['type'] == 'regular' and params[0] == "black":
            colours.append('BROWN')
            colours.append('DARKBROWN')

        # Add possible prefix categories to list.
        possible_prefix_categories = []
        if colour in self.names_dict["colour_prefixes"]:
            possible_prefix_categories.append(self.names_dict["colour_prefixes"][choice(colours)])
        if biome is not None and biome in self.names_dict["biome_prefixes"]:
            possible_prefix_categories.append(self.names_dict["biome_prefixes"][biome])

        # Choose appearance-based prefix if possible and named_after_appearance because True.
        if named_after_appearance and possible_prefix_categories and not named_after_biome_:
            prefix_category = random.choice(possible_prefix_categories)
            self.prefix = random.choice(prefix_category)
        elif named_after_biome_ and possible_prefix_categories:
            prefix_category = random.choice(possible_prefix_categories)
            self.prefix = random.choice(prefix_category)
        else:
            self.prefix = random.choice(self.names_dict["normal_prefixes"])

    # Generate possible suffix
    def give_suffix(self, pelt, biome, tortiepattern):
        if pelt is None or pelt == 'SingleColour':
            self.suffix = random.choice(self.names_dict["normal_suffixes"])
        else:
            named_after_pelt = not random.getrandbits(2)  # Chance for True is '1/8'.
            named_after_biome = not random.getrandbits(3)  # 1/8
            # Pelt name only gets used if there's an associated suffix.
            if named_after_pelt:
                if pelt in ["Tortie", "Calico"] and tortiepattern in self.names_dict["tortie_pelt_suffixes"]:
                    self.suffix = random.choice(self.names_dict["tortie_pelt_suffixes"][tortiepattern])
                elif pelt in self.names_dict["pelt_suffixes"]:
                    self.suffix = random.choice(self.names_dict["pelt_suffixes"][pelt])
                else:
                    self.suffix = random.choice(self.names_dict["normal_suffixes"])
            elif named_after_biome:
                if biome in self.names_dict["biome_suffixes"]:
                    self.suffix = random.choice(self.names_dict["biome_suffixes"][biome])
                else:
                    self.suffix = random.choice(self.names_dict["normal_suffixes"])
            else:
                self.suffix = random.choice(self.names_dict["normal_suffixes"])

    def __repr__(self):
        # Handles predefined suffixes (such as newborns being kit),
        # then suffixes based on ages (fixes #2004, just trust me)
        if self.status in self.names_dict["special_suffixes"] and not self.specsuffix_hidden:
            return self.prefix + self.names_dict["special_suffixes"][self.status]
        if game.config['fun']['april_fools']:
            return self.prefix + 'egg'
        return self.prefix + self.suffix


names = Name()
