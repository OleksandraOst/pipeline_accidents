import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def csv_load():
    df = pd.read_csv('/Users/ostapiko/Desktop/Validere/pipeline-incidents-comprehensive-data.csv', encoding = "ISO-8859-1",
                       usecols=['Substance', 'Year'])#, 'Reported Date', 'Occurrence Date and Time'])
    
    df_clean = df[df['Substance'].isin(['Crude Oil - Sour', 'Crude Oil - Synthetic','Crude Oil - Sweet', 'Diluent', 'Bitumen' ])]
    df_clean = df_clean.reset_index(drop=True)
    df_clean = df_clean.sort_values(['Substance'], ascending=[False])
    print(df_clean)
    return df_clean['Substance'], df_clean['Year'], df_clean


def hist_plot(data, name):
        n, bins, patches = plt.hist(x=data, bins='auto', color='darkblue',
                            alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Energy Value')
        plt.title('Electronic_E Distribution')
        plt.text(-17500, 150, r'$\mu=$'+str(np.round(np.mean(data),2) ) )
        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

        # plt.hist(data['Electronic_E'])
        # plt.title('Electronic_E Distribution, first 2000 materials')
        # plt.savefig(name)
        # plt.close()
        plt.show()

def main():
    oils, years, whole_data = csv_load()
    labels, counts = np.unique(oils, return_counts=True)
    plt.bar(labels, counts, align='center')
    plt.xlabel('Type of crude oil')
    plt.ylabel('Number of accidents')

    plt.show()

    # hist_plot(years,'Electronic_E_new2')

main()