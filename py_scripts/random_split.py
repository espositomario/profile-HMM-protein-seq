from sys import argv
import random
def splitlist(input_list):
    mid_index = len(input_list)//2
    half_1 = input_list[:mid_index]
    half_2 = input_list[mid_index:]
    return  half_1, half_2

if __name__ == '__main__':
    if len(argv) != 6:   
        print("Wrong num. of arguments -> Usage: python random_split.py hmm_result kunitz.list non_kunitz.list subset_1 subset_2")
        exit()
    kunitz_list = []
    not_kunitz_list = []
    result_list = []
    with open(argv[1]) as result,open(argv[2]) as kunitz,open(argv[3]) as not_kunitz:
        with open(argv[4],'w') as out_1 , open(argv[5],'w') as out_2:
            #import kunitz list and not_kunitz
            for line in result:
                line = line.rstrip().split()
                result_list.append(line)
            for line in kunitz:
                line = line.strip()
                kunitz_list.append([line,1])
            for line in not_kunitz:
                line = line.strip()
                not_kunitz_list.append([line,0])
            #randomize the lists
            random.Random(2).shuffle(kunitz_list)
            random.Random(2).shuffle(not_kunitz_list)
            #split both lists
            kunitz_1, kunitz_2 = splitlist(kunitz_list)
            not_kunitz_1, not_kunitz_2 = splitlist(not_kunitz_list)
            #merge to crerate subset1 and 2
            subset_1 = [*kunitz_1, *not_kunitz_1]
            subset_2 = [*kunitz_2, *not_kunitz_2]
            #now create the tsv file containing id ,e-val and 1/0
            ####out_1---------------------
            index_collector = []
            for i in range(len(subset_1)):
                for j in range(len(result_list)):
                    if subset_1[i][0] == result_list[j][0]:
                        out_1.write(subset_1[i][0]+'\t'+result_list[j][1]+'\t'+str(subset_1[i][1])+'\n')
                        index_collector.append(int(i))
            for i in range(len(subset_1)):
                if i not in index_collector:
                    out_1.write(subset_1[i][0]+'\t'+'99'+'\t'+str(subset_1[i][1])+'\n')
            #out_2---------------------
            index_collector = []
            for i in range(len(subset_2)):
                for j in range(len(result_list)):
                    if subset_2[i][0] == result_list[j][0]:
                        out_2.write(subset_2[i][0]+'\t'+result_list[j][1]+'\t'+str(subset_2[i][1])+'\n')
                        index_collector.append(int(i))
            for i in range(len(subset_2)):
                if i not in index_collector:
                    out_2.write(subset_2[i][0]+'\t'+'99'+'\t'+str(subset_2[i][1])+'\n')
            #merge into 2 subsets corresponding to optimization and testing set
