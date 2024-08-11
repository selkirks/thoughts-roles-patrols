import os
from copy import copy

import pygame
import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None
        
        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")
            
    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"
                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )
                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite
                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'lineart', 'singlecolours', 'speckledcolours', 'tabbycolours',
            'whitepatches', 'minkstorties', 'minkswhite', 'eyes', 'eyes2', 'eyes3', 'eyes4', 'beetleeyes', 'beetleeyes2', 'beetlemore', 'beetlemore2', 'skin', 'scars', 'missingscars',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars',
            'bengalcolours', 'marbledcolours', 'rosettecolours', 'smokecolours', 'tickedcolours', 
            'mackerelcolours', 'classiccolours', 'sokokecolours', 'agouticolours', 'singlestripecolours',
            'maskedcolours', 
            'shadersnewwhite', 'lineartdead', 'tortiepatchesmasks', 
            'medcatherbs', 'lineartdf', 'lightingnew', 'fademask',
            'fadestarclan', 'fadedarkforest', 'symbols'

        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        # Define eye colors
        eye_colors = [
            ['YELLOW', 'AMBER', 'HAZEL', 'PALEGREEN', 'GREEN', 'BLUE', 'DARKBLUE', 'GREY', 'CYAN', 'EMERALD',
             'HEATHERBLUE', 'SUNLITICE'],
            ['COPPER', 'SAGE', 'COBALT', 'PALEBLUE', 'BRONZE', 'SILVER', 'PALEYELLOW', 'GOLD', 'GREENYELLOW']
        ]
        beetle_eyes = [
            ['ROSE', 'ALGAE', 'SEAFOAM', 'LIGHT FLAME', 'CLOUDY', 'RED', 'TURQUOISE',
             'SWAMP', 'RAINY', 'AQUAMARINE', 'EARTH', 'PUMPKIN'],
            ['LILAC', 'PERIWINKLE', 'VIOLET', 'POND', 'DIRT', 'BROWN', 'CEDAR', 'CHRISTMAS', 'COTTON CANDY'],
        ]
        beetle_more = [    
            ['DARK PINE', 'FALL', 'FOREST FIRE', 'GOLD MOON', 'HALLOWEEN', 'LOBELIA', 
             'MIDNIGHT', 'MOONSTONE', 'OXIDIZED', 'SNOW', 'BERRY BANANA', 'DAWN SKY'],
            ['TWILIGHT SKY', 'WORMY', 'BLUE HAZEL', 'THUNDERBOLT', 'VOLCANO', 'SEASHELL', 'PARADOX', 'CURSE', 'BLESSING']
        ]
        myst_eyes = [    
            ['ETA', 'CARINA', 'EAGLE', 'GHOST HEAD', 'LAGOON', 'MILKY WAY', 'SOUL', 'SWAN', 'TARANTULA', 'VEIL', 'SHROUD', 'CARI'],
            ['SEA FOAM', 'LILAC2', 'AZURE', 'STORM', 'RUSSET', 'SAND', 'MIST', 'AMETHYST', 'TEMPEST']
        ]
        for row, colors in enumerate(eye_colors):
            for col, color in enumerate(colors):
                self.make_group('eyes', (col, row), f'eyes{color}')
                self.make_group('eyes2', (col, row), f'eyes2{color}')

        for row, colors in enumerate(myst_eyes):
            for col, color in enumerate(colors):
                self.make_group('eyes3', (col, row), f'eyes{color}')
                self.make_group('eyes4', (col, row), f'eyes2{color}')
        
        for row, colors in enumerate(beetle_eyes):
            for col, color in enumerate(colors):
                self.make_group('beetleeyes', (col, row), f'eyes{color}')
                self.make_group('beetleeyes2', (col, row), f'eyes2{color}')

        for row, colors in enumerate(beetle_more):
            for col, color in enumerate(colors):
                self.make_group('beetlemore', (col, row), f'eyes{color}')
                self.make_group('beetlemore2', (col, row), f'eyes2{color}')

        # white patches
        for a, i in enumerate(['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO',
            'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE']):
            self.make_group('whitepatches', (a, 0), f'white{i}')
        for a, i in enumerate(['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 
            'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL']):
            self.make_group('whitepatches', (a, 1), f'white{i}')
        # ryos white patches
        for a, i in enumerate(['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO',
            'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD']):
            self.make_group('whitepatches', (a, 2), f'white{i}')
        for a, i in enumerate(['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY',
            'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER']):
            self.make_group('whitepatches', (a, 3), f'white{i}')
        for a, i in enumerate(
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW',
                'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW']):
            self.make_group('whitepatches', (a, 4), f'white{i}')
        # beejeans white patches + perrio's point marks, painted, and heart2 + anju's new marks + key's blackstar
        for a, i in enumerate(['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',
            'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER']):
            self.make_group('whitepatches', (a, 5), f'white{i}')
        # acorn's white patches + ryos' bub + fable lovebug + frankie trixie
        for a, i in enumerate(['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART',
            'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE']):
            self.make_group('whitepatches', (a, 6), f'white{i}')
        # acorn's white patches: the sequel
        for a, i in enumerate(['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE',
            'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS']):
            self.make_group('whitepatches', (a, 7), f'white{i}')
        for a, i in enumerate(['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR',
            'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS']):
            self.make_group('whitepatches', (a, 8), f'white{i}')
        for a, i in enumerate(['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']):
            self.make_group('whitepatches', (a, 9), 'white' + i)
                        
                                # minks white patches
        for a, i in enumerate(['MINKONE', 'MINKTWO', 'MINKTHREE', 'MINKFOUR', 'MINKREDTAIL', 'MINKDELILAH', 'MINKHALF', 'MINKSTREAK', 'MINKMASK', 'MINKSMOKE']):
            self.make_group('minkswhite', (a, 0), f'white{i}')
        for a, i in enumerate(['MINKMINIMALONE', 'MINKMINIMALTWO', 'MINKMINIMALTHREE', 'MINKMINIMALFOUR', 'MINKOREO', 'MINKSWOOP', 'MINKCHIMERA', 'MINKCHEST', 'MINKARMTAIL', 'MINKGRUMPYFACE']):
            self.make_group('minkswhite', (a, 1), f'white{i}')
        for a, i in enumerate(['MINKMOTTLED', 'MINKSIDEMASK', 'MINKEYEDOT', 'MINKBANDANA', 'MINKPACMAN', 'MINKSTREAMSTRIKE', 'MINKSMUDGED', 'MINKDAUB', 'MINKEMBER', 'MINKBRIE']):
            self.make_group('minkswhite', (a, 2), f'white{i}')
        for a, i in enumerate(['MINKORIOLE', 'MINKROBIN', 'MINKBRINDLE', 'MINKPAIGE', 'MINKROSETAIL', 'MINKSAFI', 'MINKDAPPLENIGHT', 'MINKBLANKET', 'MINKBELOVED', 'MINKBODY']):
            self.make_group('minkswhite', (a, 3), f'white{i}')
        for a, i in enumerate(['MINKSHILOH', 'MINKFRECKLED', 'MINKHEARTBEAT']):
            self.make_group('minkswhite', (a, 4), f'white{i}')

        # single (solid)
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlecolours', (a, 0), f'single{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlecolours', (a, 1), f'single{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlecolours', (a, 2), f'single{i}')
        # tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tabbycolours', (a, 0), f'tabby{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tabbycolours', (a, 1), f'tabby{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tabbycolours', (a, 2), f'tabby{i}')
        # marbled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('marbledcolours', (a, 0), f'marbled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('marbledcolours', (a, 1), f'marbled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('marbledcolours', (a, 2), f'marbled{i}')
        # rosette
                
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('rosettecolours', (a, 0), f'rosette{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('rosettecolours', (a, 1), f'rosette{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('rosettecolours', (a, 2), f'rosette{i}')
        # smoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('smokecolours', (a, 0), f'smoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('smokecolours', (a, 1), f'smoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('smokecolours', (a, 2), f'smoke{i}')
        # ticked
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('tickedcolours', (a, 0), f'ticked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('tickedcolours', (a, 1), f'ticked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('tickedcolours', (a, 2), f'ticked{i}')
        # speckled
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('speckledcolours', (a, 0), f'speckled{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('speckledcolours', (a, 1), f'speckled{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('speckledcolours', (a, 2), f'speckled{i}')
        # bengal
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('bengalcolours', (a, 0), f'bengal{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('bengalcolours', (a, 1), f'bengal{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('bengalcolours', (a, 2), f'bengal{i}')
        # mackerel
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('mackerelcolours', (a, 0), f'mackerel{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('mackerelcolours', (a, 1), f'mackerel{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('mackerelcolours', (a, 2), f'mackerel{i}')
        # classic
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('classiccolours', (a, 0), f'classic{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('classiccolours', (a, 1), f'classic{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('classiccolours', (a, 2), f'classic{i}')
        # sokoke
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('sokokecolours', (a, 0), f'sokoke{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('sokokecolours', (a, 1), f'sokoke{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('sokokecolours', (a, 2), f'sokoke{i}')
        # agouti
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('agouticolours', (a, 0), f'agouti{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('agouticolours', (a, 1), f'agouti{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('agouticolours', (a, 2), f'agouti{i}')
        # singlestripe
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('singlestripecolours', (a, 0), f'singlestripe{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('singlestripecolours', (a, 1), f'singlestripe{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('singlestripecolours', (a, 2), f'singlestripe{i}')
        # masked tabby
        for a, i in enumerate(['WHITE', 'PALEGREY', 'SILVER', 'GREY', 'DARKGREY', 'GHOST', 'BLACK']):
            self.make_group('maskedcolours', (a, 0), f'masked{i}')
        for a, i in enumerate(['CREAM', 'PALEGINGER', 'GOLDEN', 'GINGER', 'DARKGINGER', 'SIENNA']):
            self.make_group('maskedcolours', (a, 1), f'masked{i}')
        for a, i in enumerate(['LIGHTBROWN', 'LILAC', 'BROWN', 'GOLDEN-BROWN', 'DARKBROWN', 'CHOCOLATE']):
            self.make_group('maskedcolours', (a, 2), f'masked{i}')
            
        # new new torties
        for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE']):
            self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL', 'GRUMPYFACE']):
            self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE']):
            self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY']):
            self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")
        for a, i in enumerate(['SHILOH', 'FRECKLED', 'HEARTBEAT']):
            self.make_group('tortiepatchesmasks', (a, 4), f"tortiemask{i}")
        for a, i in enumerate(['MINKFULLWHITE', 'MINKANY', 'MINKTUXEDO', 'MINKLITTLE', 'MINKCOLOURPOINT', 'MINKVAN', 'MINKANYTWO',
            'MINKMOON', 'MINKPHANTOM', 'MINKPOWDER', 'MINKBLEACHED', 'MINKSAVANNAH', 'MINKFADESPOTS', 'MINKPEBBLESHINE']):
            self.make_group('minkstorties', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINKEXTRA', 'MINKONEEAR', 'MINKBROKEN', 'MINKLIGHTTUXEDO', 'MINKBUZZARDFANG', 'MINKRAGDOLL', 
            'MINKLIGHTSONG', 'MINKVITILIGO', 'MINKBLACKSTAR', 'MINKPIEBALD', 'MINKCURVED', 'MINKPETAL', 'MINKSHIBAINU', 'MINKOWL']):
            self.make_group('minkstorties', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MINKTIP', 'MINKFANCY', 'MINKFRECKLES', 'MINKRINGTAIL', 'MINKHALFFACE', 'MINKPANTSTWO', 'MINKGOATEE', 'MINKVITILIGOTWO',
            'MINKPAWS', 'MINKMITAINE', 'MINKBROKENBLAZE', 'MINKSCOURGE', 'MINKDIVA', 'MINKBEARD']):
            self.make_group('minkstorties', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['MINKTAIL', 'MINKBLAZE', 'MINKPRINCE', 'MINKBIB', 'MINKVEE', 'MINKUNDERS', 'MINKHONEY',
            'MINKFAROFA', 'MINKDAMIEN', 'MINKMISTER', 'MINKBELLY', 'MINKTAILTIP', 'MINKTOES', 'MINKTOPCOVER']):
            self.make_group('minkstorties', (a, 3), f'tortiemask{i}')
        for a, i in enumerate(['MINKAPRON', 'MINKCAPSADDLE', 'MINKMASKMANTLE', 'MINKSQUEAKS', 'MINKSTAR', 'MINKTOESTAIL', 'MINKRAVENPAW',
                'MINKPANTS', 'MINKREVERSEPANTS', 'MINKSKUNK', 'MINKKARPATI', 'MINKHALFWHITE', 'MINKAPPALOOSA', 'MINKDAPPLEPAW']):
            self.make_group('minkstorties', (a, 4), f'tortiemask{i}')
        for a, i in enumerate(['MINKHEART', 'MINKLILTWO', 'MINKGLASS', 'MINKMOORISH', 'MINKSEPIAPOINT', 'MINKMINKPOINT', 'MINKSEALPOINT',
            'MINKMAO', 'MINKLUNA', 'MINKCHESTSPECK', 'MINKWINGS', 'MINKPAINTED', 'MINKHEARTTWO', 'MINKWOODPECKER']):
            self.make_group('minkstorties', (a, 5), f'tortiemask{i}')
        for a, i in enumerate(['MINKBOOTS', 'MINKMISS', 'MINKCOW', 'MINKCOWTWO', 'MINKBUB', 'MINKBOWTIE', 'MINKMUSTACHE', 'MINKREVERSEHEART',
            'MINKSPARROW', 'MINKVEST', 'MINKLOVEBUG', 'MINKTRIXIE', 'MINKSAMMY', 'MINKSPARKLE']):
            self.make_group('minkstorties', (a, 6), f'tortiemask{i}')
        for a, i in enumerate(['MINKRIGHTEAR', 'MINKLEFTEAR', 'MINKESTRELLA', 'MINKSHOOTINGSTAR', 'MINKEYESPOT', 'MINKREVERSEEYE',
            'MINKFADEBELLY', 'MINKFRONT', 'MINKBLOSSOMSTEP', 'MINKPEBBLE', 'MINKTAILTWO', 'MINKBUDDY', 'MINKBACKSPOT', 'MINKEYEBAGS']):
            self.make_group('minkstorties', (a, 7), f'tortiemask{i}')
        for a, i in enumerate(['MINKBULLSEYE', 'MINKFINN', 'MINKDIGIT', 'MINKKROPKA', 'MINKFCTWO', 'MINKFCONE', 'MINKMIA', 'MINKSCAR',
            'MINKBUSTER', 'MINKSMOKEY', 'MINKHAWKBLAZE', 'MINKCAKE', 'MINKROSINA', 'MINKPRINCESS']):
            self.make_group('minkstorties', (a, 8), f'tortiemask{i}')
        for a, i in enumerate(['MINKLOCKET', 'MINKBLAZEMASK', 'MINKTEARS', 'MINKDOUGIE']):
            self.make_group('minkstorties', (a, 9), 'tortiemask' + i)

<<<<<<< Updated upstream
        # SKINS
        for a, i in enumerate(['BLACK', "RED", 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN']):
            self.make_group('skin', (a, 0), f"skin{i}")
        for a, i in enumerate(['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH']):
            self.make_group('skin', (a, 1), f"skin{i}")
        for a, i in enumerate(['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']):
            self.make_group('skin', (a, 2), f"skin{i}")
=======
        for row, patches in enumerate(white_patches):
            for col, patch in enumerate(patches):
                self.make_group('whitepatches', (col, row), f'white{patch}')

        # Define colors and categories
        color_categories = [
            ['WHITE', 'PALEGREY', 'LIGHTGREY', 'GREY', 'DARKGREY', 'BLACK', 'OBSIDIAN', 'GHOST', 'PALEBLUE', 'LIGHTBLUE', 'BLUE', 'DARKBLUE', 'SILVERCHOCOLATE', 
             'SILVERGINGER'],
            ['DARKSLATE', 'SLATE', 'LIGHTSLATE', 'PALESLATE', 'PALELILAC', 'LIGHTLILAC', 'LILAC', 'DARKLILAC', 'DARKASH', 'ASH', 'LIGHTASH', 'PALEASH', 'SILVERCINNAMON', 
             'SILVERRED'],
            ['PALEBROWN', 'LIGHTBROWN', 'BROWN', 'DARKBROWN', 'EBONY', 'DARKCHOCOLATE', 'CHOCOLATE', 'LIGHTCHOCOLATE', 'PALECHOCOLATE', 'PALECINNAMON', 
             'LIGHTCINNAMON', 'CINNAMON', 'SILVERFAWN'],
            ['DARKCINNAMON', 'DARKFAWN', 'FAWN', 'LIGHTFAWN', 'PALEFAWN', 'PALECREAM', 'LIGHTCREAM', 'CREAM', 'DARKCREAM', 'DARKGOLD', 'GOLD', 'LIGHTGOLD', 
             'SILVERCREAM'],
            ['PALEGOLD', 'SUNSHINE', 'BRONZE', 'COPPER', 'DARKORANGE', 'ORANGE', 'LIGHTORANGE', 'PALEORANGE', 'PALEGINGER', 'LIGHTGINGER', 'GINGER', 
             'DARKGINGER', 'SILVERGOLD'],
            ['RUSSET', 'DARKRED', 'RED', 'LIGHTRED', 'PALERED', 'SILVER', 'SILVERGREY', 'SILVERBLUE', 'SILVERSLATE', 'SILVERLILAC', 'SILVERASH', 'SILVERBROWN', 
             'SILVERORANGE']
        ]

        color_types = [
            'singlecolours', 'tabbycolours', 'marbledcolours', 'rosettecolours',
            'smokecolours', 'tickedcolours', 'speckledcolours', 'bengalcolours',
            'mackerelcolours', 'classiccolours', 'sokokecolours', 'agouticolours',
            'singlestripecolours', 'maskedcolours'
        ]

        for row, colors in enumerate(color_categories):
            for col, color in enumerate(colors):
                for color_type in color_types:
                    self.make_group(color_type, (col, row), f'{color_type[:-7]}{color}')

        # tortiepatchesmasks
        tortiepatchesmasks = [
            ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE'],
            ['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
             'GRUMPYFACE'],
            ['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE'],
            ['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY'],
            ['SHILOH', 'FRECKLED', 'HEARTBEAT']
        ]


# Define mink's tortie patches
        minks_tortie_patches = [
            ['MINKFULLWHITE', 'MINKANY', 'MINKTUXEDO', 'MINKLITTLE', 'MINKCOLOURPOINT', 'MINKVAN', 'MINKANYTWO',
             'MINKMOON', 'MINKPHANTOM', 'MINKPOWDER',
             'MINKBLEACHED', 'MINKSAVANNAH', 'MINKFADESPOTS', 'MINKPEBBLESHINE'],
            ['MINKEXTRA', 'MINKONEEAR', 'MINKBROKEN', 'MINKLIGHTTUXEDO', 'MINKBUZZARDFANG', 'MINKRAGDOLL',
             'MINKLIGHTSONG', 'MINKVITILIGO', 'MINKBLACKSTAR',
             'MINKPIEBALD', 'MINKCURVED', 'MINKPETAL', 'MINKSHIBAINU', 'MINKOWL'],
            ['MINKTIP', 'MINKFANCY', 'MINKFRECKLES', 'MINKRINGTAIL', 'MINKHALFFACE', 'MINKPANTSTWO', 'MINKGOATEE',
             'MINKVITILIGOTWO', 'MINKPAWS', 'MINKMITAINE',
             'MINKBROKENBLAZE', 'MINKSCOURGE', 'MINKDIVA', 'MINKBEARD'],
            ['MINKTAIL', 'MINKBLAZE', 'MINKPRINCE', 'MINKBIB', 'MINKVEE', 'MINKUNDERS', 'MINKHONEY', 'MINKFAROFA',
             'MINKDAMIEN', 'MINKMISTER', 'MINKBELLY',
             'MINKTAILTIP', 'MINKTOES', 'MINKTOPCOVER'],
            ['MINKAPRON', 'MINKCAPSADDLE', 'MINKMASKMANTLE', 'MINKSQUEAKS', 'MINKSTAR', 'MINKTOESTAIL', 'MINKRAVENPAW',
             'MINKPANTS', 'MINKREVERSEPANTS',
             'MINKSKUNK', 'MINKKARPATI', 'MINKHALFWHITE', 'MINKAPPALOOSA', 'MINKDAPPLEPAW'],
            ['MINKHEART', 'MINKLILTWO', 'MINKGLASS', 'MINKMOORISH', 'MINKSEPIAPOINT', 'MINKMINKPOINT', 'MINKSEALPOINT',
             'MINKMAO', 'MINKLUNA', 'MINKCHESTSPECK',
             'MINKWINGS', 'MINKPAINTED', 'MINKHEARTTWO', 'MINKWOODPECKER'],
            ['MINKBOOTS', 'MINKMISS', 'MINKCOW', 'MINKCOWTWO', 'MINKBUB', 'MINKBOWTIE', 'MINKMUSTACHE',
             'MINKREVERSEHEART', 'MINKSPARROW', 'MINKVEST',
             'MINKLOVEBUG', 'MINKTRIXIE', 'MINKSAMMY', 'MINKSPARKLE'],
            ['MINKRIGHTEAR', 'MINKLEFTEAR', 'MINKESTRELLA', 'MINKSHOOTINGSTAR', 'MINKEYESPOT', 'MINKREVERSEEYE',
             'MINKFADEBELLY', 'MINKFRONT',
             'MINKBLOSSOMSTEP', 'MINKPEBBLE', 'MINKTAILTWO', 'MINKBUDDY', 'MINKBACKSPOT', 'MINKEYEBAGS'],
            ['MINKBULLSEYE', 'MINKFINN', 'MINKDIGIT', 'MINKKROPKA', 'MINKFCTWO', 'MINKFCONE', 'MINKMIA', 'MINKSCAR',
             'MINKBUSTER', 'MINKSMOKEY', 'MINKHAWKBLAZE',
             'MINKCAKE', 'MINKROSINA', 'MINKPRINCESS'],
            ['MINKLOCKET', 'MINKBLAZEMASK', 'MINKTEARS', 'MINKDOUGIE']
        ]

        for row, masks in enumerate(tortiepatchesmasks):
            for col, mask in enumerate(masks):
                self.make_group('tortiepatchesmasks', (col, row), f"tortiemask{mask}")
        for row, minkmasks in enumerate(minks_tortie_patches):
            for col, minkmask in enumerate(minkmasks):
                self.make_group('minkstorties', (col, row), f"tortiemask{minkmask}")
        for row, masks in enumerate(tortiepatchesmasks):
            for col, mask in enumerate(masks):
                self.make_group('tortiepatchesmasks', (col, row), f"tortiemask{mask}")

        # Define skin colors 
        skin_colors = [
            ['BLACK', 'RED', 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN'],
            ['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH'],
            ['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']
        ]

        for row, colors in enumerate(skin_colors):
            for col, color in enumerate(colors):
                self.make_group('skin', (col, row), f"skin{color}")
>>>>>>> Stashed changes

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """
        for a, i in enumerate(
                ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", 
                 "BRIDGE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND", "BURNPAWS", "BURNTAIL"]):
            self.make_group('scars', (a, 0), f'scars{i}')
        for a, i in enumerate(
                ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE",
                 "FROSTFACE", "FROSTTAIL", "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"]):
            self.make_group('scars', (a, 1), f'scars{i}')
        for a, i in enumerate(
                ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE",
                 "LEGBITE", "NECKBITE", "FACE"]):
            self.make_group('scars', (a, 2), f'scars{i}')
        for a, i in enumerate(
                ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]):
            self.make_group('scars', (a, 3), f'scars{i}')
        # missing parts
        for a, i in enumerate(
                ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]):
            self.make_group('missingscars', (a, 0), f'scars{i}')

            # Accessories
        for a, i in enumerate([
            "MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"]):
            self.make_group('medcatherbs', (a, 0), f'acc_herbs{i}')
        for a, i in enumerate([
            "BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"]):
            self.make_group('medcatherbs', (a, 1), f'acc_herbs{i}')
        for a, i in enumerate([
            "OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER"]):
            self.make_group('medcatherbs', (a, 3), f'acc_herbs{i}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        for a, i in enumerate([
            "RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]):
            self.make_group('medcatherbs', (a, 2), f'acc_wild{i}')
        for a, i in enumerate(["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"]):
            self.make_group('collars', (a, 0), f'collars{i}')
        for a, i in enumerate(["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"]):
            self.make_group('collars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINK", "PURPLE", "MULTI", "INDIGO"]):
            self.make_group('collars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL",
            "LIMEBELL"
        ]):
            self.make_group('bellcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"]):
            self.make_group('bellcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]):
            self.make_group('bellcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
            "LIMEBOW"
        ]):
            self.make_group('bowcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"]):
            self.make_group('bowcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]):
            self.make_group('bowcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON",
            "LIMENYLON"
        ]):
            self.make_group('nyloncollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"]):
            self.make_group('nyloncollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]):
            self.make_group('nyloncollars', (a, 2), f'collars{i}')
    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                x_mod = 0
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_mod += variant_index
                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (i + x_mod, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1
            

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()
