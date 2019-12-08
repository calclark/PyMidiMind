import mido.messages.messages as msgs
import mido

from typing import List


def get_midi_notes(msgs_list: List):
    cache = {}
    notes = []
    for msg in msgs_list:
        if msg.is_meta or msg.type != 'note_on':
            continue
        if str(msg.note) in cache.keys():
            notes.append(MidiNote(cache[str(msg.note)], msg))
            del cache[str(msg.note)]
        else:
            cache[str(msg.note)] = msg
    return notes


class MidiNote:

    def __init__(self, on_msg: msgs.Message, off_msg: msgs.Message):
        self.on_msg = on_msg
        self.off_msg = off_msg

    @property
    def velocity(self):
        return self.on_msg.velocity

    @property
    def channel(self):
        return self.on_msg.channel

    @property
    def note(self):
        return self.on_msg.note

    def __eq__(self, other):
        if not isinstance(other, MidiNote):
            return NotImplemented
        return self.velocity == other.velocity and self.note == other.note and self.channel == other.channel

    def __hash__(self):
        return hash((self.velocity, self.channel, self.note))

    def as_msgs(self):
        start = mido.Message('note_on', note=self.note,
                             channel=self.channel, velocity=self.velocity,
                             time=0)
        end = mido.Message('note_off', note=self.note,
                           channel=self.channel, velocity=self.velocity,
                           time=480)
        return (start, end)

    def __str__(self):
        return 'Note: {} Channel: {} Velocity: {}'.format(
            self.note, self.channel, self.velocity)
