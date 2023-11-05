import pickle
import time
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def get_qpt(city):
    # 경로 알아서 수정
    with open("../data/international/" + city + "_Digraph.pkl", 'rb') as file1, open("../data/international/" + city + "_qpt.pkl",
                                                                                     'wb') as file2:
        G = pickle.load(file1)

        # 노드의 개수
        num_nodes = len(G.nodes())
        num = num_nodes + 1
        # 빈 2차원 넘파이 인접행렬 생성
        adjacency_matrix = np.zeros((num, num))

        for u, v, data in G.edges(data=True):
            adjacency_matrix[u][v] = data['travel_time']

        adjacency_matrix = csr_matrix(adjacency_matrix)

        qpt = []
        # 첫 번째 행 인덱스 때문에 무한대로 채워줌
        inf_list = [float('inf')] * num
        qpt.append(inf_list)

        for start in G.nodes():
            dist_matrix = dijkstra(adjacency_matrix, directed=True, return_predecessors=False,
                                   indices=start)
            qpt.append(dist_matrix)

        qpt = np.array(qpt)
        # 분으로 환산
        qpt /= 60

        qpt = np.round(qpt, 2)
        print(qpt)

        pickle.dump(qpt, file2)


def get_spd(city):
    # 경로 알아서 수정
    with open("../data/international/" + city + "_Digraph.pkl", 'rb') as file1, open("../data/international/" + city + "_spd.pkl",
                                                                                     'wb') as file2:
        G = pickle.load(file1)

        # 노드의 개수
        num_nodes = len(G.nodes())
        num = num_nodes + 1
        # 빈 2차원 넘파이 인접행렬 생성
        adjacency_matrix = np.zeros((num, num))

        for u, v, data in G.edges(data=True):
            adjacency_matrix[u][v] = data['length']

        adjacency_matrix = csr_matrix(adjacency_matrix)

        spd = []
        # 첫 번째 행 인덱스 때문에 무한대로 채워줌
        inf_list = [float('inf')] * num
        spd.append(inf_list)

        for start in G.nodes():
            dist_matrix = dijkstra(adjacency_matrix, directed=True, return_predecessors=False,
                                   indices=start)
            spd.append(dist_matrix)

        spd = np.array(spd)

        spd = np.round(spd, 2)
        print(spd)

        pickle.dump(spd, file2)


def main():
    # 경로 알아서 수정
    with open("../txts/international.txt", 'r') as file:
        for line in file:
            city = line.strip()
            print(city)

            # 빠름
            start_time = time.time()
            get_spd(city)
            get_qpt(city)
            end_time = time.time()

            elapse_time = (end_time - start_time) / 60
            print(f"elsaped time : {elapse_time} minutes")



main()
