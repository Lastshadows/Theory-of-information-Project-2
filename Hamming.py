
# takes a code word of 4 bits in the form of a string that will be coded
# following the Hamming code algorithm. the resulting coded word of 7 bits
# will be returned by the function as a string.
def hamming7_4(codeWord):

    if(len(codeWord) != 4):
        print("error : word is not 4 bits long \n")
        return -1

    index = 0
    # initialisation of the codedWord. Bits are set to 2 at first to check
    # errors afterward, or to -1 for the parity bits positions
    codedWord = [-1, -1, 2, -1, 2, 2, 2]

    for bit in codeWord:
        # we go until the next real data bit element in the codedWord
        while(codedWord[index] == -1):
            index += 1

        # we copy data from codeWord in codedWord
        if(bit == '1'):
            codedWord[index] = 1
        if(bit == '0'):
            codedWord[index] = 0
        if((bit != '0') & (bit != '1')):
            print("Error : codeWord contains a char that is neither 1 nor 0")
        index += 1

    # we set the parity bits
    for i in range(7):

        # if parity bit
        if(codedWord[i] == -1):
            nbOfBitToCheck = i+1
            nbOfBitChecked = 0
            j = i
            parityCount = 0

            while(j<7):

                #check elements
                while(nbOfBitChecked < nbOfBitToCheck):
                    if(codedWord[j] == 1):
                        parityCount += 1
                    nbOfBitChecked += 1
                    j+=1

                # bits have been checked
                # we now must skip bits
                nbOfBitChecked = 0
                j += nbOfBitToCheck

            # if even number of bit 1
            if ((parityCount % 2) == 0) :
                codedWord[i] = 0
            # if odd number of bit 1
            else :
                codedWord[i] = 1
    # conversion from list of integers to a string
    codedWordStr = ''
    for bit in codedWord:
        codedWordStr += str(bit)
    return codedWordStr

# this method assumes that we give it 7 bit long words, stored as a string.
# this method returns a 4 bit long string corresponding to the traduction
# and potentially correction.
def decodeHamming7_4(codedWord):
    if (len(codedWord) != 7):
        print("error : word is not 7 bits long \n")
        return -1

    correctMsg = ''

    # getting the parity bit received
    parityBit1 = int(codedWord[0])
    parityBit2 = int(codedWord[1])
    parityBit4 = int(codedWord[3])

    # computing the parity bit seen
    realPB1 = (int(codedWord[2]) + int(codedWord[4]) + int(codedWord[6]))%2
    realPB2 = (int(codedWord[2]) + int(codedWord[5]) + int(codedWord[6]))%2
    realPB4 = (int(codedWord[4]) + int(codedWord[5]) + int(codedWord[6]))%2

    errorBit = 0

    # computing the index of the erroneous bit if any
    if realPB1 != parityBit1:
        errorBit +=1
    if realPB2 != parityBit2:
        errorBit +=2
    if realPB4 != parityBit4:
        errorBit +=4
    errorBit -= 1

    # copying the content of the codedWord into a corrected list
    corrected = []
    for bit in codedWord:
        corrected.append(bit)

    # if error detected, correct the error in corrected
    if (errorBit != -1):
        if(corrected[errorBit] == '0'):
            corrected[errorBit] = '1'
        elif (corrected[errorBit] == '1'):
            corrected[errorBit] = '0'
        else:
            print("error in decodeHamming7_4 : character was not a bit ")

    # after correction, extraction of the data bits and concatenation with the resulting string

    correctMsg += corrected[2]
    correctMsg += corrected[4]
    correctMsg += corrected[5]
    correctMsg += corrected[6]

    return correctMsg




