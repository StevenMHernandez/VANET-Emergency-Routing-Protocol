# VANET-Emergency-Routing-Protocol

## PySim

### Overview

Network configuration settings are stored in three files: `vehicle.csv`, 
`roads.csv`, and `intersections.csv`.

`intersections.csv` contains information about each intersection. The format 
for each line is: `<name>,<pos_x>,<pos_y>`.

`roads.csv` contains formation about roads connecting the intersections.
The format for each line is: 
`<start_node_name>,<end_node_name>,<speed_limit>,<road_blocked>`.
In the simulator, road names are the concatenation of the names of their 
intersections.

`vehicle.csv` contains vehicle-specific information like the node ID number and
navigation route. The format for each line is: 
`<node_id>;<road_1>,<road_2>,...,<road_n>`.


 