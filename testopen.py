speech = open('./dataset/donald_trump.txt', encoding = 'utf8')

read_speech = speech.read()

print(type(speech))       # <class '_io.TextIOWrapper'>
print(type(read_speech))  # <class 'str'>

print(read_speech)

speech.close()