import matplotlib as plt
import numpy as  np 

def plotMultipleNumpylist(plotDict, yLabel, xLable):
    # this function plots multiple lines using values from diffrent numpy list
    _max = []
    for key, item  in plotDict.items(): 
        plt.plot(item, linewidth = .7)
        _max.append(max(item))

    plt.ylabel(yLabel)
    plt.xlabel(xLable)
    _text_loc_y = max(_max)
    plt.axvline(120, ymin=0, ymax =100, linestyle = 'dashed', color = 'maroon')
    plt.text(120, _text_loc_y, "   GRAMs Launching", {'color': 'maroon', 'fontsize': 10})
    
    plt.legend(plotDict.keys(), loc='upper left')
    plt.show()

    return 
