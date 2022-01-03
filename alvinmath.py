import numpy as np
import matplotlib.pyplot as plt

def geneNormalizedSeire(inputSer):
    if(sum(inputSer) != 0):
        return [float(i)/sum(inputSer) for i in inputSer]
    else: 
        print("\t the input sum of serries equals to zero!!!!")
        return None

def getListAverage(lst):
    if(len(lst) != 0):
        return sum(lst)/ len(lst)
    else: 
        print("empty list, ckeck ... ")
        return None

def listReduct(list1, list2):
    result= []
    if(len(list1) != len(list2)):
        print("the length of two lists are not the same, please check, fucntion returning... ")
    else: 
        for i in range(len(list1)):
            result.append(list1[i] - list2[i])
    return result

def listAdd(list1, list2):
    result= []
    if(len(list1) != len(list2)):
        print("the length of two lists are not the same, please check, fucntion returning... ")
    else: 
        for i in range(len(list1)):
            result.append(list1[i] + list2[i])
    return result

def listMultiple(list1, list2):
    result= []
    if(len(list1) != len(list2)):
        print("the length of two lists are not the same, please check, fucntion returning... ")
    else: 
        for i in range(len(list1)):
            result.append(list1[i] * list2[i])
    return result


def listDivide(list1, list2):
    result= []
    if(len(list1) != len(list2)):
        print("the length of two lists are not the same, please check, fucntion returning... ")
    else: 
        if( 0 in list1 or 0 in list2):
            print("there is 0 detected for either list1 or list2, rsult may be inf")
            for i in range(len(list1)):
                if(list2[i] == 0):
                    result.append(float('inf'))
                else:
                    result.append(list1[i]/ list2[i])
    return result

def smooth1DNparray(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def nthRoot(num, nroot):
    return num ** (1/nroot)


def massUnitToMg(mass, unit):
    # transfer mass into mg
    mass = float(mass)
    result = mass
    if (unit == "kg"):
        result = result * 1000 * 1000
    elif(unit == "g"):
        result = result * 1000
    else: 
        pass
    return result




# if __name__ == '__main__':

#     t=np.linspace(-4,4,100)
#     x=np.sin(t)
#     xn=x+np.random.randn(len(t))*0.1
#     y=smooth1DNparray(xn)


#     plt.figure(figsize=(14,6))
#     plt.plot(xn,linewidth = .3)
#     plt.plot(y,linewidth = .3)
#     plt.legend(["before", "after"])
#     plt.show()

#     # pass


