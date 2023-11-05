import heapq
import pickle
import time
import numpy as np


def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph}
    travel_times = {node: float('inf') for node in graph}
    distances[start_node] = 0
    travel_times[start_node] = 0

    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_info in graph[current_node].items():
            length = edge_info['length']
            travel_time = edge_info['travel_time']

            new_distance = current_distance + length
            new_travel_time = travel_times[current_node] + travel_time

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                travel_times[neighbor] = new_travel_time
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return travel_times
    # return distances, travel_times


def cal(city, graph_dict):
    with open("../data/international/" + city + "_spt_np.pkl", 'wb') as file:
        num = len(graph_dict.keys())

        spts = np.zeros((num + 1, num + 1))

        for start_node in graph_dict.keys():
            travel_times = dijkstra(graph_dict, start_node)
            for end, spt in travel_times.items():
                spts[start_node][end] = spt


        # 분으로 환산
        spts /= 60
        spts = np.round(spts, 2)


        pickle.dump(spts, file)


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
