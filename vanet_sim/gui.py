import tkinter as tk

from vanet_sim import simulation, vehicle_net, road_net

NODE_DIAMETER = 20


class MapFrame(tk.Frame):
    def __init__(self, master, road_map, *args, **kwargs):
        super(MapFrame, self).__init__(master, *args, **kwargs)
        self.road_map = road_map

        c_width, c_height = self._calc_canvas_bounds()
        self.canvas = tk.Canvas(self, width=c_width, height=c_height)
        self.canvas.pack()
        self._draw_map()

    def _draw_map(self):
        """Draws the road map.

        Note: The axes in the canvas are transposed from normal
        conventions, so the x and y coordinates are flipped. In TK, the
        vertical axis is x, and the horizontal axis is y.
        """
        for key in self.road_map.road_dict:
            road = self.road_map.road_dict[key]

            x1 = (NODE_DIAMETER / 2) + road.start_node.y_pos
            y1 = (NODE_DIAMETER / 2) + road.start_node.x_pos
            x2 = (NODE_DIAMETER / 2) + road.end_node.y_pos
            y2 = (NODE_DIAMETER / 2) + road.end_node.x_pos

            if road.is_obstructed:
                self.canvas.create_line(x1, y1, x2, y2, fill='red')
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill='black')

        for key in self.road_map.int_dict:
            intsct = self.road_map.int_dict[key]

            x1 = intsct.y_pos
            y1 = intsct.x_pos
            x2 = intsct.y_pos + NODE_DIAMETER
            y2 = intsct.x_pos + NODE_DIAMETER

            self.canvas.create_oval(x1, y1, x2, y2, fill='#FFFFFF')

            x = (NODE_DIAMETER / 2) + intsct.y_pos
            y = (NODE_DIAMETER / 2) + intsct.x_pos

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


if __name__ == '__main__':
    road_map = road_net.RoadMap(intersection_file='intersections.csv',
                                road_file='roads.csv')

    root = tk.Tk()
    root.title('PySim')
    frame = MapFrame(root, road_map)
    frame.pack()
    root.mainloop()
    #
    # # vehicles = vehicle_net.build_vehicle_net(filepath='vehicle_net2.csv',
    # #                                          road_map=road_map)
    #
    # # sim = simulation.Simulation(d_time=0.5,
    # #                             road_map=road_map,
    # #                             vehicle_net=vehicles)
    #
    # gui = Gui(road_map=road_map)
    #
    # root.mainloop()
    # # sim.run(time_duration=10)
