def sm2(grade, repetition: int, easiness: float, interval: int):
	if grade >= 3:  # Correct response
		if repetition == 0:
			interval = 1
		elif repetition == 1:
			interval = 6
		else:
			interval = round(interval * easiness)
		repetition += 1
	else:  # Incorrect response
		repetition = 0
		interval = 1

	easiness = easiness + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
	if easiness < 1.3:
		easiness = 1.3

	return repetition, easiness, interval
