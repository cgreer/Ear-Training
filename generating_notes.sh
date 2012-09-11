for i in $( cat ~/projects/GuitarTraining/guitarFreqs.txt ); do rec $i.wav synth 1.5 pluck $i; done
