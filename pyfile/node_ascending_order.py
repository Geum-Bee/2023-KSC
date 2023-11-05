import networkx as nx
import osmnx as ox
import pickle


def node_ascending_order(graph, ordering_num):
    # vertex ID 1부터 오름차순으로 만들기
    new_node_id_mapping = {}
    new_id = 1
    for old_node_id in graph.nodes():
        new_node_id_mapping[old_node_id] = new_id
        new_id += 1

    new_graph = nx.relabel_nodes(graph, new_node_id_mapping)

    print(f"original graph             = {graph}")
    print(f"node ascending order graph = {new_graph}")


    # 경로 알아서 바꾸기
    save_path = "../data/international/" + ordering_num + ".pkl"
    with open(save_path, 'wb') as file:
        pickle.dump(new_graph, file)


def main():
    ordering_num = 1

    # txt 파일 알아서 바꾸기
    with open("../txts/place_name_international.txt", "r", encoding='utf-8') as file:
        for line in file:
            place_name = line.strip()
            graph = ox.graph_from_place(place_name, network_type='drive')

            node_ascending_order(graph, str(ordering_num))

            ordering_num += 1


main()