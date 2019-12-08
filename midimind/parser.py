#!/usr/bin/env python3

import random
from typing import List, Dict


class MidiModel:

    def __init__(self):
        self.continuation_dict = {}

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
