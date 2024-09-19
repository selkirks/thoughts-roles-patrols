from .genotype import *
from .phenotype import *
from random import choice, random
from operator import xor

class Namer():
    def __init__ (self, used_prefixes=[]):
        self.used_prefixes = used_prefixes

    def start(self, genotype: Genotype, phenotype: Phenotype, chimera_pheno = None, moons=0):
        self.genotype = genotype
        self.phenotype = phenotype
        self.moons = moons

        if genotype:
            params = self.parse_chimera() if genotype.chimera else self.get_categories(genotype, phenotype)

            print(params)
            print(genotype.ShowGenes())
            print(genotype.tortiepattern)
            print(genotype.specialred)

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
        
        if set_one[1] or set_two[1] or xor(set_one[0] in ['red', 'cream'], set_two[0] in ['red', 'cream']):
            tortie = True

        if set_one[3] == 'high' or (self.moons == 0 and set_one[4] == 'colourpoint'):
            white = 'high'
        elif set_one[3] == 'mid' or set_two[3] == 'high' or set_one[1] == 'white' or set_two[1] in ['white', 'silver shaded'] or (self.moons == 0 and set_two[4] == 'colourpoint'):
            white = 'mid'
        elif set_one[3] == 'low' or set_two[3] == 'mid':
            white = 'low'

        #mixing solid + tabby or different base-colours changes tabby pattern to blotched
        if set_one[0] != set_two[0] and set_one[0] not in ['red', 'cream'] and set_two[0] not in ['red', 'cream']:
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
        elif (('o' not in genotype.sexgene or genotype.tortiepattern == ['revCRYPTIC']) or (genotype.ext[0] == 'ea' and ((moons > 11 and genotype.agouti[0] != 'a') or (moons > 23))) or (genotype.ext[0] == 'er' and moons > 23) or (genotype.ext[0] == 'ec' and moons > 0 and (genotype.agouti[0] != 'a' or moons > 5))) and not (genotype.silver[0] == 'I' and genotype.specialred in ['blue-red', 'cinnamon']):
            if genotype.dilute[0] == 'd' or genotype.pinkdilute[0] == 'dp' or (genotype.silver[0] == 'I' and genotype.specialred in ['cameo', 'merle']):
                base = 'cream'
            else:
                base = 'red'
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
            
        if base in ['red', 'cream'] or (genotype.agouti[0] != "a" and genotype.ext[0] != "Eg") or (genotype.ext[0] not in ['Eg', 'E']) or 'light smoke' in phenotype.silvergold:
            sprite = phenotype.GetTabbySprite()
            if 'bar' in sprite or 'ghost' in sprite:
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
        
        if genotype.white[1] in ['ws', 'wt'] and genotype.whitegrade > 7:
            white = 'high'
        elif genotype.white[1] in ['ws', 'wt'] or (genotype.white[0] in ['ws', 'wt'] and genotype.whitegrade > 4) or genotype.white[0] == 'wsal':
            white = 'mid'
        elif white != 'mid' and ((genotype.white[0] in ['ws', 'wt'] and genotype.whitegrade > 1) or genotype.white[0] == 'wg') and genotype.white_pattern != "No":
            white = 'low'

        if genotype.pointgene[0] == 'cs' or 'masked' in phenotype.silvergold:
            point = 'colourpoint'
        elif genotype.pointgene == ['cb', 'cb'] or (genotype.pointgene == ['cm', 'cm'] and phenotype.colour != 'sable'):
            point = 'sepia'
            if base in ['red', 'cream']:
                point = 'none'
            elif base in ['fawn', 'cinnamon']:
                point = 'colourpoint'
        elif genotype.pointgene[0] == 'cb':
            point = 'mink'
            if base != 'black':
                point = 'colourpoint'

        return [base, tortie, tabby, white, point]

    def solid(self):
        pass
    def tabby(self):
        pass
    def point(self):
        pass
    def black(self):
        pass
    def blue(self):
        pass
    def chocolate(self):
        pass
    def lilac(self):
        pass
    def cinnamon(self):
        pass
    def fawn(self):
        pass
    def red(self):
        pass
    def cream(self):
        pass
    def white(self):
        pass