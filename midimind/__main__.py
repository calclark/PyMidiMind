import sys
import mido

from .model import MidiModel, gen_motif_dict, get_midi_notes

if len(sys.argv) != 3:
    print("USAGE: midimind TRAINING_FILE OUTPUT_FILE")

in_file = mido.MidiFile(sys.argv[1])
messages = []
for msg in in_file:
    messages.append(msg)

main_midi = MidiModel()

symbols = get_midi_notes(messages)
motifs = gen_motif_dict(symbols)
main_midi.train(motifs)

output = mido.MidiFile()
track = mido.MidiTrack()
output.tracks.append(track)

context = symbols

for i in range(200):
    context.append(main_midi.respond(context))

for note in context:
    start, end = note.as_msgs()
    track.append(start)
    track.append(end)

output.save(sys.argv[2])
