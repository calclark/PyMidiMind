import sys
from mido import MidiFile


def printMidiFile(midi):
    for i, track in enumerate(midi.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)


def midiMsgGenerator(track):
    for msg in track:
        yield msg


if __name__ == "__main__":
    from parser import MidiModel
    mid = MidiFile(sys.argv[1])
    mm = MidiModel()
