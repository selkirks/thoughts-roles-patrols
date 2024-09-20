from .genotype import *
from .phenotype import *
from random import choice, random
from operator import xor
from copy import deepcopy
import numpy as np

class Namer():
    def __init__ (self, used_prefixes=[]):
        self.used_prefixes = used_prefixes
        if os.path.exists('resources/dicts/names/alt_prefixes.json'):
            with open('resources/dicts/names/alt_prefixes.json') as read_file:
                self.all_prefixes = ujson.loads(read_file.read())

    def start(self, genotype: Genotype, phenotype: Phenotype, chimera_pheno = None, moons=0):
        self.genotype = genotype
        self.phenotype = phenotype
        self.chimera_pheno = chimera_pheno
        self.moons = moons

        if genotype:
            params = self.parse_chimera() if genotype.chimera else self.get_categories(genotype, phenotype)

            # print(params)
            # print(genotype.ShowGenes())
            # print(genotype.tortiepattern)
            # print(genotype.specialred)

            if params[0] in ['white', 'silver shaded'] or (params[3] == 'high' and random() < 0.2):
                return self.white(params[0])
            elif params[0] == 'black':
                return self.black(params)

    def parse_chimera(self):

        base = ""
        tortie = False
        tabby = {
            'pattern' : '',
            'type' : 'regular'
        }
        white = 'none'
        point = 'none'

        #compare different chimera halves here
        set_one = self.get_categories(self.genotype, self.phenotype)
        set_two = self.get_categories(self.genotype.chimerageno, self.chimera_pheno)


        #the easy part
        if set_one[1] in ['white', 'silver shaded'] and set_two[1] in ['white', 'silver shaded']:
            base = 'white'
            return [base, tortie, tabby, white, point]
        
        if set_one[1] or set_two[1] or xor(set_one[0] in ['ginger', 'cream'], set_two[0] in ['ginger', 'cream']):
            tortie = True

        if set_one[3] == 'high' or (self.moons == 0 and set_one[4] == 'colourpoint'):
            white = 'high'
        elif set_one[3] == 'mid' or set_two[3] == 'high' or set_one[1] == 'white' or set_two[1] in ['white', 'silver shaded'] or (self.moons == 0 and set_two[4] == 'colourpoint'):
            white = 'mid'
        elif set_one[3] == 'low' or set_two[3] == 'mid':
            white = 'low'

        #mixing solid + tabby or different base-colours changes tabby pattern to blotched
        if set_one[0] != set_two[0] and set_one[0] not in ['ginger', 'cream'] and set_two[0] not in ['ginger', 'cream']:
            tabby['pattern'] = 'blotched'
        
        #mixing different bases

        if (set_one[0] in ['black', 'chocolate', 'cinnamon'] and set_two[0] in ['black', 'chocolate', 'cinnamon']):
            if xor(set_one[2]['type'] == 'silver', set_two[2]['type'] == 'silver'):
                tortie = True
                tabby['type'] = 'silver'
            elif xor(set_one[2]['type'] == 'golden', set_two[2]['type'] == 'golden'):
                tortie = True
                if 'regular' in [set_one[2]['type'], set_two[2]['type']] and '' not in [set_one[2]['pattern'], set_two[2]['pattern']]:
                    tabby['type'] = 'regular'
                else:
                    tabby['type'] = 'dark'
            
            if 'black' in [set_one[0], set_two[0]]:
                base = 'black'
            elif 'chocolate' in [set_one[0], set_two[0]]:
                base = 'chocolate'
            else:
                base = 'cinnamon'
        elif (set_one[0] in ['blue', 'lilac', 'fawn'] and set_two[0] in ['blue', 'lilac', 'fawn']):
            if xor(set_one[2]['type'] == 'silver', set_two[2]['type'] == 'silver'):
                tortie = True
                tabby['type'] = 'silver'
            elif xor(set_one[2]['type'] == 'golden', set_two[2]['type'] == 'golden'):
                tortie = True
                if 'regular' in [set_one[2]['type'], set_two[2]['type']] and '' not in [set_one[2]['pattern'], set_two[2]['pattern']]:
                    tabby['type'] = 'regular'
                else:
                    tabby['type'] = 'dark'
            
            if 'blue' in [set_one[0], set_two[0]]:
                base = 'blue'
            elif 'lilac' in [set_one[0], set_two[0]]:
                base = 'lilac'
            else:
                base = 'fawn'
        else:
            tabby['type'] = 'silver'
            if set_one[4] != 'none':
                tortie = True
            if 'black' in [set_one[0], set_two[0]]:
                base = 'black'
            elif 'chocolate' in [set_one[0], set_two[0]]:
                base = 'chocolate'
            else:
                if 'blue' in [set_one[0], set_two[0]]:
                    base = 'blue'
                elif 'lilac' in [set_one[0], set_two[0]]:
                    base = 'lilac'
                else:
                    base = 'fawn'

        #mixing different types of point

        point = set_one[4]

    def get_categories(self, genotype, phenotype):
        
        # Categories are split into: base, tortie?, tabby (pattern, silver, golden), white amount, point
        base = ""
        tortie = False
        tabby = {
            'pattern' : '',
            'type' : 'regular'
        }
        white = 'none'
        point = 'none'

        try:
            phenotype.maincolour
        except:
            phenotype.SpriteInfo(self.moons)

        if (phenotype.colour in ['white', 'albino'] or 
            (phenotype.maincolour == 'white' and not phenotype.patchmain) or
            (genotype.tortiepattern == ['revCRYPTIC'] and genotype.brindledbi) or 
            (genotype.dilute[0] == 'd' and genotype.pinkdilute[0] == 'dp' and 
                (('dove' in phenotype.colour and genotype.saturation < 2) or 
                ('platinum' in phenotype.colour and genotype.saturation < 3) or
                ('dove' not in phenotype.colour and 'platinum' not in phenotype.colour)))
            ):
            base = 'white'
            return [base, tortie, tabby, white, point]
        elif ('silver' in phenotype.silvergold and ('shaded' in phenotype.tabby or 'chinchilla' in phenotype.tabby)):
            base = 'silver shaded'
            return [base, tortie, tabby, white, point]
        elif (('o' not in genotype.sexgene or genotype.tortiepattern == ['revCRYPTIC']) or (genotype.ext[0] == 'ea' and ((self.moons > 11 and genotype.agouti[0] != 'a') or (self.moons > 23))) or (genotype.ext[0] == 'er' and self.moons > 23) or (genotype.ext[0] == 'ec' and self.moons > 0 and (genotype.agouti[0] != 'a' or self.moons > 5))) and not (genotype.silver[0] == 'I' and genotype.specialred in ['blue-red', 'cinnamon']):
            if genotype.dilute[0] == 'd' or genotype.pinkdilute[0] == 'dp' or (genotype.silver[0] == 'I' and genotype.specialred in ['cameo', 'merle']):
                base = 'cream'
            else:
                base = 'ginger'
        else:
            if ('O' in genotype.sexgene and not genotype.brindledbi and 'CRYPTIC' not in genotype.tortiepattern[0]) or 'bimetal' in phenotype.silvergold or (genotype.silver[0] == 'I' and genotype.specialred == 'merle'):
                tortie = True
            elif ('O' in genotype.sexgene and genotype.brindledbi):
                white = 'mid'
            
            if (genotype.eumelanin[0] == 'bl') or (phenotype.colour == 'sable' and genotype.pointgene[0] == 'cm') or 'cinnamon' in phenotype.maincolour or 'fawn' in phenotype.spritecolour:
                if 'fawn' in phenotype.spritecolour or genotype.dilute[0] == 'd' or genotype.pinkdilute[0] == 'dp':
                    base = 'fawn'
                else:
                    base = 'cinnamon'
            elif genotype.eumelanin[0] == 'b' or 'lilac' in phenotype.spritecolour:
                if 'lilac' in phenotype.spritecolour or genotype.dilute[0] == 'd' or genotype.pinkdilute[0] == 'dp':
                    base = 'lilac'
                else:
                    base = 'chocolate'
            else:
                if 'blue' in phenotype.spritecolour or genotype.dilute[0] == 'd' or genotype.pinkdilute[0] == 'dp':
                    base = 'blue'
                else:
                    base = 'black'
            
        if base in ['ginger', 'cream'] or (genotype.agouti[0] != "a" and genotype.ext[0] != "Eg") or (genotype.ext[0] not in ['Eg', 'E']) or 'light smoke' in phenotype.silvergold:
            sprite = phenotype.GetTabbySprite()
            if 'bar' in sprite or 'ghost' in sprite or 'chinchilla' in phenotype.tabby:
                tabby['pattern'] = 'ticked'
            elif sprite in ['marbled', 'classic']:
                tabby['pattern'] = 'blotched'
            elif 'braid' in sprite or 'mack' in sprite or 'pins' in sprite:
                tabby['pattern'] = 'mackerel'
            else:
                tabby['pattern'] = 'spotted'

            if 'smoke' in phenotype.silvergold or 'masked' in phenotype.silvergold or (('charcoal' in phenotype.tabtype or genotype.ruftype == 'low') and genotype.wbtype in ['low', 'medium']):
                tabby['type'] = 'dark'
            elif 'silver' in phenotype.silvergold or 'cameo' in phenotype.silvergold or 'bimetal' in phenotype.silvergold or genotype.brindledbi:
                tabby['type'] = 'silver'
            elif phenotype.silvergold:
                tabby['type'] = 'golden'
        
        if (genotype.white[1] in ['ws', 'wt'] and genotype.whitegrade > 7) or (self.moons < 6 and genotype.karp[0] == 'K'):
            white = 'high'
        elif genotype.white[1] in ['ws', 'wt'] or (genotype.white[0] in ['ws', 'wt'] and genotype.whitegrade > 4) or genotype.white[0] == 'wsal' or (self.moons > 12 and genotype.vitiligo) or genotype.karp[0] == 'K':
            white = 'mid'
        elif white != 'mid' and ((genotype.white[0] in ['ws', 'wt'] and genotype.whitegrade > 1) or genotype.white[0] == 'wg' or (genotype.vitiligo and self.moons > 5)) and genotype.white_pattern != "No":
            white = 'low'

        if genotype.pointgene[0] == 'cs' or 'masked' in phenotype.silvergold or (self.moons < 4 and genotype.fevercoat) or (self.moons > 3 and genotype.bleach[0] == 'lb'):
            point = 'colourpoint'
        elif genotype.pointgene == ['cb', 'cb'] or (genotype.pointgene == ['cm', 'cm'] and phenotype.colour != 'sable'):
            point = 'sepia'
            if base in ['ginger', 'cream']:
                point = 'none'
            elif base in ['fawn', 'cinnamon']:
                point = 'colourpoint'
        elif genotype.pointgene[0] == 'cb':
            point = 'mink'
            if base != 'black':
                point = 'colourpoint'

        return [base, tortie, tabby, white, point]

    def solid(self, base, tortie, tabby, white):
        possible_prefixes = self.all_prefixes[base]['tortie' if tortie else 'plain']['solid'][white + '_white']

        possible_prefixes += self.all_prefixes['general']['any']
        try:
            possible_prefixes += self.all_prefixes['general'][self.phenotype.length.replace('haired', 'hair')]
        except:
            pass
        if white in ['mid', 'high']:
            possible_prefixes += self.all_prefixes['general']['white_patches']
        if tortie:
            possible_prefixes += self.all_prefixes['general']['tortie']
        if tabby:
            possible_prefixes += self.all_prefixes['general'][tabby]
        filtered = deepcopy(possible_prefixes)
        filtered = np.setdiff1d(filtered, self.used_prefixes, True)
        try:
            filtered = np.setdiff1d(filtered, self.all_prefixes['filter_for'], True)

        if len(filtered) > 0:
            return choice(filtered)
        else:
            return choice(possible_prefixes)
    def tabby(self, base, tortie, tabby, white):
        possible_prefixes = self.all_prefixes[base]['tortie' if tortie else 'plain']['tabby'][tabby['pattern']]
        try:
            possible_prefixes = possible_prefixes[tabby['type']]
        except:
            possible_prefixes = possible_prefixes[tabby['regular']]

        if tabby['type'] != 'silver':
            possible_prefixes = possible_prefixes[white + '_white']

        possible_prefixes += self.all_prefixes[base]['tortie' if tortie else 'plain']['tabby']['general']
        try:
            possible_prefixes = possible_prefixes[tabby['type']]
        except:
            possible_prefixes = possible_prefixes[tabby['regular']]

        if tabby['type'] != 'silver':
            possible_prefixes = possible_prefixes[white + '_white']
        
        possible_prefixes += self.all_prefixes['general']['any']
        try:
            possible_prefixes += self.all_prefixes['general'][self.phenotype.length.replace('haired', 'hair')]
        except:
            pass
        if white in ['mid', 'high']:
            possible_prefixes += self.all_prefixes['general']['white_patches']
        if tortie:
            possible_prefixes += self.all_prefixes['general']['tortie']
        if tabby['pattern']:
            possible_prefixes += self.all_prefixes['general'][tabby['pattern']]
        filtered = deepcopy(possible_prefixes)
        filtered = np.setdiff1d(filtered, self.used_prefixes, True)
        try:
            filtered = np.setdiff1d(filtered, self.all_prefixes['filter_for'], True)

        if len(filtered) > 0:
            return choice(filtered)
        else:
            return choice(possible_prefixes)
    def point(self, base, tortie, point, white):
        possible_prefixes = self.all_prefixes[base]['tortie' if tortie else 'plain']['point']
        
        try:
            possible_prefixes = possible_prefixes[point]
        except:
            possible_prefixes = possible_prefixes['colourpoint']

        try:
            possible_prefixes = possible_prefixes[white + '_white']
        except:
            try:
                possible_prefixes = possible_prefixes['with_white']
            except:
                pass
        
        possible_prefixes += self.all_prefixes['general']['any']
        try:
            possible_prefixes += self.all_prefixes['general'][self.phenotype.length.replace('haired', 'hair')]
        except:
            pass
        if white in ['mid', 'high']:
            possible_prefixes += self.all_prefixes['general']['white_patches']
        if tortie:
            possible_prefixes += self.all_prefixes['general']['tortie']
        
        filtered = deepcopy(possible_prefixes)
        filtered = np.setdiff1d(filtered, self.used_prefixes, True)
        try:
            filtered = np.setdiff1d(filtered, self.all_prefixes['filter_for'], True)

        if len(filtered) > 0:
            return choice(filtered)
        else:
            return choice(possible_prefixes)

    def black(self, params):
        if params[4] != 'none':
        
        if params[2]['type'] == 'golden' and params[2]['pattern'] == 'ticked':
            return self.golden('golden shaded')

        pass
    def blue(self, params):
        pass
    def chocolate(self, params):
        pass
    def lilac(self, params):
        pass
    def cinnamon(self, params):
        pass
    def fawn(self, params):
        pass
    def red(self, params):
        pass
    def golden(self, pattern):
        
    def cream(self, params):
        pass
    def white(self, base):
        if base == 'silver shaded' and random() > 0.33:
            possible_prefixes = self.all_prefixes['silver shaded']
        else:
            possible_prefixes = self.all_prefixes['white']
        
        filtered = deepcopy(possible_prefixes)
        filtered = np.setdiff1d(filtered, self.used_prefixes, True)
        try:
            filtered = np.setdiff1d(filtered, self.all_prefixes['filter_for'], True)

        if len(filtered) > 0:
            return choice(filtered)
        else:
            return choice(possible_prefixes)