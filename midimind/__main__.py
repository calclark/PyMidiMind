import sys
import mido

from .model import MidiModel, gen_motif_dict, get_midi_notes
from .view import MidiFileWriter

if len(sys.argv) != 3:
    print("USAGE: midimind TRAINING_FILE OUTPUT_FILE")

in_file = mido.MidiFile(sys.argv[1])

model_list = []
for track in in_file.tracks:
    curr_model = MidiModel()
    model_list.append(curr_model)

    symbols = get_midi_notes(track, in_file.ticks_per_beat)
    motifs = gen_motif_dict(symbols)
    curr_model.train(motifs)

    curr_model.text = []
    for i in range(100):
        curr_model.respond()

MidiFileWriter(model_list, sys.argv[2]).render()
