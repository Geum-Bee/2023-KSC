import heapq
import pickle
import time
import numpy as np


def dijkstra(graph, start_node):
    # 초기화: 각 노드까지의 최단 travel_time과 length를 무한대로 설정하고, 시작 노드의 travel_time과 length는 0으로 설정한다.
    travel_times = {node: float('inf') for node in graph}
    lengths = {node: float('inf') for node in graph}
    travel_times[start_node] = 0
    lengths[start_node] = 0

    # 우선순위 큐를 사용하여 노드를 방문 순서대로 처리한다.
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_time, current_node = heapq.heappop(priority_queue)

        # 이미 처리한 노드인 경우 스킵
        if current_time > travel_times[current_node]:
            continue

        # 인접한 노드를 검사하면서 최단 travel_time과 length를 업데이트한다.
        for neighbor, edge_info in graph[current_node].items():
            length = edge_info['length']
            travel_time = edge_info['travel_time']

            new_time = current_time + travel_time
            new_length = lengths[current_node] + length

            if new_time < travel_times[neighbor]:
                travel_times[neighbor] = new_time
                lengths[neighbor] = new_length
                heapq.heappush(priority_queue, (new_time, neighbor))

    # return travel_times, lengths4
    return lengths


def cal(city, graph_dict):
    with open("../data/international/" + city + "_qpd_np.pkl", 'wb') as file:
        num = len(graph_dict.keys())

        qpds = np.zeros((num + 1, num + 1))


        for start_node in graph_dict.keys():
            lengths = dijkstra(graph_dict, start_node)
            for end, qpd in lengths.items():
                qpds[start_node][end] = qpd

        qpds = np.round(qpds, 2)


        pickle.dump(qpds, file)


def get_nested_dict_graph(city):
    with open("../data/international/" + city + "_Digraph.pkl", 'rb') as file:
        G = pickle.load(file)

    # 그래프를 딕셔너리로 변환
    graph = {}
    for node in G.nodes():
        edges_data = {}
        for neighbor in G.successors(node):
            edge_data = G.get_edge_data(node, neighbor)
            edges_data[neighbor] = edge_data
        graph[node] = edges_data

    return graph


def main():
    with open("../txts/international.txt", 'r') as file:
        for line in file:
            city = line.strip()
            print(city)

            start_time = time.time()

            graph_dict = get_nested_dict_graph(city)
            cal(city, graph_dict)

            end_time = time.time()

            elapse_time = (end_time - start_time) / 60
            print(f"elsaped time : {elapse_time} minutes")


main()
