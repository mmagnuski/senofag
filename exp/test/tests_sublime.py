#############
# to mozna potem wywalic:

from psychopy import core, visual, event, monitors
import os

PTH = os.path.dirname(os.path.abspath(__file__))
os.chdir(PTH)

#############

#################################################
# InLine6 (from 'BlockProc1' --> 'TrialProc1'):
#################################################

# To mozna potem pobierac z innego pliku:

exp = dict()
exp["ChoiceType"] = []
exp["Target"] = []
exp["Target.RESP"] = []
exp["Effect"] = []
exp["Prime"] = []
exp["TrialType"] = []


#################################################
# DEBUG info
print "\n"
print "======"
print "ChoiceType: ", exp["ChoiceType"]
print "Target: ", exp["Target"]
print "Target RESP: ", exp["Target.RESP"], "\n"

# =============================
import stim      # potem zmienic 
import VariableDeclaration as vd

# Sprawdzamy czy jest odpowiedz
if exp["Target.RESP"] == "":
	exp["Effect"] = stim.stim["grey"]
	#print "brak odpowiedzi"
else:

	# ===========================
	# Sprawdzamy czy jest cued i
	# niepoprawne
	if exp["ChoiceType"] == "Cued" and \
		exp["Target"] == stim.stim["tleft"] and \
		exp["Target.RESP"] == "l":
				
			exp["Effect"] = stim.stim["grey"]
			#print "cued i niepoprawne"
			
				
	elif exp["ChoiceType"] == "Cued" and \
			exp["Target"] == stim.stim["tright"] and \
			exp["Target.RESP"] == "d":
				
				exp["Effect"] == stim.stim["grey"]
				#print "cued i niepoprawne"
	else:
		
			# Wiemy juz ze odpowiedz jest poprawna albo dowolna
			
			#(rozbilem ten pkt na 2: comp, a ponizej incomp)
			if exp["Prime"] == stim.stim["pleft"] and \
				exp["Target.RESP"] == "d": 
					
					exp["Effect"] == vd.left_comp
					#print "left compatible"
					#print "left_comp: ", vd.left_comp
					
			elif exp["Prime"] == "prime_right.png" and \
				exp["Target.RESP"] == "l":
					
					exp["Effect"] == vd.right_comp
					#print "right compatible"
					#print "right_comp: ", vd.right_comp
					
			elif exp["Prime"] == "prime_left.png" and \
				exp["Target.RESP"] == "l": 
					
					exp["Effect"] == vd.right_incomp 
					#print "right incompatible"
					#print "right_incomp: ", vd.right_incomp
					
			elif exp["Prime"] == "prime_right.png" and \
				exp["Target.RESP"] == "d": 
					
					exp["Effect"] == vd.left_incomp
					#print "left incompatible"
					#print "left_incomp: ", vd.left_incomp
			
			
			
			# ===========================
			# Sprawdzamy czy jest neutral
			if exp["TrialType"] == "neut":
				
				#print "neutral"
				
				if exp["Target.RESP"] == "l":
					
					exp["Effect"] == vd.right_neut
					#print "right_neut: ", vd.right_neut
					
				elif exp["Target.RESP"] == "d":
				
					exp["Effect"] == vd.left_neut
					#print "left_neut: ", vd.left_neut
print "Everything OK"    