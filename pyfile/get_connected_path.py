import pickle
import time
import sys


def get_connected_path(city, sampling_num):

    # 변경 가능
    # sampling_num = 6000

    with open("../segments/" + city + "_sp_segments_" + str(sampling_num) + ".txt", 'r') as sp_segs, \
            open("../segments/" + city + "_qp_segments_" + str(sampling_num) + ".txt", 'r') as qp_segs, \
            open("../data/international/" + city + "_spd.pkl", "rb") as file1, \
            open("../connected_path/" + city + "_connected_path_" + str(sampling_num) + ".txt", 'w') as result:

        spds = pickle.load(file1)

        for sp_seg, qp_seg in zip(sp_segs, qp_segs):
            sp_seg = eval(sp_seg)
            qp_seg = eval(qp_seg)

            if sp_seg[-1] == "same":
                # qp_seg 마지막 원소도 같으니 생략
                result.write("['same']" + '\n')
            else:
                if len(sp_seg) == 0 or len(qp_seg) == 0:
                    result.write("['no_balanced_path']" + '\n')
                else:
                    if len(sp_seg) == len(qp_seg):
                        min_balanced_distance = float('inf')
                        shortest_path_distance_and_nodes = []

                        for path1, path2 in zip(sp_seg, qp_seg):

                            for sp_vertex in path1:
                                for qp_vertex in path2:
                                    # 노드 사이의 거리는 Shortest Path로 구하자.
                                    shortest_distance = spds[sp_vertex][qp_vertex]

                                    if shortest_distance < min_balanced_distance:
                                        min_balanced_distance = shortest_distance
                                        start_node = sp_vertex
                                        end_node   = qp_vertex

                        shortest_path_distance_and_nodes.append(min_balanced_distance)
                        shortest_path_distance_and_nodes.append(start_node)
                        shortest_path_distance_and_nodes.append(end_node)

                        result.write(str(shortest_path_distance_and_nodes) + '\n')

                    else:
                        min_balanced_distance = float('inf')
                        shortest_path_distance_and_nodes = []
                        # # 길이가 다르므로 for문을 이렇게
                        for path1 in sp_seg:
                            for path2 in qp_seg:
                                for sp_vertex in path1:
                                    for qp_vertex in path2:
                                        # 노드 사이의 거리는 최단거리로 구하자.
                                        shortest_distance = spds[sp_vertex][qp_vertex]

                                        if shortest_distance < min_balanced_distance:
                                            min_balanced_distance = shortest_distance
                                            start_node = sp_vertex
                                            end_node = qp_vertex

                        shortest_path_distance_and_nodes.append(min_balanced_distance)
                        shortest_path_distance_and_nodes.append(start_node)
                        shortest_path_distance_and_nodes.append(end_node)

                        result.write(str(shortest_path_distance_and_nodes) + '\n')


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
            get_connected_path(city, sampling_num)

            end_time = time.time()

            elapse_time = (end_time - start_time) / 60
            print(f"elsaped time : {round(elapse_time, 2)} minutes")



if __name__ == "__main__":
    main()
