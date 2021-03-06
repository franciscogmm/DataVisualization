import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import warnings
import seaborn as sns
import matplotlib.cm as cm
from pylab import savefig
warnings.filterwarnings("ignore")
pd.options.display.mpl_style = 'default'
sns.set(style="white", color_codes=True)

def help():
    print '''class: Viz(df)
                self.df
                functions:
                    .scatterplot(x,y,size,mode)
                    .jointplot(x,y,size,kind)
                    .facetgrid(x,y,color_column,size,legend)
                    .pairplot(columns,color_column,size,diag_kind,kind)
                    .boxplot(x,y,size,orient)
                    .boxplot_all(orient,size)
                    .histogram(size,bins,grid)
                    .hist_one(column,size,bins)
                    .barplot(x,y,color_column)
                    .countplot(column,orient)
                    .bubble(x,y,size_column)
            '''

class Viz():
    '''
    based on pandas and seaborn: http://seaborn.pydata.org/tutorial/categorical.html
    '''
    def __init__(self, dataframe):
        self.df = dataframe
        
    def scatterplot(self, x, y, size = 5, mode = None):
        ''' params. 
                        x   : x-axis variable
                        y   : y-axis variable
                        mode: categorical, joint, None; Default is None
                        size: toggle size of figure; Default = 5'''

        if mode == 'categorical':
            sns.stripplot(x = x, y = y, data = self.df, size = size, jitter = True)

        elif mode == 'joint':
            sns.jointplot(x = x, y = y, data=self.df, size = size)

        else:
            self.df.plot(kind = 'scatter', x = x, y = y)

        
        
    def jointplot(self, x, y, size = 5, kind = 'scatter'):
        ''' params. 
                        x   : x-axis variable
                        y   : y-axis variable
                        kind: scatter, reg, resid, kde, or hex; Default = scatter
                        size: toggle size of figure; Default = 5'''
        sns.jointplot(x = x, y = y, data = self.df, size = size, kind = kind)
        
    def facetgrid(self, x, y, color_column = None, size = 5, legend = True):
        ''' params. 
                        x           : x-axis variable
                        y           : y-axis variable
                        color_column: column used to define colors; Default = None
                        size        : toggle size of figure; Default = 5
                        legend      : True or False only; Default = True'''
        if color_column == None:
            if legend == True:
                sns.FacetGrid(self.df, size = size).map(plt.scatter, x, y).add_legend()

            elif legend == False:
                sns.FacetGrid(self.df, size = size).map(plt.scatter, x, y)

            else:
                print 'Legend should be True or False.'
        else:
            if legend == True:
                sns.FacetGrid(self.df, hue = color_column, size = size).map(plt.scatter, x, y).add_legend()

            elif legend == False:
                sns.FacetGrid(self.df, hue = color_column, size = size).map(plt.scatter, x, y)

            else:
                print 'Legend should be True or False.'

    def pairplot(self, columns, color_column = None, size = 5, diag_kind = 'hist', kind = 'scatter'):
        ''' params. 
                        columns     : columns to compare relationship of
                        color_column: column used to define colors; Default = None
                        size        : toggle size of figure; Default = 5
                        diag_kind   : hist, kde; Default = hist
                        kind        : scatter, reg; Default = scatter'''
        if color_column == None:
            sns.pairplot(self.df.ix[:,columns], size = size, diag_kind = diag_kind, kind = kind)
        else:    
            sns.pairplot(self.df.ix[:,columns], hue = color_column, size = size, diag_kind = diag_kind, kind = kind)
        
    def boxplot(self, x, y, size = 8, orient = 'h'):
        ''' params. 
                        x           : x-axis variable
                        y           : y-axis variable
                        size        : toggle size of figure; Default = 8
                        orient      : horizontal = h, vertical = v'''
        ratio = 6.0/8
        sns.boxplot(x = x, y = y, data = self.df, orient = orient).figure.set_size_inches(size, size * ratio)   
        
    def boxplot_all(self, orient = 'v', size = 8):
        ''' params. 
                        orient: h or v
                        size  : toggle size of figure; Default = 8'''
        ratio = 6.0/8
        sns.boxplot(data = self.df, orient = orient).figure.set_size_inches(size, size * ratio) 
        
    def histogram(self,size = 10, bins = 25, grid = False):
        '''params.
                        size: toggle size of figure; Default = 10
                        bins: number of bins; Default = 25
                        grid: show grid; Default = False'''
        figsize = (size,size)
        self.df.hist(figsize = figsize, bins = bins)
    
    def hist_one(self, column, size = 10, bins = 25):
        '''params.
                        column: column to use
                        size  : toggle size of figure; Default = 10
                        bins  : number of bins to use; Default = 25'''
        arr = self.df[str(column)].copy()
        arr = np.array(arr)
        figsize = (size,size)
        fig = plt.figure(figsize = figsize)
        ax = fig.add_subplot(111)
        ax.hist(arr, bins = bins)
        plt.xlabel(column, fontsize = size * 20/15)
        plt.show()

    def barplot(self, x, y, color_column = None):
        '''params.
                        x           : x-axis variable
                        y           : y-axis variable
                        color_column: column used to define colors; Default = None'''
        if color_column == None:
            sns.barplot(x = x, y = y, data = self.df)
        else:
            sns.barplot(x = x, y = y, hue = color_column, data = self.df)
        
    def countplot(self, column, orient = 'v'):
        '''params.
                        column: column to plot
                        orient: h or v; Default = v'''
        if orient == 'v':
            sns.countplot(x = column, data=self.df)
        elif orient == 'h':
            sns.countplot(y = column, data=self.df)
        else:
            print 'Orient should be h(horizontal) or v(vertical)'
            
    def bubble(self, x, y, size_column):
        '''params.
                        x          : x-axis variable
                        y          : y-axis variable
                        size_column: column to define size; optional'''
        N = len(self.df[str(size_column)].unique())
        colors=cm.rainbow(np.random.rand(N))
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x = self.df[str(x)], y = self.df[str(y)], s = self.df[str(size_column)], color = colors)
        plt.show()  
	    
