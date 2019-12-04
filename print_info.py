#function printing the information out the colonies 
def print_info(colonies, inner_step):
    '''
    Describe:
    Print out colony and inner step information.


    Positional argument:
    -> colonies:            dictionary of colonies
    -> inner_step:          pseudo step
    '''

    for key in colonies.keys():

        print('Colony {0}: '.format(len(colonies[key].points)))
        print('Inner_step: {}'.format(inner_step))


    return 