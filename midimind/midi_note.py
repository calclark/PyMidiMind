import mido.messages.messages as msgs


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

    def __str__(self):
        return 'Note: {} Channel: {} Velocity: {} Duration: {}'.format(
            self.note, self.channel, self.velocity, self.duration)
