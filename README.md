# GO/NoGo Task for fMRI/EEG Experiment

In the scanner we start we the Staircase script to get the individual stimulation duration for the go/nogo task.

## Go/NoGo short training (only outside the scanner)

After the first instruction outside, run the '01_go_nogo_short_training.py' script to get the participant
familiar with the go/noGo task. Enter the subject id, the run number (has to be a number between 1 and 4),
and the stimulus duration in frames. For the training we will use 12 frames. Select the go side and the language.

## Evaluate the short training (only outside)

After the short go/nogo training, run the '02_evaluate_short_go_nogo_training.py'.
This will give you the results of the short training in percentages. To check, whether
participants understood the task, they should have almost no mistakes in the catch trials,
high values in both go conditions, some mistakes in the weak nogo condition and really low

## Staircase (only in the scanner)

Open the '03_go_nogo_staircase.py' script in psychopy. Enter the Subject ID and the session.
Leave everything else as it is. Maybe change the language

## Analyse the Staircase (only in the scanner)

To get the number of frames or duration of the staircase, run '04_analyse_staircase.py'.
Select the staircase .csv script you want to analyse. The frames will be shown in the PsychoPy Terminal.

values in the strong nogo condition.

## Go/NoGo task (only in the scanner)

In the scanner, participants will run the actual task. To do this, open '05_go_nogo_task.py'.
Enter Subject ID, Run Number (has to be a number between 1 and 4), the stimulus duration in frames
(from the staircase if difficult version, or 12 if easy version). Also select the go side, the language
and enter the session number (day 1 or 2).
