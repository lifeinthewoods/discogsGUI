#! /bin/python3.2
#
# Discogs Record Collection GUI V 0.1a
# now in version control!

import curses, traceback, string, os, xml.dom.minidom
from xml.dom.minidom import parse

# globals for GUI
hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
menu_attr = curses.A_NORMAL

EXIT = 0
CONTINUE = 1

MAX_Y = None
MAX_X = None

SPLIT_X = None

SEARCHINPUT = None

INPUTTYPE = 'artist up'

POS = 0

## Data Processing Classes and Functions
class entry(object):
    # Entry Class to get all variables for each entry
    def __init__(self, releaseId, artist, title, year, genre, formatType):
        self.releaseId = releaseId
        self.artist = artist
        self.title = title
        self.year = str(year)
        self.genre = genre
        self.formatType = formatType
    def __repr__(self):
        return repr((self.releaseId, self.artist, self.title, self.year, \
                     self.genre, self.formatType))
    def return_releaseId(self):
        return self.releaseId
    def return_artist(self):
        return self.artist
    def return_title(self):
        return self.title
    def return_year(self):
        return self.year
    def return_genre(self):
        return self.genre
    def return_format(self):
        return self.formatType

def get_release_info(dom):
    # get the id in <release id = 'xxxxxxxxx'>
    final = []
    for ele in dom.getElementsByTagName('release'):
        releaseId = ele.getAttribute('id') # very first attribute in xml
        artist = get_artist(ele)
        title = get_title(ele)
        year = get_year(ele)
        genre = get_genre(ele)
        formatType = get_format(ele)
        final.append(entry(releaseId, artist, title, year, genre, formatType)) # make the list
    return final

# Funtions to populate each new release object.  releaseId is
# is for each release.  <release id ="xxxxxxxx"> in the xml.
def get_artist(node):
    for child in node.getElementsByTagName('name'):
        if child.parentNode.localName == 'artist':
            return(child.firstChild.nodeValue)
def get_title(node):
    for child in node.getElementsByTagName('title'):
        if child.parentNode.localName == 'release':
            return(child.firstChild.nodeValue)
def get_year(node):
    for child in node.getElementsByTagName('released'):
        if child.parentNode.localName == 'release':
            return(child.firstChild.nodeValue)
def get_genre(node):
    for child in node.getElementsByTagName('genre'):
        if child.parentNode.localName == 'genres':
            return(child.firstChild.nodeValue)
def get_format(node):
    for child in node.getElementsByTagName('format'):
        return child.getAttribute('name')

def search_fields(node, fromInput, releaseObjectList):
    # simple search function.  allows for searing for any field, case insensative.
    if (fromInput.lower() in node.return_artist().lower()) == True or \
       (fromInput.lower() in node.return_title().lower()) == True or \
       (fromInput.lower() in node.return_year().lower()) == True or \
       (fromInput.lower() in node.return_genre().lower()) == True or \
       (fromInput.lower() in node.return_format().lower()) == True: # list of fields to check against user input
        return(True)

def sort_items(toSortList):
    # sorts everything by artist, title, year, and format, forward and reverse.  Returns a
    # dictionary of lists with the keys being all the artist, title, etc.
    artistUp = sorted(toSortList, key=lambda x: x.artist)
    artistDown = sorted(toSortList, key=lambda x: x.artist, reverse = True)
    titleUp = sorted(toSortList, key=lambda x: x.title)
    titleDown = sorted(toSortList, key=lambda x: x.title, reverse = True)
    yearUp = sorted(toSortList, key=lambda x: x.year)
    yearDown = sorted(toSortList, key=lambda x: x.year, reverse = True)
    formatUp = sorted(toSortList, key=lambda x: x.formatType)
    formatDown = sorted(toSortList, key=lambda x: x.formatType, reverse = True)
    return ({'artistUp':artistUp, 'artistDown':artistDown, 'titleUp':titleUp, \
             'titleDown':titleDown, 'yearUp':yearUp, 'yearDown':yearDown, \
             'formatUp':formatUp, 'formatDown':formatDown})

def return_matches(userInput, release, printAll = False):
    # returns a list of nodes that match the search query
    searchHits = []
    for item in release:
        if printAll == False:
            if search_fields(item, userInput, release) == True:
                searchHits.append(item)
        else:
            searchHits.append(item)
    return searchHits

# # how i printed things in the test program
# def main():
#     dom = parse('discogs.xml') # parse the document                              
#     release = get_release_info(dom) # get list of all objects with data filled in
#     while True:
#         userInput = input('Search for what?  ') # simple test prompt             
#         if userInput == 'quit':
#             sys.exit()
#         else:
#             searchHits = return_matches(userInput, release)
#         print(searchHits)
#         Alphadict = sort_items(searchHits)
#         sortIt = input('Sort by what? ')
#         print_sorted(sortIt, alphaDict, release)
#
# if __name__ == '__main__':
#     main()

## UI and Data Interaction Functions

def print_entry(releaseId, release, lineNum):
    # print out the entry in a semi-pretty format
    global POS
    POS = 0
    for item in release:
        if item.return_releaseId() == releaseId:
            global artistWin, titleWin, yearWin, genreWin, formatWin 
            artistWin.addstr(lineNum, 1, item.return_artist())
            titleWin.addstr(lineNum, 1, item.return_title())
            yearWin.addstr(lineNum, 1, item.return_year())
            genreWin.addstr(lineNum, 1, item.return_genre())
            formatWin.addstr(lineNum, 1, item.return_format())

def print_sorted(userChoice, alpha, release):
    # print out the types in whatever order the users asks for
    global POS
    POS = 0
    if userChoice == 'artist up':
        yPos = 1
        for listPoint in alpha['artistUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'artist down':
        yPos = 1
        for listPoint in alpha['artistDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'title up':
        yPos = 1
        for listPoint in alpha['titleUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'title down':
        yPos = 1
        for listPoint in alpha['titleDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'year up':
        yPos = 1
        for listPoint in alpha['yearUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'year down':
        yPos = 1
        for listPoint in alpha['yearDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'format up':
        yPos = 1
        for listPoint in alpha['formatUp']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    elif userChoice == 'format down':
        yPos = 1
        for listPoint in alpha['formatDown']:     # print all the hits
            print_entry(listPoint.return_releaseId(), release, yPos)
            yPos += 1
    else:
        return CONTINUE

def erase_hits():
    artistWin.erase()
    titleWin.erase()
    yearWin.erase()
    genreWin.erase()
    formatWin.erase()

def refresh_hits():
    global artistWin, titleWin, yearWin, genreWin, formatWin
    artistWin.refresh(POS, 0, 3, 1, MAX_Y-3, SPLIT_X)
    titleWin.refresh(POS, 0, 3, SPLIT_X+1, MAX_Y-3, 2*SPLIT_X)
    yearWin.refresh(POS, 0, 3, 2*SPLIT_X+1, MAX_Y-3, 3*SPLIT_X)
    genreWin.refresh(POS, 0, 3, 3*SPLIT_X+1, MAX_Y-3, 4*SPLIT_X)
    formatWin.refresh(POS, 0, 3, 4*SPLIT_X+1, MAX_Y-3, MAX_X-1)

def show_collection(release):
    searchHits = return_matches(SEARCHINPUT, release)
    alphaDict = sort_items(searchHits)
    erase_hits()
    if SEARCHINPUT != '':
        print_sorted(INPUTTYPE, alphaDict, release)
    refresh_hits()

## UI Section Functions

def menus_setup(menus):
    # create the top menu for selecting things
    left = 2
    for menu in menus:
        menu_name = menu[0]
        menu_hotkey = menu_name[0]
        menu_no_hot = menu_name[1:]
        screen.addstr(1, left, menu_hotkey, hotkey_attr)
        screen.addstr(1, left+1, menu_no_hot, menu_attr)
        left = left + len(menu_name)+3
        topbar_key_handler((str.upper(menu_hotkey), menu[1]))
        topbar_key_handler((str.lower(menu_hotkey), menu[1]))
    screen.refresh()


def topbar_key_handler(key_assign=None, key_dict={}):
    # magic I stole from gnosis.cx
    global SEARCHINPUT
    global POS
    if key_assign:                
        key_dict[ord(key_assign[0])] = key_assign[1]
    else:
        screen.addstr(1, MAX_X-21, " "*20)
        screen.refresh()
        curserPos =  MAX_X-20
        curserMin = curserPos
        screen.move(1, curserPos)
        c = screen.getch()
        userInput = ''
        while c != 10: # 10 is the enter key
            if c == curses.KEY_DOWN: 
                POS += 1
                refresh_hits()
                screen.move(1, curserPos)
                c = screen.getch()
            elif c == curses.KEY_UP and POS > 0:
                POS -= 1
                refresh_hits()
                screen.move(1, curserPos)
                c = screen.getch()
            elif c == curses.KEY_UP and POS == 0:
                refresh_hits()        
                screen.move(1, curserPos)
                c = screen.getch()
            elif c == 127: # 127 is backspace
                if curserPos > curserMin:
                    userInput = userInput[:-1]
                    curserPos -= 1
                    screen.move(1, curserPos)
                    screen.addch(' ') # del character
                    screen.refresh()
                    screen.move(1, curserPos)
                    SEARCHINPUT = userInput
                    show_collection(release)
                    c = screen.getch()
                elif curserPos == curserMin: 
                    userInput = ''
                    SEARCHINPUT = userInput
                    show_collection(release)
                    c = screen.getch()
            elif c < 257: 
                userInput += chr(c)
                screen.addch(1, curserPos, chr(c))
                screen.refresh()
                curserPos += 1
                screen.move(1, curserPos)
                SEARCHINPUT = userInput
                show_collection(release)
                c = screen.getch()
            else:
                c = screen.getch()
        # c = str(screen.getstr(1, MAX_X-20), encoding='utf8')  
        screen.refresh()
        if len(userInput) == 0:
            return CONTINUE
        elif ord(userInput[0]) not in key_dict.keys() or len(userInput) > 1:
            SEARCHINPUT = userInput
            show_collection(release)
            return CONTINUE
        elif ord(userInput[0]) in (curses.KEY_END, ord('!')) and \
                len(userInput) == 1:
            return 0
        else:
            return key_dict[ord(userInput[0])]()


def rm_col(MAX_Y, MAX_X):
    # erase old right box edge when window gets resized
    for yPos in range(1, MAX_Y-1):
        screen.delch(yPos, MAX_X-1)

def rm_row(MAX_Y, MAX_X):
    # erase old bottom box edge when window gets resized
    screen.deleteln()

def exit_func():
    # exit function
    return EXIT

def file_func():
    # file menu for exiting, exiting, etc.
    global INPUTTYPE
    fMenu = curses.newwin(6,20,2,1)
    fMenu.box()
    fMenu.addstr(1,2, "W", hotkey_attr)
    fMenu.addstr(1,3, "rite Something", menu_attr)
    fMenu.addstr(2,2, "C", hotkey_attr)
    fMenu.addstr(2,3, "lear", menu_attr)
    fMenu.addstr(3,2, "T", hotkey_attr)
    fMenu.addstr(3,3, "ype", menu_attr)
    fMenu.refresh()
    set_menu = True
    while set_menu == True:
        c = fMenu.getch()
        if c in (ord('W'), ord('w')):
            screen.addstr(10,10, "Well Hot Damn")
            screen.move(1,23)
            fMenu.erase()
            screen.refresh()
            set_menu = False
        elif c in (ord('C'), ord('c')):
            erase_hits()
            screen.move(1,23)
            fMenu.erase()
            set_menu = False
        elif c in (ord('T'), ord('t')):
            fMenu.addstr(3, 7, "->", menu_attr)
            fMenu.refresh()
            typeMenu = curses.newwin(10, 18, 4, 10)
            typeMenu.box()
            typeMenu.addstr(1, 2, "1", hotkey_attr)
            typeMenu.addstr(1, 3, " Artist Up", menu_attr)
            typeMenu.addstr(2, 2, "2", hotkey_attr)
            typeMenu.addstr(2, 3, " Artist Down", menu_attr)
            typeMenu.addstr(3, 2, "3", hotkey_attr)
            typeMenu.addstr(3, 3, " Title Up", menu_attr)
            typeMenu.addstr(4, 2, "4", hotkey_attr)
            typeMenu.addstr(4, 3, " Title Down", menu_attr)
            typeMenu.addstr(5, 2, "5", hotkey_attr)
            typeMenu.addstr(5, 3, " Year Up", menu_attr)
            typeMenu.addstr(6, 2, "6", hotkey_attr)
            typeMenu.addstr(6, 3, " Year Down")
            typeMenu.addstr(7, 2, "7", hotkey_attr)
            typeMenu.addstr(7, 3, " Format Up", menu_attr)
            typeMenu.addstr(8, 2, "8", hotkey_attr)
            typeMenu.addstr(8, 3, " Format Down", menu_attr)
            t = typeMenu.getch()
            if t == ord('1'):
                INPUTTYPE = 'artist up'
                show_collection(release)
            elif t ==ord('2'):
                INPUTTYPE = 'artist down'
                show_collection(release)
            elif t == ord('3'):
                INPUTTYPE = 'title up'
                show_collection(release)
            elif t == ord('4'):
                INPUTTYPE = 'title down'
                show_collection(release)
            elif t == ord('5'):
                INPUTTYPE = 'year up'
                show_collection(release)
            elif t == ord('6'):
                INPUTTYPE = 'year down'
                show_collection(release)
            elif t == ord('7'):
                INPUTTYPE = 'format up'
                show_collection(release)
            elif t == ord('8'):
                INPUTTYPE = 'format down'
                show_collection(release)
            typeMenu.erase()
            fMenu.erase()
            screen.refresh()
            set_menu = False
        else:
            curses.beep()
    return CONTINUE

def main(stdscr):
    # set up screen for standard terminal size
    global screen
    global MAX_Y
    global MAX_X
    screen = stdscr.subwin(3,MAX_X,0,0)
    screen.keypad(1)
    screen.box()
    screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
    screen.refresh()

    # define menus
    file_menu = ("File", file_func)
    exit_menu = ("Exit", exit_func) # EXIT

    # add topbar menu
    menus_setup((file_menu, exit_menu))

    # set up field windows (soon to be) according to user preferences
    global SPLIT_X
    SPLIT_X = int(MAX_X/5)
    global artistWin, titleWin, yearWin, genreWin, formatWin

    # Set up XML
    dom = parse('discogs.xml') # parse the document                              
    global release 
    release = get_release_info(dom) # get list of all objects with data filled in

    # set up subwindow "pads"
    artistWin = curses.newpad(len(release), 256)
    titleWin = curses.newpad(len(release), 256)
    yearWin = curses.newpad(len(release), 256)
    genreWin = curses.newpad(len(release), 256)
    formatWin = curses.newpad(len(release), 256)

    #topbar menu loop
    while topbar_key_handler():
        new_y, new_x = stdscr.getmaxyx()
        if (new_y, new_x) != (MAX_Y, MAX_X):
            if new_x > MAX_X:
                rm_col(MAX_Y, MAX_X)
            if new_y > MAX_Y:
                rm_row(MAX_Y, MAX_X)
        MAX_Y, MAX_X = new_y, new_x
        SPLIT_X = int(MAX_X/5)
        curses.resizeterm(MAX_Y, MAX_X)
        artistWin.refresh(POS, 0, 3, 1, MAX_Y-3, SPLIT_X)
        titleWin.refresh(POS, 0, 3, SPLIT_X+1, MAX_Y-3, 2*SPLIT_X)
        yearWin.refresh(POS, 0, 3, 2*SPLIT_X+1, MAX_Y-3, 3*SPLIT_X)
        genreWin.refresh(POS, 0, 3, 3*SPLIT_X+1, MAX_Y-3, 4*SPLIT_X)
        formatWin.refresh(POS, 0, 3, 4*SPLIT_X+1, MAX_Y-3, MAX_X-1)
        screen.box()
        screen.hline(2, 1, curses.ACS_HLINE, MAX_X-2)
        screen.refresh()
        # artistWin = curses.newpad(MAX_Y-3, SPLIT_X, 3, 1)
        # titleWin = curses.newpad(MAX_Y-3, SPLIT_X, 3, SPLIT_X+1)
        # yearWin = curses.newpad(MAX_Y-3, SPLIT_X, 3, 2*SPLIT_X+1)
        # genreWin = curses.newpad(MAX_Y-3, SPLIT_X, 3, 3*SPLIT_X+1)
        # formatWin = curses.newpad(MAX_Y-3, SPLIT_X-2, 3, 4*SPLIT_X+1)
        refresh_hits()

if __name__=='__main__':
    try:
        # initialize curses
        stdscr=curses.initscr()
        MAX_Y, MAX_X = stdscr.getmaxyx()
        # turn of fechoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard
        # input
        curses.noecho() ; curses.cbreak()

        # make the cursor invisible
        curses.curs_set(0)

        # in keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be
        # returned
        stdscr.keypad(1)
        main(stdscr)
        # set everything back to normal for clean exit
        screen.keypad(0)
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
    except:
        # in event of an error, restore the terminal
        # to a sane state
        screen.keypad(0)
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()  # print the exception

