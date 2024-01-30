import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats  
from scipy.stats import shapiro 



def boxes_distr(df_list: list, col_list: list, labels: str, out_name: str) -> None:
    """
    This function creates statistical box plot for chosen data frames and for given column values.
    Args:
        df_list: list of data frames
        col_list: column values to use (for these data sets years were used)
        labels: plots labels
        out_name: name of the output file
    Returns: 
        None
    """
    incident_numbers = []
    for val in range(len(col_list)):

        _, number = np.unique( (df_list[val])[col_list[val]], return_counts=True)
        incident_numbers.append(number)

    plt.boxplot(incident_numbers, labels = labels)
    plt.title('Data distribution and outliers')
    plt.savefig('BoxPlot'+out_name+'.png',bbox_inches='tight', dpi = 300)
    plt.close()



def shapiro_norm(df: pd.DataFrame, years: list, column: str) -> None:
    """
    This function tests normality of the data using Shapiro–Wilk test.
    Args:
        df: data frame to test
        years: data years list of strings
        column: column name of data frame to use
    Returns: 
        None
    """
    data = df[column]
    labels, counts = np.unique(data, return_counts=True)
    shap_test = shapiro(counts)
   
    print('Shapiro-Wilk Test',shap_test)
    plt.hist(counts, label = 'Statistics = '+str(np.round(shap_test[0],3))+', p_val = '+str(np.round(shap_test[1],3)) )
    plt.title('Data distribution from '+years[0]+' to '+years[1])
    plt.legend()
    plt.savefig('Shapiro_'+years[0]+'_'+years[1]+'.png',bbox_inches='tight', dpi = 300)
    plt.close()


def inhibitors_price(min_price: float, max_price: float, corrosion_cost_year: float) -> None:
    """
    This function calculates the price of inhibitors which should not ecxeed corrosion cost per year.
    Args:
        min_price: minimum estimated price of the inhibitor (usd)
        max_price: maximum estimated price of the inhibitor (usd)
        corrosion_price_year: cost of corrosion for oil industry per year (usd)
    Returns: 
        None
    """
    num_point = 100 #number of points to plot

    inh_kg_price = np.linspace(min_price, max_price, num_point)  #usd  (100-500rp) 1.2-6.02

    #how much crude oil is produced per day in the USA according to https://www.eia.gov/tools/faqs/faq.php?id=268&t=6#:~:text=EIA's%20data%20for%202022%20indicates,oil%E2%80%9411.911%20million%20b%2Fd
    oil_per_day = 11.911*10**6  #barell/day

    #assumed that the efficiency of the inhibitors is 80% according to https://pdf.indiamart.com/impdf/6557468533/MY-971284/corrosion-inhibitor-for-crude-oil.pdf
    efficiency = 0.8 

    #to reach 80% efficiency inhibitor concentration chould be from 50 to 100ppm according to https://pdf.indiamart.com/impdf/6557468533/MY-971284/corrosion-inhibitor-for-crude-oil.pdf
    #average values is chosen
    inh_concentratiion = 75 #ppm 

    #1 ppm = 1 mg per liter
    
    b_to_l = 159 #1 oil barrel = 159 liters
    mg_to_kg = 1e-6 #mg to kg

    inh_need_day = (oil_per_day*b_to_l*inh_concentratiion*mg_to_kg)/efficiency #kg
    inh_need_year = inh_need_day*365 #1 year = 365 days
    total_price = inh_need_year*inh_kg_price #USD
    corrosion_list = [corrosion_cost_year]*num_point

    plt.plot(inh_kg_price, total_price, '-',label = 'Inhibitors cost per year')
    plt.plot(inh_kg_price, corrosion_list, '-', label = 'Annual money lost because of corrosion')

    idx = np.argwhere(np.diff(np.sign(total_price - corrosion_list))).flatten()
    plt.plot(inh_kg_price[idx], total_price[idx], 'bo', label = 'Max inhibitor price $'+str(int(inh_kg_price[idx])))
    plt.legend()
    plt.xlabel('Inhibitor price per kg')
    plt.ylabel('US dollars')
    plt.title('Maximum inhibitor cost')
    plt.savefig('InhibitorsCost.png',bbox_inches='tight', dpi = 300)
    










