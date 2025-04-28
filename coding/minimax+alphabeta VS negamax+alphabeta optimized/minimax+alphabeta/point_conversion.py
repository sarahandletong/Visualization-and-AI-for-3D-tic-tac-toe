class PointConversion(object):

    def __init__(self, grid_size, i):
        self.grid_size = grid_size
        self.i = i

    def to_3d(self):
        cell_id = int(self.i)
        z = cell_id / pow(self.grid_size, 2)
        cell_id %= pow(self.grid_size, 2)
        y = cell_id / self.grid_size
        x = cell_id % self.grid_size
        return tuple(cell_id + 1 for cell_id in (x, y, z))

    def to_int(self):
        x, y, z = [int(i) for i in self.i]
        if all(i > 0 for i in (x, y, z)):
            return (x - 1) * pow(self.grid_size, 0) + (y - 1) * pow(self.grid_size, 1) + (z - 1) * pow(self.grid_size,
                                                                                                       2)
        return None





