from sys import argv
import seaborn as sns
import pandas as pd
import math
#confusion matrix format
#TP FN 
#FP TN
def get_cm(input_file,t):
    fn_list = []
    fp_list = []
    m = [[0,0],[0,0]]
    with open(input_file) as file:    
        for line in file:
            line = line.rstrip().split()
            if float(line[1]) < t:
                if line[2] == '1':
                    m[0][0] += 1    #TP
                else:
                    m[1][0] += 1    #FP
                    fp_list.append(line[0])
            else:
                if line[2] == '1':  #FN
                    m[0][1] += 1
                    fn_list.append(line[0])
                else:               #TN
                    m[1][1] += 1
        return m,fn_list,fp_list
def get_acc(cm):
    acc = (cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])
    return acc
def get_mcc(cm):
    mcc = ((cm[1][1]*cm[0][0])-(cm[0][1]*cm[1][0]))/((cm[0][0]+cm[1][0])*(cm[0][0]+cm[0][1])*(cm[1][1]+cm[1][0])*(cm[1][1]+cm[0][1]))**0.5
    return mcc
if __name__ == '__main__':
    if len(argv) != 5:   
        print("Wrong num. of arguments -> Usage: python classifictaion.py <subset1> <subset2> <threshold1> <threshold2> \n Example: python classifictaion.py subset1 subset2 1e-1 1e-10")
        exit()
    subset1 = argv[1]
    subset2 = argv[2]
    t1 = math.log10(float(argv[3]))
    t2 = math.log10(float(argv[4]))
    e_list = []
    mcc_list = []
    subset_id = []
    #iterate over evalues and compute MCC
    for exp in range(int(t2),int(t1)+1):
        t = 10**exp
        #subset 1
        mcc = get_mcc(get_cm(subset1,t)[0])
        mcc_list.append(mcc)
        subset_id.append(1)
        e_list.append(t)
        #subset2
        mcc = get_mcc(get_cm(subset2,t)[0])
        mcc_list.append(mcc)
        subset_id.append(2)
        e_list.append(t)
    #create a df to generate the lineplot
    data = {"E-values": e_list, "MCC": mcc_list, "Subset_ID": subset_id}
    df = pd.DataFrame(data)
    # Display the df
    df.sort_values(by=['Subset_ID','E-values'], inplace=True)
    df2 = df.to_string(index=False)
    print(df2,'\n')
    # Iterate over each subset and find the E-value range that maximizes MCC
    grouped = df.groupby('Subset_ID')
    for subset_id, subset_data in grouped:
        best_mcc = subset_data['MCC'].max()  # Maximum MCC value
        best_evalues = subset_data.loc[subset_data['MCC'] == best_mcc, 'E-values']  # E-values corresponding to the maximum MCC
        # Print the results
        print(f"SUBSET {subset_id}:"+'\n')
        print('------------------------------------------------------------------')
        print("Best MCC:", best_mcc)
        print("Best E-values Range:", best_evalues.tolist(),'\n')
        #plot the confusion matrix
        cm,fn,fp = get_cm(argv[subset_id],float(max(best_evalues)))
        print('Cofusion matrix:')
        for el in cm:
            print(el)
        print('\n'+'False negatives: ',fn)
        print('False positives: ',fp)
        print('------------------------------------------------------------------'+'\n')
# Create the lineplot
    lplot = sns.lineplot(data=df,x='E-values',y='MCC',hue='Subset_ID', marker="o", markersize=6, palette='colorblind')
    lplot.set(xscale='log')
# Set labels and title
    lplot.set_xlabel("E-value threshold")
    lplot.set_ylabel("MCC")
    lplot.set_title("")
    plot_image = lplot.get_figure()
    plot_image.savefig('lineplot.png',dpi=200)

