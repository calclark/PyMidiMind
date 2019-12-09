from typing import List
import mido


def get_midi_notes(msg_list: List):
    cache = []
    notes = []
    for msg in msg_list:
        if msg.is_meta or (msg.type != 'note_on' and msg.type != 'note_off'):
            continue
        counter = msg.time

        curr_tone = (msg.note, msg.channel)
        if curr_tone in cache:
            chord = []
            for tone in cache:
                chord.append(MidiNote(tone[0], tone[1], counter))
            notes.append(MidiChord(tuple(chord)))
            cache.remove(curr_tone)
        else:
            chord = []
            for tone in cache:
                chord.append(MidiNote(tone[0], tone[1], counter))
            if chord:
                notes.append(MidiChord(tuple(chord)))
            counter = 0
            cache.append(curr_tone)

    for note in notes:
        print(note)
    return notes


class MidiNote:

    def __init__(self, note, channel, duration, velocity=64):
        self.note = note
        self.velocity = velocity
        self.channel = channel
        self.duration = duration

    def __eq__(self, other):
        if not isinstance(other, MidiNote):
            return NotImplemented
        return (self.velocity == other.velocity
                and self.note == other.note
                and self.channel == other.channel
                and self.duration == other.duration)

    def __hash__(self):
        return hash((self.velocity, self.channel, self.note, self.duration))

    def as_msgs(self):
        start = mido.Message('note_on', note=self.note,
                             channel=self.channel, velocity=self.velocity,
                             time=0)
        end = mido.Message('note_off', note=self.note,
                           channel=self.channel, velocity=0,
                           time=self.duration)
        return (start, end)

    def __str__(self):
        return 'Note: {} Channel: {} Velocity: {} Duration: {}'.format(
            self.note, self.channel, self.velocity, self.duration)


class MidiChord():

    def __init__(self, tones):
        self.tones = tones

    def __eq__(self, other):
        if not isinstance(other, MidiChord):
            return NotImplemented
        return self.tones == other.tones

    def __hash__(self):
        return hash(self.tones)

    def __str__(self):
        s = ""
        for note in self.tones:
            s += str(note)
        return s

    def as_msgs(self):
        starts = []
        stops = []
        for tone in self.tones:
            start, stop = tone.as_msgs()
            starts.append(start)
            stops.append(stop)
        return starts + stops
