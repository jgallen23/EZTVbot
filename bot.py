import irclib
import re
import os
import csv

data_file = os.path.expanduser("~/.eztvbot")

irc = irclib.irc("irc.efnet.pl", "6667", "jga_tv", "jgaPyBot", "jga tvdwnl", "#eztv", debug = False)

def read_data():
    if os.path.exists(data_file):
        return [row for row in csv.reader(open(data_file, 'rb'))]
    else:
        return []

def write_data(data):
    writer = csv.writer(open(data_file, 'wb'), quoting=csv.QUOTE_NONE)
    writer.writerows(data)

def data_received(data):
    """
    :^EZBot^!ezbot@staff.eztv.se PRIVMSG #EZTV :Out now: American Idol S09E01 HDTV XviD-2HD - http://www.bt-chat.com/download.php?id=69578
    :^EZBot^!ezbot@staff.eztv.se PRIVMSG #EZTV :Out now: American Idol S08E03 HDTV XviD-2HD - http://re.zoink.it/4b566e97
    MATCH %s [('\x02American Idol S08E03 HDTV XviD-2HD\x02', 'http://re.zoink.it/4b566e97\x02\x02\x02\x02\r')]
    """
    #print data
    if data.startswith(":^EZBot^"):
        data = data.replace("\x02", "").replace("\r", "")
        print data
        matches = re.compile(":\^EZBot\^!.*?Out now: (.*?) - (.*?)$").findall(data)
        if len(matches) != 0:
            match = matches[0]
            print "MATCH", match
            current_data = read_data()
            exists = [data for data in current_data if data[0] == match[0]]
            if not exists:
                current_data.append(match)
                write_data(current_data)

irc.data_received_handler = data_received

try:
    irc.connect()
except KeyboardInterrupt:
    irc.disconnect()

