import copy
import time
import sys


def get_segments(city, sampling_num):
    # 변경해야함
    # sampling_num   = 6000
    sp_txt         = "../sampling/" + city + "_sp_sample_"   + str(sampling_num) + ".txt"
    qp_txt         = "../sampling/" + city + "_qp_sample_"   + str(sampling_num) + ".txt"
    sp_seg         = "../segments/" + city + "_sp_segments_" + str(sampling_num) + ".txt"
    qp_seg         = "../segments/" + city + "_qp_segments_" + str(sampling_num) + ".txt"

    line_count       = 0
    same_path        = 0
    no_balanced_path = 0
    case_1           = 0
    case_2_3         = 0
    case_4           = 0

    with open(sp_txt, 'r') as file1, open(qp_txt, 'r') as file2, open(sp_seg, 'w') as file3, open(qp_seg, 'w') as file4:
        for sp, qp in zip(file1, file2):
            sp = sp.strip()
            qp = qp.strip()

            line_count += 1

            if sp == qp:
                sp = eval(sp)
                qp = eval(qp)

                sp.append("same")
                qp.append("same")

                file3.write(str(sp) + '\n')
                file4.write(str(qp) + '\n')
                same_path += 1

            else:
                sp = eval(sp)
                qp = eval(qp)

                copy_sp = copy.deepcopy(sp)
                copy_qp = copy.deepcopy(qp)

                for i, sp_val in enumerate(copy_sp):
                    for j, qp_val in enumerate(copy_qp):
                        if sp_val == qp_val:
                            copy_sp[i] = 0
                            copy_qp[j] = 0

                sp_segments = []
                sp_segment  = []

                sp_zero_lists = []
                sp_zero_list  = []

                for value in copy_sp:
                    if value == 0:
                        sp_zero_list.append(value)

                        if sp_segment:
                            sp_segments.append(sp_segment)
                            sp_segment = []
                    else:
                        sp_segment.append(value)

                        if sp_zero_list:
                            sp_zero_lists.append(sp_zero_list)
                            sp_zero_list = []

                if sp_segment:
                    sp_segments.append(sp_segment)

                if sp_zero_list:
                    sp_zero_lists.append(sp_zero_list)

                qp_segments = []
                qp_segment  = []

                qp_zero_lists = []
                qp_zero_list  = []

                for value in copy_qp:
                    if value == 0:
                        qp_zero_list.append(value)

                        if qp_segment:
                            qp_segments.append(qp_segment)
                            qp_segment = []
                    else:
                        qp_segment.append(value)

                        if qp_zero_list:
                            qp_zero_lists.append(qp_zero_list)
                            qp_zero_list = []

                if qp_segment:
                    qp_segments.append(qp_segment)

                if qp_zero_list:
                    qp_zero_lists.append(qp_zero_list)

                file3.write(str(sp_segments) + '\n')
                file4.write(str(qp_segments) + '\n')

                # 체크용
                # print(sp)
                # print(sp_segments)
                # print(sp_zero_lists)
                # print(qp)
                # print(qp_segments)
                # print(qp_zero_lists)
                #
                # is_same = len(sp_segments) == len(qp_segments)
                #
                # if not is_same:
                #     print("False")


                if len(sp_segments) == 0 or len(qp_segments) == 0:
                    no_balanced_path += 1

                elif len(sp_segments) == 2 and len(qp_segments) == 2 and (len(sp_segments[0]) == 1 and
                                                                          len(sp_segments[-1]) == 1 and
                                                                          len(qp_segments[0]) == 1 and
                                                                          len(qp_segments[-1]) == 1):
                    case_4 += 1
                elif len(sp_zero_lists) == 2 and len(qp_zero_lists) == 2:
                    case_2_3 += 1
                else:
                    case_1 += 1


    print(f"All Paths        : {line_count}")
    print(f"No Balanced Path : {no_balanced_path}")
    print(f"Same Path        : {same_path}")
    print(f"case-1           : {case_1}")
    print(f"case-2-3         : {case_2_3}")
    print(f"case-4           : {case_4}")
    # 체크용
    print(f"All Sum          : {no_balanced_path + same_path + case_1 + case_2_3 + case_4}")
    print()
    print(f"{round(no_balanced_path / line_count * 100, 2)} {round(same_path / line_count * 100, 2)} {round(case_1 / line_count * 100, 2)} "
          f"{round(case_2_3 / line_count * 100, 2)} {round(case_4 / line_count * 100, 3)}")
    print()


def main():
    if len(sys.argv) >= 2:
        sampling_num = int(sys.argv[1])
    #     print("매개변수:", sampling_num)
    # else:
    #     print("매개변수가 제공되지 않았습니다.")
    with open("../txts/international.txt", 'r') as file1:
        for line in file1:
            city = line.strip()
            print(city)

            start_time = time.time()
            get_segments(city, sampling_num)

            end_time = time.time()

            elapse_time = (end_time - start_time) / 60
            print(f"elsaped time : {round(elapse_time, 2)} minutes")


if __name__ == "__main__":
    main()
