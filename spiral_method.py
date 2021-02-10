# import pandas as np
import numpy as np
import math
import matplotlib

major_key_ratio = [0.6025,0.2930,0.1145]
minor_key_ratio = [0.6011,0.2121,0.1868]
# major_key_ratio = minor_key_ratio = [0.5353,0.2743,0.1904]
spiral_radius = 1
spiral_height = math.sqrt(2/15)
height_translation = np.array([[0,0,spiral_height]]).reshape(3,1)
transformation_matrix = np.array([[0,1,0],[-1,0,0],[0,0,1]])
structure_arr = []
spiral_index = {
        -8:['F-'],
        -7:['C-'],
        -6:['G-'],
        -5:['D-'],
        -4:['A-'],
        -3:['E-'],
        -2:['B-'],
        -1:['F'],
        0:['C'],
        1:['G'],
        2:['D'],
        3:['A'],
        4:['E'],
        5:['B'],
        6:['F#'],
        7:['C#'],
        8:['G#'],
        9:['D#'],
        10:['A#'],
        11:['E#'],
        12:['B#'],
    }


class SpiralArray:
    def __init__(self, k , m, name):
        self.k = k
        self.m = m
        self.pitch = np.zeros((1,3))
        self.chord = np.zeros((1, 3))
        self.key = np.zeros((1,3))
        self.name = name
        self.set_pitch()
        self.set_chord()
        self.set_key()

    def set_pitch(self):
        self.pitch = np.array([[spiral_radius*math.sin(self.k*math.pi/2),spiral_radius*math.cos(self.k*math.pi/2),self.k*spiral_height]])
        self.pitch = self.pitch.reshape(3,1)

    def set_chord(self):
        perfect_fifth_pitch = np.add(np.matmul(transformation_matrix,self.pitch),height_translation)
        if self.m == "M":
            third_pitch = np.add(self.pitch,height_translation * 4)
        else:
            third_pitch = np.subtract(perfect_fifth_pitch,height_translation * 4)
        temp = np.append(self.pitch,np.append(perfect_fifth_pitch,third_pitch,axis=1),axis=1).transpose()
        if self.m == "M":
            self.chord = np.matmul(np.array([major_key_ratio]),temp)
        elif self.m == "m":
            self.chord = np.matmul(np.array([minor_key_ratio]), temp)
        self.chord = self.chord.reshape(3,1)

    def set_key(self):
        dominant_chord = np.add(np.matmul(transformation_matrix,self.chord),height_translation)
        subdominant_chord = np.add(np.matmul(np.linalg.inv(transformation_matrix),self.chord),-1*height_translation)
        temp = np.append(self.chord,np.append(dominant_chord,subdominant_chord,axis=1),axis=1).transpose()
        self.key = np.matmul(np.array([major_key_ratio]), temp)



def generate_coe(pitch_list, duration_list):
    result = []
    for i in range(0,3):
        arr = [duration_list[j]*pitch_list[j][i] for j in range(0,len(pitch_list))]
        result.append(float(sum(arr)/sum(duration_list)))
    return result

def run_find_segment(notes_bef,duration_bef,notes_aft,duration_aft):
    pitch_list_bef = []
    duration_list_bef = []
    pitch_list_aft = []
    duration_list_aft = []
    spiral_arr_list_bef = []
    spiral_arr_list_aft = []
    # print(len(notes_bef),len(duration_bef),len(notes_aft),len(duration_aft))
    for j in notes_bef:
        for index, value in spiral_index.items():
            if j in value:
                # print(index,j,value)
                spiral_arr_list_bef.append(SpiralArray(index, "M", j))
    for j in notes_aft:
        for index, value in spiral_index.items():
            if j in value:
                # print(index,j,value)
                spiral_arr_list_aft.append(SpiralArray(index, "M", j))
    for index,value in enumerate(spiral_arr_list_bef):
        pitch_list_bef.append(value.pitch)
        duration_list_bef.append(duration_bef[index])
    coe_bef = generate_coe(pitch_list_bef,duration_list_bef)
    for index,value in enumerate(spiral_arr_list_aft):
        pitch_list_aft.append(value.pitch)
        duration_list_aft.append(duration_aft[index])
    coe_aft = generate_coe(pitch_list_aft,duration_list_aft)

    return np.linalg.norm(np.array(coe_bef) - np.array(coe_aft))


def run_find_tonal_center(notes,duration):
    print(notes)
    pitch_list = []
    duration_list = []
    spiral_arr_list = []
    for j in notes:
        for index, value in spiral_index.items():
            if j in value:
                # print(index,j,value)
                spiral_arr_list.append(SpiralArray(index,"M",j))

    test2 = [1 / 4, 1 / 4, 1 / 8, 1 / 4]
    print(duration)
    # spiral_arr_list = [SpiralArray(2,"M",'D'),SpiralArray(6,"M",'F#'),SpiralArray(3,"M",'A')] // for testing only
    # print(np.append(np.append(test[1].pitch, test[0].pitch, axis=1), test[2].pitch, axis=1))
    # print(np.sum(np.append(np.append(test[1].pitch, test[0].pitch, axis=1), test[2].pitch, axis=1), axis=1))

    for index,value in enumerate(spiral_arr_list):
        pitch_list.append(value.pitch)
        duration_list.append(duration[index])
        # calculate ce
        coe = generate_coe(pitch_list,duration_list)
        major_score = []
        minor_score = []
        minor_key = []
        major_key = []
        # loop with initialized spiral Array of keys

        for i in structure_arr:
            minor_diff = np.array(coe) - np.array(i['minor_spiral_array'].key)
            major_diff = np.array(coe) - np.array(i['major_spiral_array'].key)
            major_score.append(np.linalg.norm(major_diff))
            major_key.append(i['note']+"major")
            minor_score.append(np.linalg.norm(minor_diff))
            minor_key.append(i['note']+"minor")
        only_major = False
        # some grouping and calculation to rank the result
        if not only_major:
            major_key += minor_key
            major_score += minor_score
        sorted_key = [x for _, x in sorted(zip(major_score, major_key))]
        major_score.sort()
        counter = 0
        old_score = major_score[0]
        old_result = ""
        endoflist = False
        initial = 0
        # print(major_score)
        # print(sorted_key)
        while not endoflist:
            if major_score[initial] == major_score[initial+1]:
                sorted_key[initial] += sorted_key.pop(initial+1)
                major_score.pop(initial+1)
            initial += 1
            try:
                major_score[initial+1]
            except IndexError:
                endoflist = True
        # print(major_score)
        # print(sorted_key)
    print("after full run on run(),the rank of key are listed as followed:")
    for index2,result in enumerate(sorted_key):
        # print(result)
        if counter > 4:
            break
        # if old_score == major_score[index2]:
        #     old_result = sorted_key[index2-1]+result
        # else:
        #     counter += 1
        #     if old_result is not "":
        #         print(old_result," with similarity score:",old_score)
        #         old_result = ""
        #     else:
        #         print(result," with similarity score:",old_score)
        # old_score = major_score[index2]
        print(result," with similarity score:",major_score[index2])
        counter += 1


def  analysis_boundaries(notes,duration):
    pitch_list = []
    duration_list = []
    spiral_arr_list = []
    for j in notes:
        for index, value in spiral_index.items():
            if j in value:
                # print(index,j,value)
                spiral_arr_list.append(SpiralArray(index, "M", j))
    test2 = [1 / 4, 1 / 4, 1 / 8, 1 / 4]
    # print(duration)
    # spiral_arr_list = [SpiralArray(2,"M",'D'),SpiralArray(6,"M",'F#'),SpiralArray(3,"M",'A')] // for testing only
    # print(np.append(np.append(test[1].pitch, test[0].pitch, axis=1), test[2].pitch, axis=1))
    # print(np.sum(np.append(np.append(test[1].pitch, test[0].pitch, axis=1), test[2].pitch, axis=1), axis=1))

    for index, value in enumerate(spiral_arr_list):
        pitch_list.append(value.pitch)
        duration_list.append(duration[index])
        # print("after ", index + 1, "th note (pitch:", value.name,"duration:",duration_list[index],
        #       "), the rank of key are listed as follow")
    return generate_coe(pitch_list, duration_list)

        # major_score = []
        # minor_score = []
        # minor_key = []
        # major_key = []



def initialize_spiral_structure():
    spiral_key = ['Gb','Db','Ab','Eb','Bb','F','C','G','D','A','E','B','F#','C#','G#','D#','A#']
    global structure_arr
    # print("xd")
    for i in spiral_key:
        for index,value in spiral_index.items():
            if i in value:
                major_key = SpiralArray(index,"M",i)
                minor_key = SpiralArray(index,"m",i)
                structure_arr.append({"note":i,"minor_spiral_array":minor_key,"major_spiral_array":major_key})

    # F3.set_key(np.append())

    # return structure_arr
