#!/usr/bin/env python3

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
from pathlib import Path
import re
import subprocess
from datetime import datetime
import urllib.request
import webbrowser

#----------------ARGUMENT PARSING-------------------#
import argparse
parser = argparse.ArgumentParser(description='HEP-JC website updating tool.')

parser.add_argument('-c', '--checkstructure', action='store_true', help='process to update document structure')
parser.add_argument('-l', '--listschedule', action='store_true', help='list the speaking schedule')
parser.add_argument('-d', '--deleteslot', action='store_true', help='delete an existing speaking slot')
parser.add_argument('-n', '--newslot', action='store_true', help='add a new speaking slot')
parser.add_argument('-DS', '--deletesemester', action='store_true', help='delete an entire semester')
parser.add_argument('-NS', '--newsemester', action='store_true', help='create an entire new semester')
parser.add_argument('-dc', '--deletechanges', action='store_true', help='delete changes to current index.html')
parser.add_argument('-db', '--deletebackups', action='store_true', help='delete any stored backup index.html files')
parser.add_argument('-p', '--preview', action='store_true', help='preview changes in default web browser')
parser.add_argument('-u', '--upload', action='store_true', help='upload changes to website')

args = parser.parse_args()
#---------------------------------------------------#

def checkYN(var):
    while var != 'N' and var != 'n' and var != 'Y' and var != 'y':
        print('ERROR:---> enter Y or N')
        var = input()
    return var

#--------------CHECK FOR WEB DATA-------------------#
emptyparams = True
file_input = None
webdata_string = ''
address = []
username = []
domain = []
if os.path.isfile('web_data.txt') == True:
    file_input = open('web_data.txt', 'r')
    webdata_string = file_input.read()
    address = re.findall('\s*WEBSITE\sADDRESS:\s*(\S+)\s*\n', webdata_string)
    username = re.findall('\s*USERNAME:\s*(\S+)\s*\n', webdata_string)
    domain = re.findall('\s*DOMAIN:\s*(\S+)\s*', webdata_string)
    file_input.close()

if address == [] or username == [] or domain == []:
    emptyparams = True
    print('----------------------------------------------------------------')
    print('ERROR:---> need to enter information into web_data.txt file.')
    print('      ---> want to input that information here? (Y/N)')
    print('----------------------------------------------------------------')

    inputYN = str(input()).upper()
    inputYN = checkYN(inputYN)
    if inputYN == 'N':
        sys.exit()
    else:
        correctQ = False
        while correctQ == False:
            print('--------------------')
            print('WEBSITE ADDRESS:')
            print('--------------------\n')
            address = str(input())

            print('--------------------')
            print('USERNAME (for secure copy):')
            print('--------------------\n')
            username = str(input())

            print('--------------------')
            print('DOMAIN (for secure copy):')
            print('--------------------\n')
            domain = str(input())

            print('--------------------')
            print('...will then use the following web data:')
            print('WEBSITE ADDRESS: %s' % address)
            print('USERNAME: %s' % username)
            print('DOMAIN: %s' % domain)
            print('--------------------\n')

            print('OK? (Y/N)')
            OKQ = str(input()).upper()
            OKQ = checkYN(OKQ)
            if OKQ == 'Y':
                webdata_text = """Website information (include /index.html at the end):
------------------------------------------------------------
WEBSITE ADDRESS: %s


Secure copy information:
------------------------------------------------------------
USERNAME: %s
DOMAIN: %s""" % (address, username, domain)

                file_output = open('web_data.txt', 'w')
                file_output.write(webdata_text)
                file_output.close()

                correctQ = True
            else:
                print('...trying again\n')

else:
    emptyparams = False
#---------------------------------------------------#

def writechanges_makebackup(string_var):
    print('--------------------')
    print('Writing changes...')
    print('--------------------')
    current_timestamp = datetime.today()
    os.rename('index.html', 'index_backup%s.html' % current_timestamp)
    file_output = open('index.html', 'w')
    file_output.write(string_var)

    print('---> made backup copy index_backup%s.html' % current_timestamp)
    print('\n')
    print('--------------------------------------------------------------------')
    print('NOTE: - In order to upload changes you need to run with the -u option.')
    print('      - To remove all changes just delete the index.html file.')
    print('      - To recover partial changes, rename appropriate local backup file to index.html.')
    print('--------------------------------------------------------------------')

if args.checkstructure == False and args.listschedule == False and args.deleteslot == False and args.newslot == False and args.deletesemester == False and args.newsemester == False and args.deletechanges == False and args.deletebackups == False and args.preview == False and args.upload == False:
    print('\n')
    print('=============================================')
    print('*~*~*~* HEP-JC WEBSITE UPDATING TOOL ~*~*~*~*')
    print('=============================================')

    chesirecat = """
                  .'\   /`.
                .'.-.`-'.-.`.
           ..._:   .-. .-.   :_...
         .'    '-.( o) (o ).-'    `.
        :  _    _ _`~(_)~`_ _    _  :
       :  /:   ' .-=_   _=-. `   ;\  :
       :   :|-.._  '     `  _..-|:   :
        :   `:| |`:-:-.-:-:'| |:'   :
         `.   `.| | | | | | |.'   .'
           `.   `-:_| | |_:-'   .'
             `-._   ````    _.-'
                 ``-------''


    -->  [c] to ensure site colors/structure up to date (*run regularly*)
    -->  [l] to list current schedule
    -->  [d] to delete a slot
    -->  [n] to add a new slot
    --> [DS] to delete a semester
    --> [NS] to add a new semester
    --> [dc] to delete current saved changes on index.html
    --> [db] to delete any stored backup index.html files
    -->  [p] to preview changes in web browser
    -->  [u] to upload changes to server

    (also can use all of the above as flags to hepjc.py)
    """
    print(chesirecat)

    runinput = input()

    if runinput == 'c':
        args.checkstructure = True
    elif runinput == 'l':
        args.listschedule = True
    elif runinput == 'd':
        args.deleteslot = True
    elif runinput == 'n':
        args.newslot = True
    elif runinput == 'DS':
        args.deletesemester = True
    elif runinput == 'NS':
        args.newsemester = True
    elif runinput == 'dc':
        args.deletechanges = True
    elif runinput == 'db':
        args.deletebackups = True
    elif runinput == 'p':
        args.preview = True
    elif runinput == 'u':
        args.upload = True

    print('\n')


# import the main webpage (if necessary and allowed):
if os.path.isfile('index.html') == 0 and emptyparams == False and args.deletebackups != True:
    url = address[0]
    response = urllib.request.urlopen(url)
    data = response.read()
    page = data.decode('utf-8')
    file_download = open('index.html', 'w')
    file_download.write(page)
    file_download.close()

file_input = Path('index.html')
string_input = ''
if file_input.is_file():
    file_input = open('index.html', 'r')
    string_input = file_input.read()

part1 = r'\s*<td>(\d+(?::\d\d)?\s*(?:AM|PM))\s-\s(\d\d/\d\d/\d\d)</td>\n'
part2 = r'\s*<td>(.+)</td>'
part3 = r'\s*<td>(.+)</td>'
part4 = r'\s*<td>(.+)</td>'
fullpart = part1 + part2 + part3 + part4
entries = re.findall(fullpart, string_input)

def list_schedule(string_input):
    entries = re.findall(fullpart, string_input)

    print('------------------------------------------------------')
    print('[No.] [TIME   DATE      ROOM]    SPEAKER')
    print('------------------------------------------------------')
    i = 1
    for entry in entries:
        if len(entry[0]) < 4:
            print('[%.3d]  [0%s %s %s]    %-5s' % (i, entry[0], entry[1], entry[2], entry[3]))
        else:
            print('[%.3d]  [%s %s %s]    %-5s' % (i, entry[0], entry[1], entry[2], entry[3]))
        i = i + 1

def find_new_slot_number(date, string_input):
    entries = re.findall(fullpart, string_input)
    datetofit = datetime.strptime(date, "%m/%d/%y")

    i = 0
    result = 0
    for entry in entries:
        if entry[1] != '':
            dateentry = datetime.strptime(entry[1], "%m/%d/%y")

            if dateentry > datetofit:
                result = i
                break
            elif (result == 0) and (i == len(entries)-1):
                result = len(entries)

        i = i + 1

    return result

if args.checkstructure == True:
    print('\n')
    print('------------------------------------------------------')
    print('CHECK DOCUMENT STRUCTURE:')
    print('------------------------------------------------------')

    green_bgcolor = '66CC66'
    past_bgcolor = 'A4A4A4'
    missed_bgcolor = '777777'

    currentslotindex = 0
    slots = re.findall('\s*<tr\s*(bgcolor=\"#[a-zA-Z0-9]+\")?\s*>\s*\n\s*<td>(\d+)(?::\d\d)?(?:AM|PM)\s*-\s*(\d\d/\d\d/\d\d)</td>\s*', string_input)
    new_string = string_input
    for slot in slots:
        if slot[2] != '':
            slotdate = datetime.strptime(slot[2], "%m/%d/%y")
            if (datetime.now() > slotdate) == True:
                newslotnumber = find_new_slot_number(slot[2],new_string)

                i = 1
                for item in new_string.split('\n'):
                    if entries[newslotnumber-1][0] + ' - ' + entries[newslotnumber-1][1] in item:
                        add_line = i - 1
                    i = i + 1

                add_string = ''
                if slot[1] != '00':
                    add_string = "\t<tr bgcolor=\"#%s\">" % past_bgcolor
                else:
                    add_string = "\t<tr bgcolor=\"#%s\">" % missed_bgcolor
                new_string = '\n'.join(new_string.split('\n')[0:add_line-1] + add_string.split('\n')[0:len(add_string.split('\n'))] + new_string.split('\n')[add_line:len(new_string.split('\n'))])

            if (datetime.now() > slotdate) == False:
                newslotnumber = find_new_slot_number(slot[2],new_string)

                i = 1
                for item in new_string.split('\n'):
                    if entries[newslotnumber-1][0] + ' - ' + entries[newslotnumber-1][1] in item:
                        add_line = i - 1
                    i = i + 1

                add_string = ''
                if slot[1] != '00':
                    add_string = "\t<tr bgcolor=\"#%s\">" % green_bgcolor
                else:
                    add_string = "\t<tr bgcolor=\"#%s\">" % missed_bgcolor
                new_string = '\n'.join(new_string.split('\n')[0:add_line-1] + add_string.split('\n')[0:len(add_string.split('\n'))] + new_string.split('\n')[add_line:len(new_string.split('\n'))])

                currentslotindex = slots.index(slot)

                break

    for slot in slots:
        if slot[2] != '' and slots.index(slot) > currentslotindex:
            slotdate = datetime.strptime(slot[2], "%m/%d/%y")
            if (datetime.now() < slotdate) == True:
                newslotnumber = find_new_slot_number(slot[2],new_string)

                i = 1
                for item in new_string.split('\n'):
                    if entries[newslotnumber-1][0] + ' - ' + entries[newslotnumber-1][1] in item:
                        add_line = i - 1
                    i = i + 1

                add_string = ''
                if slot[1] != '00':
                    add_string = "\t<tr>"
                else:
                    add_string = "\t<tr bgcolor=\"#%s\">" % missed_bgcolor
                new_string = '\n'.join(new_string.split('\n')[0:add_line-1] + add_string.split('\n')[0:len(add_string.split('\n'))] + new_string.split('\n')[add_line:len(new_string.split('\n'))])


    # determine current semester to decide expand/collapse profile
    semester_pattern = r'<label\s+for="((?:fall|spring|summer))([0-9]+)">'
    find_semesters = re.findall(semester_pattern, string_input)

    print('------------------------------------------------------')
    print('Which is the current semester?')
    print('------------------------------------------------------')

    for i in range(0,len(find_semesters)):
        print('[%d] %s %s' % (i,find_semesters[i][0],find_semesters[i][1]))

    semesterint = int(input())
    while semesterint > len(find_semesters)-1 or semesterint < 0 or isinstance(semesterint,int) == False:
        print('ERROR:---> enter a valid current semester.')
        semesterint = int(input())
    current_semester = find_semesters[semesterint]

    line1 = r'(\s*<label\sfor=\"[a-z]+\d\d\d\d\">[A-Z]+\s\d\d\d\d\s*&nbsp;<br>\s*\[click to expand/collapse\]</label>\s*\n'
    line2 = r'\s*<input.*>\n'
    line3 = r'\s*</td>\s*\n'
    line4 = r'\s*</tr>\s*\n'
    line5 = r'\s*</tbody>\s*)'
    matchlines = line1 + line2 + line3 + line4 + line5
    changeline= r'<tbody\sclass=\"hide\"\s*(.*)>'
    toggledata = re.findall(matchlines+changeline, new_string)
    for i in range(0,len(toggledata)):
        if i != semesterint and toggledata[i][1] == '':
            print('CHANGES: found previous/future semester that is expanded on page load....fixing.')
            new_string = re.sub(re.escape(toggledata[i][0]) + r'<tbody\sclass=\"hide\"\s*.*>', toggledata[i][0] + r'<tbody class="hide" style="display:none">' + r'\n', new_string)
        elif i == semesterint and toggledata[i][1] != '':
            print('CHANGES: found current semester that is collapsed on page load....fixing.')
            new_string = re.sub(re.escape(toggledata[i][0]) + r'<tbody\sclass=\"hide\"\s*.*>', toggledata[i][0] + r'<tbody class="hide">' + r'\n', new_string)

    writechanges_makebackup(new_string)

if args.listschedule == True:
    print('\n')
    print('------------------------------------------------------')
    print('LIST SLOTS:')
    print('------------------------------------------------------')

    list_schedule(string_input)

if args.deleteslot == True:
    print('\n')
    print('------------------------------------------------------')
    print('DELETE AN EXISTING SLOT:')
    print('------------------------------------------------------\n')
    print('Press any key to list current slots.')
    input()
    list_schedule(string_input)

    print('\n')
    print('Input the [No.] of the slot to remove:')
    delete_index = int(input())
    while isinstance(delete_index, int) == False:
        print('ERROR:---> enter a valid slot (an integer) to delete.')
        delete_index = input()

    i = 1
    kill_line = 0
    entries = re.findall(fullpart, string_input)
    for item in string_input.split('\n'):
        if entries[delete_index-1][0] + ' - ' + entries[delete_index-1][1] in item:
            kill_line = i - 1
            begin_kill = i - 2
            end_kill = i + 4
        i = i + 1

    new_string = '\n'.join(string_input.split('\n')[0:kill_line-2] + string_input.split('\n')[kill_line+5:len(string_input.split('\n'))])

    print('\n')
    print('------------------------------------------------------')
    print('CONFIRM RESULTING SCHEDULE:')
    print('------------------------------------------------------')
    print('\n')

    print('Deleting the following slot:')
    print(entries[delete_index-1])
    print('will produce the following schedule...press [ENTER].')

    list_schedule(new_string)

    print('\n')
    print('Confirm removal of this slot? (Y or N)')
    confirm_deleteQ = str(input()).upper()
    confirm_deleteQ = checkYN(confirm_deleteQ)

    if confirm_deleteQ == 'Y':
        writechanges_makebackup(new_string)

if args.newslot == True:
    print('\n')
    print('------------------------------------------------------')
    print('ADD A NEW SLOT:')
    print('------------------------------------------------------')
    finalizeQ = 'N'

    print('--------------------------------')
    print('Is this to show that a talk will *not* be held (e.g., spring break)? (Y/N)')
    talknotheldQ = str(input()).upper()
    talknotheldQ = checkYN(talknotheldQ)
    print('--------------------------------')

    if talknotheldQ == 'Y':
        print('--------------------------------')
        print('Enter date that will be missed (mm/dd/yy):')
        new_date = input()
        while re.compile("\d\d/\d\d/\d\d").match(new_date) == None:
            print('ERROR:---> enter date in requested format.')
            new_date = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter the message to be shown in place of the talk title:')
        new_title = input()
        print('--------------------------------')

        print('================================')
        print('================================')
        print(r'Finalize the posting containing the following information? (Y or N):')
        print('DATE: %s' % new_date)
        print('ROOM: ---')
        print('SPEAKER: ---')
        print('TITLE: %s' % new_title)
        print('================================')
        print('================================')

        finalizeQ = str(input()).upper()
        finalizeQ = checkYN(finalizeQ)

        add_string = ''
        add_string += '\n'
        add_string += '\t' + r'<tr bgcolor="#777777">' + '\n'
        add_string += '\t' + r'<td>00AM - %s</td>' % new_date + '\n'
        add_string += '\t' + r'<td>&mdash;&mdash;&mdash;</td>' + '\n'
        add_string += '\t' + r'<td>&mdash;&mdash;&mdash;</td>' + '\n'
        add_string += '\t' + r'<td>%s</td>' % new_title + '\n'
        add_string += '\t' + r'</tr>' + "\n"

        newslotnumber = find_new_slot_number(new_date,string_input)

        i = 1
        for item in string_input.split('\n'):
            if newslotnumber != len(entries):
                if entries[newslotnumber][0] + ' - ' + entries[newslotnumber][1] in item:
                    add_line = i - 2
                i = i + 1
            else:
                if entries[len(entries)-1][0] + ' - ' + entries[len(entries)-1][1] in item:
                    add_line = i + 5
                i = i + 1

        new_string = '\n'.join(string_input.split('\n')[0:add_line-1] + add_string.split('\n')[0:len(add_string.split('\n'))] + string_input.split('\n')[add_line:len(string_input.split('\n'))])

        writechanges_makebackup(new_string)

    while finalizeQ == 'N':
        print('--------------------------------')
        print('Enter time (xxAM or xxPM):')
        new_time = input()
        new_time = new_time.replace(" ", "") # get rid of any spaces (particularly between numbers and AM/PM)
        while re.compile("\d\d(AM|PM)").match(new_time) == None:
            print('ERROR:---> enter time in requested format.')
            new_time = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter date (mm/dd/yy):')
        new_date = input()
        while re.compile("\d\d/\d\d/\d\d").match(new_date) == None:
            print('ERROR:---> enter date in requested format.')
            new_date = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter room for talk (PAS ###):')
        new_room = input()
        while re.compile("PAS \d\d\d").match(new_room) == None:
            print('ERROR:---> enter room in requested format.')
            new_room = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter the speaker\'s name (first last):')
        new_speaker = input()
        while re.compile("^[a-zA-Z]*(&[^&;]+;)*[a-zA-Z]*\s+[a-zA-Z]*(&[^&;]+;)*[a-zA-Z]*$").match(new_speaker) == None:
            print('ERROR:---> enter speaker name in requested format.')
            new_speaker = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter talk/paper title:')
        new_title = input()
        print('--------------------------------')

        print('--------------------------------')
        print('Enter web link to *main* paper that will be discussed (if none press [ENTER]):')
        new_link = input()
        while re.compile("^https?://.*$").match(new_link) == None:
            if new_link == '':
                break
            print('ERROR:---> link must begin with http(s)://')
            new_link = input()
        print('--------------------------------')

        otherlinks = []
        if new_link != '':
            print('--------------------------------')
            print('Any other relevant papers that should be linked for this talk? (Y or N)')
            otherlinksQ = str(input()).upper()
            otherlinksQ = checkYN(otherlinksQ)

            if otherlinksQ == 'Y' or otherlinksQ == 'y':
                while len(otherlinks) >= 0:
                    print('Enter other link #%d:' % (len(otherlinks)+1))
                    otherlinkenter = input()
                    while re.compile("^https?://.*$").match(otherlinkenter) == None:
                        print('ERROR:---> link must begin with http(s)://')
                        otherlinkenter = input()
                    otherlinks.append(otherlinkenter)

                    print('Any others? (Y or N)')
                    otherlinksQ = str(input()).upper()
                    otherlinksQ = checkYN(otherlinksQ)
                    if otherlinksQ == 'N':
                        break
            print('--------------------------------')

        print('================================')
        print('================================')
        print(r'Finalize the posting containing the following information? (Y or N):')
        print('TIME: %s' % new_time)
        print('DATE: %s' % new_date)
        print('ROOM: %s' % new_room)
        print('SPEAKER: %s' % new_speaker)
        print('TALK/PAPER TITLE: %s' % new_title)
        if new_link != '':
            print('MAIN LINK: %s' % new_link)
        for otherlink in otherlinks:
            print('OTHER LINK #%d: %s' % (otherlinks.index(otherlink)+1, otherlink))
        print('================================')
        print('================================')

        finalizeQ = str(input()).upper()
        finalizeQ = checkYN(finalizeQ)
        if finalizeQ == 'Y':
            add_date = datetime.strptime(new_date, "%m/%d/%y")

            titletext = ''
            # construct title link
            if new_link == '':
                titletext += r'%s' % new_title
            else:
                titletext += r'<a href=%s target="_blank">%s</a>' % (new_link, new_title)
            # construct (see also [1] [2]...) links
            if len(otherlinks) != 0:
                titletext += r' (see also '
                for otherlink in otherlinks:
                    if otherlinks.index(otherlink) != len(otherlinks) - 1:
                        titletext += r'<a href="%s" target="_blank">[%d]</a> ' % (otherlink, otherlinks.index(otherlink)+1)
                    else:
                        titletext += r'<a href="%s" target="_blank">[%d]</a>' % (otherlink, otherlinks.index(otherlink)+1)
                titletext += r')'

            add_string = ''
            add_string += '\n'
            if add_date > datetime.now():
                add_string += '\t' + r'<tr>' + '\n'
            elif add_date <= datetime.now():
                add_string += '\t' + r'<tr bgcolor="#A4A4A4">' + '\n'
            add_string += '\t' + r'<td>%s - %s</td>' % (new_time,new_date) + '\n'
            add_string += '\t' + r'<td>%s</td>' % new_room + '\n'
            add_string += '\t' + r'<td>%s</td>' % new_speaker + '\n'
            add_string += '\t' + r'<td>%s</td>' % titletext + '\n'
            add_string += '\t' + r'</tr>' + "\n"

            newslotnumber = find_new_slot_number(new_date,string_input)

            i = 1
            for item in string_input.split('\n'):
                if newslotnumber != len(entries):
                    if entries[newslotnumber][0] + ' - ' + entries[newslotnumber][1] in item:
                        add_line = i - 2
                    i = i + 1
                else:
                    if entries[len(entries)-1][0] + ' - ' + entries[len(entries)-1][1] in item:
                        add_line = i + 5
                    i = i + 1

            new_string = '\n'.join(string_input.split('\n')[0:add_line-1] + add_string.split('\n')[0:len(add_string.split('\n'))] + string_input.split('\n')[add_line:len(string_input.split('\n'))])

            writechanges_makebackup(new_string)

            break

if args.deletesemester == True:
    semester_pattern = r'<label\s+for="((?:fall|spring|summer))([0-9]+)">'
    find_semesters = re.findall(semester_pattern, string_input)

    print('------------------------------------------------------')
    print('CHOOSE A SEMESTER TO DELETE (enter [#]):')
    print('------------------------------------------------------')
    for i in range(0,len(find_semesters)):
        print('[%d] %s %s' % (i,find_semesters[i][0],find_semesters[i][1]))

    semesterint = int(input())
    while semesterint > len(find_semesters)-1 or semesterint < 0 or isinstance(semesterint,int) == False:
        print('ERROR:---> enter a valid semester to delete.')
        semesterint = int(input())

    i = 1
    beginkill_line = 0
    endkill_line = 0
    find_endtable = re.findall('</table>', string_input)
    for item in string_input.split('\n'):
        if find_semesters[semesterint][0]+find_semesters[semesterint][1] in item:
            beginkill_line = i - 4

        if semesterint < len(find_semesters)-1:
            if find_semesters[semesterint+1][0]+find_semesters[semesterint+1][1] in item:
                endkill_line = i - 5
        else:
            if find_endtable[0] in item:
                print('here')
                endkill_line = i - 2
                break

        i = i + 1

    new_string = '\n'.join(string_input.split('\n')[0:beginkill_line-1] + string_input.split('\n')[endkill_line:len(string_input.split('\n'))])

    writechanges_makebackup(new_string)

if args.newsemester == True:
    def seasonint(season):
        season = str(season).upper()
        if season == 'SPRING':
            return 0
        elif season == 'SUMMER':
            return 1
        else:
            return 2

    def compare_sems(sem1, sem2):
        # return -1 for sem1 > sem2
        # return +0 for sem1 = sem2
        # return +1 for sem1 < sem2

        yearcompare = 0
        seasoncompare = 0

        if int(sem1[1]) > int(sem2[1]):
            yearcompare = -1
        elif int(sem1[1]) == int(sem2[1]):
            yearcompare = 0
        else:
            yearcompare = 1

        if seasonint(sem1[0]) > seasonint(sem2[0]):
            seasoncompare = -1
        elif seasonint(sem1[0]) == seasonint(sem2[0]):
            seasoncompare = 0
        else:
            seasoncompare = 1

        if yearcompare == 1:
            return 1
        elif yearcompare == 0:
            return seasoncompare
        else:
            return -1


    print('------------------------------------------------------')
    print('CREATE NEW SEMESTER OF SPEAKING SLOTS:')
    print('------------------------------------------------------')

    print('--------------------------------')
    print('What year?')
    print('--------------------------------')
    new_year = int(input())
    while isinstance(new_year,int) == False or new_year < 2000:
        print('ERROR:---> enter a valid semester year.')
        new_year = int(input())

    print('--------------------------------')
    print('What season? (spring/summer/fall)')
    print('--------------------------------')
    new_season = str(input()).upper()
    while new_season != 'SPRING' and new_season != 'SUMMER' and new_season != 'FALL':
        print('ERROR:---> enter a valid semester season.')
        new_season = str(input()).upper()

    sem_add = [new_season, new_year]

    semester_pattern = r'<label\s+for="((?:fall|spring|summer))([0-9]+)">'
    find_semesters = re.findall(semester_pattern, string_input)
    sems = [list(el) for el in find_semesters]
    sems = [[el[0].upper(),el[1]] for el in sems]

    # check to see if semester already exists
    for sem in sems:
        if compare_sems(sem, sem_add) == 0:
            print('ERROR: semester selected already exists! (delete it first if necessary)')
            break

    sem_after = []

    # check for semester that follows sem_add (except if first/last)
    for i in range(0,len(sems)):
        if compare_sems(sems[i], sem_add) == +1 and i+1 < len(sems):
            sem_after = sems[i+1]
            break

    # check to see if it should be the earliest listed
    if compare_sems(sems[0], sem_add) == -1:
        sem_after = sems[0]

    # check to see if it should be the latest listed
    if compare_sems(sems[len(sems)-1], sem_add) == +1:
        sem_after = []

    semtag = sem_add[0].lower() + str(sem_add[1])
    semtext = """\t<tbody class="labels">
    <tr>
    <td colspan="4">
    <label for="%s">%s %s &nbsp;<br> [click to expand/collapse]</label>
    <input type="checkbox" name="%s" id="%s" data-toggle="toggle">
    </td>
    </tr>
    </tbody>

    <tbody class="hide">

    <tr>
    <td>00AM - 00/00/00</td>
    <td>TBA</td>
    <td>TBA</td>
    <td>TBA</td>
    </tr>

    </tbody>
    """ % (semtag, sem_add[0].upper(), str(sem_add[1]), semtag, semtag)

    if sem_after != []:
        semaftertag = sem_after[0].lower() + str(sem_after[1])
        i = 1
        add_line = 0
        for item in string_input.split('\n'):
            if r'<label for="%s">%s %s &nbsp;<br> [click to expand/collapse]</label>' % (semaftertag,sem_after[0].upper(),str(sem_after[1])) in item:
                add_line = i - 4
                break
            i = i + 1

        new_string = '\n'.join(string_input.split('\n')[0:add_line] + semtext.split('\n')[0:len(semtext.split('\n'))] + string_input.split('\n')[add_line:len(string_input.split('\n'))])
    else:
        i = 1
        add_line = 0
        for item in string_input.split('\n'):
            if r'</table>' in item:
                add_line = i - 3
                break
            i = i + 1

        new_string = '\n'.join(string_input.split('\n')[0:add_line] + ('\n' + semtext).split('\n')[0:len(semtext.split('\n'))] + string_input.split('\n')[add_line:len(string_input.split('\n'))])

    writechanges_makebackup(new_string)

if args.deletechanges == True:
    print('\n')
    print('------------------------------------------------------')
    print('DELETE CHANGES to current index.html FILE:')
    print('------------------------------------------------------')
    for f in os.listdir('.'):
        if re.search('index.html', f):
            print('---> %s removed.' % f)
            os.remove(f)

if args.deletebackups == True:
    print('\n')
    print('------------------------------------------------------')
    print('DELETE BACKUP index.html FILES:')
    print('------------------------------------------------------')
    for f in os.listdir('.'):
        if re.search('index_backup.+\.html', f):
            print('---> %s removed.' % f)
            os.remove(f)

if args.preview == True:
    webbrowser.open('index.html', new=2)

if args.upload == True:
    print('\n')
    print('------------------------------------------------------')
    print('UPLOAD index.html CHANGES TO SERVER:')
    print('------------------------------------------------------')

    sourcefile = 'index.html'
    destinationfile = 'public_html/index.html'

    subprocess.Popen(["scp", sourcefile, "%s@%s:%s" % (username[0],domain[0],destinationfile)]).wait()

    print('Was the transfer successful? (Y or N)')
    check = input()
    check = checkYN(check)
    if check != 'Y':
        print('OK, saved index.html changes --- check login credentials and try again to upload.')

if args.checkstructure == False and args.listschedule == False and args.deleteslot == False and args.newslot == False and args.deletesemester == False and args.newsemester == False and args.deletechanges == False and args.deletebackups == False and args.preview == False and args.upload == False:
    print('\n')
    print('=============================================')
    print('------------------QUITTING-------------------')
    print('=============================================')
