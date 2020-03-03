import random

class Channel:

    # msg must be a list of strings. Each string representing a binary value
    # proba is the probability for a bit in the message to be shifted. Must be
    # bewteen 0 and 100.
    def __init__(self, msg, proba):
        self.message = msg
        self.corruptedMessage = []

        # for each bit, we check if there is a pseudo error.
        # If yes, we change it
        for word in self.message:
            corruptedWord = ''

            for bit in word:
                error = False
                rand = random.randint(0, 100)
                # simulation of a random error
                if rand < proba:
                    error = True

                # depending on the error factor, bits are corrupted or not
                if bit == '0':
                    if error:
                        corruptedWord += '1'
                    else:
                        corruptedWord += '0'

                elif bit == '1':
                    if error:
                        corruptedWord += '0'
                    else:
                        corruptedWord += '1'

                # if a char that is neither 1 or 0 is read, error
                if((bit != '1') and (bit != '0')):
                    print("error in channel, a letter in the message isn't a bit : " + str(bit))
                    break

            self.corruptedMessage.append(corruptedWord)

    def getMessage(self):
        return self.message

    def getCorruptedMessage(self):
        return self.corruptedMessage
