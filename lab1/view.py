"""Functions for printing database data"""


def print_composition_list(lst):
    for elem in lst:
        print '\tAuthor: %s; title: %s; duration: %s' % (elem.get_performer(),
                                                         elem.get_title(), elem.get_duration())
    print ''


def print_data(database):
    if database:
        for field in database.data_list:
            print 'Performer: %s; country: %s' % (field.get_name(), field.get_country())
            print_composition_list(field.get_composition_list())


def print_performer(performer):
    if performer:
        print 'Performer: %s; country: %s\nCompositions:\n' % (performer.get_name(),
                                                               performer.get_country())
        print_composition_list(performer.get_composition_list())


def print_special(lst):
    print 'Authors with average duration of song more than 4 minutes: \n'
    for elem in lst:
        print_performer(elem)

"""Functions for displaying user interface"""


def start_menu():
    print '''Hello. You entered to the database with different music performers\n
          where you can find out list ot their composition and some other infor-
          mation about them.

          To find performer by name press        - 1
          Add new performer to database press    - 2
          Edit information about performer press - 3
          See list of performers with average
            duration of the composition press    - 4
          See the list of all performers press   - 5
          Remove the performer press             - 6
          Exit - press                           - 7\n\n'''

    return int(raw_input('Enter the number: '))


def search_or_del():
    return raw_input('Enter name of performer: ')


def add_performer():
    return (raw_input('Enter name of new performer: '),
            raw_input('Enter country of new performer: '))


def add_composition():
    return (raw_input('Enter title of new composition: '),
            raw_input('Enter duration of new composition: '))


def edit():
    print '''Edit information about performer press        - 1
             Add new composition to the list press         - 2
             Edit information about some composition press - 3\n\n'''
    return int(raw_input('Enter the number: '))


def edit_performer():
    print '''Edit name press    - 1
             Edit country press - 2\n\n'''
    return int(raw_input('Enter the number: '))


def edit_composition():
    print '''Edit title press    - 1
             Edit duration press - 2\n\n'''
    return int(raw_input('Enter the number: '))


def search_or_del_compos():
    return raw_input('Enter the title: ')


def new_value():
    return raw_input('Enter new value: ')

"""Functions for printing error messages"""


def failed_search(object_name):
    print "%s you want to search doesn't exist\n" % object_name
