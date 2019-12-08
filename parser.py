#!/usr/bin/env python3


notes = ["D", "C", "B", "C", "D", "D", "D", "C", "C", "C", "D", "F", "F", "D",
        "C", "B", "C", "D", "D", "D", "D", "C", "C", "D", "C", "B"]

motifs = {}
currMot = ""
for note in notes:
    currMot += note
    if currMot in motifs:
        motifs[currMot] += 1
    else:
        motifs[currMot] = 1
        currMot = ""

probs = {}
for motif, count in motifs.items():
    context = motif[:-1]
    note = motif[-1]
    if context in probs:
        probs[context].append((note, count))
    else:
        probs[context] = [(note, count)]

for context, nexts in probs.items():
    print(context, nexts)
