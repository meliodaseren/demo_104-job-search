speech = open('./dataset/trump_speech.txt', encoding = 'utf8')

# read_speech = speech.read()
# read_speech = speech.readlines()

print("--" * 50)
print("Type of speech %s" %(type(speech)))       # <class '_io.TextIOWrapper'>
# print("Type of read_speech %s" %(type(read_speech)))  # <class 'str'>
print("--" * 50)

# print(read_speech)

for line in speech:
    print(line.strip())
    print("=" * 50)

speech.close()