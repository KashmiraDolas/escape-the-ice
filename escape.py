#__author__ = "Kashmira Dolas"
"""
file: escape.py
language: python3
author:   Kashmira Dolas

description: finds out from which squares you can escape and for those squares
from which you can escape, how quickly you can
"""


from graph import Graph
import searchalgs
import sys

pond = []
path = {}

def chk_east(i,j, column):
    '''
    this function returns the east neighbor of the state
    :param i: row number of the square in the pond
    :param j: column number of the square in the pond
    :param column: the height of the pond
    :return: cur
    '''

    cur = ()
    eastflag = True
    # check for east neighbors
    for k in range(j + 1, column):
        if pond[i][k] == '*' and k - 1 == j:
            eastflag = False
            break
        if pond[i][k] == '*' and k - 1 != j:
            eastflag = False
            cur = (i, k - 1)
            #print('....')
            #print(cur)
            #print('\n')
            break
        elif pond[i][j] != '*' and k == column - 1 and eastflag:
            cur = (i, column - 1)
            #print('---')
            #print(cur)
            #print('\n')
    eastflag = True
    return cur

def chk_west(i, j):
    '''
    this function returns the west neighbor of the state
    :param i: row number of the square in the pond
    :param j: column number of the square in the pond
    :return: cur
    '''
    cur= ()
    westflag = True
    # check for west neighbors
    k = 0
    if j != 0:
        k = j - 1
    while (True):
        if k == 0:
            break
        if j == 0:
            westflag = False
            break
        elif pond[i][k] == '*' and k + 1 == j:
            westflag = False
            break
        elif pond[i][k] == '*' and k + 1 != j:
            westflag = False
            cur = (i, k + 1)
            #print('w***')
            #print(cur)
            #print('\n')
            break
        k = k - 1
    if j != 0 and westflag:
        cur = (i, 0)
        #print('w---')
        #print(cur)
        #print('\n')
    westflag = True
    return cur

def chk_south(i, j, row):
    '''
        this function returns the south neighbor of the state
        :param i: row number of the square in the pond
        :param j: column number of the square in the pond
        :param row: the width of the pond
        :return: cur
        '''
    cur =()
    southflag = True
    # check for south neighbors
    for k in range(i + 1, row):
        if pond[k][j] == '*' and k - 1 == i:
            southflag = False
            break
        if pond[k][j] == '*' and k - 1 != i:
            southflag = False
            cur = (k - 1, j)
            #print('s....')
            #print(cur)
            #print('\n')
            break
        elif pond[i][j] != '*' and k == row - 1 and southflag:
            cur = (row - 1 , j)
            #print('s---')
            #print(cur)
            #print('\n')
    southflag = True
    return cur

def chk_north(i, j):
    '''
    this function returns the north neighbor of the state
    :param i: row number of the square in the pond
    :param j: column number of the square in the pond
    :return: cur
    '''
    cur =()
    northflag = True
    # check for north neighbors
    k = 0
    if i != 0:
        k = i - 1
    while (True):
        if i == 0:
            northflag = False
            break
        elif pond[k][j] == '*' and k + 1 == i:
            northflag = False
            break
        elif pond[k][j] == '*' and k + 1 != i:
            northflag = False
            cur = (k+1, j)
            #print('n***')
            #print(cur)
            #print('\n')
            break
        if k == 0:
            break
        k = k - 1
    if i != 0 and northflag:
        cur = (0, j)
        #print('n---')
        #print(cur)
        #print('\n')
    northflag = True
    return cur


def Processfile(file):
    '''
    This function processes the file, creates graph and finds shortest path
    :param file: file to be processed
    :return: None
    '''
    column = 0
    row = 0
    with open (file+'.txt') as f:
        for i in f:
            temp = i.strip().split(" ")
            #print(temp)
            if len(temp) == 3  and temp[0].isdigit():
                row = int(temp [0])
                column = int(temp [1])
                escape = int(temp [2])
                if escape > row-1:
                    print('Invalid escape point \nError!')
                    sys.exit(0)
            elif temp[0] == '.' or temp [0]  == '*':
                if len(temp) == column:
                    pond.append(temp)
                else:
                    print('Invalid Input or Number of Rows/Columns and pond '
                          'height/width mismatch \nError!')
                    sys.exit(0)
            else:
                print('Invalid Input Error!')
                sys.exit(0)
    if len(pond) != row:
        print('Invalid Input or Number of Rows/Columns and pond height/width '
              'mismatch \nError!')
        sys.exit(0)
    if pond[escape][column-1] == '*':
        print('Escape point has a rock.. No sqaures are escapable')
        sys.exit(0)

    g = Graph()

    for i in range (row) :
        for j in range (column):
            #print(str(i) + ',' + str(j) + '-' + pond[i][j])
            state = (i,j)
            if pond[i][j] != '*':
                # check for east neighbors
                cur = chk_east(i, j, column)
                if cur != ():
                    g.addEdge(state, cur)
                #check for west neighbors
                cur = chk_west(i,j)
                if cur != ():
                    g.addEdge(state, cur)
                #check for south neighbors
                cur = chk_south(i,j,row)
                if cur != ():
                    g.addEdge(state, cur)
                #check for north neighbors
                cur = chk_north(i,j)
                if cur != ():
                    g.addEdge(state, cur)

    #print("-----------------------------")
    #for state in g:
        #print(state)

    d = g.getVertex((escape, column - 1))  # d -> destination
    for i in range(row):
        for j in range(column):
            if pond[i][j] != '*' :
                s = g.getVertex((i, j))
                l =[]
                if searchalgs.findShortestPath(s, d) != None:
                    for x in searchalgs.findShortestPath(s, d):
                        if x != None:
                            l.append(x.id)
                    #print(l)
                    #l = [x.id for x in searchalgs.findShortestPath(s,d) ]
                p = len(l)-1
                cur = (j,i)
                if p not in path.keys():
                    path[p] = [cur]
                else:
                    path[p].append(cur)
    return column, escape



def main():
    '''
    Main function
    :return: None
    '''
    try:  # HANDLING FILE NOT FOUND EXCEPTIONS
        print("PLease enter the file name (WITHOUT '.txt')")
        file = input("\n")
        c, e = Processfile(file)

    except FileNotFoundError as fnfe:
        print(fnfe, file=sys.stderr)
        #print(Olivers_Tracker._dequeue(), '###')

    #print(path)
    for key in path.keys():
        if  key != -1:#key != 0 and
            if key == 0:
                path[1].append(path[0][0])
                #print(path[1])
            #print(path[key])
            if key!=0:
                print(str(key)+':'+str(path[key]))
        if key == -1 and path[key] == [(c-1,e)]:
            print('1:' + str(path[key]))
        elif key == -1 and path[key] != [(c-1,e)]:
            print('Points that have no escape:')
            print(str(path[key]))
        #0,0 0,1 3,1 3.2 1,2 1,4



if __name__ == '__main__':
    main()