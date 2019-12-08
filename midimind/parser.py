#!/usr/bin/env python3

import random
from typing import List, Dict
from midi_note import MidiNote
from fractions import Fraction
import mido.frozen


class MidiModel:

    def __init__(self):
        self.continuation_dict = {}

    class MsgMap:
        def __init__(self, msg):
            self.msg = msg
            self.time_acc = 0

    @staticmethod
    def gen_motif_dict(symbols: List):
        motifs = {}
        motif_buffer = []
        for symbol in symbols:
            motif_buffer.append(symbol)
            curr_motif = tuple(motif_buffer)
            if curr_motif in motifs:
                motifs[curr_motif] += 1
            else:
                motifs[curr_motif] = 1
                motif_buffer.clear()
        return motifs

    def train(self, motif_dict: Dict):
        for motif, count in motif_dict.items():
            context = motif[:-1]
            note = motif[-1]
            if context in self.continuation_dict:
                self.continuation_dict[context].append((note, count))
            else:
                self.continuation_dict[context] = [(note, count)]

    def respond(self, context: List):
        subtext = ()
        for i in range(len(context)):
            temptext = tuple(context[i:len(context)])
            if temptext in self.continuation_dict:
                subtext = temptext
                break

        symbol_list = []
        for symbol in self.continuation_dict[subtext]:
            symbol_list += [symbol[0]] * symbol[1]
        return random.choice(symbol_list)

    @classmethod
    def get_midi_notes(cls, msgs: List, ticks_per_beat: int):
        cache = {}
        notes = []
        msgs_list = map(lambda x: mido.frozen.freeze_message(x), msgs)
        for msg in msgs_list:
            if msg.is_meta or msg.type != 'note_on':
                continue

            MidiModel._add_time_to_cache_members(cache, msg.time)

            print([str(x) for x in cache])

            if msg in cache.keys():
                notes.append(MidiNote(
                    mido.frozen.thaw_message(cache[msg].msg),
                    mido.frozen.thaw_message(msg),
                    Fraction(cache[msg].time_acc, ticks_per_beat)))
                del cache[msg]
            else:
                cache[msg] = cls.MsgMap(msg)

        return notes

    @staticmethod
    def _add_time_to_cache_members(cache, time):
        for val in cache.values():
            val.time_acc += time
