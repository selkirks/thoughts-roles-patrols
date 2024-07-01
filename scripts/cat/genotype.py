from random import choice, randint, random
import json
from scripts.cat.breed_functions import breed_functions
from operator import xor
import math


class Genotype:
    def __init__(self, odds, ban_genes=True, spec=None):
        self.odds = odds
        self.ban_genes = ban_genes
        if spec:
            self.chimera = False
            self.chimerapattern = None
        else:
            a = randint(1, odds['chimera'])
            if a == 1:
                self.chimera = True
            else:
                self.chimera = False
            self.chimerapattern = None
        if self.chimera:
            self.chimerageno = Genotype(self.odds, self.ban_genes, 'chimera')
        else:
            self.chimerageno = None
        
        self.furLength = ""
        self.longtype = choice(['long', 'long', 'long', 'medium'])
        self.eumelanin = ["", ""]
        self.sexgene = ["", ""]
        self.specialred = None
        self.tortiepattern = None
        self.brindledbi = False
        self.gender = ""
        self.dilute = ""
        self.white = ["", ""]
        self.whitegrade = randint(1, 5)
        self.white_pattern = []
        self.vitiligo = False
        self.deaf = False
        self.pointgene = ["", ""]
        self.silver = ""
        self.agouti = ["", ""]
        self.mack = ""
        self.ticked = ""
        self.breakthrough = False

        self.wirehair = ["wh", "wh"]
        self.laperm = ["lp", "lp"]
        self.cornish = ["R", "R"]
        self.urals = ["Ru", "Ru"]
        self.tenn = ["Tr", "Tr"]
        self.fleece = ["Fc", "Fc"]
        self.sedesp = ["Hr", "Hr"]
        self.ruhr = ["hrbd", "hrbd"]
        self.ruhrmod = ""
        self.lykoi = ["Ly", "Ly"]

        self.pinkdilute = ["Dp", "Dp"]
        self.dilutemd = ["dm", "dm"]
        self.ext = ["E", "E"]
        self.corin = ["N", "N"]
        self.karp = ["k", "k"]
        self.bleach = ["Lb", "Lb"]
        self.ghosting = ["gh", "gh"]
        self.satin = ["St", "St"]
        self.glitter = ["Gl", "Gl"]

        self.curl = ["cu", "cu"]
        self.fold = ["fd", "fd"]
        self.manx = ["ab", "ab"]
        self.manxtype = choice(["long", "most", "most", "stubby", "stubby", "stubby", "stubby", "stubby", "stubby", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "stumpy", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "riser", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy", "rumpy"])
        self.kab = ["Kab", "Kab"]
        self.toybob = ["tb", "tb"]
        self.jbob = ["Jb", "Jb"]
        self.kub = ["kub", "kub"]
        self.ring = ["Rt", "Rt"]
        self.munch = ["mk", "mk"]
        self.poly = ["pd", "pd"]
        self.pax3 = ["NoDBE", "NoDBE"]

        self.wideband = ""
        self.wbtype = ""
        self.wbsum = 0

        self.rufousing = ""
        self.ruftype = ""
        self.rufsum = 0

        self.bengal = ""
        self.bengtype = ""
        self.bengsum = 0

        self.sokoke = ""
        self.soktype = ""
        self.soksum = 0

        self.spotted = ""
        self.spottype = ""
        self.spotsum = 0

        self.tickgenes = ""
        self.ticktype = ""
        self.ticksum = 0

        self.body_ranges = [1, 4, 9, 27, 9, 4, 1]
        self.height_ranges = [1, 4, 9, 36, 108, 36, 9, 2, 2, 1]

        def getindexes(m, size):
            inds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            
            for i in range(0, size):
                for j in range(0, i+1):
                    inds[i] += m[j]
            
            return inds
        self.body_indexes = getindexes(self.body_ranges, 7)
        self.height_indexes = getindexes(self.height_ranges, 10)

        self.body_value = 0
        self.height_value = 0
        self.shoulder_height = 0
        self.body_label = ""
        self.height_label = ""

        self.refraction = False
        self.pigmentation = False

        self.lefteye = ""
        self.righteye = ""
        self.lefteyetype = "Error"
        self.righteyetype = "Error"

        self.extraeye = None
        self.extraeyetype = ""
        self.extraeyecolour = ""

        self.breeds = {}
        self.somatic = {}

    def __getitem__(self, name):
        return getattr(self, name)
    
    def fromJSON(self, jsonstring):
        #jsonstring = json.loads(jsonstring)

        self.furLength = jsonstring["furLength"]
        self.eumelanin = jsonstring["eumelanin"]
        self.sexgene = jsonstring["sexgene"]
        self.tortiepattern = jsonstring["tortiepattern"]
        self.brindledbi = jsonstring["brindledbi"]

        self.specialred = jsonstring['specialred']
        self.chimera = jsonstring['chimera']
        self.chimerapattern = jsonstring['chimerapattern']
        if(jsonstring["chimerageno"]):
            self.chimerageno = Genotype(self.odds, self.ban_genes, 'chimera')
            self.chimerageno.fromJSON(jsonstring["chimerageno"])
        else:
            self.chimerageno = None    
        self.deaf = jsonstring['deaf']
        self.longtype = jsonstring["longtype"]

        self.gender = jsonstring["gender"]
        self.dilute = jsonstring["dilute"]
        self.white = jsonstring["white"]
        self.whitegrade = jsonstring["whitegrade"]
        self.vitiligo = jsonstring["vitiligo"]
        self.pointgene = jsonstring["pointgene"]
        self.silver = jsonstring["silver"]
        self.agouti = jsonstring["agouti"]
        self.mack = jsonstring["mack"]
        self.ticked = jsonstring["ticked"]
        self.breakthrough = jsonstring["breakthrough"]

        self.wirehair = jsonstring["wirehair"]
        self.laperm = jsonstring["laperm"]
        self.cornish = jsonstring["cornish"]
        self.urals = jsonstring["urals"]
        self.tenn = jsonstring["tenn"]
        self.fleece = jsonstring["fleece"]
        self.sedesp = jsonstring["sedesp"]
        self.ruhr = jsonstring["ruhr"]
        self.ruhrmod = jsonstring["ruhrmod"]
        self.lykoi = jsonstring["lykoi"]
    
        self.pinkdilute = jsonstring["pinkdilute"]
        self.dilutemd = jsonstring["dilutemd"]
        self.ext = jsonstring["ext"]
        try:
            self.corin = jsonstring["corin"]
        except:
            self.corin = jsonstring["sunshine"]
        self.karp = jsonstring["karp"]
        self.bleach = jsonstring["bleach"]
        self.ghosting = jsonstring["ghosting"]
        self.satin = jsonstring["satin"]
        self.glitter = jsonstring["glitter"]
    
        self.curl = jsonstring["curl"]
        self.fold = jsonstring["fold"]
        self.manx = jsonstring["manx"]
        self.manxtype = jsonstring["manxtype"]
        self.kab = jsonstring["kab"]
        self.toybob = jsonstring["toybob"]
        self.jbob = jsonstring["jbob"]
        self.kub = jsonstring["kub"]
        self.ring = jsonstring["ring"]
        self.munch = jsonstring["munch"]
        self.poly = jsonstring["poly"]
        try:
            self.pax3 = jsonstring["pax3"]
        except:
            self.pax3 = jsonstring['altai']
            for i in range(2):
                if self.pax3[i] == 'Al':
                    self.pax3[i] = 'DBEalt'
                else:
                    self.pax3[i] = 'NoDBE'

        self.wideband = jsonstring["wideband"]
        #self.wbtype = jsonstring["wbtype"]
        #self.wbsum = jsonstring["wbsum"]

        self.rufousing = jsonstring["rufousing"]
        #self.ruftype = jsonstring["ruftype"]
        #self.rufsum = jsonstring["rufsum"]

        self.bengal = jsonstring["bengal"]
        #self.bengtype = jsonstring["bengtype"]
        #self.bengsum = jsonstring["bengsum"]

        self.sokoke = jsonstring["sokoke"]
        #self.soktype = jsonstring["soktype"]
        #self.soksum = jsonstring["soksum"]

        self.spotted = jsonstring["spotted"]
        #self.spottype = jsonstring["spottype"]
        #self.spotsum = jsonstring["spotsum"]

        self.tickgenes = jsonstring["tickgenes"]
        #self.ticktype = jsonstring["ticktype"]
        #self.ticksum = jsonstring["ticksum"]

        self.refraction = jsonstring["refraction"]
        self.pigmentation = jsonstring["pigmentation"]

        self.lefteye = jsonstring["lefteye"]
        self.righteye = jsonstring["righteye"]
        self.lefteyetype = jsonstring["lefteyetype"]
        self.righteyetype = jsonstring["righteyetype"]
        
        self.extraeye = jsonstring["extraeye"]
        self.extraeyetype = jsonstring["extraeyetype"]
        self.extraeyecolour = jsonstring["extraeyecolour"]

        if len(str(self.refraction)) > 2:
            self.EyeConvert()

        try:
            self.breeds = json.loads(jsonstring["breeds"])
        except:
            self.breeds = {}
        try:
            self.somatic = json.loads(jsonstring["somatic"])
        except:
            self.somatic = {}
        
        try:
            self.body_value = jsonstring["body_type"]
            self.height_value = jsonstring["height"]
            self.shoulder_height = jsonstring["shoulder_height"]
        except:
            self.GenerateBody()

        self.GeneSort()
        self.PolyEval()
        self.EyeColourName()

    def toJSON(self):
        chimgen = None

        if self.chimerageno:
            chimgen = self.chimerageno.toJSON()

        return {
            "furLength": self.furLength,
            "longtype": self.longtype,
            "eumelanin": self.eumelanin,
            "sexgene" : self.sexgene,
            "specialred" : self.specialred,
            "tortiepattern" : self.tortiepattern,
            "brindledbi" : self.brindledbi,

            "chimera" : self.chimera,
            "chimerapattern" : self.chimerapattern,
            "chimerageno" : chimgen,

            "gender": self.gender,
            "dilute": self.dilute,
            "white" : self.white,
            "whitegrade" : self.whitegrade,
            "vitiligo" : self.vitiligo,
            "deaf" : self.deaf,
            "pointgene" : self.pointgene,
            "silver" : self.silver,
            "agouti" : self.agouti,
            "mack" : self.mack,
            "ticked" : self.ticked,
            "breakthrough" : self.breakthrough,

            "wirehair" : self.wirehair,
            "laperm" : self.laperm,
            "cornish" : self.cornish,
            "urals" : self.urals,
            "tenn" : self.tenn,
            "fleece" : self.fleece,
            "sedesp" : self.sedesp,
            "ruhr" : self.ruhr,
            "ruhrmod" : self.ruhrmod,
            "lykoi" : self.lykoi,

            "pinkdilute" : self.pinkdilute,
            "dilutemd" : self.dilutemd,
            "ext" : self.ext,
            "corin" : self.corin,
            "karp" : self.karp,
            "bleach" : self.bleach,
            "ghosting" : self.ghosting,
            "satin" : self.satin,
            "glitter" : self.glitter,

            "curl" : self.curl,
            "fold" : self.fold,
            "manx" : self.manx,
            "manxtype" : self.manxtype,
            "kab" : self.kab,
            "toybob" : self.toybob,
            "jbob" : self.jbob,
            "kub" : self.kub,
            "ring" : self.ring,
            "munch" : self.munch,
            "poly" : self.poly,
            "pax3" : self.pax3,

            "wideband" : self.wideband,
            "rufousing" : self.rufousing,
            "bengal" : self.bengal,
            "sokoke" : self.sokoke,
            "spotted" : self.spotted,
            "tickgenes" : self.tickgenes,
            "refraction" :self.refraction,
            "pigmentation" : self.pigmentation,
            
            "lefteye" : self.lefteye,
            "righteye" : self.righteye,
            "lefteyetype" :self.lefteyetype,
            "righteyetype" : self.righteyetype,
            
            "extraeye" : self.extraeye,
            "extraeyetype" :self.extraeyetype,
            "extraeyecolour" : self.extraeyecolour,

            "body_type" : self.body_value,
            "height" : self.height_value,
            "shoulder_height" : self.shoulder_height,

            "breeds" : json.dumps(self.breeds),
            "somatic" : json.dumps(self.somatic)
        }

    def Generator(self, special=None):
        if randint(1, self.odds["other_breed"]) == 1:
            return self.BreedGenerator(special)
        if self.chimera:
            self.chimerageno.Generator()
        
        a = randint(1, self.odds['vitiligo'])
        if a == 1:
            self.vitiligo = True
        
        self.GenerateBody()

        # FUR LENGTH
        
        a = randint(1, 4)

        if a == 1:
            self.furLength = ["L", "L"]
        elif a == 4:
            self.furLength = ["l", "l"]
        else:
            self.furLength = ["L", "l"]

        # EUMELANIN

        for i in range(2):
            if randint(1, 10) == 1:
                self.eumelanin[i] = "bl"
            elif randint(1, 5) == 1:
                self.eumelanin[i] = "b"
            else:
                self.eumelanin[i] = "B"

        # RED GENE

        if (random() < 0.5 and special != "fem") or special == "masc":
            self.sexgene = ["", "Y"]
            if randint(1, self.odds['XXX/XXY']) == 1:
                self.sexgene = ["", "", "Y"]
            
                for i in range(2):
                    if randint(1, 4) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            else:
                if randint(1, 4) == 1:
                    self.sexgene[0] = "O"
                else:
                    self.sexgene[0] = "o"
            self.gender = "tom"
        else:
            if randint(1, self.odds['XXX/XXY']) == 1:
                self.sexgene = ["", "", ""]
                for i in range(3):
                    if randint(1, 4) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            else:
                for i in range(2):
                    if randint(1, 4) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            self.gender = "molly"
        if 'o' in self.sexgene and 'O' in self.sexgene and randint(1, self.odds['brindled_bicolour'])==1:
            self.brindledbi = True 
        
        if(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'merle', 'merle', 'merle', 'merle', 'merle', 'blue-red', 'blue-tipped', 'blue-tipped', 'cinnamon'])

        # DILUTE

        a = randint(1, 4)

        if a == 1:
            self.dilute = ["D", "D"]
        elif a == 4:
            self.dilute = ["d", "d"]
        else:
            self.dilute = ["D", "d"]

        # WHITE

        for i in range(2):

            if randint(1, 100) == 1:
                self.white[i] = "wg"
            elif randint(1, 100) == 1:
                self.white[i] = "wt"
            elif randint(1, 100) == 1:
                self.white[i] = "wsal"
            elif randint(1, 20) == 1:
                self.white[i] = "W"
            elif randint(1, 2) == 1:
                self.white[i] = "ws"
            else:
                self.white[i] = "w"

        # ALBINO

        for i in range(2):
            a = randint(1, 100)
            b = randint(1, 100)
            c = randint(1, 10)
            d = randint(1, 5)

            if a == 1 and not self.ban_genes:
                self.pointgene[i] = "c"
            elif b == 1:
                self.pointgene[i] = "cm"
            elif c == 1:
                self.pointgene[i] = "cb"
            elif d == 1:
                self.pointgene[i] = "cs"
            else:
                self.pointgene[i] = "C"

        # SILVER

        a = randint(1, 100)

        if a == 1:
            self.silver = ["I", "I"]
        elif a < 12:
            self.silver = ["I", "i"]
        else:
            self.silver = ["i", "i"]

        # AGOUTI

        for i in range(2):
            a = randint(1, 100)
            b = randint(1, 2)
            if a == 1:
                self.agouti[i] = "Apb"
            elif b == 1:
                self.agouti[i] = "A"
            else:
                self.agouti[i] = "a"

        # MACKEREL

        a = randint(1, 4)

        if a == 1:
            self.mack = ["Mc", "Mc"]
        elif a == 4:
            self.mack = ["mc", "mc"]
        else:
            self.mack = ["Mc", "mc"]

        # TICKED

        a = randint(1, 25)

        if a == 1:
            self.ticked = ["Ta", "Ta"]
        elif a <= 6:
            self.ticked = ["Ta", "ta"]
            if randint(1, 25) == 1:
                self.breakthrough = True
        else:
            self.ticked = ["ta", "ta"]

        # YORK, WIREHAIR, LAPERM, CORNISH, URAL, TENN, FLEECE

        A = [0, 0, 0, 0, 0, 0, 0]
        
        for i in range(6):
            a = randint(1, 1600)
            A[i] = a
        
        if A[1] == 1:
            self.wirehair = ["Wh", "Wh"]
        elif A[1] <= 41:
            self.wirehair = ["Wh", "wh"]
        
        if A[2] == 1:
            self.laperm = ["Lp", "Lp"]
        elif A[2] <= 41:
            self.laperm = ["Lp", "lp"]
        
        if A[3] == 1:
            self.cornish = ["r", "r"]
        elif A[3] <= 41:
            self.cornish = ["R", "r"]
        
        if A[4] == 1:
            self.urals = ["ru", "ru"]
        elif A[4] <= 41:
            self.urals = ["Ru", "ru"]
        
        if A[5] == 1:
            self.tenn = ["tr", "tr"]
        elif A[5] <= 41:
            self.tenn = ["Tr", "tr"]
        
        if A[0] == 1:
            self.fleece = ["fc", "fc"]
        elif A[0] <= 41:
            self.fleece = ["Fc", "fc"]
            
        
        #SELKIRK/DEVON/HAIRLESS
    
        for i in range(2):
            a = randint(1, 100)
            b = randint(1, 40)
            c = randint(1, 40)

            if a == 1 and not self.ban_genes:
                self.sedesp[i] = "hr"
            elif b == 1:
                self.sedesp[i] = "re"
            elif c == 1:
                self.sedesp[i] = "Se"


        #ruhr + ruhrmod + lykoi

        a = randint(1, 10000)

        if a == 1 and not self.ban_genes:
            self.ruhr = ["Hrbd", "Hrbd"]
        elif a <= 101 and not self.ban_genes:
            self.ruhr = ["Hrbd", "hrbd"]
        
        a = randint(1, 4)

        if a == 1:
            self.ruhrmod = ["hi", "hi"]
        elif a == 4:
            self.ruhrmod = ["ha", "ha"]
        else:
            self.ruhrmod = ["hi", "ha"]

        a = randint(1, 10000)

        if a == 1 and not self.ban_genes:
            self.lykoi = ["ly", "ly"]
        elif a <= 101 and not self.ban_genes:
            self.lykoi = ["Ly", "ly"]

        # pinkdilute + dilutemd

        a = randint(1, 2500)

        if a == 1 and not self.ban_genes:
            self.pinkdilute = ["dp", "dp"]
        elif a <= 51 and not self.ban_genes:
            self.pinkdilute[1] = "dp"
        
        a = randint(1, 2500)

        if a == 1:
            self.dilutemd = ["Dm", "Dm"]
        elif a <= 51:
            self.dilutemd[0] = "Dm"

        # ext

        for i in range(2):
            a = randint(1, 50)
            b = randint(1, 40)
            c = randint(1, 40)
            d = randint(1, 40)

            if a == 1:
                self.ext[i] = "Eg"
            elif b == 1:
                self.ext[i] = "ec"
            elif c == 1:
                self.ext[i] = "er"
            elif d == 1:
                self.ext[i] = "ea"

        #sunshine

        for i in range(2):
            a = randint(1, 40)
            b = randint(1, 40)
            c = randint(1, 40)

            if a == 1:
                self.corin[i] = "sh" #sunSHine
            elif b == 1:
                self.corin[i] = "sg" #Siberian Gold / extreme sunshine
            elif c == 1:
                self.corin[i] = "fg" #Flaxen Gold
            else:
                self.corin[i] = "N" #No

        # karp + bleach + ghosting + satin + glitter

        for i in range(5):
            a = randint(1, 10000)
            A[i] = a

        if A[0] == 1:
            self.karp = ["K", "K"]
        elif A[0] <= 101:
            self.karp[0] = "K"

        if A[1] == 1:
            self.bleach = ["lb", "lb"]
        elif A[1] <= 101:
            self.bleach[1] = "lb"
        
        if A[2] == 1:
            self.ghosting = ["Gh", "Gh"]
        elif A[2] <= 101:
            self.ghosting[0] = "Gh"
        
        if A[3] == 1:
            self.satin = ["st", "st"]
        elif A[3] <= 101:
            self.satin[1] = "st"
        
        if A[4] == 1:
            self.glitter = ["gl", "gl"]
        elif A[4] <= 101:
            self.glitter[1] = "gl"

        # curl + fold

        a = randint(1, 2500)

        if a == 1:
            self.curl = ["Cu", "Cu"]
        elif a <= 51:
            self.curl[0] = "Cu"
        
        a = randint(1, 50)

        if a == 1 and not self.ban_genes:
            self.fold[0] = "Fd"


        #  manx + kab + toybob + jbob + kub + ring

        a = randint(1, 40)
        b = randint(1, 40)

        if a == 1:
            self.manx = ["Ab", "ab"]
        elif b == 1 and not self.ban_genes:
            self.manx = ["M", "m"]
        
        for i in range(5):
            a = randint(1, 1600)
            A[i] = a

        if A[0] == 1:
            self.kab = ["kab", "kab"]
        elif A[0] <= 41:
            self.kab[1] = "kab"
        
        if A[1] == 1:
            self.toybob = ["Tb", "Tb"]
        elif A[1] <= 41:
            self.toybob[0] = "Tb"

        if A[2] == 1:
            self.jbob = ["jb", "jb"]
        elif A[2] <= 41:
            self.jbob[1] = "jb"
        
        if A[3] == 1:
            self.kub = ["Kub", "Kub"]
        elif A[3] <= 41:
            self.kub[0] = "Kub"

        if A[4] == 1:
            self.ring = ["rt", "rt"]
        elif A[4] <= 41:
            self.ring[1] = "rt"
        
        # munch + poly + altai

        a = randint(1, 50)

        if a == 1 and not self.ban_genes:
            self.munch[0] = "Mk"
        
        a = randint(1, 100)

        if a == 1:
            self.poly = ["Pd", "Pd"]
        elif a <= 11:
            self.poly[0] = "Pd"
        
        a = randint(1, 25)

        if a == 1 and not self.ban_genes:
            self.pax3 = ['DBEalt', choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])]
        elif a <= 51:
            self.pax3[0] = choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])

        genes = ["2", "2", "1", "1", "1", "1", "1", "1", "0", "0"]

        self.wideband = ''
        self.rufousing = ''
        self.spotted = ''
        self.tickgenes = ''
        self.bengal = ''
        self.sokoke = ''
        self.refraction = ''
        self.pigmentation = ''
        
        for i in range(0, 8):
            self.wideband += choice(genes)
            self.wbsum += int(self.wideband[i])

        for i in range(0, 4):
            self.rufousing += choice(genes)
            self.rufsum += int(self.rufousing[i])

        genesspot = ["2", "1", "0"]

        for i in range(0, 4):
            self.spotted += choice(genesspot)
            self.spotsum += int(self.spotted[i])

        genesmild = ["2", "2", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.tickgenes += choice(genesmild)
            self.ticksum += int(self.tickgenes[i])

        for i in range(0, 4):
            self.bengal += choice(genesmild)
            self.bengsum += int(self.bengal[i])

        sokgenes = ["2", "2", "1", "1", "1", "1", "0", "0", "0"]

        for i in range(0, 4):
            self.sokoke += choice(sokgenes)
            self.soksum += int(self.sokoke[i])

        self.GeneSort()
        self.PolyEval()

        if randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.EyeColourFinder()

    def AltGenerator(self, special=None):
        if randint(1, self.odds["kittypet_breed"]) == 1:
            return self.BreedGenerator(special)
        
        if self.chimera:
            self.chimerageno.AltGenerator()
        a = randint(1, self.odds['vitiligo'])
        if a == 1:
            self.vitiligo = True
        
        self.GenerateBody()

        # FUR LENGTH

        a = randint(1, 4)

        if a == 1:
            self.furLength = ["L", "L"]
        elif a == 4:
            self.furLength = ["l", "l"]
        else:
            self.furLength = ["L", "l"]

        # EUMELANIN

        for i in range(2):
            if randint(1, 3) == 1:
                self.eumelanin[i] = "bl"
            elif randint(1, 2) == 1:
                self.eumelanin[i] = "b"
            else:
                self.eumelanin[i] = "B"

        # RED GENE

        if (randint(1, 2) == 1 and special != "fem") or special == "masc":
            self.sexgene = ["", "Y"]
            if randint(1, self.odds['XXX/XXY']) == 1:
                self.sexgene = ["", "", "Y"]
            
                for i in range(2):
                    if randint(1, 2) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            elif randint(1, 2) == 1:
                self.sexgene[0] = "O"
            else:
                self.sexgene[0] = "o"
            self.gender = "tom"
        else:
            if randint(1, self.odds['XXX/XXY']) == 1:
                self.sexgene = ["", "", ""]
                for i in range(3):
                    if randint(1, 2) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            else:
                for i in range(2):
                    if randint(1, 3) == 1:
                        self.sexgene[i] = "O"
                    else:
                        self.sexgene[i] = "o"
            self.gender = "molly"
        if 'o' in self.sexgene and 'O' in self.sexgene and randint(1, self.odds['brindled_bicolour'])==1:
            self.brindledbi = True 

        if(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'merle', 'merle', 'merle', 'merle', 'merle', 'blue-red', 'blue-tipped', 'blue-tipped', 'cinnamon'])
        # DILUTE

        a = randint(1, 4)

        if a == 1:
            self.dilute = ["D", "D"]
        elif a == 4:
            self.dilute = ["d", "d"]
        else:
            self.dilute = ["D", "d"]

        # WHITE

        for i in range(2):

            if randint(1, 25) == 1:
                self.white[i] = "wg"
            elif randint(1, 25) == 1:
                self.white[i] = "wt"
            elif randint(1, 25) == 1:
                self.white[i] = "wsal"
            elif randint(1, 20) == 1:
                self.white[i] = "W"
            elif randint(1, 2) == 1:
                self.white[i] = "ws"
            else:
                self.white[i] = "w"

        # ALBINO

        for i in range(2):
            a = randint(1, 25)
            b = randint(1, 25)
            c = randint(1, 10)
            d = randint(1, 5)

            if a == 1 and not self.ban_genes:
                self.pointgene[i] = "c"
            elif b == 1:
                self.pointgene[i] = "cm"
            elif c == 1:
                self.pointgene[i] = "cb"
            elif d == 1:
                self.pointgene[i] = "cs"
            else:
                self.pointgene[i] = "C"

        # SILVER

        a = randint(1, 25)

        if a == 1:
            self.silver = ["I", "I"]
        elif a < 7:
            self.silver = ["I", "i"]
        else:
            self.silver = ["i", "i"]

        # AGOUTI
    
        for i in range(2):
            a = randint(1, 20)
            b = randint(1, 2)
            if a == 1:
                self.agouti[i] = "Apb"
            elif b == 1:
                self.agouti[i] = "A"
            else:
                self.agouti[i] = "a"

        

        # MACKEREL

        a = randint(1, 4)

        if a == 1:
            self.mack = ["Mc", "Mc"]
        elif a == 4:
            self.mack = ["mc", "mc"]
        else:
            self.mack = ["Mc", "mc"]

        # TICKED

        a = randint(1, 25)

        if a == 1:
            self.ticked = ["Ta", "Ta"]
        elif a <= 6:
            self.ticked = ["Ta", "ta"]
            if randint(1, 25) == 1:
                self.breakthrough = True
        else:
            self.ticked = ["ta", "ta"]

        # YORK, WIREHAIR, LAPERM, CORNISH, URAL, TENN, FLEECE

        A = [0, 0, 0, 0, 0, 0, 0]
        
        for i in range(6):
            a = randint(1, 100)
            A[i] = a
        
        if A[1] == 1:
            self.wirehair = ["Wh", "Wh"]
        elif A[1] <= 21:
            self.wirehair = ["Wh", "wh"]
        
        if A[2] == 1:
            self.laperm = ["Lp", "Lp"]
        elif A[2] <= 21:
            self.laperm = ["Lp", "lp"]
        
        if A[3] == 1:
            self.cornish = ["r", "r"]
        elif A[3] <= 21:
            self.cornish = ["R", "r"]
        
        if A[4] == 1:
            self.urals = ["ru", "ru"]
        elif A[4] <= 21:
            self.urals = ["Ru", "ru"]
        
        if A[5] == 1:
            self.tenn = ["tr", "tr"]
        elif A[5] <= 21:
            self.tenn = ["Tr", "tr"]
        
        if A[0] == 1:
            self.fleece = ["fc", "fc"]
        elif A[0] <= 21:
            self.fleece = ["Fc", "fc"]
            
        
        #SELKIRK/DEVON/HAIRLESS
    
        for i in range(2):
            a = randint(1, 25)
            b = randint(1, 10)
            c = randint(1, 10)

            if a == 1 and not self.ban_genes:
                self.sedesp[i] = "hr"
            elif b == 1:
                self.sedesp[i] = "re"
            elif c == 1:
                self.sedesp[i] = "Se"


        #ruhr + ruhrmod + lykoi

        a = randint(1, 100)

        if a == 1 and not self.ban_genes:
            self.ruhr = ["Hrbd", "Hrbd"]
        elif a <= 21 and not self.ban_genes:
            self.ruhr = ["Hrbd", "hrbd"]
        
        a = randint(1, 4)

        if a == 1:
            self.ruhrmod = ["hi", "hi"]
        elif a == 4:
            self.ruhrmod = ["ha", "ha"]
        else:
            self.ruhrmod = ["hi", "ha"]

        a = randint(1, 100)

        if a == 1 and not self.ban_genes:
            self.lykoi = ["ly", "ly"]
        elif a <= 21 and not self.ban_genes:
            self.lykoi = ["Ly", "ly"]

        a = randint(1, 200)

        # pinkdilute + dilutemd

        a = randint(1, 125)

        if a == 1 and not self.ban_genes:
            self.pinkdilute = ["dp", "dp"]
        elif a <= 26 and not self.ban_genes:
            self.pinkdilute[1] = "dp"
        
        a = randint(1, 125)

        if a == 1:
            self.dilutemd = ["Dm", "Dm"]
        elif a <= 26:
            self.dilutemd[0] = "Dm"

        # ext

        for i in range(2):
            a = randint(1, 25)
            b = randint(1, 20)
            c = randint(1, 20)
            d = randint(1, 20)

            if a == 1:
                self.ext[i] = "Eg"
            elif b == 1:
                self.ext[i] = "ec"
            elif c == 1:
                self.ext[i] = "er"
            elif d == 1:
                self.ext[i] = "ea"

        #sunshine

        for i in range(2):
            a = randint(1, 20)
            b = randint(1, 20)
            c = randint(1, 20)

            if a == 1:
                self.corin[i] = "sh" #sunSHine
            elif b == 1:
                self.corin[i] = "sg" #Siberian Gold / extreme sunshine
            elif c == 1:
                self.corin[i] = "fg" #Flaxen Gold
            else:
                self.corin[i] = "N" #No

        # karp + bleach + ghosting + satin + glitter

        for i in range(5):
            a = randint(1, 250)
            A[i] = a

        if A[0] == 1:
            self.karp = ["K", "K"]
        elif A[0] <= 51:
            self.karp[0] = "K"

        if A[1] == 1:
            self.bleach = ["lb", "lb"]
        elif A[1] <= 51:
            self.bleach[1] = "lb"
        
        if A[2] == 1:
            self.ghosting = ["Gh", "Gh"]
        elif A[2] <= 51:
            self.ghosting[0] = "Gh"
        
        if A[3] == 1:
            self.satin = ["st", "st"]
        elif A[3] <= 51:
            self.satin[1] = "st"
        
        if A[4] == 1:
            self.glitter = ["gl", "gl"]
        elif A[4] <= 51:
            self.glitter[1] = "gl"

        # curl + fold

        a = randint(1, 625)

        if a == 1:
            self.curl = ["Cu", "Cu"]
        elif a <= 26:
            self.curl[0] = "Cu"
        
        a = randint(1, 25)

        if a == 1 and not self.ban_genes:
            self.fold[0] = "Fd"


        #  manx + kab + toybob + jbob + kub + ring

        a = randint(1, 40)
        b = randint(1, 40)

        if a == 1:
            self.manx = ["Ab", "ab"]
        elif b == 1 and not self.ban_genes:
            self.manx = ["M", "m"]
        
        for i in range(5):
            a = randint(1, 100)
            A[i] = a

        if A[0] == 1:
            self.kab = ["kab", "kab"]
        elif A[0] <= 21:
            self.kab[1] = "kab"
        
        if A[1] == 1:
            self.toybob = ["Tb", "Tb"]
        elif A[1] <= 21:
            self.toybob[0] = "Tb"

        if A[2] == 1:
            self.jbob = ["jb", "jb"]
        elif A[2] <= 21:
            self.jbob[1] = "jb"
        
        if A[3] == 1:
            self.kub = ["Kub", "Kub"]
        elif A[3] <= 21:
            self.kub[0] = "Kub"

        if A[4] == 1:
            self.ring = ["rt", "rt"]
        elif A[4] <= 21:
            self.ring[1] = "rt"
        
        # munch + poly + altai

        a = randint(1, 20)

        if a == 1 and not self.ban_genes:
            self.munch[0] = "Mk"
        
        a = randint(1, 25)

        if a == 1:
            self.poly = ["Pd", "Pd"]
        elif a <= 6:
            self.poly[0] = "Pd"
        
        a = randint(1, 125)

        if a == 1 and not self.ban_genes:
            self.pax3 = ['DBEalt', choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])]
        elif a <= 26:
            self.pax3[0] = choice(['DBEcel', 'DBEcel', 'DBEre', 'DBEalt', 'DBEalt'])

        self.wideband = ''
        self.rufousing = ''
        self.spotted = ''
        self.tickgenes = ''
        self.bengal = ''
        self.sokoke = ''
        self.refraction = ''
        self.pigmentation = ''
        
        genes = ["2", "2", "1", "1", "1", "1", "0", "0"]

        for i in range(0, 8):
            self.wideband += choice(genes)
            self.wbsum += int(self.wideband[i])

        for i in range(0, 4):
            self.rufousing += choice(genes)
            self.rufsum += int(self.rufousing[i])

        genesspot = ["2", "1", "0"]

        for i in range(0, 4):
            self.spotted += choice(genesspot)
            self.spotsum += int(self.spotted[i])
        
        genesmild = ["2", "2", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0"]

        for i in range(0, 4):
            self.tickgenes += choice(genesmild)
            self.ticksum += int(self.tickgenes[i])

        for i in range(0, 4):
            self.bengal += choice(genesmild)
            self.bengsum += int(self.bengal[i])

        sokgenes = ["2", "2", "1", "1", "1", "1", "0", "0", "0"]

        for i in range(0, 4):
            self.sokoke += choice(sokgenes)
            self.soksum += int(self.sokoke[i])

        self.GeneSort()

        self.PolyEval()

        if randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.EyeColourFinder()

    def BreedGenerator(self, special=None):
        if self.chimera:
            self.chimerageno.Generator()
        
        breedlist = [
            "Abyssinian", "American Bobtail", "American Curl", "American Shorthair", "American Burmese", "Aphrodite", 
                "Arabian Mau", "Asian/Burmese", "Australian Mist",
            "Bambino", "Bengal", "Birman", "Brazilian Shorthair", "British", 
            "Cheetoh", "Ceylon", "Chartreux", "Chausie", "Clippercat", "Cornish Rex",
            "Devon Rex", "Donskoy", 
            "Egyptian Mau", "European Shorthair", 
            "Foldex", 
            "Gaelic Fold", "German Longhair", "German Rex",
            "Havana", "Highlander", 
            "Japanese Bobtail", 
            "Kanaani", "Karelian Bobtail", "Khao Manee", "Kinkalow", "Korat", "Kurilian Bobtail",
            "Lambkin", "LaPerm", "Lin-Qing Lion cat", "Lykoi",
            "Mandalay/Burmese", "Maine Coon", "Manx", "Mekong Bobtail", "Munchkin", 
            "Napoleon", "New Zealand", "Norwegian Forest cat", 
            "Ocicat", "Oriental/Siamese", 
            "Persian/Exotic", "Peterbald", "Pixie-Bob", 
            "Ragamuffin", "Ragdoll", "Russian",
            "Savannah", "Selkirk Rex", "Serengeti", "Siberian", "Singapura", "Skookum", "Snowshoe", "Sokoke", "Sphynx",
            "Tennessee Rex", "Thai", "Tonkinese", "Toybob", "Toyger", "Turkish", 
            "Ural Rex"
        ]
        editedlist = [
            "Abyssinian", "American Bobtail", "American Curl", "American Shorthair", "American Burmese", "Aphrodite", 
                "Arabian Mau", "Asian/Burmese", "Australian Mist",
            "Bengal", "Birman", "Brazilian Shorthair", "British", 
            "Cheetoh", "Ceylon", "Chartreux", "Chausie", "Clippercat", "Cornish Rex",
            "Devon Rex", 
            "Egyptian Mau", "European Shorthair", 
            "German Longhair", "German Rex",
            "Havana", "Highlander", 
            "Japanese Bobtail", 
            "Kanaani", "Karelian Bobtail", "Khao Manee", "Korat", "Kurilian Bobtail",
            "LaPerm", "Lin-Qing Lion cat",
            "Mandalay/Burmese", "Maine Coon", "Mekong Bobtail", 
            "New Zealand", "Norwegian Forest cat", 
            "Ocicat", "Oriental/Siamese", 
            "Pixie-Bob", 
            "Ragamuffin", "Ragdoll", "Russian",
            "Savannah", "Selkirk Rex", "Serengeti", "Siberian", "Singapura", "Snowshoe", "Sokoke",
            "Tennessee Rex", "Thai", "Tonkinese", "Toybob", "Toyger", "Turkish", 
            "Ural Rex"
        ]
        if self.ban_genes:
            gen = breed_functions["generator"][choice(editedlist)]
        else:    
            gen = breed_functions["generator"][choice(breedlist)]

        self = gen(self, special)

        self.GeneSort()

        if self.body_value == 0:
            self.body_value = randint(self.body_indexes[2]+1, self.body_indexes[3])
        if self.height_value == 0:
            self.height_value = randint(self.height_indexes[3]+1, self.height_indexes[4])

        if randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()

        self.PolyEval()
        self.EyeColourFinder()

    def KitGenerator(self, par1, par2=None):
        try:
            par2 = par2.genotype
        except:
            par2 = par2
        
        for breed in par1.breeds:
            if par1.breeds[breed] >= 0.1:
                self.breeds[breed] = par1.breeds[breed] / 2 
        for breed in par2.breeds:
            if par2.breeds[breed] >= 0.1:
                if self.breeds.get(breed, False):
                    self.breeds[breed] += par2.breeds[breed] / 2
                else:
                    self.breeds[breed] = par2.breeds[breed] / 2 
        
        self.KitEyes(par1, par2)

        if self.chimera:
            self.chimerageno.KitGenerator(par1, par2)
    
        if randint(1, 5) == 1:
            self.whitegrade = par1.whitegrade
        elif randint(1, 5) == 1:
            self.whitegrade = par2.whitegrade

        if (par1.vitiligo and par2.vitiligo):
            a = randint(1, round((self.odds['vitiligo']/4)))
        elif(par1.vitiligo or par2.vitiligo):
            a = randint(1, round((self.odds['vitiligo']/2)))
        else:
            a = randint(1, self.odds['vitiligo'])

        if(a == 1):
            self.vitiligo = True    
        
        
        self.furLength = [choice(par1.furLength), choice(par2.furLength)]

        if self.furLength[0] == "l":
            x = self.furLength[1]
            self.furLength[1] = self.furLength[0]
            self.furLength[0] = x
        
        self.eumelanin = [choice(par1.eumelanin), choice(par2.eumelanin)]
        mum = ["", ""]
        pap = ["", "Y"]
        if not xor('Y' in par1.sexgene, 'Y' in par2.sexgene):
            if('Y' in par1.sexgene):
                if(randint(1, 2) == 1):
                    mum[0] = par1.sexgene[0]
                    mum[1] = mum[0]
                    pap[0] = par2.sexgene[0]
                else:
                    mum[0] = par2.sexgene[0]
                    mum[1] = mum[0]
                    pap[0] = par1.sexgene[0]
            else:
                if len(par1.sexgene) > 2:
                    mum[0] = par1.sexgene[0]
                    mum[1] = par1.sexgene[1]
                    mum.append(par1.sexgene[2])
                    pap[0] = par2.sexgene[0]
                elif len(par2.sexgene) > 2:
                    mum[0] = par2.sexgene[0]
                    mum[1] = par2.sexgene[1]
                    mum.append(par2.sexgene[2])
                    pap[0] = par2.sexgene[0]
                else:
                    if('O' in par1.sexgene and 'o' in par1.sexgene):
                        mum[0] = par1.sexgene[0]
                        mum[1] = par1.sexgene[1]
                        pap[0] = par2.sexgene[0]
                    elif ('O' in par2.sexgene and 'o' in par2.sexgene):
                        mum[0] = par2.sexgene[0]
                        mum[1] = par2.sexgene[1]
                        pap[0] = par1.sexgene[0]
                    else:
                        if(random() < 0.5):
                            mum[0] = par2.sexgene[0]
                            mum[1] = par2.sexgene[1]
                            pap[0] = par1.sexgene[0]
                        else:
                            mum[0] = par1.sexgene[0]
                            mum[1] = par1.sexgene[1]
                            pap[0] = par2.sexgene[0]

        elif('Y' in par1.sexgene):
            mum = par2.sexgene
            pap = par1.sexgene
        else:
            mum = par1.sexgene
            pap = par2.sexgene
        

        if randint(1, self.odds['XXX/XXY']) == 1:
            self.sexgene = ["", "", ""]
            if randint(1, 2) == 1:
                self.gender = 'tom'
                if randint(1, 2) == 1:
                    self.sexgene[0] = choice(mum)
                    self.sexgene[1] = pap[0]
                    self.sexgene[2] = 'Y'
                else:
                    self.sexgene[2] = 'Y'
                    if len(mum) < 3:
                        self.sexgene[0] = mum[0]
                        self.sexgene[1] = mum[1]
                    else:
                        a = randint(0, 2)
                        b = randint(0, 2)
                        while b == a:
                            b = randint(0, 2)
                        
                        self.sexgene[0] = mum[a]
                        self.sexgene[1] = mum[b]
            else:
                self.gender = 'molly'
                if len(mum) < 3:
                    self.sexgene[0] = mum[0]
                    self.sexgene[1] = mum[1]
                else:
                    a = randint(0, 2)
                    b = randint(0, 2)
                    while b == a:
                        b = randint(0, 2)
                    
                    self.sexgene[0] = mum[a]
                    self.sexgene[1] = mum[b]
                self.sexgene[2] = pap[0]

        else:
            if(randint(1, 2) == 1):
                self.sexgene[1] = "Y"
                self.sexgene[0] = choice(mum)
                self.gender = "tom"
            else:
                self.sexgene = [choice(mum), pap[0]]
                self.gender = "molly"
        
        
        if 'o' in self.sexgene and 'O' in self.sexgene and randint(1, self.odds['brindled_bicolour'])==1:
            self.brindledbi = True 
        
        if(par1.specialred and random() < 0.2):
            self.specialred = par1.specialred
        if(par2.specialred and random() < 0.2):
            self.specialred = par2.specialred
        elif(random() < 0.05):
            self.specialred = choice(['cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'cameo', 'merle', 'merle', 'merle', 'merle', 'merle', 'blue-red', 'blue-tipped', 'blue-tipped', 'cinnamon'])

        self.dilute = [choice(par1.dilute), choice(par2.dilute)]

        if(self.dilute[0] == "d"):
            x = self.dilute[1]
            self.dilute[1] = self.dilute[0]
            self.dilute[0] = x
        
        self.white = [choice(par1.white), choice(par2.white)]

        self.pointgene = [choice(par1.pointgene), choice(par2.pointgene)]

        self.silver = [choice(par1.silver), choice(par2.silver)]

        if(self.silver[0] == "i"):
            x = self.silver[1]
            self.silver[1] = self.silver[0]
            self.silver[0] = x

        self.agouti = [choice(par1.agouti), choice(par2.agouti)]

        self.mack = [choice(par1.mack), choice(par2.mack)]

        if(self.mack[0] == "mc"):
            x = self.mack[1]
            self.mack[1] = self.mack[0]
            self.mack[0] = x

        self.ticked = [choice(par1.ticked), choice(par2.ticked)]

        if self.ticked[0] != self.ticked[1] and randint(1, 25) == 1:
            self.breakthrough = True

        if(self.ticked[0] == "ta"):
            x = self.ticked[1]
            self.ticked[1] = self.ticked[0]
            self.ticked[0] = x

        self.wirehair = [choice(par1.wirehair), choice(par2.wirehair)]

        if(self.wirehair[0] == "wh"):
            x = self.wirehair[1]
            self.wirehair[1] = self.wirehair[0]
            self.wirehair[0] = x

        self.laperm = [choice(par1.laperm), choice(par2.laperm)]

        if(self.laperm[0] == "lp"):
            x = self.laperm[1]
            self.laperm[1] = self.laperm[0]
            self.laperm[0] = x

        self.cornish = [choice(par1.cornish), choice(par2.cornish)]

        if(self.cornish[0] == "r"):
            x = self.cornish[1]
            self.cornish[1] = self.cornish[0]
            self.cornish[0] = x

        self.urals = [choice(par1.urals), choice(par2.urals)]

        if(self.urals[0] == "ru"):
            x = self.urals[1]
            self.urals[1] = self.urals[0]
            self.urals[0] = x

        self.tenn = [choice(par1.tenn), choice(par2.tenn)]

        if(self.tenn[0] == "tr"):
            x = self.tenn[1]
            self.tenn[1] = self.tenn[0]
            self.tenn[0] = x

        self.fleece = [choice(par1.fleece), choice(par2.fleece)]

        if(self.fleece[0] == "fc"):
            x = self.fleece[1]
            self.fleece[1] = self.fleece[0]
            self.fleece[0] = x

        self.sedesp = [choice(par1.sedesp), choice(par2.sedesp)]

        self.ruhr = [choice(par1.ruhr), choice(par2.ruhr)]

        if(self.ruhr[0] == "hrbd"):
            x = self.ruhr[1]
            self.ruhr[1] = self.ruhr[0]
            self.ruhr[0] = x

        self.ruhrmod = [choice(par1.ruhrmod), choice(par2.ruhrmod)]

        if(self.ruhrmod[0] == "ha"):
            x = self.ruhrmod[1]
            self.ruhrmod[1] = self.ruhrmod[0]
            self.ruhrmod[0] = x

        self.lykoi = [choice(par1.lykoi), choice(par2.lykoi)]

        if(self.lykoi[0] == "ly"):
            x = self.lykoi[1]
            self.lykoi[1] = self.lykoi[0]
            self.lykoi[0] = x

        self.pinkdilute = [choice(par1.pinkdilute), choice(par2.pinkdilute)]

        if(self.pinkdilute[0] == "dp"):
            x = self.pinkdilute[1]
            self.pinkdilute[1] = self.pinkdilute[0]
            self.pinkdilute[0] = x

        self.dilutemd = [choice(par1.dilutemd), choice(par2.dilutemd)]

        if(self.dilutemd[0] == "dm"):
            x = self.dilutemd[1]
            self.dilutemd[1] = self.dilutemd[0]
            self.dilutemd[0] = x

        self.ext = [choice(par1.ext), choice(par2.ext)]
        self.corin = [choice(par1.corin), choice(par2.corin)]

        self.karp = [choice(par1.karp), choice(par2.karp)]

        if(self.karp[0] == "k"):
            x = self.karp[1]
            self.karp[1] = self.karp[0]
            self.karp[0] = x

        self.bleach = [choice(par1.bleach), choice(par2.bleach)]

        if(self.bleach[0] == "lb"):
            x = self.bleach[1]
            self.bleach[1] = self.bleach[0]
            self.bleach[0] = x

        self.ghosting = [choice(par1.ghosting), choice(par2.ghosting)]

        if(self.ghosting[0] == "gh"):
            x = self.ghosting[1]
            self.ghosting[1] = self.ghosting[0]
            self.ghosting[0] = x

        self.satin = [choice(par1.satin), choice(par2.satin)]

        if(self.satin[0] == "st"):
            x = self.satin[1]
            self.satin[1] = self.satin[0]
            self.satin[0] = x

        self.glitter = [choice(par1.glitter), choice(par2.glitter)]

        if(self.glitter[0] == "gl"):
            x = self.glitter[1]
            self.glitter[1] = self.glitter[0]
            self.glitter[0] = x

        self.curl = [choice(par1.curl), choice(par2.curl)]

        if(self.curl[0] == "cu"):
            self.curl[0] = self.curl[1]
            self.curl[1] = "cu"

        self.fold = [choice(par1.fold), choice(par2.fold)]

        if(self.fold[0] == "fd"):
            self.fold[0] = self.fold[1]
            self.fold[1] = "fd"
        
        self.manx = [choice(par1.manx), choice(par2.manx)]

        self.kab = [choice(par1.kab), choice(par2.kab)]

        if(self.kab[0] == "kab"):
            self.kab[0] = self.kab[1]
            self.kab[1] = "kab"

        self.toybob = [choice(par1.toybob), choice(par2.toybob)]

        if(self.toybob[0] == "tb"):
            self.toybob[0] = self.toybob[1]
            self.toybob[1] = "tb"

        self.jbob = [choice(par1.jbob), choice(par2.jbob)]

        if(self.jbob[0] == "jb"):
            self.jbob[0] = self.jbob[1]
            self.jbob[1] = "jb"

        self.kub = [choice(par1.kub), choice(par2.kub)]

        if(self.kub[0] == "kub"):
            self.kub[0] = self.kub[1]
            self.kub[1] = "kub"

        self.ring = [choice(par1.ring), choice(par2.ring)]

        if(self.ring[0] == "rt"):
            self.ring[0] = self.ring[1]
            self.ring[1] = "rt"

        self.munch = [choice(par1.munch), choice(par2.munch)]

        if(self.munch[0] == "mk"):
            self.munch[0] = self.munch[1]
            self.munch[1] = "mk"

        self.munch = [choice(par1.munch), choice(par2.munch)]

        if(self.munch[0] == "mk"):
            self.munch[0] = self.munch[1]
            self.munch[1] = "mk"

        self.poly = [choice(par1.poly), choice(par2.poly)]

        if(self.poly[0] == "pd"):
            self.poly[0] = self.poly[1]
            self.poly[1] = "pd"

        self.pax3 = [choice(par1.pax3), choice(par2.pax3)]

        if(self.pax3[0] == "NoDBE"):
            self.pax3[0] = self.pax3[1]
            self.pax3[1] = "NoDBE"

        self.wideband = ""
        for i in range(8):
            tempwb = 0
            if par1.wideband[i] == "2" or (par1.wideband[i] == "1" and randint(1, 2) == 1):
                tempwb = tempwb+1
                self.wbsum +=1
            if par2.wideband[i] == "2" or (par2.wideband[i] == "1" and randint(1, 2) == 1):
                tempwb = tempwb+1
                self.wbsum +=1
            self.wideband += str(tempwb)
        
        self.rufousing = ""
        for i in range(4):
            tempruf = 0
            if par1.rufousing[i] == "2" or (par1.rufousing[i] == "1" and randint(1, 2) == 1):
                tempruf = tempruf+1
                self.rufsum +=1
            if par2.rufousing[i] == "2" or (par2.rufousing[i] == "1" and randint(1, 2) == 1):
                tempruf = tempruf+1
                self.rufsum +=1
            self.rufousing += str(tempruf)
        
        self.bengal = ""
        for i in range(4):
            tempbeng = 0
            if par1.bengal[i] == "2" or (par1.bengal[i] == "1" and randint(1, 2) == 1):
                tempbeng = tempbeng+1
                self.bengsum +=1
            if par2.bengal[i] == "2" or (par2.bengal[i] == "1" and randint(1, 2) == 1):
                tempbeng = tempbeng+1
                self.bengsum +=1
            self.bengal += str(tempbeng)
        
        self.sokoke = ""
        for i in range(4):
            tempsok = 0
            if par1.sokoke[i] == "2" or (par1.sokoke[i] == "1" and randint(1, 2) == 1):
                tempsok = tempsok+1
                self.soksum +=1
            if par2.sokoke[i] == "2" or (par2.sokoke[i] == "1" and randint(1, 2) == 1):
                tempsok = tempsok+1
                self.soksum +=1
            self.sokoke += str(tempsok)
        
        self.spotted = ""
        for i in range(4):
            tempspot = 0
            if par1.spotted[i] == "2" or (par1.spotted[i] == "1" and randint(1, 2) == 1):
                tempspot = tempspot+1
                self.spotsum +=1
            if par2.spotted[i] == "2" or (par2.spotted[i] == "1" and randint(1, 2) == 1):
                tempspot = tempspot+1
                self.spotsum +=1
            self.spotted += str(tempspot)
        
        self.tickgenes = ""
        for i in range(4):
            temptick = 0
            if par1.tickgenes[i] == "2" or (par1.tickgenes[i] == "1" and randint(1, 2) == 1):
                temptick = temptick+1
                self.ticksum +=1
            if par2.tickgenes[i] == "2" or (par2.tickgenes[i] == "1" and randint(1, 2) == 1):
                temptick = temptick+1
                self.ticksum +=1
            self.tickgenes += str(temptick)

        wobble = randint(1, int(sum(self.body_ranges) / 20))
        self.body_value = randint(min(par1.body_value-wobble, par2.body_value-wobble), max(par1.body_value+wobble, par2.body_value+wobble))

        wobble = randint(1, int(sum(self.height_ranges) / 20))
        self.height_value = randint(min(par1.height_value-wobble, par2.height_value-wobble), max(par1.height_value+wobble, par2.height_value+wobble))

        if self.body_value < 1:
            self.body_value = 1
        if self.body_value > sum(self.body_ranges):
            self.body_value = sum(self.body_ranges)
        
        if self.height_value < 1:
            self.height_value = 1
        if self.height_value > sum(self.height_ranges):
            self.height_value = sum(self.height_ranges)


        if(randint(1, self.odds['random_mutation']) == 1):
            self.Mutate()

        self.GeneSort()

        if randint(1, self.odds['somatic_mutation']) == 1:
            self.GenerateSomatic()
        
        self.PolyEval()
        self.EyeColourFinder()

    def KitEyes(self, par1, par2):
        multipliers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        multipliers2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    
        def maths(par, m):
            m[par-1] += 10
            for i in range(0, par-1):
                m[i] += 10 / 5 ** (par-i-1);
            
            for i in range(par, 11):
                m[i] += 10 / 5 ** (i-par+1);
            return m
    
        multipliers = maths(par1.refraction, multipliers)
        multipliers = maths(par2.refraction, multipliers)
        multipliers = maths(math.floor((int(par1.refraction) + int(par2.refraction))/2), multipliers)
        multipliers2 = maths(par1.pigmentation, multipliers2)
        multipliers2 = maths(par2.pigmentation, multipliers2)
        multipliers2 = maths(math.floor((int(par1.pigmentation) + int(par2.pigmentation))/2), multipliers2)

        x = sum(multipliers)
        x2 = sum(multipliers2)

        def getindexes(m):
            inds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            
            for i in range(0, 11):
                for j in range(0, i+1):
                    inds[i] += m[j]
            
            return inds
        indexes = getindexes(multipliers)
        indexes2 = getindexes(multipliers2)

        num = random() * x
        self.refraction = next((n for n in range(len(indexes)) if num < indexes[n])) + 1
        num = random() * x2
        self.pigmentation = next((n for n in range(len(indexes2)) if num < indexes2[n])) + 1

    def GenerateBody(self):
        x = sum(self.body_ranges)

        self.body_value = randint(1, x)

        x = sum(self.height_ranges)

        self.height_value = randint(1, x)
 
    def PolyEval(self):
        wbtypes = ["low", "medium", "high", "shaded", "chinchilla"]
        ruftypes = ["low", "medium", "rufoused"]

        self.wbsum = 0
        self.rufsum = 0
        self.bengsum = 0
        self.soksum = 0
        self.spotsum = 0
        self.ticksum = 0
        
        for i in self.wideband:
            self.wbsum += int(i)
        for i in self.rufousing:
            self.rufsum += int(i)
        for i in self.bengal:
            self.bengsum += int(i)
        for i in self.sokoke:
            self.soksum += int(i)
        for i in self.spotted:
            self.spotsum += int(i)
        for i in self.tickgenes:
            self.ticksum += int(i)
        
        if self.wbsum < 6:
            self.wbtype = wbtypes[0]
        elif self.wbsum < 10:
            self.wbtype = wbtypes[1]
        elif self.wbsum < 12: 
            self.wbtype = wbtypes[2]
        elif self.wbsum < 14: 
            self.wbtype = wbtypes[3]
        else: 
            self.wbtype = wbtypes[4]

        if self.rufsum < 3: 
            self.ruftype = ruftypes[0]
        elif self.rufsum < 6: 
            self.ruftype = ruftypes[1]
        else:
            self.ruftype = ruftypes[2]

        spottypes = ["fully striped", "slightly broken", "broken stripes", "mostly broken", "spotted"]

        if self.spotsum < 1: 
            self.spottype = spottypes[0]
        elif self.spotsum < 3:
            self.spottype = spottypes[1]
        elif self.spotsum < 6:
            self.spottype = spottypes[2]
        elif self.spotsum < 8: 
            self.spottype = spottypes[3]
        else:
            self.spottype = spottypes[4]
        
        ticktypes = ["full barring", "reduced barring", "agouti"]

        if self.ticksum < 4: 
            self.ticktype = ticktypes[0]
        elif self.ticksum < 6:
            self.ticktype = ticktypes[1]
        else:
            self.ticktype = ticktypes[2]

        bengtypes = ["normal markings", "mild bengal", "full bengal"]

        if self.bengsum < 4: 
            self.bengtype = bengtypes[0]
        elif self.bengsum < 6:
            self.bengtype = bengtypes[1]
        else:
            self.bengtype = bengtypes[2]

        soktypes = ["normal markings", "mild fading", "full sokoke"]

        if self.soksum < 4: 
            self.soktype = soktypes[0]
        elif self.soksum < 6:
            self.soktype = soktypes[1]
        else:
            self.soktype = soktypes[2]

        body_types = ['snub-nosed', 'cobby', 'semi-cobby', 'intermediate', 'semi-oriental', 'oriental', 'wedge-faced']
        height_types = ['teacup', 'tiny', 'small', 'below average', 'average', 'above average', 'large', 'massive', 'giant', 'goliath']

        index = next((n for n in range(7) if self.body_value <= self.body_indexes[n]))
        self.body_label = body_types[index]

        index = next((n for n in range(10) if self.height_value <= self.height_indexes[n]))
        self.height_label = height_types[index]

        if self.shoulder_height > 0:
            return

        if index == 0:
            self.shoulder_height = 5.00
        elif index == 1:
            value = self.height_value - self.height_indexes[index-1]
            step = (6-5.01) / self.height_ranges[index]
            self.shoulder_height = 5.01 + value * (random() * step)
        elif index == 2:
            value = self.height_value - self.height_indexes[index-1]
            step = (7.5-6.01) / self.height_ranges[index]
            self.shoulder_height = 6.01 + value * (random() * step)
        elif index == 3:
            value = self.height_value - self.height_indexes[index-1]
            step = (8.99-7.51) / self.height_ranges[index]
            self.shoulder_height = 7.51 + value * (random() * step)
        elif index == 4:
            value = self.height_value - self.height_indexes[index-1]
            step = (11-9) / self.height_ranges[index]
            self.shoulder_height = 9 + value * (random() * step)
        elif index == 5:
            value = self.height_value - self.height_indexes[index-1]
            step = (12.5-11.01) / self.height_ranges[index]
            self.shoulder_height = 11.01 + value * (random() * step)
        elif index == 6:
            value = self.height_value - self.height_indexes[index-1]
            step = (14-12.51) / self.height_ranges[index]
            self.shoulder_height = 12.51 + value * (random() * step)
        elif index == 7:
            value = self.height_value - self.height_indexes[index-1]
            step = (14.99-14.01) / self.height_ranges[index]
            self.shoulder_height = 14.01 + value * (random() * step)
        elif index == 8:
            value = self.height_value - self.height_indexes[index-1]
            step = (15.99-15.00) / self.height_ranges[index]
            self.shoulder_height = 15.00 + value * (random() * step)
        elif index == 9:
            self.shoulder_height = 16.00
        
        if self.munch[0] == 'Mk':
            self.shoulder_height /= 1.75
        self.shoulder_height = round(self.shoulder_height, 2)
    
    def GeneSort(self):
        if self.eumelanin[0] == "bl":
            self.eumelanin[0] = self.eumelanin[1]
            self.eumelanin[1] = "bl"
        elif self.eumelanin[0] == "b" and self.eumelanin[1] != "bl":
            self.eumelanin[0] = self.eumelanin[1]
            self.eumelanin[1] = "b"

        if len(self.sexgene) > 2 and self.sexgene[2] == "O" and self.sexgene[0] == "o":
            self.sexgene[2] = self.sexgene[0]
            self.sexgene[0] = "O"
        elif len(self.sexgene) > 2 and self.sexgene[2] == "O":
            self.sexgene[2] = self.sexgene[1]
            self.sexgene[1] = "O"
        elif self.sexgene[1] == "O":
            self.sexgene[1] = self.sexgene[0]
            self.sexgene[0] = "O"

        if self.white[0] == "wg":
            self.white[0] = self.white[1]
            self.white[1] = "wg"
        elif self.white[0] == "wsal" and self.white[1] != "wg":
            self.white[0] = self.white[1]
            self.white[1] = "wsal"
        elif self.white[0] == "w" and self.white[1] != "wg" and self.white[1] != "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "w"
        elif self.white[0] == "wt" and self.white[1] != "wg" and self.white[1] != "w" and self.white[1] != "wsal":
            self.white[0] = self.white[1]
            self.white[1] = "wt"
        elif self.white[1] == "W":
            self.white[1] = self.white[0]
            self.white[0] = "W"

        if self.pointgene[0] == "c":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "c"
        elif self.pointgene[0] == "cm" and self.pointgene[1] != "c":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "cm"
        elif self.pointgene[0] == "cs" and self.pointgene[1] != "c" and self.pointgene[1] != "cm":
            self.pointgene[0] = self.pointgene[1]
            self.pointgene[1] = "cs"
        elif self.pointgene[1] == "C":
            self.pointgene[1] = self.pointgene[0]
            self.pointgene[0] = "C"

        if self.agouti[0] == "a":
            self.agouti[0] = self.agouti[1]
            self.agouti[1] = "a"
        elif self.agouti[0] == "Apb" and self.agouti[1] != "a":
            self.agouti[0] = self.agouti[1]
            self.agouti[1] = "Apb"

        if self.sedesp[0] == "re":
            self.sedesp[0] = self.sedesp[1]
            self.sedesp[1] = "re"
        elif self.sedesp[0] == "hr" and self.sedesp[1] != "re":
            self.sedesp[0] = self.sedesp[1]
            self.sedesp[1] = "hr"
        elif self.sedesp[1] == "Se":
            self.sedesp[1] = self.sedesp[0]
            self.sedesp[0] = "Se"

        if self.ext[0] == "ec":
            self.ext[0] = self.ext[1]
            self.ext[1] = "ec"
        elif self.ext[0] == "er" and self.ext[1] != "ec":
            self.ext[0] = self.ext[1]
            self.ext[1] = "er"
        elif self.ext[1] == "Eg":
            self.ext[1] = self.ext[0]
            self.ext[0] = "Eg"
        elif self.ext[1] == "E" and self.ext[0] != "Eg":
            self.ext[1] = self.ext[0]
            self.ext[0] = "E"

        if self.corin[0] == "sh":
            self.corin[0] = self.corin[1]
            self.corin[1] = "sh"
        elif self.corin[0] == "fg":
            self.corin[0] = self.corin[1]
            self.corin[1] = "fg"
        elif self.corin[0] == "sg":
            self.corin[0] = self.corin[1]
            self.corin[1] = "sg"

        if self.manx[1] == "M":
            self.manx[1] = self.manx[0]
            self.manx[0] = "M"
        elif self.manx[1] == "Ab":
            self.manx[1] = self.manx[0]
            self.manx[0] = "Ab"

    def EyeColourFinder(self):
        eyecolours = {
        "R1" : ["Citrine", "Golden Beryl", "Yellow", "Pale Golden", "Golden", "Amber", "Light Orange", "Orange", "Cinnabar", "Auburn", "Copper", "Ice Blue", "Pink"],
        "R2" : ["Pale Citrine", "Pale Yellow", "Lemon", "Deep Yellow", "Dull Golden", "Honey", "Pale Orange", "Burnt Orange", "Dark Orange", "Russet", "Dark Topaz", "Aquamarine", "Rose"],
        "R3" : ["Lemonade Yellow", "Straw Yellow", "Dandelion Yellow", "Banana Yellow", "Sunglow Yellow", "Copal", "Dull Orange", "Rust Orange", "Topaz", "Chocolate", "Burgundy", "Sky Blue", "Magenta"],
        "R4" : ["Light Celadon", "Pale Chartreuse", "Pear Green", "Brass Yellow", "Golden Green", "Butterscotch", "Dusty Orange", "Tawny", "Jasper", "Light Brown", "Earth", "Cyan", "Periwinkle"],
        "R5" : ["Light Jade", "Pale Lime", "Spring Bud", "Chartreuse", "Pale Hazel", "Yellow Hazel", "Golden Flourite", "Beaver Brown", "Sienna", "Chestnut", "Umber", "Baby Blue", "Violet"],
        "R6" : ["Light Flourite", "Mantis Green", "Spring Green", "Lime", "Green Tea", "Hazel", "Golden Brown", "Dark Copal", "Cinnamon", "Raw Umber", "Sepia", "Aqua", "Glass"],
        "R7" : ["Pale Emerald", "Apple Green", "Shamrock", "Lemon-Lime", "Peridot", "Antique Brass", "Dark Hazel", "Brown-Green", "Hazel Brown", "Bronze", "Bistre Brown", "Cerulean", "Moonstone"],
        "R8" : ["Malachite", "Olivine", "Pastel Green", "Bright Green", "Pistachio", "Dull Olive", "Murky Green", "Jungle Green", "Hemlock Green", "Thatch Green", "Muddy", "Ocean Blue", "Albino Ice Blue"],
        "R9" : ["Pale Turquoise", "Mint", "Snake Green", "Dark Lime", "Fern Green", "Dull Green", "Dark Fern Green", "Olive", "Tumbleweed Green", "Bronze Olive", "Deep Bronze", "Teal", "Albino Aquamarine"],
        "R10" : ["Turquoise", "Viridian", "Green Onion", "Leaf Green", "Green", "Sap Green", "Dark Leaf Green", "Forest Green", "Dark Peridot", "Seaweed Green", "Dark Olive", "Sapphire", "Albino Sky Blue"],
        "R11" : ["Deep Turquoise", "Amazonite", "Pine Green", "Deep Leaf Green", "Jade", "Emerald", "Deep Green", "Deep Forest Green", "Dark Green", "Dark Moss Green", "Black Olive", "Azure", "Albino Azure"]
        }
        sectoralindex = randint(0, 74)
        het2index = randint(0, 99)
        blueindex = 1
        hetindex = 1

        if not self.refraction:
            refgrade = choice([1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11])
            piggrade = choice([1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 10, 10, 11])
            self.refraction = refgrade
            self.pigmentation = piggrade
        else:
            refgrade = self.refraction
            piggrade = self.pigmentation

        if self.dilute[0] == "d" or self.pointgene == ["cb", "cb"] or self.pointgene == ["cb", "c"] or self.pointgene == ["cb", "cm"]:
            if randint(1, 5) == 1 and piggrade > 1:
                piggrade = piggrade - 1
        
        if self.pinkdilute[0] == 'dp' or self.pointgene == ["cb", "cs"] or piggrade == 0 or ((self.pointgene == ["cb", "cm"] or self.pointgene == ["cm", "cm"] or self.pointgene == ["cm", "c"]) and randint(1, 5) == 1):
            piggrade = 1

        def RefTypeFind(x, piggrade):
            y = eyecolours['R' + str(x)][piggrade-1]

            return y
        
        def SecondaryRefTypeFind(x, piggrade):
            y = ""

            piggrade = "P" + str(piggrade)
            if piggrade == "P12":
                piggrade = "blue"
            elif piggrade == "P13":
                piggrade = "albino"
                    
            y += "R" + str(x) + " ; " + str(piggrade) + ""
            return y
        
        


        if self.white == ["w","w"] or self.white == ["w", "wg"] or self.white == ["wg", "wg"]:
            blueindex = randint(0, 99)
        elif self.white == ["ws","w"] or self.white == ["ws","wg"] or self.white == ["wt", "w"] or self.white == ["wt", "wg"]:
            blueindex = randint(0, 74)
        elif self.white == ["ws","ws"] or self.white == ["wt", "wt"] or self.white == ["ws", "wt"]:
            blueindex = randint(0, 24)
        elif self.pointgene == ["cb","cs"]:
            blueindex = randint(0, 7)
        elif self.white[0] == "W":
            blueindex = randint(0, 14)
            if randint(1, 4) == 1 and blueindex == 0:
                self.deaf = True
        if self.white == ["W","W"]:
            blueindex = randint(0, 2)
            if randint(1, 4) < 4 and blueindex == 0:
                self.deaf = True
        
        if self.pointgene[0] == "cs" or ((self.pointgene == ["cb","cm"] or self.pointgene == ["cm","cm"] or self.pointgene == ["cm","c"]) and randint(0, 4)==0):
            blueindex = 0
        

        if 'ws' not in self.white and 'wt' not in self.white:
            hetindex = randint(0, 74)
        elif self.white[0] in ['ws', 'wt'] and self.white[1] not in ['ws', 'wt']:
            hetindex = randint(0, 24)
        elif self.white[0] in ['ws', 'wt'] and self.white[1] in ['ws', 'wt']:
            hetindex = randint(0, 14)
        elif self.white[0] == "W":
            hetindex = randint(0, 9)
            if randint(1, 10) == 1 and hetindex == 0:
                self.deaf = True
        if self.white == ["W","W"]:
            hetindex = randint(0, 2)
            if randint(1, 8) == 1 and hetindex == 0:
                self.deaf = True

        if self.pax3[0] != 'NoDBE':
            if 'NoDBE' not in self.pax3:
                blueindex = 0
                if (self.pax3 == ['DBEalt', 'DBEalt'] and random() < 0.33) or self.pax3 != ['DBEalt', 'DBEalt']:
                    self.deaf = True
            elif 'DBEre' not in self.pax3 and random() >= 0.1:
                if random() < 0.33:
                    blueindex = 0
                else:
                    hetindex = 0
            elif 'DBEre' in self.pax3:
                blueindex = 0
                if random() < 0.33:
                    self.deaf = True

        if het2index == 0 and not ("c" in self.pointgene and self.pointgene[0] != "C") and blueindex != 0:
            tempref = randint(1, 11)
            temppig = randint(1, 12)
            if randint(1, 2)==1:
                self.lefteye = RefTypeFind(tempref, temppig)
                self.righteye = RefTypeFind(refgrade, piggrade)

                self.lefteyetype = SecondaryRefTypeFind(tempref, temppig)
                self.righteyetype = SecondaryRefTypeFind(refgrade, piggrade)
            else:
                self.righteye = RefTypeFind(tempref, temppig)
                self.lefteye = RefTypeFind(refgrade, piggrade)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, piggrade)
                self.righteyetype = SecondaryRefTypeFind(tempref, temppig)
        else:
            self.righteye = RefTypeFind(refgrade, piggrade)
            self.lefteye = RefTypeFind(refgrade, piggrade)

            self.lefteyetype = SecondaryRefTypeFind(refgrade, piggrade)
            self.righteyetype = SecondaryRefTypeFind(refgrade, piggrade)

            if(sectoralindex == 0):
                self.extraeye = 'sectoral' + str(randint(1, 6))
            a = [randint(1, 11), randint(1, 12)]
            self.extraeyecolour = RefTypeFind(a[0], a[1])
            self.extraeyetype = SecondaryRefTypeFind(a[0], a[1])
                
                
            if "c" in self.pointgene and self.pointgene[0] != "C":
                self.lefteye = RefTypeFind(refgrade, 13)
                self.righteye = RefTypeFind(refgrade, 13)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, 13)
                self.righteyetype = SecondaryRefTypeFind(refgrade, 13)

                if het2index == 0:
                    tempref = randint(1, 11)
                    if randint(0, 1)==0:
                        self.lefteye = RefTypeFind(tempref, 13)
                        self.lefteyetype = SecondaryRefTypeFind(tempref, 13)
                    else:
                        self.righteye = RefTypeFind(tempref, 13)
                        self.righteyetype = SecondaryRefTypeFind(tempref, 13)
                elif self.extraeye:
                    self.extraeyecolour = RefTypeFind(a[0], 13)
                    self.extraeyetype = SecondaryRefTypeFind(a[0], 13)
            elif(blueindex == 0):
                self.lefteye = RefTypeFind(refgrade, 12)
                self.righteye = RefTypeFind(refgrade, 12)

                self.lefteyetype = SecondaryRefTypeFind(refgrade, 12)
                self.righteyetype = SecondaryRefTypeFind(refgrade, 12)

                if het2index == 0:
                    tempref = randint(1, 11)
                    if random() < 0.5:
                        self.lefteye = RefTypeFind(tempref, 12)
                        self.lefteyetype = SecondaryRefTypeFind(tempref, 12)
                    else:
                        self.righteye = RefTypeFind(tempref, 12)
                        self.righteyetype = SecondaryRefTypeFind(tempref, 12)
                elif self.extraeye:
                    self.extraeyecolour = RefTypeFind(a[0], 12)
                    self.extraeyetype = SecondaryRefTypeFind(a[0], 12)
            elif hetindex == 0:
                if random() < 0.5:
                    self.lefteye = RefTypeFind(refgrade, 12)
                    self.lefteyetype = SecondaryRefTypeFind(refgrade, 12)
                else:
                    self.righteye = RefTypeFind(refgrade, 12)
                    self.righteyetype = SecondaryRefTypeFind(refgrade, 12)

    def EyeColourName(self):
    
        eyecolours = {
        "R1" : ["Citrine", "Golden Beryl", "Yellow", "Pale Golden", "Golden", "Amber", "Light Orange", "Orange", "Cinnabar", "Auburn", "Copper", "Ice Blue", "Pink"],
        "R2" : ["Pale Citrine", "Pale Yellow", "Lemon", "Deep Yellow", "Dull Golden", "Honey", "Pale Orange", "Burnt Orange", "Dark Orange", "Russet", "Dark Topaz", "Aquamarine", "Rose"],
        "R3" : ["Lemonade Yellow", "Straw Yellow", "Dandelion Yellow", "Banana Yellow", "Sunglow Yellow", "Copal", "Dull Orange", "Rust Orange", "Topaz", "Chocolate", "Burgundy", "Sky Blue", "Magenta"],
        "R4" : ["Light Celadon", "Pale Chartreuse", "Pear Green", "Brass Yellow", "Golden Green", "Butterscotch", "Dusty Orange", "Tawny", "Jasper", "Light Brown", "Earth", "Cyan", "Periwinkle"],
        "R5" : ["Light Jade", "Pale Lime", "Spring Bud", "Chartreuse", "Pale Hazel", "Yellow Hazel", "Golden Flourite", "Beaver Brown", "Sienna", "Chestnut", "Umber", "Baby Blue", "Violet"],
        "R6" : ["Light Flourite", "Mantis Green", "Spring Green", "Lime", "Green Tea", "Hazel", "Golden Brown", "Dark Copal", "Cinnamon", "Raw Umber", "Sepia", "Aqua", "Glass"],
        "R7" : ["Pale Emerald", "Apple Green", "Shamrock", "Lemon-Lime", "Peridot", "Antique Brass", "Dark Hazel", "Brown-Green", "Hazel Brown", "Bronze", "Bistre Brown", "Cerulean", "Moonstone"],
        "R8" : ["Malachite", "Olivine", "Pastel Green", "Bright Green", "Pistachio", "Dull Olive", "Murky Green", "Jungle Green", "Hemlock Green", "Thatch Green", "Muddy", "Ocean Blue", "Albino Ice Blue"],
        "R9" : ["Pale Turquoise", "Mint", "Snake Green", "Dark Lime", "Fern Green", "Dull Green", "Dark Fern Green", "Olive", "Tumbleweed Green", "Bronze Olive", "Deep Bronze", "Teal", "Albino Aquamarine"],
        "R10" : ["Turquoise", "Viridian", "Green Onion", "Leaf Green", "Green", "Sap Green", "Dark Leaf Green", "Forest Green", "Dark Peridot", "Seaweed Green", "Dark Olive", "Sapphire", "Albino Sky Blue"],
        "R11" : ["Deep Turquoise", "Amazonite", "Pine Green", "Deep Leaf Green", "Jade", "Emerald", "Deep Green", "Deep Forest Green", "Dark Green", "Dark Moss Green", "Black Olive", "Azure", "Albino Azure"]
        }

        def setup(eyestring):
            eye = eyestring.split(' ; ')
            ref = eye[0]
            pig = int(eye[1].replace("albino", '13').replace('blue', '12').replace('P', ''))
            return eyecolours[ref][pig-1]
        self.lefteye = setup(self.lefteyetype)
        self.righteye = setup(self.righteyetype)
        if self.extraeyecolour != '':
            self.extraeyecolour = setup(self.extraeyetype)

    def EyeConvert(self):
        refsum = 0
        pigsum = 0
        refgrade = 1
        piggrade = 1

        for i in self.refraction:
            refsum += int(i)
        for i in self.pigmentation:
            pigsum += int(i)
            
        if refsum == 0:
            refgrade = 1
        elif refsum <= 1:
            refgrade = 2
        elif refsum <= 3:
            refgrade = 3
        elif refsum <= 5:
            refgrade = 4
        elif refsum <= 7:
            refgrade = 5
        elif refsum <= 10:
            refgrade = 6
        elif refsum <= 12:
            refgrade = 7
        elif refsum <= 14:
            refgrade = 8
        elif refsum <= 16:
            refgrade = 9
        elif refsum < 18:
            refgrade = 10
        else:
            refgrade = 11

        if pigsum == 0:
            piggrade = 1
        elif pigsum <= 1:
            piggrade = 2
        elif pigsum <= 3:
            piggrade = 3
        elif pigsum <= 5:
            piggrade = 4
        elif pigsum <= 7:
            piggrade = 5
        elif pigsum <= 10:
            piggrade = 6
        elif pigsum <= 12:
            piggrade = 7
        elif pigsum <= 14:
            piggrade = 8
        elif pigsum <= 16:
            piggrade = 9
        elif pigsum < 18:
            piggrade = 10
        else:
            piggrade = 11

        self.refraction = refgrade
        self.pigmentation = piggrade

    def ShowGenes(self):
        self.PolyEval()
        self.Cat_Genes = [self.furLength, self.eumelanin, self.sexgene, self.dilute, self.white, self.pointgene, self.silver,
                     self.agouti, self.mack, self.ticked]
        self.Fur_Genes = [self.wirehair, self.laperm, self.cornish, self.urals, self.tenn, self.fleece, self.sedesp, self.ruhr, self.ruhrmod, self.lykoi]
        self.Other_Colour = [self.pinkdilute, self.dilutemd, self.ext, self.corin, self.karp, self.bleach, self.ghosting, self.satin, self.glitter]
        self.Body_Genes = [self.curl, self.fold, self.manx, self.kab, self.toybob, self.jbob, self.kub, self.ring, self.munch, self.poly, self.pax3]
        self.Polygenes = ["Rufousing:", self.rufousing, self.ruftype, "Bengal:", self.bengal, self.bengtype, "Sokoke:", self.sokoke, self.soktype, "Spotted:", self.spotted, self.spottype, "Ticked:", self.tickgenes, self.ticktype]
        self.Polygenes2 = ["Wideband:", self.wideband, self.wbtype, "Refraction:", self.refraction, "Pigmentation:", self.pigmentation]

        return self.Cat_Genes, "Other Fur Genes: ", self.Fur_Genes, "Other Colour Genes: ", self.Other_Colour, "Body Mutations: ", self.Body_Genes, "Polygenes: ", self.Polygenes, self.Polygenes2
    
    def Mutate(self):
        print("MUTATION!")
        wheremutation = ["body", "furtype", "furtype", "othercoat", "othercoat", "othercoat", "maincoat", "maincoat", "maincoat", "maincoat", "maincoat", "maincoat"]
        where = choice(wheremutation)

        if where == 'body':
            self.Bodymutation()
        elif where == 'furtype':
            self.FurTypemutation()
        elif where == 'othercoat':
            self.OtherCoatmutation()
        else:
            self.MainCoatmutation()

    def Bodymutation(self):
        whichgene = ["curl", "fold", "manx", "karel", "kuril", "toybob", "japanese", "ringtail", "munchkin", "polydactyl", "polydactyl", "polydactyl", "polydactyl"]
        
        if self.ban_genes:
            whichgene.remove("fold")
            whichgene.remove("munchkin")
        
        which = choice(whichgene)

        if(which == "curl"):
            if(self.curl[0] == 'cu'):
                self.curl[0] = 'Cu'
            elif(self.curl[1] == 'cu'):
                self.curl[1] = 'Cu'
            else:
                self.Mutate()
        elif(which == 'fold'):
            if(self.fold[0] == 'fd'):
                self.fold[0] = 'Fd'
            elif(self.fold[1] == 'fd'):
                self.fold[1] = 'Fd'
            else:
                self.Mutate()
        elif(which == 'manx'):
            if(self.manx[0] == 'm' or self.manx[0] == 'ab'):
                if(random() < 0.34) and not self.ban_genes:
                    self.manx[0] = 'M'
                else:
                    self.manx[0] = 'Ab'
            if(self.manx[1] == 'm' or self.manx[1] == 'ab'):
                if(random() < 0.34) and not self.ban_genes:
                    self.manx[1] = 'M'
                else:
                    self.manx[1] = 'Ab'
            else:
                self.Mutate()
        elif(which == 'japanese'):
            if(self.jbob[1] == 'Jb'):
                self.jbob[1] = 'jb'
            elif(self.jbob[0] == 'Jb'):
                self.jbob[0] = 'jb' 
            else:
                self.Mutate()
        elif(which == 'toybob'):
            if(self.toybob[0] == 'tb'):
                self.toybob[0] = 'Tb'
            elif(self.toybob[1] == 'tb'):
                self.toybob[1] = 'Tb'
            else:
                self.Mutate()
        elif(which == 'karel'):
            if(self.kab[1] == 'Kab'):
                self.kab[1] = 'kab'
            elif(self.kab[0] == 'Kab'):
                self.kab[0] = 'kab'
            else:
                self.Mutate()
        elif(which == 'kuril'):
            if(self.kub[0] == 'kub'):
                self.kub[0] = 'Kub'
            elif(self.kub[1] == 'kub'):
                self.kub[1] = 'Kub'
            else:
                self.Mutate()
        elif(which == 'ringtail'):
            if(self.ring[1] == 'Rt'):
                self.ring[1] = 'rt'
            elif(self.ring[0] == 'Rt'):
                self.ring[0] = 'rt'
            else:
                self.Mutate()
        elif(which == 'munchkin'):
            if(self.munch[0] == 'mk'):
                self.munch[0] = 'Mk'
            elif(self.munch[1] == 'mk'):
                self.munch[1] = 'Mk'
            else:
                self.Mutate()
        else:
            if(self.poly[0] == 'pd'):
                self.poly[0] = 'Pd'
            elif(self.poly[1] == 'pd'):
                self.poly[1] = 'Pd'
            else:
                self.Mutate()
        
        print(which)
    
    def FurTypemutation(self):
        whichgene = ["wirehair", "laperm", "cornish", "urals", "tennessee", "fleecy", "sedesp", "sedesp", "sedesp", "lykoi", "russian"]
        
        if self.ban_genes:
            whichgene.remove("lykoi")
            whichgene.remove("russian")

        which = choice(whichgene)

        if(which == 'wirehair'):
            if(self.wirehair[0] == 'wh'):
                self.wirehair[0] = 'Wh'
            elif(self.wirehair[1] == 'wh'):
                self.wirehair[1] = 'Wh'
            else:
                self.Mutate()
        elif(which == 'laperm'):
            if(self.laperm[0] == 'lp'):
                self.laperm[0] = 'Lp'
            elif(self.laperm[1] == 'lp'):
                self.laperm[1] = 'Lp'
            else:
                self.Mutate()
        elif(which == 'cornish'):
            if(self.cornish[1] == 'R'):
                self.cornish[1] = 'r'
            elif(self.cornish[0] == 'R'):
                self.cornish[0] = 'r'
            else:
                self.Mutate()
        elif(which == 'urals'):
            if(self.urals[1] == 'Ru'):
                self.urals[1] = 'ru'
            elif(self.urals[0] == 'Ru'):
                self.urals[0] = 'ru'
            else:
                self.Mutate()
        elif(which == 'tennessee'):
            if(self.tenn[1] == 'Tr'):
                self.tenn[1] = 'tr'
            elif(self.tenn[0] == 'Tr'):
                self.tenn[0] = 'tr'
            else:
                self.Mutate()
        elif(which == 'fleecy'):
            if(self.fleece[1] == 'Fc'):
                self.fleece[1] = 'fc'
            elif(self.fleece[0] == 'Fc'):
                self.fleece[0] = 'fc'
            else:
                self.Mutate()
        elif(which == 'sedesp'):
            if('Hr' not in self.sedesp):
                self.Mutate()
            if(random() < 0.34):
                if(self.sedesp[0] == 'Hr'):
                    self.sedesp[0] = 'Se'
                else:
                    self.sedesp[1] = 'Se'
            else:
                if(self.sedesp[1] == 'Hr'):
                    if(random() < 0.25) and not self.ban_genes:
                        self.sedesp[1] = 'hr'
                    else:
                        self.sedesp[1] = 're'
                else:
                    if(random() < 0.25) and not self.ban_genes:
                        self.sedesp[0] = 'hr'
                    else:
                        self.sedesp[0] = 're'
        elif(which == 'lykoi'):
            if(self.lykoi[1] == 'Ly'):
                self.lykoi[1] = 'ly'
            elif(self.lykoi[0] == 'Ly'):
                self.lykoi[0] = 'ly'
            else:
                self.Mutate()
        else:
            if(self.ruhr[0] == 'Hr'):
                self.ruhr[0] = 'Hrbd'
            elif(self.ruhr[1] == 'Hr'):
                self.ruhr[1] = 'Hrbd'
            else:
                self.Mutate()
        print(which)

    def OtherCoatmutation(self):
        whichgene = ["dilute mod", "pinkdilute", "extention", "corin", "karpati", "bleaching", "ghosting", "satin", "glitter"]

        if self.ban_genes:
            whichgene.remove("pinkdilute")

        which = choice(whichgene)

        if(which == 'pinkdilute'):
            if(self.pinkdilute[1] == 'Dp'):
                self.pinkdilute[1] = 'dp'
            elif(self.pinkdilute[0] == 'Dp'):
                self.pinkdilute[0] = 'dp'
            else:
                self.Mutate()
        elif(which == 'dilute mod'):
            if(self.dilutemd[0] == 'dm'):
                self.dilutemd[0] = 'Dm'
            elif(self.dilutemd[1] == 'dm'):
                self.dilutemd[1] = 'Dm'
            else:
                self.Mutate()
        elif(which == 'extention'):
            if('E' not in self.ext):
                self.Mutate()
            elif(self.ext[1] == 'E'):
                self.ext[1] = choice(['ea', 'er', 'ec'])
            else:
                self.ext[0] = choice(['ea', 'er', 'ec'])
        elif(which == 'corin'):
            if(self.corin[1] == 'N'):
                self.corin[1] = choice(['sh', 'sg', 'fg'])
            elif(self.corin[0] == 'N'):
                self.corin[0] = choice(['sh', 'sg', 'fg'])
            else:
                self.Mutate()
        elif(which == 'karpati'):
            if(self.karp[0] == 'k'):
                self.karp[0] = 'K'
            elif(self.karp[1] == 'k'):
                self.karp[1] = 'K'
            else:
                self.Mutate()
        elif(which == 'bleaching'):
            if(self.bleach[1] == 'Lb'):
                self.bleach[1] = 'lb'
            elif(self.bleach[0] == 'Lb'):
                self.bleach[0] = 'lb'
            else:
                self.Mutate()
        elif(which == 'ghosting'):
            if(self.ghosting[0] == 'gh'):
                self.ghosting[0] = 'Gh'
            elif(self.ghosting[1] == 'gh'):
                self.ghosting[1] = 'Gh'
            else:
                self.Mutate()
        elif(which == 'satin'):
            if(self.satin[1] == 'St'):
                self.satin[1] = 'st'
            elif(self.satin[0] == 'St'):
                self.satin[0] = 'st'
            else:
                self.Mutate()
        elif(which == 'glitter'):
            if(self.glitter[1] == 'Gl'):
                self.glitter[1] = 'gl'
            elif(self.glitter[0] == 'Gl'):
                self.glitter[0] = 'gl'
            else:
                self.Mutate()
        print(which)
    
    def MainCoatmutation(self):
        whichgene = ["furlength", "black", "red", "dilute", "KIT", "albino", "silver", "agouti", "mackerel", "ticked", 'DBE']
        which = choice(whichgene)

        if(which == 'furlength'):
            if(self.furLength[1] == 'L'):
                self.furLength[1] = 'l'
            elif(self.furLength[0] == 'L'):
                self.furLength[0] = 'l'
            else:
                self.Mutate()
        elif(which == 'black'):
            if(self.eumelanin[0] == 'bl'):
                self.Mutate()
            elif(self.eumelanin[1] == 'B'):
                self.eumelanin[1] = 'b'
            elif(self.eumelanin == ['b', 'bl']):
                self.eumelanin[0] = 'bl'
            elif(self.eumelanin == ['b', 'b']):
                self.eumelanin[1] = 'bl'
            elif(self.eumelanin == ['B', 'bl']):
                self.eumelanin[0] = 'b'
            else:
                if(random() < 0.5):
                    self.eumelanin[0] = 'b'
                else:
                    self.eumelanin[1] = 'bl'
        elif(which == 'red'):
            if('o' not in self.sexgene):
                self.Mutate()
            if(self.sexgene[0] == 'o'):
                self.sexgene[0] = 'O'
            elif(self.sexgene[1] == 'o'):
                self.sexgene[1] = 'O'
            else:
                self.sexgene[2] = 'O'
        elif(which == 'dilute'):
            if(self.dilute[1] == 'D'):
                self.dilute[1] = 'd'
            elif(self.dilute[0] == 'D'):
                self.dilute[0] = 'd'
            else:
                self.Mutate()
        elif(which == 'KIT'):
            if('w' not in self.white):
                self.Mutate()
            elif(random() < 0.34):
                if(self.white[0] == 'w'):
                    self.white[0] = 'W'
                else:
                    self.white[1] = 'W'
            elif(random() < 0.2):
                if(self.white[1] == 'w'):
                    self.white[1] = choice(['wg', 'wsal'])
                else:
                    self.white[0] = choice(['wg', 'wsal'])
            else:
                if(self.white[0] == 'w'):
                    self.white[0] = choice(['wt', 'ws', 'ws', 'ws', 'ws'])
                else:
                    self.white[1] = choice(['wt', 'ws', 'ws', 'ws', 'ws'])
        elif(which == 'albino'):
            if('C' not in self.pointgene):
                self.Mutate()
            elif(self.pointgene[1] == 'C'):
                self.pointgene[1] = choice([choice(['c', 'cm']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb'])])
                if self.ban_genes:
                    self.pointgene[1] = choice(['cm', choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb'])])
            else:
                self.pointgene[0] = choice([choice(['c', 'cm']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb'])])
                if self.ban_genes:
                    self.pointgene[0] = choice(['cm', choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb']), choice(['cs', 'cb'])])
        elif(which == 'silver'):
            if(self.silver[0] == 'i'):
                self.silver[0] = 'I'
            elif(self.silver[1] == 'i'):
                self.silver[1] = 'I'
            else:
                self.Mutate()
        elif(which == 'agouti'):
            if(self.agouti[0] == 'A'):
                self.agouti[0] = 'a'
            elif(self.agouti[1] == 'A'):
                self.agouti[1] = 'a'
            else:
                self.Mutate()
        elif(which == 'mackerel'):
            if(self.mack[1] == 'Mc'):
                self.mack[1] = 'mc'
            elif(self.mack[0] == 'Mc'):
                self.mack[0] = 'mc'
            else:
                self.Mutate()
        elif(which == 'ticked'):
            if(self.ticked[0] == 'ta'):
                self.ticked[0] = 'Ta'
            elif(self.ticked[1] == 'ta'):
                self.ticked[1] = 'Ta'
            else:
                self.Mutate()
        else:
            if(self.pax3[0] == 'NoDBE'):
                self.pax3[0] = choice(['DBEcel', 'DBEre', 'DBEalt'])
            elif(self.pax3[1] == 'NoDBE'):
                self.pax3[1] = choice(['DBEcel', 'DBEre', 'DBEalt'])
            else:
                self.Mutate()
        print(which)
    
    def GenerateSomatic(self):
        self.somatic["base"] = choice(['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail', 
                                    'underbelly1', 'right front bicolour2', 'left front bicolour2', 
                                    'right back bicolour2', 'left back bicolour2'])

        possible_mutes = {
        "furtype" : ["wirehair", "laperm", "cornish", "urals", "tenn", "fleece", "sedesp"],
        "other" : ["pinkdilute", "ext", "corin", "karp"],
        "main" : ["eumelanin", "sexgene", "dilute", "white", "pointgene", "silver", "agouti"]
        }

        for gene in possible_mutes["furtype"]:
            if gene in ['wirehair', 'laperm', 'sedesp']:
                if self[gene][0] in ['Wh', 'Lp', 'Se', 'hr', 're']:
                    possible_mutes["furtype"].remove(gene)
            try:
                if self[gene][0] in ['r', 'ru', 'tr', 'fc']:
                    possible_mutes["furtype"].remove(gene)
                elif self[gene][1] in ['R', 'Ru', 'Tr', 'Fc']:
                    possible_mutes["furtype"].remove(gene)
            except:
                continue
        for gene in possible_mutes["other"]:
            if gene == 'corin' and (self.agouti[0] == 'a' or self.ext[0] == 'Eg'):
                possible_mutes["other"].remove(gene)
                continue
            elif gene in ['ext', 'karp', 'ghosting']:
                if self[gene][0] in ['Eg', 'K', 'Gh']:
                    possible_mutes["other"].remove(gene)
                    continue
            if self[gene][0] in ['dp', 'ec', 'ea', 'er', 'sh', 'sg', 'fg', 'lb', 'st', 'gl']:
                possible_mutes["other"].remove(gene)
            elif self[gene][1] in ['Dp', 'E', 'N', 'Lb', 'St', 'Gl']:
                possible_mutes["other"].remove(gene)
        for gene in possible_mutes["main"]:
            if gene in ['mack', 'ticked', 'silver'] and (self.agouti[0] == 'a' or self.ext[0] == 'Eg'):
                possible_mutes["main"].remove(gene)
                continue
            elif gene == 'agouti' and self.ext[0] == 'Eg':
                possible_mutes["main"].remove(gene)
                continue
            elif gene in ['sexgene', 'white']:
                if self[gene][0] in ['O', 'W', 'ws', 'wt']:
                    possible_mutes["main"].remove(gene)
                    continue
            if self[gene][0] in ['b', 'bl', 'd', 'wg', 'wsal', 'cs', 'cb', 'cm', 'c', 'Apb', 'a']:
                possible_mutes["main"].remove(gene)
            elif self[gene][1] in ['B', 'D', 'w', 'C', 'A']:
                possible_mutes["main"].remove(gene)
        
        whichgene = ['furtype', 'other', 'main', 'other', 'main', 'main']
        if self.white[0] == 'W':
            whichgene = ['furtype']
        for cate in whichgene:
            if len(possible_mutes[cate]) == 0:
                whichgene.remove(cate);
        if len(whichgene) > 0:
            self.somatic["gene"] = choice(possible_mutes[choice(whichgene)])

        
        if self.white[1] in ['ws', 'wt'] and self.somatic["base"] not in ['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail']:
            self.somatic["base"] = choice(['Somatic/leftface', 'Somatic/rightface', 'Somatic/tail'])
        if self.somatic["gene"] in possible_mutes["furtype"]:
            self.somatic["base"] = "Somatic/tail"
        
        alleles = {
            "wirehair" : ['Wh'],
            "laperm" : ['Lp'],
            "cornish" : ['r'],
            "urals" : ['ru'],
            "tenn" : ['tr'],
            "fleece" : ['fc'],
            "sedesp" : ['Se'],

            'pinkdilute' : ['dp'],
            "ext" : ['Eg', 'ec', 'er', 'ea'],
            "sunshine" : ['sh', 'sg', 'fg'],
            "karp" : ['K'],
            "bleach" : ['lb'],
            "ghosting" : ['Gh'],

            'eumelanin' : ['b', 'bl'],
            'sexgene' : ['O'],
            "dilute" : ['d'],
            "white" : ['W', 'wsal'],
            "pointgene" : ['cb', 'cs', 'cm', 'c'],
            "silver" : ['I'],
            "agouti" : ['Apb', 'a']
        }

        self.somatic["allele"] = choice(alleles[self.somatic['gene']])

    def FormatSomatic(self):
        body = {
            "Somatic/leftface" : "face",
            "Somatic/rightface" : "face",
            "Somatic/tail" : 'tail',
            "underbelly1" : 'underbelly',
            'right front bicolour2' : 'front leg', 
            'left front bicolour2' : 'front leg', 
            'right back bicolour2' : 'back leg', 
            'left back bicolour2' : 'back leg'
        }
        if not self.somatic.get('gene', False):
            return ""

        return self.somatic['gene'] + ' mutated to \'' + self.somatic['allele'] + "\' on " + body[self.somatic['base']]





