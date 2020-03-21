

from datetime import datetime
import json
import pandas as pd
from datetime import timedelta


#############################################################################

f = "%Y-%m-%d %H:%M:%S" # time format


##########################################################################################
# Event start time and end time
time_slot = {
    'startTime': '2020-03-18 08:00:00',
    'endTime': '2020-03-18 22:00:00'
}

###########################################################################################

def rounding_time_stamp(temp_timestamp):
    ''' function for calculation round time like 4:10 to 4:15, pandas
    data frame is used for processing timestamp'''
    temp_list = []
    for i in range(len(temp_timestamp)):
        temp_stamp = dict()
        temp_stamp['df_startTime'] = pd.Timestamp(temp_timestamp[i]['startTime'])
        temp_stamp['df_endTime'] = pd.Timestamp(temp_timestamp[i]['endTime'])
        temp_list.append(temp_stamp)
    df = pd.DataFrame(temp_list)
    len_df = df.shape[0]
    df['startTime'] = df['df_startTime'].dt.round('15min')
    df['endTime'] = df['df_endTime'].dt.round('15min')

    for x in range(len_df):
        time_diff = pd.Timedelta(df['endTime'][x] - df['startTime'][x]).seconds / 60.0
        if time_diff == float('15.0'):
            print('status ok')
        else:
            print('please enter a valid time stamp for meeting')
    df['startTime'] = df['startTime'].astype(str)
    df['endTime'] = df['endTime'].astype(str)
    new_df = (df.drop(['df_startTime', 'df_endTime'], axis=1))
    len_new_df = new_df.shape[0]

    final_list = []
    for x in range(len_new_df):
        temp = dict()
        temp['startTime'] = new_df['startTime'][x]
        temp['endTime'] = new_df['endTime'][x]
        final_list.append(temp)

    return final_list


################################################################################

def processing_available_time(new_available_time_slot):
    '''function for processing and forming processed data to actual output'''
    new_temp_list = []
    for i in range(len(new_available_time_slot)):
        new_temp_list.append(new_available_time_slot[i]['startTime'])
        new_temp_list.append(new_available_time_slot[i]['endTime'])
    new_temp_list.sort()

    final_output = converting_list_to_data(new_temp_list)
    return final_output

#######################################################################################

def converting_list_to_data(new_temp_list):
    '''function to convert list of processed data in dictonary '''
    final_confirmed_available_slot = []
    len_tmp = len(new_temp_list)

    for i in range(0, len_tmp, 2):
        temp_dict = dict()
        temp_dict['startTime'] = new_temp_list[i]
        temp_dict['endTime'] = new_temp_list[i + 1]
        t1 = datetime.strptime(temp_dict['startTime'], f)
        t2 = datetime.strptime(temp_dict['endTime'], f)
        # for checking if two continuous meeting
        if t1 == t2:
            pass
        else:
            final_confirmed_available_slot.append(temp_dict)

    return final_confirmed_available_slot


#########################################################################################


def blocked_time_calulation(block_list, end_flag):
    ''' for calculating the available time slots and check for various validation '''

    len_block_list = len(block_list)
    output_result = []
    for i in range(len_block_list - 1):
        temp = dict()
        temp['startTime'] = block_list[i]['endTime']
        temp['endTime'] = block_list[i + 1]['startTime']
        output_result.append(temp)

    if end_flag:
        pass
    else:
        temp = dict()
        temp['startTime'] = block_list[len_block_list - 1]['endTime']
        temp['endTime'] = time_slot['endTime']
        output_result.append(temp)

    return output_result


#####################################################################################


def blocked_slots(first_user, second_user):
    ''' finding total available time slot if input of  block time is passed '''
    len_first_user = len(first_user)
    len_second_user = len(second_user)
    if len_first_user > 0:
        first_user = rounding_time_stamp(first_user)
    if len_second_user > 0:
        second_user = rounding_time_stamp(second_user)

    new_blocked_list = first_user + second_user

    new_sorted_blocked_list = sorted(new_blocked_list, key=lambda t: t['startTime'])

    flag_check = False
    first_blocked_time = datetime.strptime(new_sorted_blocked_list[0]['startTime'], f)
    time_start = datetime.strptime(time_slot['startTime'], f)
    if time_start ==first_blocked_time:
        flag_check = True
    else:
        flag_check = False

    len_sorted_blocked_list = len(new_sorted_blocked_list)
    end_time = datetime.strptime(time_slot['endTime'], f)
    last_blocked_time =  datetime.strptime(new_sorted_blocked_list[len_sorted_blocked_list-1]['startTime'], f)
    end_flag = False
    if end_time == last_blocked_time :
        end_flag = True
    else:
        end_flag = False

    output_result = []

    if flag_check:
        output_result = blocked_time_calulation(new_sorted_blocked_list,end_flag)
    else:
        new_temp = dict()
        new_temp['startTime'] = time_slot['startTime']
        new_temp['endTime'] = new_sorted_blocked_list[0]['startTime']
        output_result.append(new_temp)
        temp_output = blocked_time_calulation(new_sorted_blocked_list,end_flag)
        output_result = output_result + temp_output

    global_available_list.extend(output_result)
    print(json.dumps(str(output_result)))
    return output_result


############################################################################################


def confirmed_block_slot(first_user_confirmed_slot, second_user_confirmed_slot, first_user, second_user):
    ''' based on the input received from user it will show all the available time slot for meeting
        it two user have same meeting time then it will show the relative response '''
    len_first_user = len(first_user_confirmed_slot)
    len_second_user = len(second_user_confirmed_slot)
    if len_first_user > 0:
        first_user_confirmed_slot = rounding_time_stamp(first_user_confirmed_slot)
    if len_second_user > 0 :
        second_user_confirmed_slot = rounding_time_stamp(second_user_confirmed_slot)


    ''' finding available time slot for user and not two user have same confirmed time slot '''

    first_user_slot = set([tuple(d.items()) for d in first_user_confirmed_slot])

    second_user_slot = set([tuple(d.items()) for d in second_user_confirmed_slot])

    check_common_time_slot = set(first_user_slot).intersection(set(second_user_slot))
    status_flag  = False
    final_output = []
    if len(check_common_time_slot) > 0:
        status_flag = True
        print('Two user have same time slot ', check_common_time_slot)
    else:
        status_flag = False
        print('No user have same time slot')
        available_processing_list =  first_user_confirmed_slot + second_user_confirmed_slot
        available_processing_list  = sorted(available_processing_list, key=lambda t: t['startTime'])

        blocked_time_slot = blocked_slots(first_user, second_user)

        new_available_time_slot = available_processing_list + blocked_time_slot
        new_available_time_slot = sorted(new_available_time_slot, key=lambda t: t['startTime'])

        final_output = processing_available_time(new_available_time_slot)
        print('final confirmed list', json.dumps(str(final_output)))
    return final_output, status_flag




#################################################################################################
def forming_data_from_list(new_list):
    ''' formating data in output form from a list'''
    len_new_list =len(new_list)
    data_dict = []
    for i in range(len_new_list -1):
        temp = dict()
        temp['startTime'] = new_list[i]
        temp['endTime'] = new_list[i+1]
        t1 = datetime.strptime(temp['startTime'], f)
        t2 = datetime.strptime(temp['endTime'], f)
        # for checking if two continuous meeting
        if t1 == t2:
            pass
        else:
            data_dict.append(temp)
    return data_dict


def time_slot_divider(interval_time_list):
    '''divide the timestamp into 15 minute slot each'''
    len_time_divider = len(interval_time_list)
    temp_list = []
    for i in range(len_time_divider):
        start_second = datetime.strptime(interval_time_list[i]['startTime'],f)
        end_second = datetime.strptime(interval_time_list[i]['endTime'], f)
        total_second = (end_second-start_second).total_seconds()
        minute_interval = timedelta(minutes=15)
        slot_list = []
        for i in range(0, int(total_second), int(minute_interval.total_seconds())):
            slot_list.append( start_second + timedelta(seconds=i))
        slot_list.append(end_second)
        slot_list = [i.strftime(f) for i in slot_list]
        final_interval_list =[]
        final_interval_list = forming_data_from_list(slot_list)
        temp_list = temp_list + final_interval_list

    return temp_list



def disallowed_slot(disallowed_time_slot,first_user_confirmed_slot, second_user_confirmed_slot, first_user, second_user ):
    ''' if the disallowed input passed along with the blocked and confirmed then
     it will return all available time slot for meeting'''
    len_disallowed_time_slot = len(disallowed_time_slot)
    if len_disallowed_time_slot > 0 :
        disallowed_time_slot = rounding_time_stamp(disallowed_time_slot)
    confirmed_time_slots, status_flag = confirmed_block_slot(first_user_confirmed_slot,second_user_confirmed_slot, first_user, second_user)
    print(confirmed_time_slots)
    new_available_slot= confirmed_time_slots + disallowed_time_slot
    processing_list = []
    if status_flag:
        return processing_list, status_flag
    else:

        final_output = processing_available_time(new_available_slot)

        processing_list = time_slot_divider(final_output)
        processing_list = json.dumps(str(processing_list))
        return processing_list, status_flag






