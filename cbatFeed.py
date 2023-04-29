#
# Python script to pull the CBAT  "Transient Objects Confirmation Page" RSS feed and turn it into a webpage
#
import feedparser
import configparser
from ukmon_meteortools.utils import sendAnEmail


# turn most recent 50 entries into a webpage
def makeWebpage(myfeed):
    with open('cbattocp.html', 'w', encoding='utf-8') as outf:
        outf.write('<html><head><title>CBAT TOCP Feed</title></head><body>\n')
        for i in range(0,50):
            entry = myfeed.entries[i]
            outf.write('<h1>{:s}</h1>'.format(entry.title))
            body = entry.content[0].value
            outf.write('{:s}'.format(body))
        outf.write('</body></html>\n')


def sendEmail(entry):
    # email a summary to the mailrecip
    localcfg = configparser.ConfigParser()
    localcfg.read('config.ini')
    mailrecip = localcfg['postprocess']['mailrecip'].rstrip()

    message=''
    for li in entry:
        message = message + li + '\n'
    sender = 'website@markmcintyreastro.co.uk'
    sendAnEmail(mailrecip, message, 'CBAT Alert', sender)


def checkIfEmailNeeded(entry):
    entryrows = entry.split('\n')
    #try:
    with open('lastrecord.txt', 'r', encoding='utf-8') as lastrec:
        lastmsg = lastrec.readlines()
        for li in range(0, len(lastmsg)):
            lastmsg[li] = lastmsg[li].strip()
        if entryrows != lastmsg:
            print('new message')
            sendEmail(entryrows)
            with open('lastrecord.txt', 'w', encoding='utf-8') as lastrec:
                lastrec.write(entry)
        else:
            print('no new messages')
    #except Exception:
    #    with open('lastrecord.txt', 'w', encoding='utf-8') as lastrec:
    #        lastrec.write(entry)


if __name__ == "__main__":
    # pull the feed data
    myfeed=feedparser.parse('http://www.cbat.eps.harvard.edu/unconf/tocp.xml')
    
    makeWebpage(myfeed)
    checkIfEmailNeeded(myfeed.entries[0].content[0].value)
