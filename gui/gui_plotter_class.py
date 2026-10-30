from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):
    def __init__(self,parent = None, width = 5, height = 4, dpi = 300): 
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axis = self.fig.add_subplot(111)
        
        super().__init__(self.fig)





def find_the_max(x_data,y_data):
    # max_x = max(x_data)
    max_y = max(y_data)
    sz = len(y_data)
    diff_list = []
    sign_list = []
    infl_points = []
    for i in range(sz-1):
        diff = (y_data[i+1] - y_data[i])/(x_data[i+1] - x_data[i])
        diff_list.append(diff)
        if abs(diff) != diff:
            n = "negative"
        elif abs(diff) == diff:
            n = "positive"
        else:
            n = "zer"

        sign_list.append(n)
        # if sign_list[i] != sign_list[i+1]:
        #     pt = y_data[i]
        #     infl_points.append(pt)

    for i in range(len(sign_list) - 1):
        if sign_list[i] != sign_list[i+1]:
            pt = y_data[i+1]
            infl_points.append(pt)

    
    if max_y in infl_points:
        to_return_y = max_y
        to_return_x = x_data[y_data.index(to_return_y)]
        to_return_y = round(to_return_y,2)
        to_return_x = round(to_return_x,2)
        return to_return_x,to_return_y
        
    else:
        return "no maxima found"


    