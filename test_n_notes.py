from utility_sound import play_wav
import random


class Sound:

    def __init__(self, note, frequency):
        self.note = note 
        self.frequency = frequency 
        self.soundFile = './sounds/individual/' + str(self.frequency) + '.wav'
        
    def play_sound(self):
        play_wav(self.soundFile)


def load_notes():
    '''give a dictionary that maps the notes name (in A3 format [NOTE,NUMBER) to sound object'''

    #load all notes
    note_sound = {}
    with open('./note_freq.info', 'r') as f:
        for line in f:
            noteName, noteFreq = line.strip().split("\t")
            noteFreq = int(noteFreq) #TODO up resolution to float
            note_sound[noteName] = Sound(noteName, noteFreq)

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

    #load/init
    note_sound = load_notes()
    conf = load_configuration('./configuration.conf')

    #get number of notes to play/guess
    numberOfNotes = int(conf["numberOfNotes"])

    #get list of notes that user would like to be tested on
    notesToTest = conf["noteSelection"].split(',')

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
        [note.play_sound() for note in randomNotes]

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
