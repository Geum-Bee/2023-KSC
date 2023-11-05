import pickle
import networkx as nx


def update_edges_with_shortest_length(graph, city):
    edge_lengths = {}  # 엣지 길이를 저장하는 딕셔너리

    # 중복된 엣지들 중 가장 짧은 길이를 업데이트하기 위해 엣지 길이 정보 수집
    for u, v, attr in graph.edges(data=True):
        edge   = (u, v)
        length = attr['length']
        time   = attr['travel_time']
        if edge in edge_lengths:
            min_length         = min(edge_lengths[edge][0], length)
            edge_lengths[edge] = (min_length, time)
        else:
            edge_lengths[edge] = (length, time)

    # 중복되는 것 다 지웠는지 확인
    key    = edge_lengths.keys()
    set_key = len(set(list(key)))

    print(f"len(key)       = {len(key)}")
    print(f"len of set key = {set_key}")

    # 노드 정보 추출
    nodes_temp = []
    for key in edge_lengths.keys():
        u, v = key
        nodes_temp.append(u)
        nodes_temp.append(v)

    nodes = list(set(nodes_temp))

    # 새로운 그래프 생성
    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node)

    for key, value in edge_lengths.items():
        u, v             = key
        min_length, time = value
        G.add_edge(u, v, length=min_length, travel_time=time)

    print(G)



    # 경로 알아서 수정
    with open("../data/international/" + city + "_Digraph.pkl", 'wb') as file:
        pickle.dump(G, file)

    print(f"{city} graph saved!")


def get_graph(city):
    # 경로 알아서 수정
    with open("../data/international/" + city + ".pkl", "rb") as file:
        graph = pickle.load(file)

    update_edges_with_shortest_length(graph, city)


def main():
    # 경로 알아서 수정
    with open("../txts/international.txt", 'r') as txt:
        for line in txt:
            city = line.strip()

            get_graph(city)


main()