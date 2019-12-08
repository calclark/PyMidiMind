#!/usr/bin/env python3

from typing import List, Dict


class MidiModel:
    def __init__(self):
        self.continuation_dict = {}

    def gen_motif_dict(self, symbols: List):
        motifs = {}
        curr_motif = []
        for symbol in symbols:
            curr_motif.append(symbol)
            if curr_motif in motifs:
                motifs[curr_motif] += 1
            else:
                motifs[curr_motif] = 1
                curr_motif.clear()
        return motifs

    def train(self, motif_dict: Dict):
        for motif, count in motif_dict.items():
            context = motif[:-1]
            note = motif[-1]
            if context in self.continuation_dict:
                self.continuation_dict[context].append((note, count))
            else:
                self.continuation_dict[context] = [(note, count)]
