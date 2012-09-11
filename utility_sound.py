
import subprocess

def sub_it(argList, suppressOut = False, suppressError = False):
   
    if suppressOut or suppressError:
        with open('./scratch_output.log', 'w') as f:
            oF = f if suppressOut else subprocess.PIPE
            eF = f if suppressError else subprocess.PIPE
            proc = subprocess.Popen(argList, stdout = oF, stderr = eF)
    else:
        proc = subprocess.Popen(argList, stdout = subprocess.PIPE)

    output = proc.communicate()[0]
    return output

def play_wav(filePath):

    return sub_it(['play', filePath], True, True)

