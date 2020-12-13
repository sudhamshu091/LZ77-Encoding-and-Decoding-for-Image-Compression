import re
import numpy as np
from PIL import Image
searchWindowSize = 0
previewWindowSize = 0

def longest_common_substring(s1, s2):
    maxLongest = 0
    offset = 0
    for i in range(0, len(s1)):
        longest = 0
        if ((i == len(s1) - len(s2) - 2)):
            break
        for j in range(0, len(s2)):
            if (i+j < len(s1)):
                if s1[i+j] == s2[j]:
                    longest = longest + 1
                    if (maxLongest < longest):
                        maxLongest = longest
                        offset = i
                else:
                    break
            else:
                break
    return maxLongest, offset

def encode_lz77(text, searchWindowSize, previewWindowSize):
    encodedNumbers = []
    encodedSizes = []
    encodedLetters = []
    i = 0
    while i < len(text):
        if i < previewWindowSize:
            encodedNumbers.append(0)
            encodedSizes.append(0)
            encodedLetters.append(text[i])
            i = i + 1
        else:
            previewString = text[i:i+previewWindowSize]
            searchWindowOffset = 0
            if (i < searchWindowSize):
                searchWindowOffset = i
            else:
                searchWindowOffset = searchWindowSize
            searchString = text[i - searchWindowOffset:i]
            result = longest_common_substring(searchString + previewString, previewString) # searchString + prevString, prevString
            nextLetter = ''
            if (result[0] == len(previewString)):
                if (i + result[0] == len(text)):
                    nextLetter = ''
                else:
                    nextLetter = text[i+previewWindowSize]
            else:
                nextLetter = previewString[result[0]]
            if (result[0] == 0):
                encodedNumbers.append(0)
                encodedSizes.append(0)
                encodedLetters.append(nextLetter)
            else:
                encodedNumbers.append(searchWindowOffset - result[1])
                encodedSizes.append(result[0])
                encodedLetters.append(nextLetter)
            i = i + result[0] + 1
    return encodedNumbers, encodedSizes, encodedLetters

def decode_lz77(encodedNumbers, encodedSizes, encodedLetters):
    i = 0
    decodedString = []
    while i < len(encodedNumbers):
        if (encodedNumbers[i] == 0):
            decodedString.append(encodedLetters[i])
        else:
            currentSize = len(decodedString)
            for j in range(0, encodedSizes[i]):
                decodedString.append(decodedString[currentSize-encodedNumbers[i]+j])
            decodedString.append(encodedLetters[i])
        i = i+1
    return decodedString


print("LZ77 Compression Algorithm")
print("=================================================================")
h = int(input("Enter 1 if you want to input an colour image file, 2 for default gray scale case:"))
if h == 1:
    file = input("Enter the filename:")
    my_string = np.asarray(Image.open(file),np.uint8)
    sudhi = my_string
    shape = my_string.shape
    print ("Enetered string is:",my_string)
    stringToEncode = str(my_string.tolist())
elif h == 2:
    array = np.arange(0, 737280, 1, np.uint8)
    my_string = np.reshape(array, (1024, 720))
    print ("Enetered string is:",my_string)
    sudhi = my_string
    stringToEncode = str(my_string.tolist())
else:
    print("You entered invalid input")                    # taking user input


print ("Enetered string is:",stringToEncode)
searchWindowSize = int(input("Enter the Search Window Size:"))
previewWindowSize = int(input("Enter the Preview Window Size:"))
[encodedNumbers, encodedSizes, encodedLetters] = encode_lz77(stringToEncode, searchWindowSize, previewWindowSize)
a =[encodedNumbers, encodedSizes, encodedLetters]
print("Compressed file generated as compressed.txt")
output = open("compressed.txt","w+")
output.write(str(a))
print("Encoded string: ", end="")
i = 0
while i < len(encodedNumbers):
    print ("{",encodedNumbers[i],":", encodedSizes[i],":", encodedLetters[i],"}",end = " ")
    i = i + 1
print("\n")
decodedString = decode_lz77(encodedNumbers, encodedSizes, encodedLetters)
uncompressed_string ="".join(decodedString)
print("Decoded string:", "".join(decodedString))

if h == 1:
    temp = re.findall(r'\d+', uncompressed_string)
    res = list(map(int, temp))
    res = np.array(res)
    res = res.astype(np.uint8)
    res = np.reshape(res, shape)
    print(res)
    print("Observe the shapes and input and output arrays are matching or not")
    print("Input image dimensions:",shape)
    print("Output image dimensions:",res.shape)
    data = Image.fromarray(res)
    data.save('uncompressed.png')
    if sudhi.all() == res.all():
        print("Success")
if h == 2:
    temp = re.findall(r'\d+', uncompressed_string)
    res = list(map(int, temp))
    print(res)
    res = np.array(res)
    res = res.astype(np.uint8)
    res = np.reshape(res, (1024, 720))
    print(res)
    data = Image.fromarray(res)
    data.save('uncompressed.png')
    print("Success")
