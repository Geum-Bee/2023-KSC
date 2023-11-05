import pickle
import osmnx as ox


# 경로 알아서 설정
txt_path = "../txts/international.txt"
with open(txt_path, 'r') as file:
    for line in file:
        city = line.strip()
        # 경로 알아서 설정
        pkl_path = "../data/international/" + city + ".pkl"
        with open(pkl_path, 'rb') as file1:
            graph = pickle.load(file1)
            print(graph)

            graph = ox.add_edge_speeds(graph)
            # calculate travel time (seconds) for all edges
            graph = ox.add_edge_travel_times(graph)

            w = 20
            k = 30
            node_wait_times = {}

            for node, degree in graph.degree():
                if degree <= 2:
                    wait_time = w
                else:
                    wait_time = w + k * (degree - 2)

                node_wait_times[node] = wait_time

            for s, t, key, data in graph.edges(keys=True, data=True):
                # 도착 vertex만 할당, 나중에 path에서 계산할때는 끝 vertex 시간 빼주기. 시작점과 끝점 시간은 빼주기로 했음
                wait_time = node_wait_times[t]
                data["travel_time"] += wait_time

        new_path = "../data/" + city + ".pkl"
        with open(new_path, 'wb') as file2:
            pickle.dump(graph, file2)

        print(f"{city} graph saved!\n")
