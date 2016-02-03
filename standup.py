from sopel import module
from os import path 
from os import mkdir
from datetime import datetime

STANDUP_DIR="/home/vmindru/standup/"
STANDUP_DIR_TODAY=STANDUP_DIR+datetime.today().strftime("%d-%m-%y")+"/"
TEAM_MEMBERS=['vkaigoro','vmindru','vmindru1']
MAX_STANDUP_SIZE=500


@module.commands('standup')
def standup(bot, trigger):
    do_prepare_dirs(STANDUP_DIR,bot,trigger)
    return do_standup(STANDUP_DIR_TODAY,bot,trigger)

def do_prepare_dirs(STANDUP_DIR,bot,trigger) :
    if not path.exists(STANDUP_DIR):
        mkdir(STANDUP_DIR,0o700)
        bot.say("standup directory missing, creating "+STANDUP_DIR)
    else:
        print("exists")
    if not path.exists(STANDUP_DIR_TODAY):
        mkdir(STANDUP_DIR_TODAY,0o700)
        bot.say("it's a new day today,creating "+STANDUP_DIR_TODAY)

def get_standup(STANDUP_DIR_TODAY):
    standup_report = {}
    for team_member in TEAM_MEMBERS:
        team_member_file = STANDUP_DIR_TODAY+team_member
        if path.exists(team_member_file):
            file = open(team_member_file , 'r')
            team_member_standup_report = file.read(MAX_STANDUP_SIZE)
            file.close()
            print(team_member_standup_report)
            standup_report[team_member]=team_member_standup_report
    return standup_report
def record_standup(STANDUP_DIR_TODAY,nick,standup_data):
    if len(standup_data) < MAX_STANDUP_SIZE:
       with open(STANDUP_DIR_TODAY+nick, "a") as standup_member_file:
               standup_member_file.write(standup_data)  
       return True
    else:
       return False
    

def do_standup(STANDUP_DIR_TODAY,bot,trigger):

    if trigger.group(3) == "get":
        standup_report = get_standup(STANDUP_DIR_TODAY)
        for element in standup_report:
            bot.say(element+" "+standup_report[element])
    elif trigger.group(3) == "record":
        if record_standup(STANDUP_DIR_TODAY,trigger.nick,trigger.group(2)):
            bot.say("recording report: "+trigger.group(2))
        else:
            msglen=str(len(trigger.group(2)))
            bot.say("your message is too big:"+msglen+" , max size:"+str(MAX_STANDUP_SIZE))

