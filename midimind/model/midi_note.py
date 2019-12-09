from functools import reduce
from typing import List
import mido


def get_midi_notes(msg_list: List):
    cache = {}
    notes = []
    for msg in msg_list:
        if msg.is_meta or (msg.type != 'note_on' and msg.type != 'note_off'):
            continue

        for m in cache.keys():
            cache[m][1] += msg.time

        key = (msg.note, msg.channel)
        if key in cache.keys():
            ticks = cache[key][1]
            notes.append(MidiNote(msg.note, cache[key][0],
                                  msg.channel, ticks))
            del cache[key]
        else:
            cache[key] = [msg.velocity, 0]

    return notes


class MidiNote:

    def __init__(self, note, velocity, channel, duration):
        self.note = note
        self.velocity = velocity
        self.channel = channel
        self.duration = duration

    @property
    def silent(self):
        return self.velocity == 0

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
