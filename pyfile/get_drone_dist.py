from scipy.spatial.distance import cdist
import pickle
import numpy as np


def latlon_to_xyz(lat, lon):
    """
    Convert latitude and longitude to 3D cartesian coordinates
    """
    R = 6371  # Earth radius in kilometers
    rad_lat = np.radians(lat)
    rad_lon = np.radians(lon)

    x = R * np.cos(rad_lat) * np.cos(rad_lon)
    y = R * np.cos(rad_lat) * np.sin(rad_lon)
    z = R * np.sin(rad_lat)

    return x, y, z


def cal(graph, city):
    node_data = {node: data for node, data in graph.nodes(data=True)}

    points     = []
    all_points = []

    for data in node_data.values():
        temp = [data['y'], data['x']]
        points.append(temp)

    points = np.array(points)


    points_xyz = np.array([latlon_to_xyz(lat, lon) for lat, lon in points])

    for point in points:
        given_point_xyz = np.array([latlon_to_xyz(*point)])
        # 거리 계산
        distances = cdist(given_point_xyz, points_xyz)[0]  # We get the first row since cdist returns a matrix
        distances *= 1000

        all_points.append(distances)

    all_points = np.round(all_points, 2)

    # 0번째 열에 0으로 가득찬 열 추가
    all_points = np.insert(all_points, 0, values=0, axis=1)

    # 0번째 행에 0으로 가득찬 행 추가
    all_points = np.insert(all_points, 0, values=0, axis=0)

    with open("../data/international/" + city + "_drone_dist.pkl", 'wb') as file:
        pickle.dump(all_points, file)


def main():
    with open("../txts/international.txt", 'r') as file1:
        for line in file1:
            city = line.strip()
            print(city)
            with open("../data/international/" + city + ".pkl", 'rb') as file2:
                G = pickle.load(file2)
            cal(G, city)


main()