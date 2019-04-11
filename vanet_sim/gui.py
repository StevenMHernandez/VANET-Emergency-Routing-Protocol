import math
import tkinter as tk

from vanet_sim import vehicle_net, road_net

NODE_DIAMETER = 20


class MapFrame(tk.Frame):
    def __init__(self, master, d_time, time_dur, road_map, vehicles, *args,
                 **kwargs):
        super(MapFrame, self).__init__(master, *args, **kwargs)
        self.d_time = d_time
        self.time_dur = time_dur
        self.road_map = road_map
        self.vehicles = vehicles

        self.cur_time = 0
        self.vehicle_widgets = {}

        c_width, c_height = self._calc_canvas_bounds()
        self.canvas = tk.Canvas(self, width=c_width, height=c_height)
        self.canvas.pack()

        self._draw_map()
        self._draw_vehicles()

    def _draw_map(self):
        """Draws the road map."""
        for key in self.road_map.road_dict:
            road = self.road_map.road_dict[key]

            x1 = (NODE_DIAMETER / 2) + road.start_node.x_pos
            y1 = (NODE_DIAMETER / 2) + road.start_node.y_pos
            x2 = (NODE_DIAMETER / 2) + road.end_node.x_pos
            y2 = (NODE_DIAMETER / 2) + road.end_node.y_pos

            if road.is_obstructed:
                self.canvas.create_line(x1, y1, x2, y2, fill='red')
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill='black')

        for key in self.road_map.int_dict:
            intsct = self.road_map.int_dict[key]

            x1 = intsct.x_pos
            y1 = intsct.y_pos
            x2 = intsct.x_pos + NODE_DIAMETER
            y2 = intsct.y_pos + NODE_DIAMETER

            self.canvas.create_oval(x1, y1, x2, y2, fill='#FFFFFF')

            x = (NODE_DIAMETER / 2) + intsct.x_pos
            y = (NODE_DIAMETER / 2) + intsct.y_pos

            self.canvas.create_text(x, y, text=intsct.name)

    def _calc_canvas_bounds(self):
        max_x = 0
        max_y = 0

        for key in self.road_map.int_dict:
            intsct = self.road_map.int_dict[key]

            if intsct.x_pos > max_x:
                max_x = intsct.x_pos

            if intsct.y_pos > max_y:
                max_y = intsct.y_pos

        return max_x + NODE_DIAMETER, max_y + NODE_DIAMETER

    def _draw_vehicles(self):
        for vehicle in vehicles:
            cur_road = self.road_map.road_dict[vehicle.cur_road.name]
            cur_node_x = cur_road.start_node.x_pos
            cur_node_y = cur_road.start_node.y_pos

            x0 = cur_node_x + (NODE_DIAMETER / 2) - 5
            y0 = cur_node_y + (NODE_DIAMETER / 2) - 5
            x1 = cur_node_x + (NODE_DIAMETER / 2) + 5
            y1 = cur_node_y + (NODE_DIAMETER / 2) + 5

            self.vehicle_widgets[vehicle.id] = self.canvas.create_oval(
                x0, y0, x1, y1, fill='#FFA500')

    def _redraw_vehicle(self):
        for vehicle in self.vehicles:
            w_id = self.vehicle_widgets[vehicle.id]
            cur_w_pos = self.canvas.coords(w_id)
            x0 = (cur_w_pos[0] + cur_w_pos[2]) / 2
            y0 = (cur_w_pos[1] + cur_w_pos[3]) / 2
            x1, y1 = self._get_abs_pos_delta(vehicle)
            d_x = x1 - x0
            d_y = y1 - y0

            self.canvas.move(w_id, d_x, d_y)

    def _get_abs_pos_delta(self, vehicle):
        cur_road = self.road_map.road_dict[vehicle.cur_road.name]
        past_node_x = cur_road.start_node.x_pos
        past_node_y = cur_road.start_node.y_pos

        next_node_x = cur_road.end_node.x_pos
        next_node_y = cur_road.end_node.y_pos

        angle = math.atan2((next_node_y - past_node_y),
                           (next_node_x - past_node_x))

        d_x = vehicle.cur_pos * math.cos(angle) + past_node_x
        d_y = vehicle.cur_pos * math.sin(angle) + past_node_y

        return d_x + NODE_DIAMETER / 2, d_y + NODE_DIAMETER / 2

    def step_sim(self):
        for vehicle in self.vehicles:
            vehicle.update_location(self.cur_time)
            self._redraw_vehicle()

        if self.cur_time < self.time_dur:
            self.cur_time += self.d_time
            self.canvas.update()
            self.canvas.after(500, self.step_sim)


if __name__ == '__main__':
    road_map = road_net.RoadMap(intersection_file='intersections.csv',
                                road_file='roads.csv')

    vehicles = vehicle_net.build_vehicle_net(filepath='vehicles2.csv',
                                             road_map=road_map)

    root = tk.Tk()
    root.title('PySim')
    frame = MapFrame(root, d_time=1, time_dur=100,
                     road_map=road_map, vehicles=vehicles)
    frame.pack()
    frame.step_sim()
    root.mainloop()

    # sim = simulation.Simulation(d_time=0.5,
    #                             road_map=road_map,
    #                             vehicle_net=vehicles)
    # sim.run(time_duration=10)
