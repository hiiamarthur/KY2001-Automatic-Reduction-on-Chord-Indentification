from musicXML import *
from spiral_method import *
import matplotlib.pyplot as plt
import time
import scipy.signal as signal
import os
# from collections import defaultdict
import collections
structure_arr = list()
rate = float
show_bound_r = int
show_bound_l = int
by_mean = bool

def initialize():
    global structure_arr
    structure_arr = initialize_spiral_structure()

def find_tonality_by_bar(s):
    segments = []
    segments_symbol = []
    beat = 0
    bar = []
    piece = []
    counter2 = 0
    # for i in [p for p in s.flat.notes]:
    #     counter2 += 1
    #     # print(i,i.beat,beat,str(type(i)))
    #     # print(clef.bestClef(s.flat.notes))
    #     if isinstance(i,harmony.ChordSymbol):
    #         continue
    #     if i.beat >= beat:
    #         bar.append(i)
    #     elif beat > i.beat:
    #         # segment
    #         tempbar = bar
    #         segment.append(append(tempbar))
    #         # print(bar)
    #         # analysis(bar)
    #         bar.clear()
    #         bar.append(i)
    #
    #         # print(bar, "yo")
    #     beat = i.beat
    previous_symbol = [""]
    # print("get bar num:",get_bar_num(s))
    for i in range(0,get_bar_num(s)):
        symbol,notes = get_note_in_bar(s,i)
        segments.append(notes)
        if len(symbol) == 0:
            symbol = [previous_symbol[-1]]
        else:
            previous_symbol = symbol
        segments_symbol.append(symbol)
        # print("\n\nhaha upper part",measure.parts[0].pitches,"\n\n lower part",measure.parts[1].pitches,"\n\nbar :",i, " segment:",segment[i])



    # for i in structure_arr:
    #     print(i['note'],i['major_spiral_array'].pitch)


    # print(len(segment))
    # for j in segment[2]:
    #     print(j)
    counter = 0
    total_note = 0
    true_case = 0
    for index,i in enumerate(segments):
        if len(i) == 0:
            continue
        notes,duration = get_segment_info(i)
        # print("In segment ",index,":")
        # print("Chord marked:",segments_symbol[index])
        flag = run_find_tonal_center(notes,duration,segments_symbol[index])
        if flag:
            true_case += 1
        notes = []
        duration = []
        counter += 1
        # if counter > 18:
        #     break

        # analysis(i)
        total_note += len(i)

    print("total note is:",total_note)
    print("total bar:",counter)
    print("bar with right prediction of segmentation",true_case)
    print("average correct %:",float(true_case)/counter)
    print("")
    return

def get_segment_info(value):
    notes = []
    pitch = []
    duration = []
    for j in value:
        # print(j.duration)
        if isinstance(j, note.Rest):
            continue
        if isinstance(j, harmony.ChordSymbol):
            continue
        if isinstance(j, harmony.NoChord):
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
    return notes,duration

def get_note_in_bar(s,i):
    measure = s.measure(i)
    notes = []
    symbol = []
    if len(measure.parts[0].pitches) == 0:
        return symbol,notes
    # print("haha , bar ", i, "  ", list(measure.parts[0].flat.notes), list(measure.parts[1].flat.notes))
    for j in measure.parts[0].flat.notes:
        if isinstance(j, note.Rest):
            continue
        if isinstance(j, harmony.NoChord):
            continue
        if isinstance(j,harmony.ChordSymbol):
            symbol.append(j)
            continue
        notes.append(j)
    for k in measure.parts[1].flat.notes:
        if isinstance(k, note.Rest):
            continue
        if isinstance(k, harmony.NoChord):
            continue
        if isinstance(k,harmony.ChordSymbol):
            symbol.append(k)
            continue
        notes.append(k)
    return symbol,notes

def get_bar_num(s):
    count = 0
    have_exist_condition = 0
    while True:
        measure = s.measure(count)
        if len(measure.parts[0].pitches) == 0 and len(measure.parts[1].pitches) == 0 and have_exist_condition:
            break
        else:
            have_exist_condition = 1
        count += 1
    return count



def is_notes_equal(notes1,notes2):
    # print("called",notes1,notes2)
    if len(notes1) != len(notes2):
        return False
    list_dict_notes1 = collections.defaultdict(list)
    list_dict_notes2 = collections.defaultdict(list)
    for note1 in notes1:
        list_dict_notes1[type(note1)].append(note1)
    for note2 in notes2:
        list_dict_notes2[type(note2)].append(note2)
    # print("a")
    # print("\n list1",list_dict_notes1[note.Note],"\n list2:",list_dict_notes2[note.Note])
    # print("here")
    if sorted(list_dict_notes1[note.Note]) == sorted(list_dict_notes2[note.Note]):
        # print("b")
        t = list(list_dict_notes1[chord.Chord])
        s = list(list_dict_notes2[chord.Chord])
        if len(t) == len(s) == 0:
            # print("c")
            return True
        try:
            # print("d")
            for elem in s:
                t.remove(elem)
        except ValueError:
            return False
        # print("e")
        return True
    else:
        return False




def segment_analysis(s):
    slur_list = []
    dot_list = []
    unit_time = 1

    note_list = [p for p in s.flat.notesAndRests]
    # while True:
    #     if type()
    print("haha",len(note_list),get_bar_num(s))
    # note_list = note_list[:1000]
    if rate == 1/2:
        average_note_density = int(len(note_list) / get_bar_num(s))
    else:
        average_note_density = int(len(note_list)/get_bar_num(s))*rate

    # average_note_density =
    coe_diff = []
    beat = 0
    bar = []
    bar_count = 0
    buffer = 0
    bar_index = []
    index = []

    note_list_no_symbol = []
    bar_info_of_note = []

    is_sluring = False
    have_set_bar_index = True
    symbol,bar_note = get_note_in_bar(s,bar_count)
    # bar_note.sort()
    increment_bar_note_list = []
    increment_duration = 0
    increment_duration_list = []
    for counter,i in enumerate(note_list):
        increment_duration_list.append(increment_duration + i.beat)
        if isinstance(i,harmony.ChordSymbol):
            continue
        if isinstance(i, note.Rest):
            continue
        if isinstance(i, harmony.NoChord):
            continue
        if len(bar_note) == 0:
            bar_count += 1
            symbol,bar_note = get_note_in_bar(s,bar_count)

            # bar_note.sort()
        increment_bar_note_list.append(i)
        # increment_bar_note_list.sort()

        if is_notes_equal(bar_note,increment_bar_note_list):

            print(s.getTimeSignatures())
            print(s.timeSignature,s.measure(bar_count).duration.quarterLength,s.measure(bar_count).beatDuration,s.measure(bar_count).beat)
            increment_duration += s.measure(bar_count).duration.quarterLength
            print("\n bar note num:",bar_count,"with note:", bar_note, "\n increment:", increment_bar_note_list)
            bar_count += 1
            increment_bar_note_list = []
            symbol,bar_note = get_note_in_bar(s,bar_count)



    for counter,i in enumerate(note_list):
        b = i.getSpannerSites()

        for thisSpanner in b:
            if 'Slur' in thisSpanner.classes:
                if thisSpanner.isFirst(i):
                    print(i, thisSpanner, thisSpanner.beat, "first")
                    is_sluring = True
                if thisSpanner.isLast(i):
                    print(i, thisSpanner, thisSpanner.beat, "end")
                    is_sluring = False
        if is_sluring:
            slur_list.append(1)
        else:
            slur_list.append(0)

        if i.articulations:
            dot_list.append(1)
        else:
            dot_list.append(0)
        # print(i,i.beat)
        unit_time += 1
        if isinstance(i,harmony.ChordSymbol):
            continue
        if isinstance(i, note.Rest):
            continue
        if isinstance(i, harmony.NoChord):
            continue
        # if len(bar_note) == 0:
        #     bar_count += 1
        #     bar_note = get_note_in_bar(s,bar_count)
        #
        #     # bar_note.sort()
        # increment_bar_note_list.append(i)
        # # increment_bar_note_list.sort()
        #
        # if is_notes_equal(bar_note,increment_bar_note_list):
        #
        #     print(s.getTimeSignatures())
        #     print(s.timeSignature,s.measure(bar_count).duration.quarterLength,s.measure(bar_count).beatDuration,s.measure(bar_count).beat)
        #     increment_duration += s.measure(bar_count).duration.quarterLength
        #     print("\n bar note num:",bar_count,"with note:", bar_note, "\n increment:", increment_bar_note_list)
        #     bar_count += 1
        #     increment_bar_note_list = []
        #     bar_note = get_note_in_bar(s,bar_count)



        # if bar_note
        # if i.beat >= beat:
        #     bar.append(i)
        # elif beat > i.beat:
        #     # print(beat,i.beat)
        #     bar_count += 1
        #     bar_index.append(bar_count)
        #     have_set_bar_index = False
        #     print("Bar above:",bar_count)
        #     bar.clear()
        #     bar.append(i)
        # if have_set_bar_index:
        #     bar_index.append(0)
        # have_set_bar_index = True
        # beat = i.beat


        # note_list_no_symbol.append(i)
        bar_info_of_note.append(bar_count)

        if(unit_time > average_note_density or len(note_list) - unit_time < average_note_density):
            notes_before_bound = note_list[unit_time-average_note_density:unit_time]
            notes_after_bound = note_list[unit_time:unit_time+average_note_density]
            # print(notes_before_bound)
            # print(notes_after_bound)
            if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_before_bound):
                if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_after_bound):
                    # if by_mean:
                        notes_before,duration_before = get_segment_info(notes_before_bound)
                        notes_after,duration_after = get_segment_info(notes_after_bound)
                        coe_diff.append(run_find_segment(notes_before,duration_before,notes_after,duration_after))
                        note_list_no_symbol.append(i)
                        index.append(len(coe_diff))
                    # else:




            # print(bar, "yo")

        print("In index :", counter,"note_num:",len(note_list_no_symbol),"algo_run_though",len(coe_diff)+buffer,"with total quater beat:", increment_duration_list[counter] , type(i), i.pitches, i.beat, list(i.pitches)[0].nameWithOctave,slur_list[counter])



        # if unit_time >= 700:
        #     break
    # index.reverse()
    fig = plt.figure(figsize=(80,9))
    label = []
    for i in index:
        if i % 5 == 0:
            label.append(i)
    plt.xticks(np.array(label))
    maxima = []
    maxima_note = []
    maxima_limit = []

    a = np.array(coe_diff)
    # maxima_list = np.r_[True, coe_diff[1:] > coe_diff[:-1]] & np.r_[coe_diff[:-1] > coe_diff[1:], True]
    maxima_index = signal.argrelextrema(np.array(coe_diff),np.greater)
    # maxima_index = maxima_index

    maxima_list = a[maxima_index]

    maxima_note_list = np.array(note_list_no_symbol,dtype=object)[maxima_index]

    print("maxima_note_list:",len(maxima_note_list),maxima_index)
    # for index,maxima_note in enumerate(maxima_note_list):
    #     print(maxima_note,bar_info_of_note[index])
    maxima_count = 0
    # for i in note_list_no_symbol:
    #     temp = ""
    #     print(i,maxima_note_list[maxima_count])
    #     if i is maxima_note_list[maxima_count] and maxima_count < len(maxima_note_list)-1:
    #         for j in list(i.pitches):
    #             temp += j.nameWithOctave + " "
    #         maxima_note.append(temp)
    #         maxima_count += 1
    #     else:
    #         maxima_note.append("")
    # maxima_count = 0
    counter = 0
    for i in coe_diff:
        temp = ""
        if i == maxima_list[maxima_count] and maxima_count < len(maxima_list)-1:
            maxima_count += 1
            maxima.append(i+0.1)
            print("diff and pitch is",i,note_list_no_symbol[counter].pitches,counter)
            for j in list(note_list_no_symbol[counter].pitches):
                temp += j.nameWithOctave + " "
            maxima_note.append(temp)
        else:
            maxima.append(0)
            maxima_note.append("--")
        maxima_limit.append(1/2)
        counter +=  1

    # print(np.array(index[show_bound_l:show_bound_r]).shape,np.array(slur_list).shape,np.array(coe_diff[show_bound_l:show_bound_r]).shape)
    plt.plot(np.array(index[show_bound_l:show_bound_r]), np.array(slur_list[show_bound_l:show_bound_r]),data=None, marker=None, color='red')
    plt.plot(np.array(index[show_bound_l:show_bound_r]), np.array(dot_list[show_bound_l:show_bound_r]),data=None, marker=None, color='green')
    plt.plot(np.array(index[show_bound_l:show_bound_r]), np.array(maxima[show_bound_l:show_bound_r]),data=None, marker=None, color='black')
    counter = 1
    for x, y in zip(np.array(index[show_bound_l:show_bound_r]), np.array(maxima[show_bound_l:show_bound_r])):
        label = "{:.2f}".format(y) + "," + maxima_note[counter]

        plt.annotate(label,  # this is the text
                     (x, y),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 1),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center
        counter += 1
    plt.plot(np.array(index[show_bound_l:show_bound_r]), np.array(maxima_limit[show_bound_l:show_bound_r]), data=None,
             marker=None, color='purple')
    plt.plot(np.array(index[show_bound_l:show_bound_r]),np.array(coe_diff[show_bound_l:show_bound_r]))
    #plot based on no. of note
    # plt.plot(np.array(bar_index).reshape(), np.array(coe_diff))
    #ploit based on no. of bar
    print(len(note_list))
    # print(coe_diff)
    plt.savefig("testgraph.png")
    plt.show()
    return


def getMusicProperties(x):
    s = '';
    t='';
    s = str(x.pitch) + ", " + str(x.duration.type) + ", " + str(x.duration.quarterLength);
    s += ", "
    if x.tie != None:
        t = x.tie.type
    s += t + ", " + str(x.pitch.ps) + ", " + str(x.octave) # + str(x.seconds)  # x.seconds not always there
    return s



def main():
    piecepath = ""
    num = input('Input A for CEG,B for BA:')
    num2 = ""
    if num is 'A':
        # piecepath = "../musicPiece/Polonaise_in_A_Major,_“Military_Polonaise”.xml"
        # piecepath = "../musicPiece/Minuet_in_G_Major.xml"
        # piecepath = "../musicPiece/Piano_Sonata_No._11.xml"
        piecepath = "../musicPiece/Prélude_in_G_Major.xml"

    if num is 'B':
        piecepath = "../musicPiece/Piano_Sonata_No._11.xml"
        piecepath = "../musicPiece/Prélude_in_G_Major.xml"
        # piecepath = "../musicPiece/Étude_in_C_Minor.mxl";
        num2 = input('Choose 1 for first layer,2 for second layer,3 for third layer:'
                     'Update: At first run: effective h = 1, window_length = 2*average_note_density')
        num3 = input('length by mean or bar(M/B)')


        global rate, show_bound_l, show_bound_r,by_mean
        if int(num2) == 1:
            rate = 2
            show_bound_l = 1
            show_bound_r = 220
        elif int(num2) == 2:
            rate = 1
            show_bound_l = 1
            show_bound_r = 220
        elif int(num2) == 3:
            rate = 1/2
            show_bound_l = 1
            show_bound_r = 220
        if num3 is 'M':
            by_mean = True
        else:
            by_mean = False
    try:

        s = getMusicPiece(piecepath)
        if num is 'A':
            piece_path = "../musicPiece"
            for root, dirs, files in os.walk(piece_path):
                for filename in files:

                    if filename.endswith('xml'):
                        print(filename)
                        sm = getMusicPiece(piece_path+'/'+filename)
                        find_tonality_by_bar(sm)
        elif num is 'B':
            segment_analysis(s)
        else:
            print("Invalid Input!")
    except converter.ConverterException as e:
        print(e)
        print("Error Reading Files")


if __name__ == "__main__":
    initialize()
    start = time.time()
    main()
    end = time.time()
    print("used time: ",end - start,"second")