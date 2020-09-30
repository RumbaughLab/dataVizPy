## ***************************************************************************
## * LIBRARIES                                                               *
## ***************************************************************************
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import itertools
from cycler import cycler


## ***************************************************************************
## * CUSTOM FUNCTION                                                         *
## ***************************************************************************

def paramsForCustomPlot(data, variableLabel='genotype', valueLabel='value', **kwargs):
    """Function to create the parametters for ploting the variable, value, subject setup manually create a dictionary for the parameter to be reused for ploting see
    
    Parameters:
        data (DataFrame): dataframe with the data
        myPal (list): list of hexadecimal RGB value should be at least the length of the variableLable // this was removed due to change in default settings
        variableLabel (str): name of the variable of interest, header of the variable column
        subjectLabel (str): name of the subject of interest, header of the subject column
        valueLabel (str): name of the subject of interest, 
    """

    subjectLabel = kwargs.get('subjectLabel', None)
    if subjectLabel is None:
        subjectLabel = 'tmpSub'
        data.index = data.index.set_names(['tmpSub'])
        data = data.reset_index()
    dfSummary=data.groupby([variableLabel,subjectLabel]).mean()
    dfSummary.reset_index(inplace=True)


    params = dict(  data=dfSummary,
                    x=str(variableLabel),
                    y=str(valueLabel),
                    hue=str(variableLabel),
                    )

    paramsNest = dict( data=data,
                    x=str(variableLabel),
                    y=str(valueLabel),
                    hue=str(variableLabel),
                    )

    ## calculate the number of observation 
    tmpObs = data[[variableLabel, valueLabel]]
    tmpObs = tmpObs.dropna()
    nobs = tmpObs.groupby(variableLabel).count()
    nobs = list(itertools.chain.from_iterable(nobs.values))
    nobs = [str(x) for x in nobs]
    nmax = tmpObs.max()[-1]

    return params, paramsNest, nobs, nmax



## ***************************************************************************
## * KEY PLOTING PARAMETERS                                                  *
## ***************************************************************************

## https://matplotlib.org/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files
## to develop and work on to modify to matplotlibrc

mpl.rcParams['pdf.fonttype'] = 42 # to make sure it is recognize as true font in illustrator
# line above may be equivalent to 
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['axes.prop_cycle'] = cycler(color=['#6e9bbd', '#e26770'])
mpl.rcParams['figure.figsize'] = [0.77, 1.2]
mpl.rcParams['figure.frameon'] = False
mpl.rcParams['figure.autolayout'] = False
mpl.rcParams['font.size'] = 6
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.major.bottom'] = True
mpl.rcParams['ytick.major.size'] =  2
mpl.rcParams['xtick.major.size'] =  0
mpl.rcParams['legend.frameon'] = False

## ***************************************************************************
## * DATA                                                                    *
## ***************************************************************************
# path = r'Y:\2020-09-Paper-ReactiveTouch\exportAttempt'
# files = glob.glob(path+'/*.csv')
# dt = pd.read_csv(files[1])
# dt = dt.T # need to transpose the table to switch to long format
# dt = dt.reset_index(col_fill='geno')
# dt.columns = ['geno'] + list(dt.loc[0][1:])
# dt = dt.drop([0])
# colgeno = dt['geno'].str.split('.', n=1, expand=True)
# dt['geno'] = colgeno[0]
# dt[list(dt.columns[1:])] = dt[list(dt.columns[1:])].apply(pd.to_numeric, errors='coerce') # convert to NaN if number present with *


# params, paramsNest, nobs, nmax = paramsForCustomPlot(data = dt,  variableLabel = 'geno', valueLabel = 'Syngap1 KO')


## ***************************************************************************
## * USAGE EXAMPLE                                                           *
## ***************************************************************************
dtt = sns.load_dataset('iris')
dtt = dtt[dtt['species'].isin(['setosa', 'virginica'])]
dtt.index = dtt.index.set_names(['tmpSub'])
params, paramsNest, nobs, nmax = paramsForCustomPlot(data = dtt,  variableLabel = 'species', valueLabel = 'sepal_length')


## ***************************************************************************
## * FIGURE                                                                  *
## ***************************************************************************
plt.close('all')
fig, ax = plt.subplots()
# fig = plt.figure()
axv = sns.violinplot(split = False, width=0.6, cut=1, **paramsNest, inner='quartile', zorder=2, linewidth = 0.5, dodge=False, ax = ax)
## change the line stile 
for l in axv.lines:
    l.set_linestyle('-')
    l.set_color('white')
    l.set_alpha(0.3)

sns.stripplot(**paramsNest, edgecolor = 'k', linewidth = 0.4,  size=2, zorder=3, ax = ax)

ax = sns.pointplot(ci=68, scale=0.1, errwidth=2, **params, palette = ['k'])
sns.pointplot(ax= ax, ci=95, scale=0.1, errwidth=1, **params, palette = ['k'])
## ensure the point plot are above everything else
## to troublehoot order of appearanc ##https://stackoverflow.com/questions/32281580/using-seaborn-how-do-i-get-all-the-elements-from-a-pointplot-to-appear-above-th
plt.setp(ax.lines, zorder=100)
plt.setp(ax.collections, zorder=100, label="")

sns.barplot(**paramsNest, edgecolor='k',  linewidth=0.4 , ci=None, dodge=False, zorder=1)


## plot the observation on the graph
## need to work on proportional positionning and not fix to one now 4% of max value
pos = range(len(nobs))
for tick,label in zip(pos,ax.get_xticklabels()):
   ax.text(pos[tick], nmax*0.04, nobs[tick], horizontalalignment='center', size='x-small', color='w', weight='semibold')

plt.xlabel(None)
plt.ylabel('test')
ax.legend_.remove()
plt.tight_layout()
plt.savefig(r"C:\Users\Windows\Desktop\test.svg")



## ***************************************************************************
## * STAT/REF TABLE                                                              *
## ***************************************************************************




