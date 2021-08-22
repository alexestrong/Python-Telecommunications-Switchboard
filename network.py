"""
File:        network.py
Author:      Alex Strong
Date:        12/4/2020
Section:     44
E-mail:      astrong3@umbc.edu
Description: This program allows you to operate a telecommunications switchboard
             by adding various components such as area codes, connecting calls, as well
             as connecting switchboards together and much more.  Makes use of dictionaries
             and file IO to save and load networks.
"""
import csv

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'


def connect_switchboards(switchboards, area_1, area_2):

    found_switch_one = False
    found_switch_two = False
    for areas in switchboards:
        if area_1 == areas:
            found_switch_one = True
        if area_2 == areas:
            found_switch_two = True

    # if both switchboards are found in the system then it will append that area code to the trunk lines
    if found_switch_one and found_switch_two:
        switchboards[area_1]['trunk_lines'].append(area_2)
        switchboards[area_2]['trunk_lines'].append(area_1)
    else:
        print('Cannot find one or both of the area codes')


def add_switchboard(switchboards, area_code):
    # makes sure area code is only 3 numbers in length
    if len(str(area_code)) == 3:
        switchboards[area_code] = {'trunk_lines': [], 'phones': {}}
    else:
        print('Please enter a 3 digit area code')


def add_phone(switchboards, area_code, phone_number):

    # checks if area code exists on a switchboard
    found_area_code = False
    for areas in switchboards:
        if area_code == areas:
            found_area_code = True

    if found_area_code:
        # assigns the phone number with basic details that can be updated later
        switchboards[area_code]['phones'][phone_number] = {}
        switchboards[area_code]['phones'][phone_number]['number'] = phone_number
        switchboards[area_code]['phones'][phone_number]['busy'] = False
        switchboards[area_code]['phones'][phone_number]['connected_to'] = None
    else:
        print('Could not find switchboards that relate to this number')


def save_network(switchboards, file_name):
    """

    :param switchboards:
    :param file_name:
    :return:
    """
    header = ['Area Code', 'Trunk Lines', 'Phones']
    single_line_dictionary = {}

    with open(file_name, 'w', newline='') as csv_file_write:
        writer = csv.DictWriter(csv_file_write, fieldnames=header)
        writer.writeheader()
        for keys in switchboards:
            single_line_dictionary['Area Code'] = keys
            single_line_dictionary['Trunk Lines'] = switchboards[keys]['trunk_lines']
            phones_list = []
            for phones in switchboards[keys]['phones']:
                phones_list.append(phones)
            single_line_dictionary['Phones'] = phones_list
            writer.writerow(single_line_dictionary)

    csv_file_write.close()


def load_network(file_name):
    """
    :param file_name: the name of the file to load.
    :return: you must return the new switchboard network.  If you don't, then it won't load properly.
    """
    new_switchboard_dictionary = {}
    with open(file_name, 'r') as csv_file_read:
        reader = csv.DictReader(csv_file_read)
        for line in reader:
            int_area_code = int(line['Area Code'])

            trunk_line_characters = ''
            for characters in line['Trunk Lines']:
                if characters not in ['[', ']', ' ']:
                    trunk_line_characters += characters
            split_trunks = trunk_line_characters.split(',')
            trunk_lines_list = split_trunks

            new_switchboard_dictionary[int_area_code] = {'trunk_lines': trunk_lines_list, 'phones': {}}

            phone_characters = ''
            for individual_characters in line['Phones']:
                if individual_characters not in ['[', ']', ' ']:
                    phone_characters += individual_characters
            split_numbers = phone_characters.split(',')
            for individual_numbers in split_numbers:
                int_numbers = individual_numbers
                # occurs if there are phone numbers associated with this area code
                if individual_numbers:
                    int_numbers = int(individual_numbers)
                    new_switchboard_dictionary[int_area_code]['phones'][int_numbers] = \
                        {'number': int_numbers, 'busy': False, 'connected_to': None}
                # occurs if there are no phone numbers that go with the given area code
                else:
                    new_switchboard_dictionary[int_area_code]['phones'] = {}

    csv_file_read.close()
    return new_switchboard_dictionary


def start_call(switchboards, start_area, start_number, end_area, end_number, current_area=None, checked_list=None):

    if not current_area:
        current_area = start_area
    if not checked_list:
        checked_list = []
    checked_list.append(current_area)

    if end_area in switchboards[current_area]['trunk_lines']:
        return True
    else:
        for trunks in switchboards[current_area]['trunk_lines']:
            if trunks not in checked_list:
                if start_call(switchboards, start_area, start_number, end_area, end_number, trunks, checked_list):
                    return True
                else:
                    return False


def connect_calls(switchboards, start_area, start_number, end_area, end_number):
    switchboards[start_area]['phones'][start_number]['busy'] = True
    switchboards[start_area]['phones'][start_number]['connected_to'] = str(end_area) + '-' + str(end_number)

    switchboards[end_area]['phones'][end_number]['busy'] = True
    switchboards[end_area]['phones'][end_number]['connected_to'] = str(start_area) + '-' + str(start_number)


def end_call(switchboards, start_area, start_number):
    if not switchboards[start_area]['phones'][start_number]['busy']:
        print('Unable to disconnect')
    else:
        print('Hanging up...')
        unsplit_destination = switchboards[start_area]['phones'][start_number]['connected_to']
        split_destination = unsplit_destination.split(HYPHEN)
        dest_area = int(split_destination[0])
        dest_end = int(split_destination[1])

        switchboards[start_area]['phones'][start_number]['busy'] = False
        switchboards[start_area]['phones'][start_number]['connected_to'] = None
        switchboards[dest_area]['phones'][dest_end]['busy'] = False
        switchboards[dest_area]['phones'][dest_end]['connected_to'] = None
        print('Connection Terminated.')


def display(switchboards):
    for code in switchboards:
        print('Switchboard with area code: ', code)
        print('\tTrunk lines are: ')
        for trunks in switchboards[code]['trunk_lines']:
            print('\t\tTrunk line connection to: ', trunks)
        print('\tLocal phone numbers')
        for phones in switchboards[code]['phones']:
            if switchboards[code]['phones'][phones]['busy']:
                print('\t\tPhone with number:', phones, 'is connected to',
                      switchboards[code]['phones'][phones]['connected_to'])
            else:
                print('\t\tPhone with number:', phones, 'is not in use')


if __name__ == '__main__':
    switchboard_dictionary = {}  # probably {} or []
    phone_book = {}
    phone_dictionary = {'full_number': '', 'area_code': '', 'in_use': False}
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            connect_switchboards(switchboard_dictionary, area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            add_switchboard(switchboard_dictionary, int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))
            add_phone(switchboard_dictionary, area_code, phone_number)
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            save_network(switchboard_dictionary, split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            switchboard_dictionary = load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:

            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))
            # checks if the source phone line is busy
            if switchboard_dictionary[src_area_code]['phones'][src_number]['busy']:
                src_busy = True
            else:
                src_busy = False

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            # checks if destination phone line is busy
            if switchboard_dictionary[dest_area_code]['phones'][dest_number]['busy']:
                dest_busy = True
            else:
                dest_busy = False

            if not src_busy and not dest_busy:
                if start_call(switchboard_dictionary, src_area_code, src_number, dest_area_code, dest_number):
                    print(split_command[1], 'and', split_command[2], 'are now connected.')
                    connect_calls(switchboard_dictionary, src_area_code, src_number, dest_area_code, dest_number)
                else:
                    print(split_command[1], 'and', split_command[2], 'were not connected.')
            else:
                print('One of these lines is already busy')

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))
            end_call(switchboard_dictionary, area_code, number)

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            display(switchboard_dictionary)

        s = input('Enter command: ')

'''{301: {'trunk_lines': [], 'phones': {6457671: False}},
 240: {'trunk_lines': [], 'phones': {6534180: False}}}

{301: {'trunk_lines': [240], 'phones': {6457671: False}}
{301: {'trunk_lines': [240], 'phones': {6457671: {'busy': False, 'connection': None}, }}'''