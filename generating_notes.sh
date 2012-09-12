#!/bin/bash

#either "pluck" or "sin"
sType=${1}
folder=${2}

while read note freq; do echo $note $freq; rec ${folder}/$freq.wav synth 1.5 ${sType} $freq fade 0 1.5 .2; done < notes_frequencies.rounded.info
