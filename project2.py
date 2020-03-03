import csv
import numpy
import Channel
import HuffmanCode
import Hamming
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import string

#Q2
def symbolPrep(verbose=False):
    # going to read every symbol and count their appearance in the text
    # creating an empty dictionnary we will fill with the symbols as they come
    symbols = {}
    totalSymb = 0
    totalDifSymb = 0
    listOfSymbols = []

    with open('text.csv', 'rt') as csvfile:

        file = csv.reader(csvfile, delimiter='\n')

        for block in file:
            for line in block:
                for char in line:

                    # we count the number of symbol
                    totalSymb += 1
                    currCharCount = symbols.setdefault(char.lower(), 0)

                    # if the symbol is new we add a new matching element to the dictionnary
                    if currCharCount == 0:
                        listOfSymbols.append(char.lower())
                        totalDifSymb += 1
                        symbols[char.lower()] = 0

                    # we increment the number of time we have encoutered the symbol
                    symbols[char.lower()] += 1

    csvfile.close()

    keys = symbols.keys()
    lowerCase = string.ascii_lowercase
    digits = string.digits

    for letter in lowerCase:
        if letter not in keys:
            symbols[letter] = 0
            listOfSymbols.append(letter)
            totalDifSymb += 1
    for d in digits:
        if d not in keys:
            symbols[d] = 0
            listOfSymbols.append(d)
            totalDifSymb += 1

    for symb in listOfSymbols:
        proba = (symbols[symb] / totalSymb)
        symbols[symb] = proba
        if verbose:
            if symb == '\n':
                print("p('\\n') = {}".format(proba))
            else:
                print("p('{}') = {}".format(symb, proba))

    print("total nb of symb = " + str(totalSymb))
    print(" size in bit : " + str(totalSymb*8))
    #print("nb of dif symb : " + str(totalDifSymb))
    print("TOTAL DIFF SYMBOL = {}".format(totalDifSymb))
    return (listOfSymbols, symbols, totalDifSymb)

#Q8 plots the sound and returns the input
def plotSound():

    # read audio samples
    input = read("sound.wav")
    audio = input[1]
    # plot the first 1024 samples
    plt.plot(audio[0:33100])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time (in 10th of ms) ")
    # set the title
    plt.title("Sample Wav")
    # display the plot
    plt.show()
    plt.clf()

    return audio

if __name__ == '__main__':

    pack = symbolPrep(verbose=True)
    dict = pack[1]
    symbols = pack[0]
    totalDifSymbols = pack[2]
    #Q3
    coder = HuffmanCode.HuffmanCoder(symbols, dict)
    coder.encoder("")
    code = coder.getCode()

    # Q4
    print("Q4: Huffman code:")
    for i, (key, value) in enumerate(sorted(code.items())):

        if key == '\n':
            print("'\\n' : {}".format(value))
        else:
            print("'{}' : {}".format(key, value))

    codedFile = []
    codedTxtSize = 0
    nbOfCharInTxt = 0
    with open('text.csv', 'rt') as csvfile:

        file = csv.reader(csvfile, delimiter='\n')

        for block in file:
            for line in block:
                for char in line:
                    nbOfCharInTxt += 1
                    codedChar = code[char.lower()]
                    codedFile.append(codedChar)
                    codedTxtSize += len(codedChar)

    csvfile.close()
    print("total number of bits of the coded text  = " + str(codedTxtSize) +
          "bits")


    #Q5
    print("empirical average length of a coded character : " + str(codedTxtSize/nbOfCharInTxt))

    expSymbLen = 0
    for symbol in symbols:
        proba = dict[symbol]
        # we add the proba of the current symbol to appear times its coded length
        expSymbLen += proba*len(code[symbol])
    print("expected average length of a coded symbol " + str(expSymbLen))

    #Q6
    print("coded txt size is of  : " + str(codedTxtSize / 8) + " bytes")
    codedTxtSizeBytes = codedTxtSize/8
    originalFileSize = nbOfCharInTxt*8
    print("Compression rate = {}/{} = {}".format(originalFileSize, codedTxtSize,
        originalFileSize/codedTxtSize))

    # Q8
    audio = plotSound()
    # print(audio)

    # Q9
    # every audio value (int) will be translated in 8 bits under a string form.
    # these binary strings are stored in the audioCodedValue list
    audioCodedValue = []
    for value in audio:
        audioCodedValue.append(f'{value:08b}')
    # print("audio values coded on 8 bits : \n" )
    # print(audioCodedValue)

    # Q10
    # we will stock the coded values of the audio file (coded on 8 bits as duo of half words in
    # the codedAudio lists. The first one has all the first half part of every value
    # coded under Hamming code, the second codedAudio list has the coded second half.
    codedAudio1 = []
    codedAudio2 = []
    # reminder : audioCodedValue : list of 8 bits string
    for codeWord in audioCodedValue:
        halfCodedWord1 = codeWord[0:4]
        halfCodedWord2 = codeWord[4:]

        # coded1,2 = string of 7 bits
        coded1 = Hamming.hamming7_4(halfCodedWord1)
        coded2 = Hamming.hamming7_4(halfCodedWord2)

        # codedAudio1,2 = list of strings (7bits long)
        codedAudio1.append(coded1)
        codedAudio2.append(coded2)

    # Q11
    # get the audio values coded on 8 bits through the channel
    # with a bit error probability of 'errorRate' percent
    errorRate = 1

    # reminder :audioCodedValue : list of 8 bits strings
    channel = Channel.Channel(audioCodedValue, errorRate)
    # print("audioCodedValue : ")
    # print(audioCodedValue)
    # print("audioCodedValue uncorrupted message : ")
    # print(channel.getMessage())
    # print("audioCodedValue corrupted message :")
    # print(channel.getCorruptedMessage())

    corruptedMsg = channel.getCorruptedMessage()

    # translation of the corrupted msg from bits to integers
    for i in range(len(corruptedMsg)):
        corruptedMsg[i] = int(corruptedMsg[i], 2)

    # plot of the corrupted msg
    plt.plot(corruptedMsg[0:33100])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time (in 10th of ms) ")
    # set the title
    plt.title("corrupted sound")
    # display the plot
    plt.show()
    plt.clf()

    dt = numpy.dtype(numpy.uint8)
    data = numpy.array(corruptedMsg, dtype=dt)
    write('corruptedSound.wav', 11025, data)

    # Q12
    # each audio value was coded on 8bit. In order to code them as hamming codes, they were
    # cut in 2 half word of 4 bits. Each of these coded half words are at the same index
    # in the corresponding codedAudio list. So first half is in codedAudio1 and
    # second half is in codedAudio2, at the same index.
    # We know make them go through our channel.

    # reminder : codedAudio1,2 are lists of 7bits string representing half
    # of a 8 bit value in a hamming code
    errorRate = 1
    channelAudio1 = Channel.Channel(codedAudio1, errorRate)
    channelAudio2 = Channel.Channel(codedAudio2, errorRate)

    # print("codedAudio1 : ")
    # print(codedAudio1)

    decodedHammingAudioBinary = []
    # we get the 7 bits corrupted values from channelAudio1,2
    corruptedHamMsg1 = channelAudio1.getCorruptedMessage()
    corruptedHamMsg2 = channelAudio2.getCorruptedMessage()

    # print("corruptedHamMsg1 : ")
    # print(corruptedHamMsg1)

    # we go through all corrupted messages and decode them
    for i in range(len(corruptedHamMsg1)):
        half1 = Hamming.decodeHamming7_4(corruptedHamMsg1[i])
        half2 = Hamming.decodeHamming7_4(corruptedHamMsg2[i])
        decodedWord = half1 + half2
        decodedHammingAudioBinary.append(decodedWord)

    # decodedHammingAudioBinary contains all corrected word
    # we can now convert it back to int, plot it and listen to it.
    # translation of the corrupted msg from bits to integers

    # translation from bit to integers
    for i in range(len(decodedHammingAudioBinary)):
        decodedHammingAudioBinary[i] = int(decodedHammingAudioBinary[i], 2)

    # print("decodedHammingAudioBinary : ")
    # print(decodedHammingAudioBinary)

    # plot of the corrected msg
    plt.plot(decodedHammingAudioBinary[0:33100])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time (in 10th of ms) ")
    # set the title
    plt.title("decoded and corrected sound ")
    # display the plot
    plt.show()

    dt = numpy.dtype(numpy.uint8)
    data = numpy.array(decodedHammingAudioBinary, dtype=dt)
    write('correctedSound.wav', 11025, data)
