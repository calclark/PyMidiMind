import mido


class MidiFileWriter():

    def __init__(self, model_list, filename):
        self.model_list = model_list
        self.filename = filename

    def render(self):
        outfile = mido.MidiFile()

        for model in self.model_list:
            track = mido.MidiTrack()
            outfile.tracks.append(track)

            track.append(mido.MetaMessage("set_tempo", tempo=1000))
            for midi_note in model.text:
                track.extend(midi_note.as_msgs())

        outfile.save(self.filename)
