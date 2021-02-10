from musicXML import *
from spiral_method import *
import matplotlib.pyplot as plt
import time
import scipy.signal as signal
structure_arr = list()
rate = float
show_bound_r = int
show_bound_l = int

def initialize():
    global structure_arr
    structure_arr = initialize_spiral_structure()

def find_tonality_by_bar(s):
    segment = []
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

    print(s,get_bar_num(s))
    for i in range(0,get_bar_num(s)):
        measure = s.measure(i)
        temp = []
        if len(measure.parts[0].pitches) == 0:
            continue
        print("haha , bar ",i ,"  ",list(measure.parts[0].flat.notes),list(measure.parts[1].flat.notes))
        for j in measure.parts[0].flat.notes:
            temp.append(j)
        for k in measure.parts[1].flat.notes:
            temp.append(k)
        segment.append(temp)
        # print("\n\nhaha upper part",measure.parts[0].pitches,"\n\n lower part",measure.parts[1].pitches,"\n\nbar :",i, " segment:",segment[i])



    # for i in structure_arr:
    #     print(i['note'],i['major_spiral_array'].pitch)


    # print(len(segment))
    # for j in segment[2]:
    #     print(j)
    counter = 0
    total_note = 0
    for index,i in enumerate(segment):

        notes,duration = get_segment_info(i)
        print("In segment ",index,":")
        run_find_tonal_center(notes,duration)
        notes = []
        duration = []
        counter += 1
        # if counter > 18:
        #     break

        analysis(segment[index])
        total_note += len(segment)

    print("total note is:",total_note)
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

def get_bar_num(s):
    count = 0
    have_exist_condition = 0
    while True:
        measure = s.measure(count)
        # print(measure.parts[0].pitches)
        if len(measure.parts[0].pitches) == 0 and have_exist_condition:
            break
        else:
            have_exist_condition = 1
        count += 1
    return count

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
        if i.beat >= beat:
            bar.append(i)
        elif beat > i.beat:
            # print(beat,i.beat)
            bar_count += 1
            bar_index.append(bar_count)
            have_set_bar_index = False
            print("Bar above:",bar_count)
            bar.clear()
            bar.append(i)
        if have_set_bar_index:
            bar_index.append(0)
        have_set_bar_index = True
        beat = i.beat
        if isinstance(i,note.Rest):
            continue
        if isinstance(i,harmony.ChordSymbol):
            continue
        if isinstance(i,harmony.NoChord):
            continue

        # note_list_no_symbol.append(i)
        bar_info_of_note.append(bar_count)

        if(unit_time > average_note_density or len(note_list) - unit_time < average_note_density):
            notes_before_bound = note_list[unit_time-average_note_density:unit_time]
            notes_after_bound = note_list[unit_time:unit_time+average_note_density]
            # print(notes_before_bound)
            # print(notes_after_bound)
            if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_before_bound):
                if any(isinstance(x, note.Note) or isinstance(x, chord.Chord) for x in notes_after_bound):
                    notes_before,duration_before = get_segment_info(notes_before_bound)
                    notes_after,duration_after = get_segment_info(notes_after_bound)
                    coe_diff.append(run_find_segment(notes_before,duration_before,notes_after,duration_after))
                    note_list_no_symbol.append(i)
                    index.append(len(coe_diff))



            # print(bar, "yo")

        print("In index :", counter,"note_num:",len(note_list_no_symbol),"algo_run_though",len(coe_diff)+buffer, type(i), i.pitches, i.beat, list(i.pitches)[0].nameWithOctave,slur_list[counter])



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

    a = np.array(coe_diff);
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
        piecepath = "../musicPiece/Piano_Sonata_No._11.xml"
    if num is 'B':
        piecepath = "../musicPiece/Piano_Sonata_No._11.xml"
        # piecepath = "../musicPiece/Étude_in_C_Minor.mxl";
        num2 = input('Choose 1 for first layer,2 for second layer,3 for third layer:'
                     'Update: At first run: effective h = 1, window_length = 2*average_note_density')
        global rate, show_bound_l, show_bound_r
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
            show_bound_l = 160
            show_bound_r = 185
    try:

        s = getMusicPiece(piecepath)
        # print(dir(s.spanners))
        count = 0
        for i in s.flat.notes:
            count += 1
            if count > 500:
                break
            # print(i,"xdd",i.articulations)


        ryans = corpus.search('ryansMammoth')
        mozart = corpus.search('mozart')
        quartet = mozart.search('Quartet No.1 in G Major');

        highland = ryans.search('Highland Regiment')
        quartetparsed = quartet[0].parse();
        highlandParsed = highland[0].parse()

        # highlandParsed.show()
        high_fragment = highlandParsed.measures(0,8)
        s_fragment = s.measures(0,8)

        highIterator = quartetparsed.recurse()
        sIterator = s_fragment.recurse()

        sslur = sIterator.spanners
        highslur = highIterator.getElementsByClass('Slur')
        higher = 0
        lower = 0
        same = 0
        count = 0

        for sl in sslur:
            print(sl,len(sl),sl.beat)
            count += 1
            if count > 50:
                break
        count  = 0
        print("hehehe")
        # for sl in highslur:
        #     print(sl,sl.beat,sl.getFirst(),sl.getLast())
        #     # print(sl)
        #     # if (count > 10):
        #     #     break
        #     count += 1
            # firstNote = sl.getFirst()
            # lastNote = sl.getLast()
            # psDiff = lastNote.pitch.ps - firstNote.pitch.ps
            # if psDiff > 0:
            #     higher += 1
            # elif psDiff < 0:
            #     lower += 1
            # else:
            #     same += 1
        # print(count)
        # s.measure(0,8).show()


        for i in s.spanners.notes:
            print(i)
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

        a = s.getSpannerSites()
        print(a)
        # s.measure(200).show()

        if num is 'A':
            find_tonality_by_bar(s)
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