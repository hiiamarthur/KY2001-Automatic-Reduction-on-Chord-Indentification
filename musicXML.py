from music21 import *
segment = list()
import sys
# from .utility import note_to_chord
# for key in sorted(environment.UserSettings().keys()):
#     print(key);
# environment.UserSettings()['musescoreDirectPNGPath'] = "/Applications/MuseScore 3.5.app/Contents/MacOS/mscore"

def analysis(bar):
    temp = list()
    pitch = []
    for i in bar:
        # print(i.duration.components[0][2],i)
        for j in list(i.pitches):
            # print(str(j)[:-1])
            temp.append(str(j)[:-1])
            pitch.append(str(j)[-1])
            # print(str(j),j.getEnharmonic())

    temp.sort()
    all_notes,occurance = count_note_num(temp)
    print(all_notes)
    weighted_note = []
    avg_weight = sum(occurance)/len(occurance)
    if len(all_notes) > 4:
        for index,value in enumerate(occurance):
            if value >= avg_weight:
                weighted_note.append(all_notes[index])
    else:
        weighted_note = all_notes
    print(weighted_note,occurance)

    print("chord name generate by chord.chord.commonName:",chord.Chord(weighted_note).commonName,chord.Chord(weighted_note).root())
    # run(weighted_note)


def count_note_num(note_list):
    previous = ""
    arr = []
    num = []

    for i in note_list:
        if i != previous:
            previous = i
            arr.append(i)
            num.append(1)
        else:
            num[-1] += 1
    return arr,num

def append(element):
    temp = []
    for i in element:
        temp.append(i)
    return temp




def getMusicPiece(path):

    # try:
    if path is None:
        s = converter.parse('../musicPiece/Troldtog.xml')
    else:
        s = converter.parse(path)

    # print(s)
    transpose = s.transpose(2)
    # transpose.show()
    # print(transpose.clef.count())
    beat = 0
    bar = []
    piece = []
    # print(s.flat.notes)
    return s

    # print([str(p) for p in transpose.pitches])
    # # transpose.write('xml', '../data/mxl/.Prélude_in_G_Major_transpose')
    # # print(s)
    # parts = instrument.partitionByInstrument(s)
    # # parts.parts
    # print(parts.parts[0])
    # if parts:
    #     notes = parts.parts[0].recurse()
    # else:
    #     notes = s.flat.notes
    #
    # for element in notes:
    #     print(element,element.beat,element.beatStr)


    # s.analyze('key')

    # sc = stream.Score()
    # p1 = stream.Part()
    # p1.id = 'part1'
    # n1 = note.Note('C4')
    # n2 = note.Note('D4')
    # p1.append(n1)
    # p1.append(n2)
    #
    # p2 = stream.Part()
    # p2.id = 'part2'
    # n3 = note.Note('E4')
    # n4 = note.Note('F4')
    # p2.append(n3)
    # p2.append(n4)
    #
    # sc.insert(0, p1)
    # sc.insert(0, p2)
    #
    # sc.elements
    # s.show()

# if __name__ == "__main__":
#     main()