
import VariableDeclaration as vd
import Conditions as cond

#######################################
# LOSOWANIE KOLOROW DO DRAGOWANIA:


# Kopiuje kolory i losuje ich kolejnosc
KolTemp = []

for i in vd.Kolory:
    KolTemp[i] = vd.Kolory[i]

# Randomize array Kolory:
random.shuffle(KolTemp)

# zakladamy ze mamy atrybuty kol1, kol2 itd:
for i in KolTemp:
    cond.exp["kol"] = KolTemp[i]

##############
# DEBUG:
print "kol = ", cond.exp["kol"]
#######################################