#Uses python3

'''
Usage:

# python3 process.py <input_file> <output_file>

The output of the process is a tab-separated file with the relevant fields from the input file
based on the model of unknownUser_savedFiles.txt

'''

import sys, random, csv, os, base64, uuid, hashlib


def parse_file(arg_in_file, arg_out_file):

    header = "File name     \tCreated at  \tCall ID                  \t\t Start time                  \t\tStop time                   \t\tDuration        \t\tIs complete interaction     \t\tAgent name      \t\tAgent ID        \t\tExtension       \t\tPhone number        \t\tDialed in number        \t\tDirection       \t\tLogger          \t\tChannel     "

    with open(arg_in_file,'r') as in_file, open(arg_out_file,'w') as out_file:
        out_file.write(header + '\n')
    
        line_num = 0
        
        for line in in_file.readlines():
            out_line = ''
            if line.startswith("File name"):
                #print(line)
                out_line += line[11:-1]
                out_line += '\t'
                block_start = line_num

            if line.startswith("Created"):
                #print(line)
                out_line += line[9:-1]
                out_line += '\t'
    
            if line_num == block_start + 5:
                out_line += line[:-1]
    
            if line.startswith("-------------------------"):
                out_line += '\n'
    
            line_num += 1
            out_file.write(out_line)

        out_file.close()

def hash_string(string):
    #uuid is used to generate a random number
    salt = uuid.uuid4().hex
    hashed_string = hashlib.sha256(salt.encode() + string.encode()).hexdigest()

    return hashed_string

def cleanse_file(arg_in_file,arg_out_file):
        
    ''' 1File name - 0
        2Created at - 1
        3Call ID - 2
        4Start time - 4
        5Stop time - 6
        6Duration - 8
        7Is complete interaction - 10
        8Agent name, xxx - 12
        9Agent ID - 14
        10Extension, XXXX - 16
        11Phone number, hash - 18
        12Dialed in number, hash - 20
        13Direction - 22
        14Logger - 24
        15Channel    26 

    '''
    #header = "call_id|start_time|end_time|duration|agent_name|agent_id|extention|phone_number|dialed_in_number|direction|logger"
    #           1       3           5       7           11      13      15          17          19                  21      23
    #                                       fix         hash                        hash        hash                        

    header = "call_id|start_time|start_date|start_hour|end_time|duration|agent_id|extention|device|phone_number|dialed_in_number|direction|logger"
    hhour = ''

    #a=dict(['filename':0,'created','call_id','start_time','end_time','duration','is_complete_interaction','agent_name','agent_id','extention','phone_number'
    #    ,'dialed_in_number','direction','logger','channel'],[0,1,2,4,6,8,10,12,14,16,18,20,22,24,26])
    
    with open(arg_in_file, "rU") as in_file, open(arg_out_file,'w') as out_file:
        out_file.write(header + '\n')
        reader = csv.reader(in_file,delimiter='\t')
        for row in reader:
            out_line = ''
            good_line=False
            index = 0
            for column in row:
                if ( (index == 1) and (column.isdigit())): 
                    good_line=True
                if (good_line):
                    if (index == 1):
                        out_line+=column
                    elif (index in (3,5)):
                        date,time,ampm = column.split(' ')
                        month,day,year = date.split('/')
                        hour,minute,seconds = time.split(':')
                        #0001-01-01 00:00:00 to 9999-12-31 23:59:59.999999 UTC.
                        if (ampm == 'PM'):
                            hour = int(hour)+12
                            if (hour == 24):
                                hour = 12
                        if (int(hour) < 10):
                            hour = '0'+hour
                        if (int(month) < 10):
                            month = '0'+month
                        if (int(day) < 10):
                            day = '0'+day

                        timestamp = str(year)+'-'+month+'-'+day+' '+str(hour)+':'+minute+':'+seconds
                        out_line+='|'+timestamp

                        if (index == 3):
                            out_line+='|'+date
                            out_line+='|'+str(hhour)


                    elif (index == 7):
                        hour,minutes,seconds = column.split(':')
                        call_duration=float(hour)*3600+float(minutes)*60+float(seconds)
                        column=str(call_duration)
                        out_line+='|'+column
                    elif (index in (13,19,21,23)):
                        out_line+='|'+column
                    elif (index == 17):
                        if (str(column)[:2] == '05'):
                            out_line+='|mobile|'+column
                        else:
                            out_line+='|landline|'+column
                    elif (index == 15):
                        #out_line+='|'+hash_string(column.encode('utf-8'))
                        out_line+='|'+column.encode('utf-8')
                    else:
                        pass
                index += 1
            out_line = out_line.replace('  ','')
            out_line = out_line.replace(' |','|')
            out_line = out_line.replace('| ','|')

            if (len(out_line) > 0):
                out_file.write(out_line + '\n')
            #out_file.write(out_line)


    

if __name__ == '__main__':
    arg_in_file = sys.argv[1]
    arg_temp_file = '/tmp/tmp'+str(random.randint(1,9223372036854775807))+'.csv'
    arg_out_file = sys.argv[2]
    parse_file(arg_in_file, arg_temp_file)
    cleanse_file(arg_temp_file,arg_out_file)
    
    os.remove(arg_temp_file)
    #remove_columns(arg_out_file + ".tmp", arg_out_file)
