import mido.messages.messages as msgs
from fractions import Fraction


class MidiNote:

    def __init__(self, on_msg: msgs.Message, off_msg: msgs.Message,
                 duration: Fraction):
        self.on_msg = on_msg
        self.off_msg = off_msg
        self._duration = duration

    @property
    def velocity(self):
        return self.on_msg.velocity

    @property
    def channel(self):
        return self.on_msg.channel

    @property
    def note(self):
        return self.on_msg.note

    @property
    def duration(self):
        return self._duration

    def __str__(self):
        return 'Note: {} Channel: {} Velocity: {} Duration: {}/{}'.format(
            self.note, self.channel, self.velocity, self.duration.numerator,
            self.duration.denominator)

    def __hash__(self):
        return (hash(self.velocity) + hash(self.channel) + hash(self.note) +
                hash(int(self.duration)))

    def __eq__(self, obj):
        return (isinstance(obj, MidiNote) and self.velocity == obj.velocity
                and self.channel == obj.velocity and self.note == obj.note
                and self.duration == obj.duration)
