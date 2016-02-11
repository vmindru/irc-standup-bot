from sopel import module
from os import path 
from os import mkdir
from os import listdir
from datetime import datetime

standup_config = {
    'STANDUP_DIR': "/home/vmindru/standup/",
    'MAX_STANDUP_SIZE': 500,
}


@module.commands('standup')
def standup(bot, trigger):


    class stand_bot:
        def __init__(self,bot,trigger,standup_config):
            self.bot = bot
            self.trigger = trigger
            self.STANDUP_DIR = standup_config['STANDUP_DIR']
            self.MAX_STANDUP_SIZE = standup_config['MAX_STANDUP_SIZE']
           
  

        def standup_dir_today(self):
            self.STANDUP_DIR_TODAY=STANDUP_DIR+datetime.today().strftime("%d-%m-%y")+"/"
            return self.STANDUP_DIR_TODAY
        
        def prepare_dirs(self,bot,trigger):
            self.standup_dir_today()
            if not path.exists(self.STANDUP_DIR):
                mkdir(self.STANDUP_DIR,0o700)
                bot.say("standup directory missing, creating "+self.STANDUP_DIR)
            else:
                print("exists")
            if not path.exists(self.STANDUP_DIR_TODAY):
                mkdir(self.STANDUP_DIR_TODAY,0o700)
                bot.say("it's a new day today,creating "+self.STANDUP_DIR_TODAY)
        
        def get_standup(self,STANDUP_DIR_TODAY):
            self.prepare_dirs(self.bot, self.trigger)
            standup_report = {}
            for team_member in listdir(STANDUP_DIR_TODAY):
                team_member_file = STANDUP_DIR_TODAY+team_member
                if path.exists(team_member_file):
                    file = open(team_member_file , 'r')
                    team_member_standup_report = file.read(MAX_STANDUP_SIZE)
                    file.close()
                    print(team_member_standup_report)
                    standup_report[team_member]=team_member_standup_report
            return standup_report
        def record_standup(self,nick,standup_data):
            self.prepare_dirs(self.bot,self.trigger)
            if len(standup_data) < self.MAX_STANDUP_SIZE:
               with open(self.STANDUP_DIR_TODAY+nick, "a") as standup_member_file:
                       standup_member_file.write(standup_data)  
               return True
            else:
               return False
            
        
        def do_standup(self):
            
             
            if trigger.group(3) == "help":
                bot.say("Usage: .standup get - print all standup reports for last day")
                bot.say("Usage: .standup record  your standup text - write down your standup report, this is concatinated and can be used multiple times per day")
                bot.say("Usage: .standup help - display this message")
        
            elif trigger.group(3) == "get":
                standup_report = self.get_standup(self.standup_dir_today())
                if len(standup_report) != 0:
                    for element in standup_report:
                        bot.say(element+" "+standup_report[element])
                else:
                    bot.say("no standup reports for today, the boys are lasy and did not report anthing")
        
            elif trigger.group(3) == "record":
                # TRY TO DO record_standup() function, if it returns TRUE anounce requestor
                if self.record_standup(self.trigger.nick,self.trigger.group(2)):
                    bot.say("recording report: "+self.trigger.group(2))
                else:
                    msglen=str(len(self.trigger.group(2)))
                    bot.say("your message is too big:"+msglen+" , max size:"+str(self.MAX_STANDUP_SIZE))
            else:
                bot.say("Usage: .standup get - print all standup reports for last day")
                bot.say("Usage: .standup record  your standup text - write down your standup report, this is concatinated and can be used multiple times per day")
                bot.say("Usage: .standup help - display this message")
        
    do_standup = stand_bot(bot,trigger,standup_config)
    do_standup.do_standup()

