import pickle
import time
import sys


def is_balanced_path(city, sampling_num):

    # 변경 가능
    # sampling_num = 6000


    connect_path   = "../connected_path/" + city + "_connected_path_" + str(sampling_num) + ".txt"
    sp_sample      = "../sampling/" + city + "_sp_sample_"  + str(sampling_num) + ".txt"
    qp_sample      = "../sampling/" + city + "_qp_sample_"  + str(sampling_num) + ".txt"
    spd_sample     = "../sampling/" + city + "_spd_sample_" + str(sampling_num) + ".txt"
    qpd_sample     = "../sampling/" + city + "_qpd_sample_" + str(sampling_num) + ".txt"
    spt_sample     = "../sampling/" + city + "_spt_sample_" + str(sampling_num) + ".txt"
    qpt_sample     = "../sampling/" + city + "_qpt_sample_" + str(sampling_num) + ".txt"
    spd_path       = "../data/international/" + city + "_spd.pkl"
    qpd_path       = "../data/international/" + city + "_qpd_np.pkl"
    spt_path       = "../data/international/" + city + "_spt_np.pkl"
    qpt_path       = "../data/international/" + city + "_qpt.pkl"

    # degree = dict(G.degree())

    with open(connect_path, 'r') as connection, \
        open(spd_path, 'rb') as f1, \
        open(qpd_path, 'rb') as f2, \
        open(spt_path, 'rb') as f3, \
        open(qpt_path, 'rb') as f4, \
        open(sp_sample, 'r') as sp_file, \
        open(qp_sample, 'r') as qp_file, \
        open(spd_sample, 'r') as spd_samp, \
        open(qpd_sample, 'r') as qpd_samp, \
        open(spt_sample, 'r') as spt_samp, \
        open(qpt_sample, 'r') as qpt_samp:

        spds = pickle.load(f1)
        qpds = pickle.load(f2)
        spts = pickle.load(f3)
        qpts = pickle.load(f4)

        s_ls        = [eval(line.strip()) for line in sp_file.readlines()]
        q_ls        = [eval(line.strip()) for line in qp_file.readlines()]
        spd_samp_ls = [eval(line.strip()) for line in spd_samp.readlines()]
        qpd_samp_ls = [eval(line.strip()) for line in qpd_samp.readlines()]
        spt_samp_ls = [eval(line.strip()) for line in spt_samp.readlines()]
        qpt_samp_ls = [eval(line.strip()) for line in qpt_samp.readlines()]

        # print(s_ls)

        line_count = 0

        same_path_num = 0
        no_balanced_path_num = 0
        balanced_path_num = 0

        for line in connection:
            line = eval(line.strip())
            if line[0] == 'same':
                same_path_num += 1
                line_count += 1
            elif line[0] == 'no_balanced_path':
                no_balanced_path_num += 1
                line_count += 1
            else:
                start_node = s_ls[line_count][0]
                mid_1_node = line[1]
                mid_2_node = line[2]
                end_node   = q_ls[line_count][-1]

                sp_dist  = spds[start_node][mid_1_node]
                mid_dist = line[0]
                qp_dist  = qpds[mid_2_node][end_node]

                # print(f"s = {start_node}")

                # print(sp_dist)
                # print(mid_dist)
                # print(qp_dist)

                sp_time  = spts[start_node][mid_1_node]
                # Shortest Path로 connected path를 구했기 때문에 mid_time은 spts에서 구함
                mid_time = spts[mid_1_node][mid_2_node]
                qp_time  = qpts[mid_2_node][end_node]

                # # spts는 모두 초로 되어있기 때문에 분으로 환산해줘야함.
                # sp_time  /= 60
                # mid_time /= 60

                balanced_dist = round(sp_dist + mid_dist + qp_dist, 2)
                balanced_time = round(sp_time + mid_time + qp_time, 2)

                # 계산실수 체크용
                # print(balanced_dist)
                # print(balanced_time)
                #
                # print(spd_samp_ls[line_count])
                # print(qpd_samp_ls[line_count])
                # print(qpt_samp_ls[line_count])
                # print(spt_samp_ls[line_count])

                if spd_samp_ls[line_count] < balanced_dist < qpd_samp_ls[line_count] and qpt_samp_ls[line_count] < balanced_time < spt_samp_ls[line_count]:
                    balanced_path_num += 1
                else:
                    no_balanced_path_num += 1

                line_count += 1


    print(f"line counted : {line_count}")
    print(f"Sum of Pahts : {same_path_num + no_balanced_path_num + balanced_path_num}")
    print(f"Same Paths : {round(same_path_num / line_count * 100, 2)}%")
    print(f"No Balanced Paths : {round(no_balanced_path_num / line_count * 100, 2)}%")
    print(f"Balanced Paths : {round(balanced_path_num / line_count * 100, 2)}%")
    print("==========================================================================")



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

            is_balanced_path(city, sampling_num)

            end_time = time.time()

            elapse_time = (end_time - start_time) / 60
            print(f"elsaped time : {round(elapse_time, 2)} minutes")



if __name__ == "__main__":
    main()