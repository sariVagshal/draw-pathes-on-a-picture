import numpy
from matplotlib import pyplot
np = numpy
plt = pyplot


from pylab import *
from numpy import *

import model
import settings

class Controller:
    def __init__(self, file_name, image_name):
        self.model = model.Model(file_name, image_name)
        self.df_with_filter = self.model.df_by_obj

    def get_file(self):
        return self.model.get_pickle_file()

    def draw_lines(self, list, multiplied = True):

        if list == []:
            fig, ax = plt.subplots()
            ax.imshow(self.model.img)
            show()
            return

        for i, tuple in enumerate(list):
            if multiplied or i == 0:
                plt.figure(i + 1)
                fig, ax = plt.subplots()
                ax.imshow(self.model.img)
            plot(*tuple, '-', 'color', rand(1, 3))
        show()

    def plot_objs(self,data):
        top10 = data.groupby(["filename", "obj"]).size().sort_values(ascending=False).head(10)
        df_by_obj = self.model.df.set_index(['filename', 'obj']).sort_index()
        main_info = []

        for t in top10.index:
            oo = df_by_obj.loc[t]
            main_info.append((oo.x, oo.y))
        if self.df_with_filter.size < settings.MAX_TO_PRESENT:
            multiplied = False
        else:
            multiplied = True
        self.draw_lines(main_info,multiplied)

    def drow_by_filters(self, filters):
        # filters is a tuples of name of filter, and his args in tuple
        # call the suit filter
        # get the data
        for filter in filters:
            if filter[0] == 1:
                self.hours_filter(*filter[1])

            elif filter[0] == 2:
                self.date_filter(filter[1][2])
                self.hours_filter(filter[1][0], filter[1][1])

            elif filter[0] == 3:
                self.area_filter(*filter[1])

            elif filter[0] == 4:
                for indx1,indx2 in filter[1]:
                    self.specific_area_filter((int(indx1),int(indx2)))

        self.plot_objs(self.df_with_filter[['x', 'y']])


    def hours_filter(self, frm, to):
        self.df_with_filter = self.df_with_filter[self.df_with_filter.time.dt.time.between(frm, to)]

    def date_filter(self, date):
        self.df_with_filter = self.df_with_filter[self.df_with_filter.time.dt.date == date]

    def area_filter(self, p1, p2):
        self.df_with_filter = self.df_with_filter[(self.df_with_filter.x.between(p1[0], p2[0])) & (self.df_with_filter.y.between(p1[1], p2[1]))]

    def specific_area_filter(self, square_indexes):
        x = self.model.img.size[0]
        y = self.model.img.size[1]
        x_size = x // settings.GRID[0]
        y_size = y // settings.GRID[1]
        p1 = (x_size * square_indexes[0], y_size * (square_indexes[1]))
        p2 = (x_size * (square_indexes[0] + 1), y_size * (square_indexes[1] + 1))
        self.area_filter(p1, p2)

    def reset_df_with_filter(self):
        self.df_with_filter = self.model.df_by_obj