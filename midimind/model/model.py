import random
from typing import List, Dict
from collections import deque


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


class MidiModel:

    def __init__(self):
        self.continuation_dict = {}
        self._text = []
        self.context = deque()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text=[]):
        self._text = new_text
        self.context = deque(new_text)

    def train(self, motif_dict: Dict):
        for motif, count in motif_dict.items():
            context = motif[:-1]
            note = motif[-1]
            if context in self.continuation_dict:
                self.continuation_dict[context].append((note, count))
            else:
                self.continuation_dict[context] = [(note, count)]

    def respond(self):
        if () not in self.continuation_dict:
            return

        while tuple(self.context) not in self.continuation_dict:
            self.context.popleft()

        symbol_list = []
        for symbol in self.continuation_dict[tuple(self.context)]:
            symbol_list += [symbol[0]] * symbol[1]

        symbol = random.choice(symbol_list)
        self._text.append(symbol)
        self.context.append(symbol)
