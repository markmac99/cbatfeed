#
# Python script to pull the CBAT  "Transient Objects Confirmation Page" RSS feed and turn it into a webpage
#
import os
import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser


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
    smtphost = localcfg['postprocess']['mailhost'].rstrip()
    smtpport = int(localcfg['postprocess']['mailport'].rstrip())
    smtpuser = localcfg['postprocess']['mailuser'].rstrip()
    smtppwd = localcfg['postprocess']['mailpwd'].rstrip()
    with open(os.path.expanduser(smtppwd), 'r') as fi:
        line = fi.readline()
        spls=line.split('=')
        smtppass=spls[1].rstrip()

    s = smtplib.SMTP(smtphost, smtpport)
    s.starttls()
    s.login(smtpuser, smtppass)
    msg = MIMEMultipart()

    msg['From']='website@markmcintyreastro.co.uk'
    msg['To']=mailrecip

    msg['Subject']='CBAT Alert'
    message=''
    for li in entry:
        message = message + li + '\n'
    msg.attach(MIMEText(message, 'plain'))
    s.sendmail(msg['From'], mailrecip, msg.as_string())
    s.close()


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
