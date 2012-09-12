
import subprocess

def sub_it(argList, suppressOut = False, suppressError = False):
    '''obsolete'''
   
    if suppressOut or suppressError:
        with open('./scratch_output.log', 'w') as f:
            oF = f if suppressOut else subprocess.PIPE
            eF = f if suppressError else subprocess.PIPE
            proc = subprocess.Popen(argList, stdout = oF, stderr = eF, shell=True)
    else:
        proc = subprocess.Popen(argList, stdout = subprocess.PIPE, shell=True)

    output = proc.communicate()[0]
    return output

def play_wav(filePath):
    '''obsolete'''

    return sub_it(['play', filePath], True, True)

def play_wavs_sequential(filePaths, delay = .5, suppressOutput = True):

    #construct sox command to call, uses pad in sox to delay wavs
    command = "play" if (len(filePaths) == 1) else "play -m" #dont mix if just one note
    for i, fileName in enumerate(filePaths):
        command += ' "|sox %s -p pad %s"' % (fileName, i * delay)
   
    #execute command in shell environment
    with open('./scratch_output.log', 'w') as f:
        outF = f if suppressOutput else subprocess.PIPE
        subprocess.Popen(command, shell=True, stdout=outF, stderr=outF).wait()


def test():

    play_wavs_sequential(["./sounds/individual/440.wav", "./sounds/individual/110.wav"], 2.0, True)

if __name__ == "__main__":
    test()





