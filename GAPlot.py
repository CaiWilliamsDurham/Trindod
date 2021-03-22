import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class Results:
    def __init__(self, results, **paramaters):
        self.Categories = paramaters
        self.Categories.update(Results='Results', Fitness='Fitness')
        self.Results = pd.read_csv(results)
        self.Results = self.Results.replace([np.inf, -np.inf], np.nan)
        self.Results = self.Results.dropna()
        self.Results['Generation'] = self.Results['Generation'].str[1:]

    def PlotOne(self, cat_name, xname, yname):

        YAverage = self.Results.groupby(['Generation']).mean()[cat_name].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()[cat_name].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()[cat_name].sort_values(ascending=False).to_numpy()
        X = pd.unique(self.Results['Generation'])
        X = range(len(X))
        plt.plot(X, YAverage)
        plt.fill_between(X, YMin, YMax, color='b', alpha=.1)
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.show()
        return

    def PlotAll(self):
        fig, ax = plt.subplots(ncols=2, nrows=4)

        X = range(len(pd.unique(self.Results['Generation'])))

        YAverage = self.Results.groupby(['Generation']).mean()['0'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['0'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['0'].sort_values(ascending=False).to_numpy()
        ax[0, 0].plot(X,YAverage)
        ax[0, 0].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[0, 0].set(ylabel='Life')


        YAverage = self.Results.groupby(['Generation']).mean()['1'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['1'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['1'].sort_values(ascending=False).to_numpy()
        ax[1, 0].plot(X, YAverage)
        ax[1, 0].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[1, 0].set(ylabel='Burn-in')

        YAverage = self.Results.groupby(['Generation']).mean()['2'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['2'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['2'].sort_values(ascending=False).to_numpy()
        ax[2, 0].plot(X, YAverage)
        ax[2, 0].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[2, 0].set(ylabel='Long-termDegradation')

        YAverage = self.Results.groupby(['Generation']).mean()['3'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['3'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['3'].sort_values(ascending=False).to_numpy()
        ax[3, 0].plot(X, YAverage)
        ax[3, 0].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[3, 0].set(xlabel='Generation', ylabel='PowerDensity')

        YAverage = self.Results.groupby(['Generation']).mean()['Fitness'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['Fitness'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['Fitness'].sort_values(ascending=False).to_numpy()
        ax[1, 1].plot(X, YAverage)
        ax[1, 1].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[1, 1].set(ylabel='Fitness')

        YAverage = self.Results.groupby(['Generation']).mean()['Results'].sort_values(ascending=False).to_numpy()
        YMin = self.Results.groupby(['Generation']).min()['Results'].sort_values(ascending=False).to_numpy()
        YMax = self.Results.groupby(['Generation']).max()['Results'].sort_values(ascending=False).to_numpy()
        ax[2, 1].plot(X, YAverage)
        ax[2, 1].fill_between(X, YMin, YMax, color='b', alpha=.1)
        ax[2, 1].set(xlabel='Generation', ylabel='LCOE')

        ax[0,1].remove()
        ax[3,1].remove()

        fig.tight_layout()
        plt.show()
        return

def directory(Dir):
    Devices = os.listdir(Dir)
    for Device in Devices:
        Results = pd.read_csv(Dir + '\\' + Device)
        Results = Results.replace([np.inf, -np.inf], np.nan)
        Results = Results.dropna()
        Results['Generation'] = Results['Generation'].str[1:]
        X = range(len(pd.unique(Results['Generation'])))
        Y = Results.groupby(['Generation']).mean()['Results'].sort_values(ascending=False).to_numpy()
        #YMin = Results.groupby(['Generation']).min()['Results'].sort_values(ascending=False).to_numpy()
        #YMax = Results.groupby(['Generation']).max()['Results'].sort_values(ascending=False).to_numpy()
        plt.plot(X, Y, label=Device)
        #plt.fill_between(X, YMin, YMax, color='b', alpha=.1)
        plt.legend()
    plt.show()
    return

#directory('Generations')
R = Results('Generations/20210322-180323.csv')
#R.PlotAll()
R.PlotOne('Results','Generations','LCOE')