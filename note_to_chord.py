import re
from itertools import chain,combinations
base_major_scale = ["C", "D", "E", "F", "G", "A", "B"]
base_interval_difference = [2,2,1,2,2,2,1]
natural_minor_adjustmnet = [0,0,1,0,0,1,1]
german_interval = [3,3,2,4]
french_interval = [2,4,2,4]
italian_interval = [6,2,4]
major_interval = [4,3]
minor_interval = [3,4]
diminished_interval = [3,3]
augmented_interval = [4,4]
root_to_interval = [0,2,4,5,7,9,11]
FLAT = '\u266D'
NATURAL = '\u266E'
SHARP = '\u266F'
DOUBLE_FLAT = '\U0001D12B'
DOUBLE_SHARP = '\U0001D12A'


def powerset(iterable,minimum_set_num,maximum_set_num):
    # powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(minimum_set_num,maximum_set_num+1))

def to_key(key,interval_difference,scale_difference):
    # for example to_key(C,3,2) returns Eb to_key(C,3,1) returns D#
    accidental = ""
    temp = base_interval_difference + base_interval_difference
    if len(key) > 1:
        if key[1] is 'b':
            accidental = FLAT
        elif key[1] is '#':
            accidental = SHARP
        if accidental is SHARP:
            interval_difference += 1
        elif accidental is FLAT:
            interval_difference -= 1
        key = key[0]


    result_key = base_major_scale[(base_major_scale.index(key)+scale_difference)%len(base_major_scale)]
    end_index = base_major_scale.index(result_key)
    start_index = base_major_scale.index(key)
    if base_major_scale.index(result_key) < base_major_scale.index(key):
        end_index += 7
    # print(result_key)
    # print(start_index,end_index)
    temp_difference = sum(temp[start_index:end_index])
    # print(temp_difference)
    while temp_difference > interval_difference:
        result_key = add_sign(result_key,FLAT)
        temp_difference -= 1
    while temp_difference < interval_difference:
        result_key = add_sign(result_key,SHARP)
        temp_difference += 1
    if accidental is not None:
        add_sign(result_key,accidental)

    result = check_for_change_accidental([result_key],0)
    return result[0]

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

def roman(x):
    # get roman and return arabic number
    dic = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        5: 'V',
        6: 'VI',
        7: 'VII',
    }
    return dic[x+1]


def slice_arr(arr,index1,index2):
    if index1 < index2:
        return arr[index1:index2]
    else:
        return arr[index1:] + arr[:index2]


def interval(note_list):
    base_note = []
    accidental = []
    index = []
    result = []
    for i in note_list:
        if len(i) > 1:
            base_note.append(i[:1])
            accidental.append(i[-1])
        else:
            base_note.append(i)
            accidental.append("")
    for j in base_note:
        index.append(base_major_scale.index(j))
    # print(index)

    for k in range(0,len(index)):
        # print(k)
        # print("xd")
        index1 = index[k % len(index)]
        index2 = index[(k+1) % len(index)]
        # print(index1,index2)
        # print(slice_arr(base_interval_difference,index1,index2))
        # print(base_interval_difference[index1:index2])
        result.append(sum(slice_arr(base_interval_difference,index1,index2)))
    # print(accidental)
    result = accidental_update_interval(accidental,result)
    return result

def accidental_update_interval(accidental,interval):
    for i in range(0,len(accidental)):
        if accidental[i] is '':
            continue
        else:
            if accidental[i] is '#':
                interval[i] -= 1
                interval[i-1] += 1
            elif accidental[i] is 'b':
                interval[i] += 1
                interval[i - 1] -= 1
    return interval


def sort_note(arr):
    base_note = []
    accidental = []
    number = []
    for i in arr:
        if len(i) > 1:
            base_note.append(i[:1])
            accidental.append(i[-1])
        else:
            base_note.append(i)
            accidental.append("")
        # base_note.sort(key=chr)
    for j in base_note:
        number.append(base_major_scale.index(j))
    # print(number)
    # print(base_note)
    # print(accidental)
    for (index,value) in enumerate(accidental):
        base_note[index] += value
    # print(base_note)
    return [x for _,x in sorted(zip(number,base_note))]


def is_subarray(mainlist, sublist):
    n = len(mainlist)
    m = len(sublist)
    # Two pointers to traverse the arrays
    i = 0
    j = 0
    # Traverse both arrays simultaneously
    while i < n and j < m:
        # If element matches
        # increment both pointers
        if mainlist[i] == sublist[j]:
            i += 1
            j += 1
            # If array B is completely
            # traversed
            if j == m:
                return True
                # If not,
        # increment i and reset j
        else:
            i = i - j + 1
            j = 0
    return False


def sub_list_index(sl,l):
    sll = len(sl)
    for ind in [i for i, e in enumerate(l) if e == sl[0]]:
        if l[ind:ind + sll] == sl:
            return ind


def get_base_note(notes, interval):
    temp = interval + interval
    tonality = str()
    base_key = str()
    note_num = int()
    chord_type = str()
    chord_name = str()
    if len(interval) == 3:
        note_num = 3
        chord_type = 'triad'
        sub_arr = []
        if is_subarray(temp, [3, 4]):
            tonality = "minor"
            base_key = notes[sub_list_index(minor_interval,temp)]
        elif is_subarray(temp, [4, 3]):
            tonality = "major"
            base_key = notes[sub_list_index(major_interval,temp)]
        elif is_subarray(temp, [3, 3]):
            tonality = "diminished"
            base_key = notes[sub_list_index(diminished_interval,temp)]
        elif is_subarray(temp, [4, 4]):
            tonality = "augmented"
            base_key = notes[sub_list_index(augmented_interval, temp)]
        else:
            tonality = None
            base_key = None
        # if len(sub_arr) > 0:
        #     occ = [i for i, a in enumerate(temp) if a == sub_arr[0]]
        #     print(occ)
        #     for b in occ:
        #         if temp[b:b + len(sub_arr)] == sub_arr:
        #             print(b)
        #             break
        #         if len(occ) - 1 == occ.index(b):
        #             print
        #             'NO SUBLIST'
        #             break

    elif len(interval) == 4:
        note_num = 4
        chord_type = 'seventh'
        if is_subarray(temp, [3, 4, 3]):
            tonality = "minor"
            base_key = notes[sub_list_index(minor_interval+[3],temp)]
        elif is_subarray(temp, [4, 3, 4]):
            tonality = "major"
            base_key = notes[sub_list_index(major_interval+[4],temp)]
        elif is_subarray(temp, [4, 3, 3]):
            tonality = "dominant"
            base_key = notes[sub_list_index(major_interval+[3], temp)]
        elif is_subarray(temp, [3, 3, 3]):
            tonality = "diminished"
            base_key = notes[sub_list_index(diminished_interval+[3],temp)]
        elif is_subarray(temp, [3, 3, 4]):
            tonality = "half_diminished"
            base_key = notes[sub_list_index(diminished_interval+[4],temp)]
        elif is_subarray(temp, [4, 4, 2]):
            tonality = "augmented"
            base_key = notes[sub_list_index(augmented_interval+[2], temp)]
        else:
            tonality = None
            base_key = None
    if is_subarray(temp,german_interval):
        note_num = 4
        tonality = "german VI"
        base_key = notes[sub_list_index(german_interval,temp)]
    elif is_subarray(temp,french_interval):
        note_num = 4
        tonality = "french VI"
        base_key = notes[sub_list_index(french_interval,temp)]
    elif is_subarray(temp,italian_interval):
        note_num = 3
        tonality = "italian VI"
        base_key = notes[sub_list_index(italian_interval,temp)]


    if is_subarray(temp,german_interval):
        note_num = 4
        chord_type = 'specific'
        chord_name = "german VI"
        base_key = notes[sub_list_index(german_interval,temp)]
    elif is_subarray(temp,french_interval):
        note_num = 4
        chord_type = 'specific'
        chord_name = "french VI"
        base_key = notes[sub_list_index(french_interval,temp)]
    elif is_subarray(temp,italian_interval):
        note_num = 3
        chord_type = 'specific'
        chord_name = "italian VI"
        base_key = notes[sub_list_index(italian_interval,temp)]
    # print(tonality)
    # print(base_key)
    # print(chord_type)
    return {'tonality': tonality, 'base_key': base_key,'note_num':note_num,'type':chord_type,'chord_name':chord_name}


def create_scale(accidentaled_key,tonality):
    # get key and generate scale with accidental for instance create_scale(G)
    # returns [G,A,B,C,D,E,F#]
    key = ""
    accidental = ""
    swap = ""
    if len(accidentaled_key) > 1:
        accidental = accidentaled_key[1]
        key = accidentaled_key[0]
    elif len(accidentaled_key) == 1:
        key = accidentaled_key
    counter = 0
    for keys in base_major_scale:
        if key in keys:
            swap = counter
        counter += 1
    scale = base_major_scale.copy()
    scale = changepos(scale, swap)
    interval_diff = changepos(base_interval_difference, swap)
    # print(scale)
    for i in range(0, 6):
        if interval_diff[i] < base_interval_difference[i]:
            interval_diff[i] += 1
            interval_diff[i + 1] -= 1
            scale[i + 1] += SHARP
        elif interval_diff[i] > base_interval_difference[i]:
            interval_diff[i] -= 1
            interval_diff[i + 1] += 1
            scale[i + 1] += FLAT
    # print(scale)
    if tonality is 'minor':
        for i in range(0,len(scale)):
            if natural_minor_adjustmnet[i] == 1:
                scale[i] += FLAT
                scale = check_for_change_accidental(scale,i)
    # print(scale)
    if accidental is '#':
        accidental_to_add = SHARP;
        for i in range(0, len(scale)):
            scale[i] += accidental_to_add
            scale = check_for_change_accidental(scale, i)
    elif accidental is 'b':
        accidental_to_add = FLAT;
        for i in range(0, len(scale)):
            scale[i] += accidental_to_add
            scale = check_for_change_accidental(scale, i)
    # print(scale)
    return scale


def add_sign(key,sign):
    return key+sign


def check_for_change_accidental(scale,i):
    if scale[i].endswith(SHARP + FLAT):
        scale[i] = scale[i].replace(SHARP + FLAT, NATURAL)
    elif scale[i].endswith(FLAT + SHARP):
        scale[i] = scale[i].replace(FLAT + SHARP, NATURAL)
    elif scale[i].endswith(FLAT + FLAT):
        scale[i] = scale[i].replace(FLAT + FLAT, DOUBLE_FLAT)
    elif scale[i].endswith(FLAT + SHARP):
        scale[i] = scale[i].replace(SHARP + SHARP, DOUBLE_SHARP)
    elif scale[i].endswith(NATURAL + SHARP) or scale[i].endswith(NATURAL + FLAT):
        scale[i] = scale[i].replace(NATURAL, "")
    return scale


def changepos(arr,pos):
    # for adding sharp or flat
    temparr = []
    for i in range(pos,pos+7):
        temparr.append(arr[i % 7])
    return temparr

def identical_list(l1,l2):
        for x, y in zip(l1, l2):
            if x != y:
                return False
        return len(l1) == len(l2)

def run(arr):
    interval_arr = []
    base_note_index = 0
    notes = str()
    # arr = list()
    major_triad_change_tonality = ["M","m","m","M","M","m","d"]
    minor_triad_change_tonality = ["m","d","M","m","m","M","M"]
    seventh_change_tonality = ["M7","m7","m7","M7","V7","m7","hd7"]
    alter_flat_chord_num = [2,6]
    alter_flat_interval = [1,8]

    # w, h = 7, 2;
    # final_tonality_determinant_mat = [["" for x in range(w)] for y in range(h)]
    # for i in range(0,len(final_tonality_determinant_mat)):
    #     if i == 0:
    #         import_list = major_change_tonality
    #     else:
    #         import_list = minor_change_tonality
    #     for j in range(0,len(final_tonality_determinant_mat[i])):
    #         if import_list[j] == "M":

    # pattern = re.compile("^[A-G][#b]?([,][A-G][#b]?)*([,][A-G][#b]?)$")
    # ask_for_input = True
    # while ask_for_input:
    #     notes = input("Enter notes (seperated by comma) (for instance:C,E,G,B) (maximum 10):")
    #     if not pattern.match(notes):
    #         print("input is not in valid format!")
    #     else:
    #         arr = notes.split(',')
    #
    #         if 10 >= len(arr) > 2:
    #             break
    #         else:
    #             print("Notes number not within limit! (3-10)")

    arr = sort_note(arr)
    arr, note_occurrence = count_note_num(arr)
    maximum = 0
    max_list = []
    # print(arr,note_occurrence)
    for index,value in enumerate(note_occurrence):
        # print(index,value)
        if value > maximum:
            maximum = value
            max_list = []
            max_list.append(arr[index])
        elif value == maximum:
            max_list.append(arr[index])
    # print(max_list,maximum)
    for i in list(powerset(arr,3,4)):
        note_set = list(i)
        arg_interval = []
        arg_major_tonality = []
        arg_minor_tonality = []
        arg_diminished_tonality = []
        arg_dominant_tonality = []
        interval_arr = interval(note_set)
        set_info = get_base_note(note_set, interval_arr)
        # print(set_info)
        reason = "tonic of the key"
        if maximum > 1:
            if len(max_list) > 1:
                tonal_center = set_info['base_key']
            else:
                tonal_center = max_list[0]
                reason = "mostly occuring notes"
        else:
            tonal_center = set_info['base_key']
        print("In note_set:",note_set)
        if set_info['base_key'] is None:
            print("There is no matching chord for notes:",note_set)
        else:
            if set_info['type'] is 'seventh':

                print("Chord Type:", set_info['tonality'], set_info['type'], "for notes:", note_set
                      ,"with tonal center:",tonal_center,"(",reason,")")

                # if set_info['tonality'] is 'minor':
                for index,tonality in enumerate(seventh_change_tonality):
                    if tonality is "M7":
                        # print({"roman":index+1,"tonality":"major",'key':to_key(set_info['base_key'],root_to_interval[index],index)})
                        arg_major_tonality.append({"roman": index + 1, "tonality": "major",
                                                   'key': to_key(set_info['base_key'], root_to_interval[index% len(root_to_interval)], index)})
                        arg_major_tonality.append({"roman": index + 3, "tonality": "minor",
                                                   'key': to_key(set_info['base_key'], root_to_interval[(index+2)% len(root_to_interval)], index+2)})
                    elif tonality is "m7":

                        arg_minor_tonality.append({"roman": index + 1, "tonality": "major",
                                                   'key': to_key(set_info['base_key'], root_to_interval[index % len(root_to_interval)], index)})
                        arg_minor_tonality.append({"roman": index + 3, "tonality": "minor",
                                                   'key': to_key(set_info['base_key'], root_to_interval[(index+2)% len(root_to_interval)], index+2)})
                    elif tonality is "V7":
                        arg_dominant_tonality.append({"roman": index + 1, "tonality": "major",
                                                      'key': to_key(set_info['base_key'], root_to_interval[index % len(root_to_interval)], index)})
                        arg_dominant_tonality.append({"roman": index + 3, "tonality": "minor",
                                                      'key': to_key(set_info['base_key'], root_to_interval[(index+2)% len(root_to_interval)], index+2)})
                    elif tonality is "hd7":
                        arg_diminished_tonality.append({"roman": index + 1, "tonality": "major",
                                                        'key': to_key(set_info['base_key'], root_to_interval[index % len(root_to_interval)],
                                                                      index)})
                        arg_diminished_tonality.append({"roman": index + 3, "tonality": "minor",
                                                        'key': to_key(set_info['base_key'], root_to_interval[(index+2)% len(root_to_interval)],
                                                                      index+2)})
                if set_info['tonality'] is 'major':
                    arr = arg_major_tonality
                elif set_info['tonality'] is 'minor':
                    arr = arg_minor_tonality
                elif set_info['tonality'] is 'dominant':
                    arr = arg_dominant_tonality
                else:
                    arr = arg_diminished_tonality
                # print(arr)
                for j in arr:
                    print("{} {} {} matched".format(j['key'], j['tonality'], roman((j['roman']-1)%7), note_set))
            elif set_info['type'] is 'triad':
                print("Chord Type:", set_info['tonality'], set_info['type'], "for notes:", note_set,"with tonal center:",tonal_center,"(",reason,")")
                # print(create_scale(set_info['base_key'],set_info['tonality']))
                # if set_info['tonality'] is 'minor':
                if set_info['tonality'] is 'augmented':
                    print("There is no match for any augmented triad in diatonic scale!")
                elif set_info['tonality'] is 'diminished':
                    # # print("xddddd")
                    # print(to_key(set_info['base_key'],1,1))
                    # # print('hahaha')
                    # print(to_key(set_info['base_key'],10,6))
                    print("{} {} {} matched".format(to_key(set_info['base_key'],1,1), 'major', roman(6), note_set))
                    print("{} {} {} matched".format(to_key(set_info['base_key'],10,6), "minor", roman(1), note_set))
                else:
                    if set_info['tonality'] is 'minor':
                        change_tonality_list = minor_triad_change_tonality
                    else:
                        change_tonality_list = major_triad_change_tonality

                    key_tonality = ""

                    for index,key in enumerate(create_scale(set_info['base_key'],set_info['tonality'])):

                        if change_tonality_list[index]=='M':
                            key_tonality = 'major'
                            arg_interval = major_interval
                        elif change_tonality_list[index]=='m':
                            key_tonality = 'minor'
                            arg_interval = minor_interval
                        elif change_tonality_list[index]=='d':
                            arg_interval = diminished_interval
                            continue
                        if key_tonality is 'major':
                            print("{} {} {} matched".format(key, "minor", roman((7 - index) % 7)+"+"))
                        print("{} {} {} matched".format(key, key_tonality, roman((7 - index) % 7)))
                    for index,chord_num in enumerate(alter_flat_chord_num):
                        key = to_key(set_info['base_key'],12-alter_flat_interval[index],7-chord_num+1)

                        print("{} {} {} matched".format(key, set_info['tonality'], FLAT + roman(chord_num-1)))
            if set_info['type'] is 'specific':
                print("Chord Type:", set_info['type'], "for notes:", note_set,
                      "with tonal center:", tonal_center, "(", reason, ")")
                print("{} {} matched".format(set_info['base_key'], set_info['chord_name']))


    if __name__ == "__main__":
        run()