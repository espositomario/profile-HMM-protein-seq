from sys import argv
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
    if len(argv) != 3:   
        print("Wrong num. of arguments -> Usage: python classifictaionv2.py <subset1> <threshold1>  \n Example: python classifictaion.py subset1 1e-10")
        exit()
    cm,fn_list,fp_list = get_cm(argv[1],float(argv[2]))
    mcc = get_mcc(cm)
    print(argv[2],'\t',mcc,'\t',cm,'\t',fn_list,'\t',fp_list)
