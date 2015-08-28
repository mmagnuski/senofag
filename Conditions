#################################################
# InLine6 (from 'BlockProc1' --> 'TrialProc1'):
#################################################

print "\n"
print "======"
print "ChoiceType: ", ChoiceType
print "Target: ", Target
print "Target RESP: ", Target.RESP, \n

# =============================
# Sprawdzamy czy jest odpowiedz
if Target.RESP = "":
	Effect = grey
	print "brak odpowiedzi"
else

	# ===========================
	# Sprawdzamy czy jest cued i
	# niepoprawne
	if ChoiceType = "Cued" and \
		Target = "target_left.png" and \
		Target.RESP = "l":
				
			Effect = grey
			print "cued i niepoprawne"
			
				
	elif ChoiceType = "Cued" and \
			Target = "target_right.png" and \
			Target.RESP = "d":
				
				Effect = grey
				print "cued i niepoprawne"
	else
		
			# Wiemy juz ze odpowiedz jest poprawna albo dowolna
			Effect = "Effect"
			
			#(rozbiłem ten pkt na 2: comp, a poniżej incomp)
			if Prime = "prime_left.png" and \
				Target.RESP = "d": 
					
					Effect = left_comp #czy dalej?
					print "left compatible"
					print "left_comp: ", left_comp
					
			elif Prime = "prime_right.png" and \
				Target.RESP = "l":
					
					Effect = right_comp
					print "right compatible"
					print "right_comp: ", right_comp
					
			elif Prime = "prime_left.png" and \
				Target.RESP = "l": 
					
					Effect = right_incomp 
					print "right incompatible"
					print "right_incomp: ", right_incomp
					
			elif Prime = "prime_right.png" and \
				Target.RESP = "d": 
					
					Effect = left_incomp
					print "left incompatible"
					print "left_incomp: ", left_incomp
					
			End if
			
			
			
			# ===========================
			# Sprawdzamy czy jest neutral
			if TrialType = "neut":
				
				print "neutral"
				
				if Target.RESP = "l":
					
					Effect = right_neut
					print "right_neut: ", right_neut
					
				elif Target.RESP = "d":
				
					Effect = left_neut
					print "left_neut: ", left_neut	
