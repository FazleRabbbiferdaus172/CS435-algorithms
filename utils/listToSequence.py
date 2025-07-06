from ..SequenceADT import Sequence

def listToSequence(l):
    s = Sequence()
    for i in l:
        s.insertLast(i)
    return s