#python script.py list_of_id_to_rem fasta_in fasta_out
from sys import argv
if __name__ == '__main__':
    if len(argv) != 4:   
        print("Wrong num. of arguments -> Usage: python remove_fasta_by_id <list of ids to rem> <fasta in> <fasta_out>")
        exit()
    id_list= []
    with open(argv[1]) as file:
        for line in file:
            line = line.rstrip()
            id_list.append(line)
    rem= 0
    c= 0
    with open(argv[2]) as fasta:
        with open(argv[3], 'w') as output:
            for line in fasta:
                line = line.rstrip()
                if line[0] == '>':
                    line = line.split('|')
                    if line[1] not in id_list:
                        output.write('>'+line[1]+'\n')
                        c += 1
                        state = True
                    else:
                        state = False
                        rem+=1
                else:
                    if state == True:
                        output.write(line+'\n')
    print('num of seq passed: ', c)
    print('num of seq removed: ', rem)
    print('seq removed:',id_list)
