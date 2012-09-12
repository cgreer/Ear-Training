from utility_sound import play_wavs_sequential
import random
import os



class Sound:

    def __init__(self, note, frequency, soundType="tone_guitar"):
        self.note = note 
        self.frequency = frequency 
        self.soundFile = './sounds/individual/' + soundType + '/' + str(self.frequency) + '.wav'
        if not os.path.exists(self.soundFile):
            print "WARNING: %s does not exist" % self.soundFile
        
    def play_sound(self):
        play_wavs_sequential([self.soundFile], .5, True)


def load_notes(soundType):
    '''give a dictionary that maps the notes name (in A3 format [NOTE,NUMBER) to sound object'''

    #load all notes
    note_sound = {}
    with open('./notes_frequencies.rounded.info', 'r') as f:
        for line in f:
            noteName, noteFreq = line.strip().split("\t")
            noteFreq = int(noteFreq) #TODO up resolution to float
            note_sound[noteName] = Sound(noteName, noteFreq, soundType)

    return note_sound
        
def n_random_notes(noteSet, numberNotes):
    '''return list of note sounds randomly chosen from set'''
    
    noteList = list(noteSet)

    #shuffle list and return numberNotes notes
    #doing it this way insures that there are no duplicates
    random.shuffle(noteList)
    return noteList[0:numberNotes]
    

def give_cookie(correct, nNotes, userAnswer):

    print "  CORRECT!" if correct else "  INCORRECT!"
    print "    Notes played", ' '.join(nNotes)
    print "    Notes Guessed", ' '.join(userAnswer)

def load_configuration(confFileName):
    conf = {}
    with open(confFileName, 'r') as f:
        for line in f:
            if any([line.startswith(x) for x in ["#", "/", "\n"]]): continue
            cKey, cValue = line.strip().split(" ")
            conf[cKey] = cValue

    return conf


def start_program():

    print
    print "################################"
    print "##        EAR TRAINING        ##"
    print "################################"
    print

    #load/init, get config values
    conf = load_configuration('./configuration.conf')
    noteDelay = float(conf["noteDelay"])
    numberOfNotes = int(conf["numberOfNotes"])
    notesToTest = conf["noteSelection"].split(',')
    soundType = conf["playStyle"]

    #load notes to be played 
    note_sound = load_notes(soundType)

    #construct note set
    noteSet = set()
    [noteSet.add(note_sound[noteName]) for noteName in notesToTest]
    noteSetNames = ' '.join([x.note for x in sorted(list(noteSet))])

    #test user
    while True:

        #play n notes
        print "\nPLAYING NOTES..."
        randomNotes = n_random_notes(noteSet, numberOfNotes)
        randomNoteNames = [x.note for x in randomNotes]
        #[note.play_sound() for note in randomNotes]
        play_wavs_sequential([note.soundFile for note in randomNotes], noteDelay, True)

        #ask user for notes played
        userAnswer = raw_input("  Which notes were played?\n   Choose from %s\n   CHOICES: " % ' '.join(notesToTest))
        if "exit" in userAnswer:
            print "GOODBYE!"
            break
        userAnswer = userAnswer.strip().split(',')

        #test if correct
        testConditions = []
        if len(userAnswer) != len(randomNoteNames):
            give_cookie(False, randomNoteNames, userAnswer) 
        else:
            if any([notePlayed != noteGuessed for notePlayed, noteGuessed in zip(randomNoteNames, userAnswer)]):
                give_cookie(False, randomNoteNames, userAnswer) 
            else:
                give_cookie(True, randomNoteNames, userAnswer) 

start_program() 
