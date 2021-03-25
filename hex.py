import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

long_sentence_length = 12
long_word_length = 12

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def lange_saetze(sentences):
	long_sentences = []

	for sentence in sentences:
		words = sentence.split()
		number_of_words = len(words)

		if number_of_words > long_sentence_length:
			long_sentences.append(sentence)

	return long_sentences

def lange_worte(words):
	long_words = []

	for word in words:
		if len(word) > long_word_length:
			long_words.append(word)

	return long_words

def passiv(sentences):
	passive_sentences = []
	
	passive_thingies = ["wird", "ist", "wurde", "war"]
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			if word in passive_thingies:
				passive_sentences.append(sentence)
				
	return passive_sentences

def fuellworte(words):
    filler_file = open("filler.txt", "r")
    filler_text = filler_file.read()
    german_filler_words = filler_text.replace(",","").split()
    
    filler_words = []
    for word in words:
        if word in german_filler_words:
            filler_words.append(word)
			
    return filler_words

def hex_warning(warning_type, text):
	if warning_type:
		print("\nWarnung: " + text)
		for item in warning_type:
			print(item)


print("Hex analysiert deinen Text")

f = open("text.txt", "r")
full_text = f.read()
sentences = split_into_sentences(full_text)
words = full_text.split()

hex_warning(lange_saetze(sentences), "Lange Sätze")
hex_warning(lange_worte(words), "Lange Wörter")
hex_warning(passiv(sentences), "Passiv (Steven King verachtet dich!)")
hex_warning(fuellworte(words), "Füllwörter")