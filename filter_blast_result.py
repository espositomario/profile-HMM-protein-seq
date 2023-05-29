from sys import argv
if __name__ == '__main__':
    if len(argv) != 4:   
        print("Wrong num. of arguments -> Usage: python filter_blast_result.py <blast_result.table> <id_list> <identity_threshold (>0-100)>")
        exit()
    with open(argv[1]) as input_file:
        with open(argv[2], 'w') as output_file:
            for line in input_file:
                line = line.rstrip().split()
                if float(line[2])>float(argv[3]):
                    output_file.write(line[1].split('|')[1]+'\n')