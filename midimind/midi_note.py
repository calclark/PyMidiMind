import mido.messages.messages as msgs
import mido


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

    @property
    def duration(self):
        return self.off_msg.time / (self.on_msg.time + self.off_msg.time)

    def as_msgs(self):
        start = mido.Message('note_on', note=self.note,
                             channel=self.channel, velocity=self.velocity,
                             time=0)
        end = mido.Message('note_off', note=self.note,
                           channel=self.channel, velocity=self.velocity,
                           time=480)
        return (start, end)

    def __str__(self):
        return 'Note: {} Channel: {} Velocity: {} Duration: {}'.format(
            self.note, self.channel, self.velocity, self.duration)
