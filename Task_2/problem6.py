#!/usr/bin/env python3

# sentence = input("Enter a sentence: ")

# words = sentence.split()       
# reversed_words = words[::-1]   

# result = " ".join(reversed_words)

# print("Reversed sentence: " + result)



sentence = input("Enter a sentence: ")

words = []
word = ""

for ch in sentence:
    if ch != " ":
        word += ch
    else:
        words.append(word)
        word = ""

if word != "":
    words.append(word)

reversed_words = []
for i in range(len(words) - 1, -1, -1):
    reversed_words.append(words[i])

result = ""
for i in range(len(reversed_words)):
    result += reversed_words[i]
    if i != len(reversed_words) - 1:
        result += " "

print("Reversed sentence: " + result)