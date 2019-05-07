import math
import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt


# Select which plots to generate in the below dictionary
def plots_to_generate():
    return {
        "Avg Number of Vehicles Per Road": avg_num_of_vehicles_per_road,
        "Avg Percentage Occupancy": avg_occupancy_per_road,
        "Avg Waiting Time": avg_speed_per_road,
        "Num Roads occupied": num_roads_occupied,
        "Num Vehicles": num_vehicles_in_network,
        "Num Stopped Vehicles": num_stopped_vehicles_in_network,
        "Percentage of Stopped Vehicles": percent_stopped_vehicles_in_network,
        "Avg Number of Neighbors Per Vehicle": avg_num_neighbors_per_vehicle,
        "Percentage of Vehicle with Zero Neighbors": percent_without_neighbors,
        "Average Percent of the Network a Vehicle can communicate with": avg_percent_of_network_communicatable_by_vehicle,
    }


# Plot generation methods
def avg_num_of_vehicles_per_road():
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()
    max_num = []
    min_num = []
    avg_num = []
    for t in fcd.findall("timestep"):
        roads = {}
        for v in t.findall("vehicle"):
            current_road = v.get("lane").split("_")[0]
            if current_road in roads:
                roads[current_road] += 1
            else:
                roads[current_road] = 1
        vals = [i for r, i in roads.items()]
        if len(vals):
            max_num.append(max(vals))
            min_num.append(min(vals))
            avg_num.append(sum(vals) / len(vals))
        else:
            max_num.append(0)
            min_num.append(0)
            avg_num.append(0)
    x = range(len(avg_num))
    plt.plot(x, max_num, label="max")
    plt.plot(x, avg_num, label="avg")
    plt.plot(x, min_num, label="min")
    plt.xlabel("Time (s)")
    plt.ylabel("Average number of vehicles per occupied road")
    plt.legend()
    plt.show()


# Plot generation methods
def avg_occupancy_per_road():
    edgeData = ET.parse('../storage/sumo/grid.edgeData.out.xml').getroot()
    avg_occupancy = []
    for i in edgeData.findall("interval"):
        l = [float(e.get("occupancy")) for e in i.findall("edge") if e.get("occupancy")]
        if len(l):
            avg_occupancy.append(sum(l) / len(l))
        else:
            avg_occupancy.append(0)
    x = range(len(avg_occupancy))
    y = avg_occupancy
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Average percentage of road occupied")
    plt.show()


def avg_speed_per_road():
    edgeData = ET.parse('../storage/sumo/grid.edgeData.out.xml').getroot()
    avg_speed = []
    for i in edgeData.findall("interval"):
        l = [float(e.get("speed")) for e in i.findall("edge") if e.get("speed")]
        if len(l):
            avg_speed.append(sum(l) / len(l))
        else:
            avg_speed.append(0)
    x = range(len(avg_speed))
    y = avg_speed
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Average speed per occupied road")
    plt.show()


def num_roads_occupied():
    edgeData = ET.parse('../storage/sumo/grid.edgeData.out.xml').getroot()
    num_roads_occupied = []
    for i in edgeData.findall("interval"):
        l = [float(e.get("occupancy")) for e in i.findall("edge") if e.get("occupancy")]
        num_roads_occupied.append(len(l))
    x = range(len(num_roads_occupied))
    y = num_roads_occupied
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of occupied road")
    plt.show()


def num_vehicles_in_network():
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()
    num_vehicles = []
    for t in fcd.findall("timestep"):
        vs = [v for v in t.findall("vehicle")]
        num_vehicles.append(len(vs))
    x = range(len(num_vehicles))
    y = num_vehicles
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of vehicles present")
    plt.show()


def num_stopped_vehicles_in_network():
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()
    num_vehicles = []
    for t in fcd.findall("timestep"):
        vs = [v for v in t.findall("vehicle") if float(v.get("speed")) == 0]
        num_vehicles.append(len(vs))
    x = range(len(num_vehicles))
    y = num_vehicles
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Number of stopped vehicles present")
    plt.show()


def percent_stopped_vehicles_in_network():
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()
    num_vehicles = []
    for t in fcd.findall("timestep"):
        vs_stopped = [v for v in t.findall("vehicle") if float(v.get("speed")) == 0]
        vs_total = [v for v in t.findall("vehicle")]

        num_vehicles.append(0 if len(vs_total) == 0 else len(vs_stopped) / len(vs_total))
    x = range(len(num_vehicles))
    y = num_vehicles
    plt.plot(x, y)
    plt.xlabel("Time (s)")
    plt.ylabel("Percentage of vehicles present which are stopped")
    plt.show()


def avg_num_neighbors_per_vehicle():
    sumocfg = ET.parse('../sumo/grid.sumocfg').getroot()
    begin = int(sumocfg.find('time/begin').get('value'))
    end = int(sumocfg.find('time/end').get('value'))
    bt = ET.parse('../storage/sumo/grid.bt.out.xml').getroot()

    counts_per_vehicle_per_time = []
    for v in bt.findall("bt"):
        counts_per_time = [0] * (end - begin)
        for s in v.findall("seen"):
            t_beg = float(s.get("tBeg"))
            t_end = float(s.get("tEnd"))
            for t in range(math.ceil(t_beg), math.floor(t_end)):
                counts_per_time[t] += 1
        counts_per_vehicle_per_time.append(counts_per_time)

    avg_num_neighbors = []
    max_num_neighbors = []
    min_num_neighbors = []
    for t in range(begin, end):
        l = [x[t] for x in counts_per_vehicle_per_time]
        if sum(l) == 0:
            avg_num_neighbors.append(0)
            max_num_neighbors.append(0)
            min_num_neighbors.append(0)
        else:
            avg_num_neighbors.append(sum(l) / len(l))
            max_num_neighbors.append(max(l))
            min_num_neighbors.append(min(l))

    x = range(len(avg_num_neighbors))
    y = avg_num_neighbors
    plt.plot(x, max_num_neighbors, label="max")
    plt.plot(x, avg_num_neighbors, label="avg")
    plt.plot(x, min_num_neighbors, label="min")
    plt.xlabel("Time (s)")
    plt.ylabel("Average number of neighbors per vehicle")
    plt.legend()
    plt.show()


def percent_without_neighbors():
    sumocfg = ET.parse('../sumo/grid.sumocfg').getroot()
    begin = int(sumocfg.find('time/begin').get('value'))
    end = int(sumocfg.find('time/end').get('value'))
    bt = ET.parse('../storage/sumo/grid.bt.out.xml').getroot()
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()

    number_of_vehicles_per_time = []
    vehicles_per_time = []
    for t in fcd.findall("timestep"):
        vs = [v.get("id") for v in t.findall("vehicle")]
        vehicles_per_time.append(vs)
        number_of_vehicles_per_time.append(len(vs))

    counts_per_vehicle_per_time = {}
    for v in bt.findall("bt"):
        counts_per_time = [0] * (end - begin)
        for s in v.findall("seen"):
            t_beg = float(s.get("tBeg"))
            t_end = float(s.get("tEnd"))
            for t in range(math.ceil(t_beg), math.floor(t_end)):
                counts_per_time[t] += 1
        counts_per_vehicle_per_time[v.get("id")] = counts_per_time

    avg_num_neighbors = []
    for t in range(begin, end):
        l = []
        for i in vehicles_per_time[t]:
            if counts_per_vehicle_per_time[i][t] == 0:
                l.append(counts_per_vehicle_per_time[i][t])
        if number_of_vehicles_per_time[t]:
            avg_num_neighbors.append(len(l) / number_of_vehicles_per_time[t])
        else:
            avg_num_neighbors.append(0)

    x = range(len(avg_num_neighbors))
    y = avg_num_neighbors
    plt.plot(x, avg_num_neighbors)
    plt.xlabel("Time (s)")
    plt.ylabel("Percentage of vehicle without neighbors")
    plt.show()


def avg_percent_of_network_communicatable_by_vehicle():
    sumocfg = ET.parse('../sumo/grid.sumocfg').getroot()
    begin = int(sumocfg.find('time/begin').get('value'))
    end = int(sumocfg.find('time/end').get('value'))
    bt = ET.parse('../storage/sumo/grid.bt.out.xml').getroot()
    fcd = ET.parse('../storage/sumo/grid.fcd.out.xml').getroot()

    num_vehicles = []
    for t in fcd.findall("timestep"):
        vs = [v for v in t.findall("vehicle")]
        num_vehicles.append(len(vs))

    counts_per_vehicle_per_time = []
    for v in bt.findall("bt"):
        counts_per_time = [0] * (end - begin)
        for s in v.findall("seen"):
            t_beg = float(s.get("tBeg"))
            t_end = float(s.get("tEnd"))
            for t in range(math.ceil(t_beg), math.floor(t_end)):
                counts_per_time[t] += 1
        counts_per_vehicle_per_time.append(counts_per_time)

    avg_percentage_of_network = []
    max_percentage_of_network = []
    min_percentage_of_network = []
    for t in range(begin, end):
        l = [x[t] for x in counts_per_vehicle_per_time]
        if sum(l) == 0:
            avg_percentage_of_network.append(0)
            max_percentage_of_network.append(0)
            min_percentage_of_network.append(0)
        else:
            avg_percentage_of_network.append(sum(l) / num_vehicles[t] / len(l))
            max_percentage_of_network.append(max(l) / num_vehicles[t])
            min_percentage_of_network.append(min(l) / num_vehicles[t])

    x = range(len(avg_percentage_of_network))
    y = avg_percentage_of_network
    plt.plot(x, max_percentage_of_network, label="max")
    plt.plot(x, avg_percentage_of_network, label="avg")
    plt.plot(x, min_percentage_of_network, label="min")
    plt.xlabel("Time (s)")
    plt.ylabel("Average percentage of network visible per vehicle")
    plt.legend()
    plt.show()


for p in plots_to_generate():
    plt.figure(p)
    plots_to_generate()[p]()
