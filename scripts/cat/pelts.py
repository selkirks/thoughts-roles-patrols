import random
from random import choice
from re import sub

import i18n

from scripts.cat.sprites import sprites
from scripts.game_structure.game_essentials import game
from .genotype import Genotype
from .phenotype import Phenotype
from scripts.game_structure.localization import get_lang_config
from scripts.utility import adjust_list_text


class Pelt:

    physical_trait_teeth = ['TEETHUPPER', 'TEETHSABRE', 'TEETHUNDERBITE']
    physical_trait_ear_type = ['EARSMALL', 'EARBIG', 'EARTALL', 'EARPANTHER']
    physical_trait_ear_fold = ['FOLDONE']
    physical_trait_headfur = ['HEADFORELOCK', 'HEADCOWLICK', 'HEADMOHAWK', 'HEADTUFT', 'HEADEMO']
    physical_trait_cheekfur = ['CHEEKLONG', 'CHEEKPOINTED', 'CHEEKFLUFF', 'CHEEKCURL']
    physical_trait_mane = ['MANESILKY', 'MANEFLUFFY', 'MANERUFF', 'MANEHORSE']
    physical_trait_tail = ['TAILCROOKED', 'TAILLONG', 'TAILFEATHER', 'TAILTUFT']
    physical_trait_bodyfur = ['BACKFLUFF', 'BACKRIDGE', 'SHOULDERTUFT']
    physical_trait_misc = ['EARTUFTS', 'LASHESUPPER', 'LASHESLOWER', 'WHISKERSLONG', 'CLAWSLONG', 'LEGTUFT']
    # bite scars by @wood pank on discord

    # scars from other cats, other animals
    scars1 = [
        "ONE",
        "TWO",
        "THREE",
        "TAILSCAR",
        "SNOUT",
        "CHEEK",
        "SIDE",
        "THROAT",
        "TAILBASE",
        "BELLY",
        "LEGBITE",
        "NECKBITE",
        "FACE",
        "MANLEG",
        "BRIGHTHEART",
        "MANTAIL",
        "BRIDGE",
        "RIGHTBLIND",
        "LEFTBLIND",
        "BOTHBLIND",
        "BEAKCHEEK",
        "BEAKLOWER",
        "CATBITE",
        "RATBITE",
        "QUILLCHUNK",
        "QUILLSCRATCH",
        "HINDLEG",
        "BACK",
        "QUILLSIDE",
        "SCRATCHSIDE",
        "BEAKSIDE",
        "CATBITETWO",
        "FOUR",
    ]

    # missing parts
    scars2 = [
        "LEFTEAR",
        "RIGHTEAR",
        "NOTAIL",
        "HALFTAIL",
        "NOPAW",
        "NOLEFTEAR",
        "NORIGHTEAR",
        "NOEAR",
        "TNR"
    ]

    # "special" scars that could only happen in a special event
    scars3 = [
        "SNAKE",
        "TOETRAP",
        "BURNPAWS",
        "BURNTAIL",
        "BURNBELLY",
        "BURNRUMP",
        "FROSTFACE",
        "FROSTTAIL",
        "FROSTMITT",
        "FROSTSOCK",
        "TOE",
        "SNAKETWO",
    ]

    # make sure to add plural and singular forms of new accs to acc_display.json so that they will display nicely
    bone_accessories = ["SNAKE", "BAT WINGS", "CANIDAE SKULL", "DEER ANTLERS", "RAM HORN", "GOAT HORN", "OX SKULL",
                        "RAT SKULL", "TEETH COLLAR", "ROE SKULL",
                        "BIRD SKULL1", "RIBS", "FISH BONES"]
    butterflies_accessories = ["PEACOCK BUTTERFLY", "DEATH HEAD HAWKMOTH", "GARDEN TIGER MOTH", "ATLAS MOTH",
                        "CECOROPIA MOTH", "WHITE ERMINE MOTH", "IO MOTH", "COMET MOTH",
                        "JADE HAWKMOTH", "HUMMINGBIRD HAWKMOTH", "OWL BUTTERFLY", "GLASSWING BUTTERFLY",
                        "QUEEN ALEXANDRA BIRDWING BUTTERFLY", "GREEN DRAGONTAIL BUTTERFLY",
                        "MENELAUS BLUE MORPHO BUTTERFLY", "DEAD LEAF BUTTERFLY"]
    stuff_accessories = ["OLD SILVER WATCH", "OLD GOLD WATCH", "GOLDEN KEY", "SILVER KEY",
                         "DVD", "OLD PENCIL", "OLD BRUSH", "BANANA PEEL", "BROKEN VHS TAPE",
                         "OLD NEWSPAPER", "SEA GLASS", "BAUBLES", "MUD AND DIRT"]
    plant_accessories = ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "CATTAIL", "POPPY", "ORANGE POPPY", "CYAN POPPY", "WHITE POPPY", "PINK POPPY",
                        "BLUEBELLS", "LILY OF THE VALLEY", "SNAPDRAGON", "HERBS", "PETALS", "NETTLE", "HEATHER", "GORSE", "JUNIPER", "RASPBERRY", "LAVENDER",
                        "OAK LEAVES", "CATMINT", "MAPLE SEED", "LAUREL", "BULB WHITE", "BULB YELLOW", "BULB ORANGE", "BULB PINK", "BULB BLUE", "CLOVERTAIL", "DAISYTAIL",
                        "LILY OF THE VALLEY", "HEATHER", "SNAPDRAGON", "GORSE",
                        "DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS"
                        ]
    wild_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS", "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS", "MORPHO BUTTERFLY", "MONARCH BUTTERFLY1", "CICADA WINGS", "BLACK CICADA"]
  
    tail_accessories = ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS", "SPARROW FEATHERS", "CLOVERTAIL", "DAISYTAIL"]

    bandana_collars = ["CRIMSONBANDANA", "BLUEBANDANA", "YELLOWANDANA", "CYANBANDANA", "REDBANDANA",
    "LIMEBANDANA" ,"GREENBANDANA", "RAINBOWBANDANA", "BLACKBANDANA", "SPIKESBANDANA", "WHITEBANDANA","PINKBANDANA", "PURPLEBANDANA", "MULTIBANDANA", "INDIGOBANDANA"]
    harness_accessories = ["CRIMSONH", "BLUEH", "YELLOWH", "CYANH", "REDH", "LIMEH", "GREENH", "RAINBOWH", "BLACKH", "SPIKESH", "WHITEH", "PINKH",
                           "PURPLEH", "MULTIH", "INDIGOH"]
    bows_accessories = ["CRIMSONBOWS", "BLUEBOWS", "YELLOWBOWS", "CYANBOWS", "REDBOWS", "LIMEBOWS","GREENBOWS", "RAINBOWBOWS", "BLACKBOWS", "SPIKESBOWS", "WHITEBOWS",
                        "PINKBOWS", "PURPLEBOWS", "MULTIBOWS", "INDIGOBOWS"]
    dogteeth_collars = ["CRIMSONTEETHCOLLAR", "BLUETEETHCOLLAR", "YELLOWTEETHCOLLAR", "CYANTEETHCOLLAR", "REDTEETHCOLLAR",
                        "LIMETEETHCOLLAR","GREENTEETHCOLLAR", "RAINBOWTEETHCOLLAR", "BLACKTEETHCOLLAR", "SPIKESTEETHCOLLAR", "WHITETEETHCOLLAR",
                        "PINKTEETHCOLLAR", "PURPLETEETHCOLLAR", "MULTITEETHCOLLAR", "INDIGOTEETHCOLLAR"]
    collars = [
        "CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME", "GREEN", "RAINBOW",
        "BLACK", "SPIKES", "WHITE", "PINK", "PURPLE", "MULTI", "INDIGO", "CRIMSONBELL", "BLUEBELL",
        "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL", "GREENBELL",
        "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL", "PINKBELL", "PURPLEBELL",
        "MULTIBELL", "INDIGOBELL", "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
        "LIMEBOW", "GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW", "PINKBOW",
        "PURPLEBOW", "MULTIBOW", "INDIGOBOW", "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON",
        "REDNYLON", "LIMENYLON", "GREENNYLON", "RAINBOWNYLON",
        "BLACKNYLON", "SPIKESNYLON", "WHITENYLON", "PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON",

        
    ]
    flower_accessories = ["DAISY", "DIANTHUS", "BLEEDING HEARTS", "FRANGIPANI", "BLUE GLORY",
                     "CATNIP FLOWER", "BLANKET FLOWER", "ALLIUM", "LACELEAF",
                      "PURPLE GLORY", "YELLOW PRIMROSE", "HESPERIS",
                      "MARIGOLD", "WISTERIA"]

    plant2_accessories = ["CLOVER", "STICK", "PUMPKIN", "MOSS", "IVY", "ACORN", "MOSS PELT", "REEDS", "BAMBOO"
                    ]

    snake_accessories = ["GRASS SNAKE", "BLUE RACER", "WESTERN COACHWHIP", "KINGSNAKE"
                     
                     ]

    smallAnimal_accessories = ["GRAY SQUIRREL", "RED SQUIRREL", "CRAB", "WHITE RABBIT", "BLACK RABBIT",
                           "BROWN RABBIT", "INDIAN GIANT SQUIRREL", "FAWN RABBIT",
                           "BROWN AND WHITE RABBIT", "BLACK AND WHITE RABBIT", "WHITE AND FAWN RABBIT", "BLACK VITILIGO RABBIT",
                           "BROWN VITILIGO RABBIT", "FAWN VITILIGO RABBIT", "BLACKBIRD", "ROBIN",
                           "JAY", "THRUSH", "CARDINAL", "MAGPIE", "CUBAN TROGON", "TAN RABBIT", "TAN AND WHITE RABBIT",
                           "TAN VITILIGO RABBIT", "RAT", "WHITE MOUSE", "BLACK MOUSE", "GRAY MOUSE", "BROWN MOUSE", "GRAY RABBIT",
                           "GRAY AND WHITE RABBIT", "GRAY VITILIGO RABBIT"
                    ]

    deadInsect_accessories = ["LUNAR MOTH", "ROSY MAPLE MOTH", "MONARCH BUTTERFLY", "DAPPLED MONARCH",
                      "POLYPHEMUS MOTH", "MINT MOTH"
                    ]

    aliveInsect_accessories = ["BROWN SNAIL", "RED SNAIL", "WORM", "BLUE SNAIL", "ZEBRA ISOPOD", "DUCKY ISOPOD", "DAIRY COW ISOPOD",
                           "BEETLEJUICE ISOPOD", "BEE", "RED LADYBUG", "ORANGE LADYBUG", "YELLOW LADYBUG"
                    ]

    fruit_accessories = ["OGRASPBERRY", "BLACKBERRY", "GOLDEN RASPBERRY", "CHERRY", "YEW"
                    ]

    crafted_accessories = ["WILLOWBARK BAG", "CLAY DAISY POT", "CLAY AMANITA POT", "CLAY BROWNCAP POT", "BIRD SKULL", "LEAF BOW"
                    ]
    tail2_accessories = ["SEAWEED", "DAISY CORSAGE"
                    ]

    """Holds all appearance information for a cat. """

    def __init__(
        self,
        genotype:Genotype,
        phenotype:Phenotype,
        physical_trait_1:str=None,
        physical_trait_2:str=None,
        physical_trait_3:str=None,
        physical_trait_4:str=None,
        physical_trait_hidden:str=None,
        physical_trait_hidden_2:str=None,
        physical_trait_hidden_3:str=None,
        physical_trait_hidden_4:str=None,
        accessory:str=None,
        paralyzed:bool=False,
        opacity:int=100,
        scars:list=None,
        tint:str="none",
        white_patches_tint:str="none",
        kitten_sprite:int=None,
        adol_sprite:int=None,
        adult_sprite:int=None,
        senior_sprite:int=None,
        para_adult_sprite:int=None,
        reverse:bool=False,
        ) -> None:
        self.genotype = genotype
        self.phenotype = phenotype
        self.cat_sprites =  {
            "kitten": kitten_sprite if kitten_sprite is not None else 0,
            "adolescent": adol_sprite if adol_sprite is not None else 0,
            "young adult": adult_sprite if adult_sprite is not None else 0,
            "adult": adult_sprite if adult_sprite is not None else 0,
            "senior adult": adult_sprite if adult_sprite is not None else 0,
            "senior": senior_sprite if senior_sprite is not None else 0,
            "para_adult": para_adult_sprite if para_adult_sprite is not None else 0,
        }        
        self.cat_sprites['newborn'] = 20
        self.cat_sprites['para_young'] = 17
        self.cat_sprites["sick_adult"] = 18
        self.cat_sprites["sick_young"] = 19
        if phenotype.length == "longhaired" and genotype.longtype == 'long' and genotype.cornish[0] == "R" and genotype.lykoi[0] == 'Ly' and genotype.sedesp[0] != "re" and 'brush' not in phenotype.furtype:    
            self.length="long"
            if self.cat_sprites['adult'] < 9:
                self.cat_sprites['adult'] += 3
                self.cat_sprites['young adult'] += 3
                self.cat_sprites['senior adult'] += 3
        elif phenotype.length != 'hairless':
            if phenotype.length == "mediumhaired":
                self.length = 'medium'
            else:
                self.length="short"
            if self.cat_sprites['adult'] > 8:
                self.cat_sprites['adult'] -= 3
                self.cat_sprites['young adult'] -= 3
                self.cat_sprites['senior adult'] -= 3
        else:
            self.length="hairless"
            if self.cat_sprites['adult'] > 8:
                self.cat_sprites['adult'] -= 3
                self.cat_sprites['young adult'] -= 3
                self.cat_sprites['senior adult'] -= 3
        self.accessory = accessory
        self.paralyzed = paralyzed
        self.opacity = opacity
        self.scars = scars if isinstance(scars, list) else []
        self.tint = tint
        self.physical_trait_1 = physical_trait_1
        self.physical_trait_2 = physical_trait_2
        self.physical_trait_3 = physical_trait_3
        self.physical_trait_4 = physical_trait_4
        self.physical_trait_hidden = physical_trait_hidden
        self.physical_trait_hidden_2 = physical_trait_hidden_2
        self.physical_trait_hidden_3 = physical_trait_hidden_3
        self.physical_trait_hidden_4 = physical_trait_hidden_4
        self.white_patches_tint = white_patches_tint
        self.cat_sprites = {
            "kitten": kitten_sprite if kitten_sprite is not None else 0,
            "adolescent": adol_sprite if adol_sprite is not None else 0,
            "young adult": adult_sprite if adult_sprite is not None else 0,
            "adult": adult_sprite if adult_sprite is not None else 0,
            "senior adult": adult_sprite if adult_sprite is not None else 0,
            "senior": senior_sprite if senior_sprite is not None else 0,
            "para_adult": para_adult_sprite if para_adult_sprite is not None else 0,
            "newborn": 20,
            "para_young": 17,
            "sick_adult": 18,
            "sick_young": 19,
        }

        self.reverse = reverse

    @staticmethod
    def generate_new_pelt(genotype, phenotype, gender:str, parents:tuple=(), age:str="adult"):
        new_pelt = Pelt(genotype, phenotype)
        
        new_pelt.init_sprite()
        new_pelt.init_scars(age)
        new_pelt.init_accessories(age)
        new_pelt.init_tint()
        new_pelt.init_physical_traits(parents)
        return new_pelt

    def init_sprite(self):
        self.cat_sprites = {
            "newborn": 20,
            "kitten": random.randint(0, 2),
            "adolescent": random.randint(3, 5),
            "senior": random.randint(12, 14),
            "sick_young": 19,
            "sick_adult": 18,
        }
        self.reverse = choice([True, False])

        if self.length != "long":
            self.cat_sprites["adult"] = random.randint(6, 8)
            self.cat_sprites["para_adult"] = 16
        else:
            self.cat_sprites["adult"] = random.randint(9, 11)
            self.cat_sprites["para_adult"] = 15
        self.cat_sprites["young adult"] = self.cat_sprites["adult"]
        self.cat_sprites["senior adult"] = self.cat_sprites["adult"]

    def init_scars(self, age):
        if age == "newborn":
            return

        if age in ["kitten", "adolescent"]:
            scar_choice = random.randint(0, 50)  # 2%
        elif age in ["young adult", "adult"]:
            scar_choice = random.randint(0, 20)  # 5%
        else:
            scar_choice = random.randint(0, 15)  # 6.67%

        if scar_choice == 1:
            self.scars.append(choice([choice(Pelt.scars1), choice(Pelt.scars3)]))

        if "NOTAIL" in self.scars and "HALFTAIL" in self.scars:
            self.scars.remove("HALFTAIL")

    def init_accessories(self, age):
        if age == "newborn":
            self.accessory = None
            return

        acc_display_choice = random.randint(0, 80)
        if age in ["kitten", "adolescent"]:
            acc_display_choice = random.randint(0, 180)
        elif age in ["young adult", "adult"]:
            acc_display_choice = random.randint(0, 100)

        if acc_display_choice == 1:
            self.accessory = choice([
                choice(Pelt.plant_accessories),
                choice(Pelt.wild_accessories),
                choice(Pelt.flower_accessories),
                choice(Pelt.plant2_accessories),
                choice(Pelt.snake_accessories),
                choice(Pelt.smallAnimal_accessories),
                choice(Pelt.deadInsect_accessories),
                choice(Pelt.aliveInsect_accessories),
                choice(Pelt.fruit_accessories),
                choice(Pelt.crafted_accessories),
                choice(Pelt.tail2_accessories),
                choice(Pelt.bone_accessories),
                choice(Pelt.butterflies_accessories),
                choice(Pelt.stuff_accessories)
            ])
        else:
            self.accessory = None

        if self.phenotype.bobtailnr > 0 and self.phenotype.bobtailnr < 5 and self.accessory in ['RED FEATHERS', 'BLUE FEATHERS', 'JAY FEATHERS']:
            self.accessory = None
        

    def init_tint(self):
        """Sets tint for pelt and white patches"""

        # PELT TINT
        # Basic tints as possible for all colors.
        base_tints = sprites.cat_tints["possible_tints"]["basic"]
        
        colour = ""
        if self.phenotype.genotype.white[0] == "W":
            colour = "WHITE"
        elif 'point' in self.phenotype.point or 'silver' in self.phenotype.silvergold or (self.phenotype.genotype.dilute[0] == 'd' and self.phenotype.genotype.pinkdilute[0] == "dp"):
            colour = "PALE"
        elif 'gold' in self.phenotype.silvergold or 'sunshine' in self.phenotype.silvergold:
            colour = "GOLDEN"
        else:
            if (self.phenotype.genotype.dilute[0] == 'd' or self.phenotype.genotype.pinkdilute[0] == "dp"):
                if self.phenotype.colour in ['cream', 'cream apricot', 'honey']:
                    colour = "CREAM"
                elif self.phenotype.colour in ['fawn', 'fawn caramel', 'buff']:
                    colour = "FAWN"
                elif self.phenotype.colour in ['lilac', 'lilac caramel', 'champagne']:
                    colour = "LILAC"
                else:
                    colour = "BLUE"
            else:
                if self.phenotype.colour in ['flame', 'red']:
                    colour = "RED"
                elif self.phenotype.colour == "cinnamon":
                    colour = "CINNAMON"
                elif self.phenotype.colour == "chocolate":
                    colour = "CHOCOLATE"
                else:
                    colour = "BLACK"
        color_group = sprites.cat_tints["colour_groups"].get(colour, "warm")
        color_tints = sprites.cat_tints["possible_tints"][color_group]

        if base_tints or color_tints:
            self.tint = choice(base_tints + color_tints)
        else:
            self.tint = "none"

        # WHITE PATCHES TINT
        # Now for white patches
        base_tints = sprites.white_patches_tints["possible_tints"]["basic"]
        if colour in sprites.cat_tints["colour_groups"]:
            color_group = sprites.white_patches_tints["colour_groups"].get(colour, "white")
            color_tints = sprites.white_patches_tints["possible_tints"][color_group]
        else:
            color_tints = []

        if base_tints or color_tints:
            self.white_patches_tint = choice(base_tints + color_tints)
        else:
            self.white_patches_tint = "none"

    def init_physical_traits(self, parents: tuple=()):
        
        trait_categories = [
            Pelt.physical_trait_teeth,
            Pelt.physical_trait_ear_type,
            Pelt.physical_trait_ear_fold,
            Pelt.physical_trait_headfur,
            Pelt.physical_trait_cheekfur,
            Pelt.physical_trait_mane,
            Pelt.physical_trait_tail,
            Pelt.physical_trait_bodyfur,
            Pelt.physical_trait_misc
        ]
        
        trait_pool = [(trait, category) for category in trait_categories for trait in category]
        
        par_traits = set()
        for p in parents:
                par_traits.add(p.pelt.physical_trait_1)
                par_traits.add(p.pelt.physical_trait_2)
                par_traits.add(p.pelt.physical_trait_3)
                par_traits.add(p.pelt.physical_trait_4)
                par_traits.add(p.pelt.physical_trait_hidden)
                par_traits.add(p.pelt.physical_trait_hidden_2)
                par_traits.add(p.pelt.physical_trait_hidden_3)
                par_traits.add(p.pelt.physical_trait_hidden_4)
        
        # Remove any None values from par_traits
        par_traits.discard(None)
        
        if par_traits:
            # Check for conflicting traits from the same category
            for category in trait_categories:
                clash_traits = par_traits.intersection(category)
                if len(clash_traits) > 1:
                    chosen_trait = random.choice(list(clash_traits))
                    par_traits = par_traits.difference(clash_traits)
                    par_traits.add(chosen_trait)
            inherit_trait_chance = int(random.random() * 100)
            if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                #Roll to inherit first trait, and if so, remove it from the list
                self.physical_trait_1 = random.choice(list(par_traits))
                par_traits.remove(self.physical_trait_1)
                if len(par_traits) > 0:
                    #If we have a first trait, roll to inherit a second, and if we do, remove it from the list
                    inherit_trait_chance = int(random.random() * 100)
                    if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                        self.physical_trait_2 = random.choice(list(par_traits))
                        par_traits.remove(self.physical_trait_2)
                        if len(par_traits) > 0:
                            #If we have a second trait, roll to inherit a third, and if we do, remove it from the list
                            inherit_trait_chance = int(random.random() * 100)
                            if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                                self.physical_trait_3 = random.choice(list(par_traits))
                                par_traits.remove(self.physical_trait_3)
                                if len(par_traits) > 0:
                                    #If we have a third trait, roll to inherit a fourth, and if we do, remove it from the list
                                    inherit_trait_chance = int(random.random() * 100)
                                    if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                                        self.physical_trait_4 = random.choice(list(par_traits))
                                        par_traits.remove(self.physical_trait_4)
            if len(par_traits) > 0:
                #If there are still leftover traits, roll to inherit as hidden with a +50% chance
                inherit_trait_chance = int((random.random() * 100) - 50)
                if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                    self.physical_trait_hidden = random.choice(list(par_traits))
                    par_traits.remove(self.physical_trait_hidden)
                    if len(par_traits) > 0:
                        #If there are still leftover traits, roll to inherit as hidden with a +50% chance
                        inherit_trait_chance = int((random.random() * 100) - 50)
                        if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                            self.physical_trait_hidden_2 = random.choice(list(par_traits))
                            par_traits.remove(self.physical_trait_hidden_2)
                            if len(par_traits) > 0:
                                #If there are still leftover traits, roll to inherit as hidden with a +50% chance
                                inherit_trait_chance = int((random.random() * 100) - 50)
                                if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                                    self.physical_trait_hidden_3 = random.choice(list(par_traits))
                                    par_traits.remove(self.physical_trait_hidden_3)
                                    if len(par_traits) > 0:
                                        #If there are still leftover traits, roll to inherit as hidden with a +50% chance
                                        inherit_trait_chance = int((random.random() * 100) - 50)
                                        if inherit_trait_chance <= game.config["cat_generation"]["physical_trait_inherit_chance"]:
                                            self.physical_trait_hidden_4 = random.choice(list(par_traits))
                                            par_traits.remove(self.physical_trait_hidden_4)
            
        # Giving cats that inherited nothing a 50% of base chance roll for new traits
        if not self.physical_trait_1:
            trait_chance = int(random.random() * 100)
            if trait_chance <= game.config["cat_generation"]["physical_trait_chance"]:
                if trait_chance <= (0.5 * game.config["cat_generation"]["physical_trait_chance"]):
                    traitcount = 2
                    trait_chance = int(random.random() * 100)
                    if trait_chance <= (0.25 * game.config["cat_generation"]["physical_trait_chance"]):
                        traitcount = 3
                        trait_chance = int(random.random() * 100)
                        if trait_chance <= (0.1 * game.config["cat_generation"]["physical_trait_chance"]):
                            traitcount = 4
                else:
                    traitcount = 1
            else:
                traitcount = 0
                
            if traitcount > 0:
                # Select the first trait and its category
                trait1, category1 = random.choice(trait_pool)
                print("Trait 1:", trait1)
                self.physical_trait_1 = trait1
                
                # Remove traits from the same category as the first trait
                trait_pool = [(trait, category) for trait, category in trait_pool if category != category1]
                
                if traitcount >= 2 and trait_pool:
                    # Select the second trait from the remaining pool
                    trait2, category2 = random.choice(trait_pool)
                    print("Trait 2:", trait2)
                    self.physical_trait_2 = trait2
                    
                    # Remove traits from the same category as the second trait
                    trait_pool = [(trait, category) for trait, category in trait_pool if category != category2]
                    
                    if traitcount >= 3 and trait_pool:
                        # Select the third trait from the remaining pool
                        trait3, category3 = random.choice(trait_pool)
                        print("Trait 3:", trait3)
                        self.physical_trait_3 = trait3
                        
                        # Remove traits from the same category as the third trait
                        trait_pool = [(trait, category) for trait, category in trait_pool if category != category3]
                        
                        if traitcount == 4 and trait_pool:
                            # Select the fourth trait from the remaining pool
                            trait4, category4 = random.choice(trait_pool)
                            print("Trait 4:", trait4)
                            self.physical_trait_4 = trait4
                        else:
                            self.physical_trait_4 = None
                    else:
                        self.physical_trait_3 = None
                        self.physical_trait_4 = None
                else:
                    self.physical_trait_2 = None
                    self.physical_trait_3 = None
                    self.physical_trait_4 = None
            else:
                self.physical_trait_1 = None
                self.physical_trait_2 = None
                self.physical_trait_3 = None
                self.physical_trait_4 = None
                
    @staticmethod
    def describe_appearance(cat, short=False):
        
        color_name = cat.phenotype.PhenotypeOutput(pattern=cat.genotype.white_pattern, gender=cat.genderalign)
        
        if not short:

            scar_details = {
                "NOTAIL": "no tail",
                "HALFTAIL": "half a tail",
                "NOPAW": "three legs",
                "NOLEFTEAR": "a missing ear",
                "NORIGHTEAR": "a missing ear",
                "NOEAR": "no ears"
            }

            scarlist = []
            for scar in cat.pelt.scars:
                if scar in scar_details:
                    scarlist.append(i18n.t(f"cat.pelts.{scar}"))
            color_name += adjust_list_text(list(set(scarlist))) if len(scarlist) > 0 else "" # note: this doesn't preserve order!
        return color_name
