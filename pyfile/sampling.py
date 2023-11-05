import networkx as nx
import pickle
import random
import time
import sys


def sampling(G, city, sampling_num):
    num_nodes  = G.number_of_nodes()

    # 수정 가능
    # sampling_num = 6000

    # sampling_rate = (num_nodes * num_nodes // 100) * sampling_num

    print(f"sampling number = {sampling_num}")
    print()

    with open("../sampling/" + city + "_spd_sample_" + str(sampling_num) + ".txt", "w") as file1, \
        open("../sampling/"  + city + "_sp_sample_"  + str(sampling_num) + ".txt", "w") as file2, \
        open("../sampling/"  + city + "_spt_sample_" + str(sampling_num) + ".txt", "w") as file3, \
        open("../sampling/"  + city + "_qpd_sample_" + str(sampling_num) + ".txt", "w") as file4, \
        open("../sampling/"  + city + "_qp_sample_"  + str(sampling_num) + ".txt", "w") as file5, \
        open("../sampling/"  + city + "_qpt_sample_" + str(sampling_num) + ".txt", "w") as file6, \
        open("../data/international/" + city + "_spd.pkl", 'rb') as file7, \
        open("../data/international/" + city + "_spt_np.pkl", 'rb') as file8, \
        open("../data/international/" + city + "_qpd_np.pkl", 'rb') as file9, \
        open("../data/international/" + city + "_qpt.pkl", 'rb') as file10:

        spds = pickle.load(file7)
        spts = pickle.load(file8)
        qpds = pickle.load(file9)
        qpts = pickle.load(file10)

        count = 0

        check_duplicatae = []

        while count < sampling_num:
            try:
                start_node = random.randint(1, num_nodes)
                end_node   = random.randint(1, num_nodes)

                while start_node == end_node:
                    end_node = random.randint(1, num_nodes)

                if (start_node, end_node) in check_duplicatae:
                    continue
                else:
                    check_duplicatae.append((start_node, end_node))

                shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
                quickest_path = nx.shortest_path(G, start_node, end_node, weight='travel_time')

                if len(shortest_path) < 5 or len(quickest_path) < 5:
                    continue

                shortest_distance  = spds[start_node][end_node]
                quickest_distance  = qpds[start_node][end_node]
                shortest_path_time = spts[start_node][end_node]
                quickest_path_time = qpts[start_node][end_node]


                # 체크용
                # print(shortest_distance)
                # print(quickest_distance)
                # print(shortest_path_time)
                # print(quickest_path_time)

                file1.write(str(round(shortest_distance, 2)) + '\n')
                file2.write(str(shortest_path) + '\n')
                file3.write(str(round(shortest_path_time, 2)) + '\n')
                file4.write(str(round(quickest_distance, 2)) + '\n')
                file5.write(str(quickest_path) + '\n')
                file6.write(str(round(quickest_path_time, 2)) + '\n')

    #             print("shortest")
    #             print(shortest_path)
    #             print(f"{round(shortest_distance, 2)} m")
    #             print(f"{round(shortest_path_time, 2)} minutes")
    #             print("============================================================================================")
    #             print("quickest")
    #             print(quickest_path)
    #             print(f"{round(quickest_distance, 2)} m")
    #             print(f"{round(quickest_path_time, 2)} minutes")
    #             print()

                count += 1

            except:
                continue


def main():
    if len(sys.argv) >= 2:
        sampling_num = int(sys.argv[1])
        print("매개변수:", sampling_num)
    else:
        print("매개변수가 제공되지 않았습니다.")


    with open("../txts/international.txt", 'r') as file1:
        for line in file1:
            city = line.strip()
            print(city)
            with open("../data/international/" + city + "_Digraph.pkl", 'rb') as file2:
                graph = pickle.load(file2)

                start_time = time.time()

                # 1 프로만 샘플링
                # sampling_num = 1
                sampling(graph, city, sampling_num)

                end_time = time.time()

                elapse_time = (end_time - start_time) / 60
                print(f"elsaped time : {round(elapse_time, 2)} minutes")



if __name__ == "__main__":
    main()
