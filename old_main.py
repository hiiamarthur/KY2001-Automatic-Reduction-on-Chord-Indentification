from musicXML import *
from spiral_method import *
import matplotlib.pyplot as plt
import time

structure_arr = list()


def initialize():
    global structure_arr
    structure_arr = initialize_spiral_structure()


def find_tonality_by_bar(s):
    segment = []
    beat = 0
    bar = []
    piece = []
    counter2 = 0
    for i in [p for p in s.flat.notes]:
        counter2 += 1
        # print(i,i.beat,beat,str(type(i)))
        # print(clef.bestClef(s.flat.notes))
        if isinstance(i, harmony.ChordSymbol):
            continue
        if i.beat >= beat:
            bar.append(i)
        elif beat > i.beat:
            # segment
            tempbar = bar
            segment.append(append(tempbar))
            # print(bar)
            # analysis(bar)
            bar.clear()
            bar.append(i)

            # print(bar, "yo")
        beat = i.beat

    # for i in structure_arr:
    #     print(i['note'],i['major_spiral_array'].pitch)

    # print(len(segment))
    # for j in segment[2]:
    #     print(j)
    counter = 0
    total_note = 0
    for index, i in enumerate(segment):

        notes, duration = get_segment_info(i)
        print("In segment ", index, ":")
        run_find_tonal_center(notes, duration)
        notes = []
        duration = []
        counter += 1
        if counter > 18:
            break

        analysis(segment[index])
        total_note += len(segment)

    print("total note is:", total_note)
    print(counter2)
    return


def get_segment_info(value):
    notes = []
    pitch = []
    duration = []
    for j in value:
        # print(j.duration)
        if isinstance(j, note.Rest):
            continue

        temp = float()
        for l in list(j.duration.components):
            temp = l[2]
        for k in list(j.pitches):
            # print(str(k)[:-1])
            notes.append(str(k)[:-1])
            pitch.append(str(k)[-1])
            duration.append(temp)
        # print(notes)
        # print(duration)
        # duration.append()
    return notes, duration


def segment_analysis(s):
    unit_time = 1
    note_list = [p for p in s.flat.notesAndRests]
    note_list = note_list[:500]
    coe_diff = []
    beat = 0
    bar = []
    bar_count = 0
    buffer = 0
    bar_index = []
    index = []
    bar_list_before = []
    bar_list_after = []
    have_set_bar_index = True
    for counter, i in enumerate(note_list):
        # print(i,i.beat)
        unit_time += 1
        if isinstance(i, harmony.ChordSymbol):
            continue
        if i.beat >= beat:
            bar.append(i)
        elif beat > i.beat:
            # print(beat,i.beat)
            bar_count += 1
            bar_index.append(bar_count)
            have_set_bar_index = False
            print("Bar above:", bar_count)
            if (bar_count % 8) / 4 == 0:
                bar_list_before.append(bar)
            elif (bar_count % 8) / 4 == 1:
                bar_list_after.append(bar)
            bar = []
            # bar.append(i)
        if have_set_bar_index:
            bar_index.append(0)
        have_set_bar_index = True
        beat = i.beat
        if isinstance(i, note.Rest):
            continue
        if isinstance(i, harmony.ChordSymbol):
            continue
        if isinstance(i, harmony.NoChord):
            continue
        if bar_count >= 8:

            notes_before_bound = note_list[:unit_time]
            notes_after_bound = note_list[unit_time:]
            if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_before_bound):
                if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_after_bound):
                    notes_before, duration_before = get_segment_info(notes_before_bound)
                    notes_after, duration_after = get_segment_info(notes_after_bound)
                    coe_diff.append(run_find_segment(notes_before, duration_before, notes_after, duration_after))
                    index.append(len(coe_diff))

                # print(bar, "yo")

            print("In index :", counter, "note_num:", len(coe_diff) + buffer, type(i), i, i.beat)

        if unit_time >= 500:
            break
    # index.reverse()
    plt.plot(np.array(index[70:110]), np.array(coe_diff[70:110]))
    # plot based on no. of note
    # plt.plot(np.array(bar_index).reshape(), np.array(coe_diff))
    # ploit based on no. of bar
    print(len(note_list))
    # print(coe_diff)
    plt.show()
    return


def getMusicProperties(x):
    s = '';
    t = '';
    s = str(x.pitch) + ", " + str(x.duration.type) + ", " + str(x.duration.quarterLength);
    s += ", "
    if x.tie != None:
        t = x.tie.type;
    s += t + ", " + str(x.pitch.ps) + ", " + str(x.octave);  # + str(x.seconds)  # x.seconds not always there
    return s


def main():
    try:

        s = getMusicPiece('../musicPiece/Polonaise_in_A_Major,_“Military_Polonaise”.xml')
        # for i in [p for p in s.flat.notesAndRests]:
        #     print(i,i.beat)
        #     if isinstance(i,note.Rest):
        #         print('yo')
        # print(dir(s.flat))
        # for i in s.flat.spanners:
        #     print(i)
        # test = s.stripTies()
        # j = 0
        # for i in test:
        #     if i.isStream:
        #         e = repeat.Expander(i)
        #         s2 = e.process()
        #         timing = s2.secondsMap
        #         test[j] = s2
        #     j += 1
        # print('pitch, duration_string, duration, tie, midi pitch, octave')
        # for a in test.recurse().notes:
        #
        #     if (a.isNote):
        #         x = a;
        #         s = getMusicProperties(x);
        #         print(s);
        #
        #     if (a.isChord):
        #         for x in a._notes:
        #             s = getMusicProperties(x);
        #             print(s);
        find_tonality_by_bar(s)
        segment_analysis(s)
    except converter.ConverterException:
        print("Error Reading Files")


if __name__ == "__main__":
    initialize()
    start = time.time()
    main()
    print("start at ", start)