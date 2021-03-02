import pandas as pd


def convert_to_matrix(arr):
    """Converts an entity's availability into
    a binary matrix"""
    map_ = {
        '12 AM': 0,
        '1 AM': 1,
        '2 AM': 2,
        '3 AM': 3,
        '4 AM': 4,
        '5 AM': 5,
        '6 AM': 6,
        '7 AM': 7,
        '8 AM': 8,
        '9 AM': 9,
        '10 AM': 10,
        '11 AM': 11,
        '12 PM': 12,
        '1 PM': 13,
        '2 PM': 14,
        '3 PM': 15,
        '4 PM': 16,
        '5 PM': 17,
        '6 PM': 18,
        '7 PM': 19,
        '8 PM': 20,
        '9 PM': 21,
        '10 PM': 22,
        '11 PM': 23
    }
    # Create 12x24 matrix of (months, hours)
    r = []
   
    for ix, cell in enumerate(arr):
        if isinstance(cell, str):
            cell = cell.replace(u'\xa0', u' ')

        r_ = [0]*24
        if cell == 'All day':
            r_ = [1]*24
        elif pd.isnull(cell):
            r_ = [0]*24
        else: # get start and end time
            for period in cell.split('; '):
                start, end = period.split(' – ')
                carry = False
                for k, v in map_.items():
                    if k == start or carry:
                        carry = True
                        r_[v] = 1

                    if k == end:
                        carry = False

                # If end is before start we need to fill
                # values over the break
                if map_[end] < map_[start]:
                    for i in range(map_[end]+1):
                        r_[i] = 1

        r.append(r_)

    return r
