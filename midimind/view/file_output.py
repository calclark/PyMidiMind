import mido


class MidiFileWriter():

    def __init__(self, model_list, filename, ticks_per_beat):
        self.model_list = model_list
        self.filename = filename
        self.ticks_per_beat = ticks_per_beat

    def render(self):
        outfile = mido.MidiFile(ticks_per_beat=self.ticks_per_beat)

        for model in self.model_list:
            track = mido.MidiTrack()
            outfile.tracks.append(track)

            for midi_note in model.text:
                track.extend(midi_note.as_msgs())

        outfile.save(self.filename)
