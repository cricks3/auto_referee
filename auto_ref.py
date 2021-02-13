"""
Functions to open AC, manage lobby chat, create a game, enter the game, send in-game messages, and upload replay file
"""
from credentials import ac_logins, cta_logins, paths
from itertools import combinations
from pywinauto import Application
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import glob
import os
import pywinauto
import time
import datetime
        
class AutoRef():
    def __init__(self):
        self.driver = None
        self.username = None
        self.chat_text = None
        self.is_autoref_requested = None
        self.hub = None
        self.game_password = "titan"
        self.elected_map = None
        self.latest_file = None
        self.participants = None
        self.below_min = None
        self.sit_outs = None
        self.map_key = {"joy" : {"map_name" : "JoyNoDHT",
                                 "has_halves" : True,
                                 "time_length" : 10, 
                                 "map_min" : 6,
                                 "map_max" : 10},
                        "bfd" : {"map_name" : "BFDnoDHT",
                                 "has_halves" : False,
                                 "time_length" : 14,
                                 "map_min" : 6,
                                 "map_max" : 10},
                        "lambda" : {"map_name" : "Lambda.0.2", 
                                    "has_halves" : False,
                                    "time_length" : 14,
                                    "map_min" : 6,
                                    "map_max" : 8},
                        "hectic" : {"map_name" : "Hectic5.0",
                                    "has_halves" : True,
                                    "time_length" : 8,
                                    "map_min" : 6,
                                    "map_max" : 10},
                        "stank" : {"map_name" : "Stank",
                                   "has_halves" : False,
                                   "time_length" : 14,
                                   "map_min" : 8,
                                   "map_max" : 10},
                        "beta" : {"map_name" : "Beta.0.0",
                                  "has_halves" : False,
                                  "time_length" : 14,
                                  "map_min" : 8,
                                  "map_max" : 10},
                        "trenches" : {"map_name" : "Trenches",
                                      "has_halves" : False,
                                      "time_length" : 14,
                                      "map_min" : 8,
                                      "map_max" : 10},
                        "lnsight" : {"map_name" : "lnsight",
                                     "has_halves" : False,
                                     "time_length" : 14,
                                     "map_min" : 8,
                                     "map_max" : 10},
                        "zodiac" : {"map_name" : "ZODIAC",
                                    "has_halves" : False,
                                    "time_length" : 14,
                                    "map_min" : 8,
                                    "map_max" : 10},
                        "mu" : {"map_name" : "Mu.0.1",
                                "has_halves" : False,
                                "time_length" : 14,
                                "map_min" : 10,
                                "map_max" : 20},
                        "goodcompany" : {"map_name" : "GoodCompanynoDHT1.1",
                                         "has_halves" : False,
                                         "time_length" : 14,
                                         "map_min" : 10,
                                         "map_max" : 20},
                        "stronghold" : {"map_name" : "StrongholdNODHT",
                                        "has_halves" : False,
                                        "time_length" : 14,
                                        "map_min" : 10,
                                        "map_max" : 20},
                        "crowded(assassin)" : {"map_name" : "Crowded(Assassin)",
                                               "has_halves" : False,
                                               "time_length" : 14,
                                               "map_min" : 10,
                                               "map_max" : 20},
                        "smear" : {"map_name" : "SmearUltimate2",
                                   "has_halves" : False,
                                   "time_length" : 14,
                                   "map_min" : 10,
                                   "map_max" : 20},
                        "trenchesxl" : {"map_name" : "Trenches-XL",
                                        "has_halves" : False,
                                        "time_length" : 14,
                                        "map_min" : 10,
                                        "map_max" : 20},
                        "strokin" : {"map_name" : "StraightStrokin",
                                     "has_halves" : False,
                                     "time_length" : 14,
                                     "map_min" : 10,
                                     "map_max" : 20},
                        "ggremix" : {"map_name" : "GG_remixNoDHT",
                                     "has_halves" : False,
                                     "time_length" : 14,
                                     "map_min" : 10,
                                     "map_max" : 20},
                        "bait" : {"map_name" : "BaitOrSwitch2",
                                  "has_halves" : False,
                                  "time_length" : 14,
                                  "map_min" : 10,
                                  "map_max" : 20},
                        "grinder" : {"map_name" : "grinder3",
                                     "has_halves" : False,
                                     "time_length" : 14,
                                     "map_min" : 10,
                                     "map_max" : 20},
                        "koth" : {"map_name" : "koth.0.9b(250)",
                                  "has_halves" : False,
                                  "time_length" : 14,
                                  "map_min" : 10,
                                  "map_max" : 20},
                        "kennedy" : {"map_name" : "kennedyNoDHT",
                                     "has_halves" : False,
                                     "time_length" : 14,
                                     "map_min" : 10,
                                     "map_max" : 20},
                        "money" : {"map_name" : "Money-Regen2.0",
                                   "has_halves" : False,
                                   "time_length" : 14,
                                   "map_min" : 10,
                                   "map_max" : 20},
                        "gamma" : {"map_name" : "Gamma.0.2",
                                   "has_halves" : False,
                                   "time_length" : 14,
                                   "map_min" : 10,
                                   "map_max" : 20}}
                        
        self.map_min = None
        self.map_max = None
        
        self.game_state = None
    
    def open_ac(self, username, password, path=r"C:\Program Files\Mozilla Firefox\firefox.exe"):
        """ 
        Summary:
        Command to open Google Chrome and navigate to Armor Critical lobby

        Parameters: 
        username (string): Username to log into Armor Critical 
        password (string): Password to log into Armor Critical 
        path (string): Path to Firefox execution file

        Return: 
        driver (WebDriver object): Selenium webdriver instance to be used by future commands 
        """
        self.username = username
        
        #instantiate selenium webdriver & navigate to Armor Critical login page
        #driver = Firefox()
        self.driver = Firefox()
        self.driver.maximize_window()
        self.driver.get("http://armorcritical.com/account")


        #enter username/password & sign-in
        self.driver.find_element_by_id('semail').send_keys(username)
        self.driver.find_element_by_id('spassword').send_keys(password)
        self.driver.find_element_by_id('signinbutton').click()     
        
    def chat_msg(self, msg, chat_room="refbot"):
        """ 
        Summary:
        Command to send messages in Armor Critical lobby

        Parameters: 
        msg (string): Message to send to a chat room
        chat_room (string):  Chat room to send the message to (Default: lobby)

        Return: 
        None
        """
        #enter chat room
        all_li = self.driver.find_elements_by_tag_name("li")
        for element in all_li:
            if chat_room in element.text:
                element.click()

        #enter & send message
        self.driver.find_element_by_id('chatinput').clear()
        self.driver.find_element_by_id('chatinput').send_keys(msg)
        self.driver.find_element_by_id('chatinput').send_keys(Keys.ENTER)
        time.sleep(1)
                                  
    def read_chat(self, chat_room="refbot"):
        """ 
        Summary:
        Command to read lobby chat 

        Parameters: 
        chat_room (string): Chat room to read.  (Default: refbot) 

        Return: 
        all_text (list): List of all strings in the chat room
        """

        #enter chat room
        all_li = self.driver.find_elements_by_tag_name("li")
        for element in all_li:
            if chat_room in element.text:
                element.click()

        #get text in chat room
        raw_text = self.driver.find_element_by_id('chatframe').text

        #clean up text
        self.chat_text = raw_text.split("\n")[4:]
    
    def manage_launch(self):
        """
        Summary:
        Chatbot will determine which players are interested in playing at a regular interval.

        Parameters:
        None

        Return:
        None
        """
        if self.driver.find_element_by_id('eventstoggle').text == "hide events":
            self.driver.find_element_by_id('eventstoggle').click()
            time.sleep(1)
        self.chat_msg("/clear")
        
        self.is_autoref_requested = False
        self.chat_msg("/topic " + str(datetime.datetime.now() + datetime.timedelta(hours=1)).split(".")[0][:-3] + " EST | RefBot is available. | Type 'refbot help' for an overview of how refbot works.")
        
        
        while self.is_autoref_requested == False:
            time.sleep(5)
            self.read_chat()
            start = datetime.datetime.now()
            self.chat_msg("/clear")

            for line in self.chat_text:
                if len(line.split(" : ")) == 2:
                    username = line.split(" : ")[0].split(" ")[-1]
                    message = line.split(" : ")[1]
                    
                    #code for 'refbot launch'
                    if message[:13] == "refbot launch" and len(message.split(" ")) == 3:
                        if message.split(" ")[2] in self.map_key.keys():
                            self.elected_map = message.split(" ")[2]
                            self.is_autoref_requested = True
                            self.chat_msg("Now hosting " + self.map_key[self.elected_map]["map_name"] + ".")
                            self.chat_msg("Please wait until refbot has entered before attempting to join the game.")
                            self.chat_msg("/topic " + str(datetime.datetime.now() + datetime.timedelta(hours=1)).split(".")[0][:-3] + " EST | RefBot is currently hosting and is unavailable.")
                            
                            
                    #code for 'refbot maps'
                    if message == "refbot maps":
                        map_listing1 = ""
                        map_listing2 = ""
                        
                        for map_name in list(self.map_key.keys())[:int(len(self.map_key.keys())/2)]:
                            map_listing1 += map_name + ", "
                        for map_name in list(self.map_key.keys())[int(len(self.map_key.keys())/2):]:
                            map_listing2 += map_name + ", "
                        map_listing2 = map_listing2[:-1] + "."
                        self.chat_msg("/pm " + username + " Here are your map options:")
                        self.chat_msg("/pm " + username + " " + map_listing1)
                        self.chat_msg("/pm " + username + " " + map_listing2)
                        
                    #code for 'refbot map details'
                    if len(message.split(" ")) == 3 and message.split(" ")[0] == "refbot" and message.split(" ")[2] == "details" and message.split(" ")[1] in self.map_key.keys():
                        map_name = message.split(" ")[1]
                        self.chat_msg("/pm " + username + " Map name - " + self.map_key[map_name]["map_name"])
                        self.chat_msg("/pm " + username + " Does this map have halves? - " + str(self.map_key[map_name]["has_halves"]))
                        self.chat_msg("/pm " + username + " Length of each half (or full game if there are no halves) - " + str(self.map_key[map_name]["time_length"]))
                        self.chat_msg("/pm " + username + " Minumum player amount - " + str(self.map_key[map_name]["map_min"]))
                        self.chat_msg("/pm " + username + " Maximum player amount -  " + str(self.map_key[map_name]["map_max"]))
    
                    #code for 'refbot help'
                    if message == "refbot help":
                        self.chat_msg("/pm " + username + " RefBot is an on demand referee that hosts & uploads CTA matches at your convenience.")
                        self.chat_msg("/pm " + username + " There are three commands associated with RefBot:")
                        self.chat_msg("/pm " + username + " Type 'refbot maps' to get a listing of available maps.")
                        self.chat_msg("/pm " + username + " Type 'refbot [map] details' to get details on a specific map.")
                        self.chat_msg("/pm " + username + " Type 'refbot launch [map]' to host & upload a specific map.")
                        
    def create_game(self, game_type="Public", hub="New York", game_password="abc"):
        """ 
        Summary:
        Command to create a game.

        Parameters:
        game_type (string): Type of CTA game (e.g. Public, Private, Top 8, Bottom 8, etc.) (Default - "Public")
        hub (string): Server location (e.g. New York, Chicago) (Default - "New York")
        game_password (string): Game password (Default - "abc")

        Return: 
        driver (WebDriver object): driver instance to be used in future commands
        game_password (string): Game password (Default - "abc")
        """
        self.hub = hub

        #click on "Create Game" button
        self.driver.find_element_by_id('newGameButton').click()

        #select map
        select = Select(self.driver.find_element_by_id('newgame_map'))
        select.select_by_visible_text(self.map_key[self.elected_map]["map_name"])

        #enter game name
        title = "CTA " + self.map_key[self.elected_map]["map_name"] + " " + game_type + " pw=" + game_password
        self.driver.find_element_by_id('newgame_name').click()
        self.driver.find_element_by_id('newgame_name').clear()
        self.driver.find_element_by_id('newgame_name').send_keys(title)

        #select hub
        ##create select variable for "Map Name" drop down
        select = Select(self.driver.find_element_by_id('newgame_hub'))

        ##select by visible text
        select.select_by_visible_text(self.hub)

        #enter password
        self.driver.find_element_by_id('newgame_password').click()
        self.driver.find_element_by_id('newgame_password').clear()
        self.driver.find_element_by_id('newgame_password').send_keys("titan")

        #click "Create" button
        self.driver.find_element_by_id('newGameCreateButton').click()
    
    def enter_game(self):
        """
        Summary:
        Joins a game that has just been created.

        Parameters:
        self.driver (WebDriver object): Selenium webdriver instance used to interact with browser
        self.game_password (string): game password
        self.hub (string): hub of the game (Default - "New York")
        self.username (string): name of the game creator

        Return:
        self.driver (WebDriver object): Selenium webdriver instance to be used by future commands
        """
        self.chat_msg("/refresh")
        time.sleep(1)

        #find created game in table 
        i = 0
        while i < 5:
            try:
                rows = self.driver.find_elements_by_tag_name("tr")
                my_game_row = 0

                for num, row in enumerate(rows):
                    if self.hub +" " + self.username in row.text:
                        my_game_row = num
                break
            except StaleElementReferenceException: 
                print('StaleElementReferenceException while trying to identify rows, trying to find element again.')
                i += 1
                
        #click on join button for created game
        self.driver.find_elements_by_class_name("gamelink")[my_game_row - 1].click()

        #enter password into alert 
        self.driver.switch_to.alert.send_keys(self.game_password)
        self.driver.switch_to.alert.accept()
        time.sleep(5)

        #navigate prompt/download JNLP file
        firefox = Application().connect(best_match="Opening armorcritical.jnlp")
        firefox.window(title="Opening armorcritical.jnlp", class_name="MozillaDialogClass").type_keys("{TAB}"*2)
        firefox.window(class_name="MozillaDialogClass").type_keys("{ENTER}")
        time.sleep(10)

        #find & open the most recent jnlp in the downloads directory
        jnlp_files = glob.glob(paths['jnlp_dls'])
        latest_file = max(jnlp_files, key=os.path.getctime)
        os.startfile(latest_file)
        time.sleep(5)

        #handle java update dialog
        for app in pywinauto.findwindows.find_elements():
            if "Java Update Needed" in str(app):
                java_update = Application().connect(best_match="Java Update Needed")
                java_update.window(title="Java Update Needed").type_keys("{TAB}"*2)
                java_update.window(title="Java Update Needed").type_keys("{ENTER}")
                
        time.sleep(10)
                
        #confirm connection to game application, navigate prompt, & start game
        i = 0
        while i < 10:
            try:
                java = Application().connect(best_match="Security Warning")
                break
            except:
                print("Element not found... waiting 5 seconds")
                i+=1
                print("Attempt #" + str(i))
                time.sleep(5)
        java.window(title="Security Warning", class_name="SunAwtDialog").type_keys("{TAB}"*2)
        java.window(title="Security Warning", class_name="SunAwtDialog").type_keys("{SPACE}")
        java.window(title="Security Warning", class_name="SunAwtDialog").type_keys("{ENTER}")
    
    def game_msg(self, msg):
        """ 
        Summary:
        Command to send messages in-game 

        Parameters: 
        msg (string):  Message to send in-game 

        Return: 
        None.

        """
        #connect to game application
        game_app = Application(backend="uia").connect(class_name="LWJGL")

        #manually swap " " for {SPACE} for pywinauto
        new_msg = msg.split(" ")
        final_msg = ""
        for word in new_msg:
            final_msg += (word+"{SPACE}")

        #send msg    
        game_app.window(title="Armor Critical").type_keys(final_msg+"{ENTER}")
        time.sleep(1)
    
    #initial commands to perform upon entering server
    def initial_commands(self):
        """
        Summary:
        Initial commands to be performed upon entering the game.
    
        Parameters: 
        line (string): individual line to be read from the replay file
        self.game_state (dict): dictionary of variables reflecting the state of the game
        self.username (string): username of the referee (referee is excluded from "all_players_dict")

        Return: 
        None
        """
        #confirm connection to game application
        i = 0
        while i < 10:
            try:
                Application(backend="uia").connect(class_name="LWJGL")
                break
            except:
                print("Element not found... waiting 5 seconds")
                i += 1
                print("Attempt #" + str(i))
                time.sleep(5)
        
        #change pw to abc so players can enter
        self.game_msg("/pass abc")
        
        #turn sound off
        game_app = Application(backend="uia").connect(class_name="LWJGL")
        game_app.window(title="Armor Critical").type_keys("{F6}")
        
        #turn switching off & specall
        self.game_msg("/switching off")
        self.game_msg("/specall")
        
        #send pm's to players in refbot lobby
        lobby_players = ""
        lobby_list = []
        
        for item in self.driver.find_elements_by_class_name("playerlist"):
            lobby_players += item.text

        for item in lobby_players.split(" "):
            if item != '' and "\n" not in item:
                lobby_list.append(item)

        for player in lobby_list:
            if player != self.username:
                self.game_msg("/pm " + player + " CTA " + self.elected_map + " pw=abc")

    #functions for pre-game matchmaking
    def player_check(self, line):
        """
        Summary:
        Updates "all_players_dict" by adding players that have been created and removing players that have left
    
        Parameters: 
        line (string): individual line to be read from the replay file
        self.game_state (dict): dictionary of variables reflecting the state of the game
        self.username (string): username of the referee (referee is excluded from "all_players_dict")

        Return: 
        None
        """
        if line[:6] == "create":
            created = line.split(" ")
            if self.username != created[1]: #filters out referee from being added to all_players_dict
                self.game_state["all_players_dict"][int(created[2])] = [created[1], int(created[6][:-2])] #player_id : ['name', rating]
                print("Player has been created.", self.game_state["all_players_dict"]) #tracking
        if line[:6] == "remove":
            removed = int(line.split("ö")[0].split(" ")[1]) #line[:-14].split(" ")
            self.game_state["all_players_dict"].pop(removed, None)#(int(removed[1]), None)
            print("Player has been removed.", self.game_state["all_players_dict"]) #tracking

    def matchmaking_update(self):
        """
        Summary:
        Gives status update on whether enough players have joined
    
        Parameters: 
        self.game_state["matchmaking_checks"] (int):  Count of how many times matchmaking has been checked
        self.game_state["rdy_to_start"] (bool): Is there enough players to start the game? (Default - False)
        self.game_state["teams_confirmed"] (bool): Have teams been confirmed after the /teams command? (Default - False)
        self.game_state["is_shutdown"] (bool): Is the game shutdown? (Default - False)

        Return: 
        None
        """   
        self.game_state["rdy_to_start"] = False
        self.game_state["teams_confirmed"] = False
        self.game_state["is_shutdown"] = False

        wait_time = 180
        player_count = len(self.game_state["all_players_dict"])

        if (self.game_state["matchmaking_checks"] <= 12):
            if player_count >= self.map_max:
                return
            elif self.map_min <= player_count < self.map_max:
                time.sleep(15)
                minute, sec = divmod(int(datetime.timedelta(seconds=45-(15*self.game_state["matchmaking_checks"])).total_seconds()), 60)
                self.game_msg("Allowing additional players to join...")
                self.game_msg("Game will begin in approximately " + "%d:%02d" % (minute, sec) + ".")
                self.game_state["matchmaking_checks"] += 1
            else:
                time.sleep(15)
                minute, sec = divmod(int(datetime.timedelta(seconds=wait_time-(15*self.game_state["matchmaking_checks"])).total_seconds()), 60)
                self.game_msg("Allowing additional players to join...")
                self.game_msg("Will shutdown in approximately " + "%d:%02d" % (minute, sec) + ".")
                self.game_state["matchmaking_checks"] +=1

        if self.game_state["matchmaking_checks"] == 13:
            self.game_msg("Player threshold not met... shutting down.")
            self.game_state["rdy_to_start"] = True #set self.game_state["rdy_to_start"] to True to exit first while loop
            self.game_state["teams_confirmed"] = True #set self.game_state["teams_confirmed"] to True to exit second while loop
            self.game_state["is_shutdown"] = True #set shutdown to True to exit last while loop

    def rdy_to_start_check(self):
        """
        Summary:
        Checks "all_players_dict" to see how many players are in the server.  Assumed every player in the server wants to play.
        Also does not allow 3v3 or 4v4 to start until a minimum amount of self.game_state["matchmaking_checks"] has been conducted.
    
        Parameters: 
        self.game_state["matchmaking_checks"] (int): Number of times the matchmaking_update function has ran
        self.game_state["rdy_to_start"] (bool): Is there enough players to start the game? 

        Return: 
        None
        """
           
        self.below_min = False
        self.sit_outs = {}
        self.participants = {}
        player_count = len(self.game_state["all_players_dict"])

        if player_count >= self.map_max:
            self.sit_outs = dict(list(self.game_state["all_players_dict"].items())[self.map_max:]) 
            self.participants = dict(list(self.game_state["all_players_dict"].items())[:self.map_max])
            self.game_state["rdy_to_start"] = True
            self.game_msg("Match now starting...")
        elif (self.map_min <= player_count < self.map_max) and (self.game_state["matchmaking_checks"] > 3):
            if player_count % 2 == 1:
                self.sit_outs = dict(list(self.game_state["all_players_dict"].items())[player_count-1:])
                self.participants = dict(list(self.game_state["all_players_dict"].items())[:player_count-1])
            else:
                self.participants = dict(list(self.game_state["all_players_dict"].items()))
            self.game_state["rdy_to_start"] = True
            self.game_msg("Match now starting...")
        else:
            self.below_min = True

    def make_teams(self):
        """
        Summary:
        Use in-game /teams command to create teams
    
        Parameters: 
        self.sit_outs (dictionary): Players that will sit out the game
        self.username (string): Name of the referee (needs to be excluded from participating)
        
        Return: 
        None.
        """
        sit_out_str = self.username + " "
        for name in self.sit_outs.values():
            sit_out_str += (name[0]+" ")
        self.game_msg("/specall")
        self.game_msg("/teams "+sit_out_str)
        print("/teams "+sit_out_str) #testing

    def explainer(self):
        """
        Summary:
        Explains the mechanics of how autoref will work to the players
    
        Parameters: 
        None

        Return: 
        None
        """
        self.game_msg("/mute all")
        self.game_msg("/pause")
        self.game_msg("Before we start, here's several things to note with refbot.")
        time.sleep(3)
        self.game_msg("1 - Please do not leave the game or move to spec at any point before the game is shutdown.")
        self.game_msg("Either of these actions will result in a 1 game suspension.")
        time.sleep(5)
        self.game_msg("2 - If you need a pause, simply enter 'pause' and it will be granted.")
        self.game_msg("During pauses, all players must reply with 'here' within the allotted time.")
        self.game_msg("Failing to respond in time will be treated as a left early.")
        time.sleep(5)
        self.game_msg("3 - Flag-in-play is turned off.  One extra minute is given to account for this change.")
        time.sleep(5)
        if self.game_state["has_halves"] == False:
            self.game_msg("4 - This map will be played continuously with no half time.")
        self.game_msg("Happy hunting...")
        self.game_msg("/unmute all")
            
    def teams_check(self):
        """
        Summary:
        After make_teams(), checks to make sure teams are equal in number (leaving/joining players can create uneven teams)
    
        Parameters: 
        self.game_state["teams_confirmed"] (bool): Have teams been confirmed to be equal in number
        self.game_state["rdy_to_start"] (bool): Is there enough players to start the game? 
        self.sit_outs (dictionary): Players that will sit out the game
        self.participants (dictionary):  Player that will participate in the game

        Return: 
        team1 (list): List of players on team 1
        team2 (list) : List of players on team 2
        """
        fo = open(self.latest_file)
        data = fo.readlines()
        fo.close()

        segment = 30 #collecting 30 lines after /teams command for team information
        index = 0
        team1 = []
        team2 = []

        for num, line in list(enumerate(data)): #determine line index of latest /teams command
            if "message Teams have been set by the rating system" in line:
                index = num
                
        team_lines = data[index:index+segment]

        for line in team_lines:
            #red team (for joy)
            if "holdpen" in line and "1960" in line:
                team1.append(int(line.split(" ")[1]))
            #green team (for joy)
            if "holdpen" in line and "2984" in line:
                team2.append(int(line.split(" ")[1]))
        
        if len(team1) == len(team2):
            self.game_state["teams_confirmed"] = True
            self.explainer()
            if self.game_state["has_halves"] == False:
                self.game_msg("/start " + str(self.game_state["time_length"]) + " 99")
            else:
                self.game_msg("/start " + str(self.game_state["time_length"]))
        else:
            self.game_msg("Teams are uneven.  Setting teams again in approximately 30 seconds...")
            self.game_msg("/specall")
            time.sleep(30)
            for line in team_lines: #check team_lines for players leaving/joining to run /teams again
                self.player_check(line)
            self.rdy_to_start_check()
            if self.below_min == True: #shut game down if player left and we're below six (5+ mins in-game have passed at this point)
                self.game_state["teams_confirmed"] = True
                self.game_state["is_shutdown"] = True
                self.game_msg("There are less than 6 players... now shutting down.")
                time.sleep(2)
                
        return team1, team2

    #functions for the actual game
    def pause_check(self, line):
        """
        Summary:
        Checks replay file to see if a participating player has requested a pause.
    
        Parameters: 
        line (string): Line of replay file to check
        self.participants (dictionary):  Players that will participate in the game

        Return: 
        player_responses (dictionary): dictionary to store player responses (used in unpause_check, initialized here)
        pause_update_checks (int): count of how many times pause_update() has ran (used in pause_update, initialized here)
        """
        pause_update_checks= 0
        player_responses = {}
        
        for player_id in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys())):
            player_responses[player_id] = False
        
        words = line.split(" ")
    
        #player requested pause
        if (words[0] == "broadcast") and (int(words[1]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))) and (words[2][:5] == "pause"):
            self.game_msg("/pause")
            self.game_msg(self.participants[int(words[1])][0]+" has asked for a pause.")
            self.game_state["is_paused"] = True
            player_id = int(words[1])
        #player left game pause
        elif (words[0] == "remove") and (int(words[1].split("ö")[0]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))):
            self.game_msg(self.participants[int(words[1].split("ö")[0])][0]+" has left the game and generated a pause.")
            self.game_state["is_paused"] = True
            player_id = int(words[1].split("ö")[0])
            self.game_state["left_early"][player_id] = self.participants[player_id]
        #player to spec pause
        elif (words[0] == "team") and (int(words[1]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))) and (words[2][:2] == "-1"):
            self.game_msg(self.participants[int(words[1])][0]+" has gone to spec and generated a pause.")
            self.game_state["is_paused"] = True
            player_id = int(words[1])
            self.game_state["left_early"][player_id] = self.participants[player_id]
        else:
            self.game_state["is_paused"] = False
            player_id = None
            
        if self.game_state["is_paused"] == True:
            self.game_msg("Players, respond with 'here' to continue play.")
            self.game_state["has_paused"] = True
        
        return player_responses, pause_update_checks

    def unpause_check(self, line, player_responses):
        """
        Summary:
        Checks replay file to see if players are present after pause.  
    
        Parameters: 
        line (string): Line of replay file to check

        Return: 
        player_responses (dictionary): dictionary to store player responses
        """
        words = line.split(" ")
        
        #account for players that may leave or go to spectator (they get left early's)
        ##paused caused by player leaving
        if (words[0] == "remove") and (int(words[1].split("ö")[0]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))):
            self.game_state["left_early"][int(words[1].split("ö")[0])] = self.participants[int(words[1].split("ö")[0])]
            
        ##pause caused by player going to spectator
        if (words[0] == "team") and (int(words[1]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))) and (words[2][:2] == "-1"):
            self.game_state["left_early"][int(words[1])] = self.participants[int(words[1])]
        
        #account for players that are present (and haven't left early) by having them say "here"
        if (words[0] == "broadcast") and (int(words[1]) in set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))) and (words[2][:4] == "here"):
            player_responses[int(words[1])] = True
            print("unpause_check() - player_responses:", player_responses) #tracking
            
        if sum(player_responses.values()) == len(set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))):
            self.game_state["is_paused"] = False
        
        return player_responses

    def pause_update(self, pause_update_checks, player_responses, team1, team2):
        """
        Summary:
        Update players on status of pause.  If all players are present, game will resume.  If players have not returned in 
        2 minutes, the non-present player(s) will be removed and others will be removed as necessary to make teams even in
        number and as close as possible in rating.
    
        Parameters: 
        line (string): Line of replay file to check
        player_id (int):  player_id of the player that requested a pause

        Return: 
        pause_update_checks (int) :
        """
        #all players accounted for but 1 or more have left --> go straight to forced sit outs logic
        if (self.game_state["is_paused"] == False) and (len(self.game_state["left_early"]) > 0):
            pause_update_checks = 7
        
        if (self.game_state["is_paused"] == False) and (len(self.game_state["left_early"]) == 0):
            self.game_msg("All players are accounted for... resuming game.")
            time.sleep(2)
            self.game_msg("/pause")
            print("pause_update() - self.game_state[is_paused]: ", self.game_state["is_paused"]) #tracking
        else:
            wait_time = 90
            time.sleep(15)
            
            if pause_update_checks <= 6:
                self.game_msg("The following players have responded: ")
                for k, v in player_responses.items():
                    if v == True:
                        self.game_msg(self.participants[k][0])
                minute, sec = divmod(int(datetime.timedelta(seconds=wait_time-(15*pause_update_checks)).total_seconds()), 60)
                self.game_msg("Play will resume when all players respond or in approximately " + "%d:%02d" % (minute, sec) + ".")
                self.game_msg("Missing players will spectate along with opposing players to rebalance teams.")
                pause_update_checks += 1
                print("pause_update() - pause_update_checks: ", pause_update_checks) #tracking
                print("pause_update() - player_responses: ", player_responses) #tracking
                
            #logic for forced sit outs
            if pause_update_checks == 7:
                self.game_state["is_paused"] = False
                
                #logic to move people to spec to continue game
                self.game_state["responded_team1"] = []
                self.game_state["responded_team2"] = []
                responded_team1_rating = 0
                responded_team2_rating = 0
                
                #only say this if players who should've responded, haven't responded
                if sum(player_responses.values()) != len(set(self.participants.keys()).difference(set(self.game_state["left_early"].keys())).difference(set(self.game_state["forced_to_sit"].keys()))):
                    self.game_msg("Time limit for pause has been reached.  Updating teams and resuming game...")
                    time.sleep(2)
                
                for player_id in player_responses.keys():
                    if self.game_state["is_half"] == False:
                        
                        #Add players that have responded to respective teams (grabbing 'name' & rating)
                        if (player_responses[player_id] == True) and (player_id in team1):
                            self.game_state["responded_team1"].append(self.participants[player_id])
                        if (player_responses[player_id] == True) and (player_id in team2):
                            self.game_state["responded_team2"].append(self.participants[player_id])

                        #Spectate each missing player & place in self.game_state["left_early"] list
                        if player_responses[player_id] == False:
                            self.game_msg("/move " + self.participants[player_id][0] + " spec")
                            self.game_state["left_early"][player_id] = self.participants[player_id]
                            #remove from self.participants
                        
                #See if there are at least 2 players remaining on each team
                if (len(self.game_state["responded_team1"]) >= 2) and (len(self.game_state["responded_team2"]) >=2):
                    #Continue game if size of teams is equal
                    if len(self.game_state["responded_team1"]) == len(self.game_state["responded_team2"]):
                        self.game_msg("Game will resume and only the remaining players will be included in the upload.")
                        self.game_msg("Missing players will serve a suspension for future games.")
                        self.game_msg("/pause")
                        self.game_state["is_paused"] = False
                        self.game_state["is_shutdown"] = False
                    else:
                        #Get team ratings for remaining players on each team
                        for player in self.game_state["responded_team1"]:
                            responded_team1_rating += player[1]
                        for player in self.game_state["responded_team2"]:
                            responded_team2_rating += player[1]

                        #Calculate player & rating gaps between teams
                        player_gap = len(self.game_state["responded_team1"]) - len(self.game_state["responded_team2"])
                        rating_gap = responded_team1_rating - responded_team2_rating
                        
                        print("pause_update() - self.game_state[responded_team1]:", self.game_state["responded_team1"]) #tracking
                        print("pause_update() - self.game_state[responded_team2]:", self.game_state["responded_team2"]) #tracking
                        print("pause_update() - responded_team1_rating:", responded_team1_rating) #tracking
                        print("pause_update() - responded_team2_rating:", responded_team2_rating) #tracking
                        print("pause_update() - player_gap:", player_gap) #tracking
                        print("pause_update() - rating_gap:", rating_gap) #tracking
                        
                        #iterate through all player combinations to find combo that minimizes rating_gap
                        #player_gap being positive/negative dictates if rating_gap is subtracted or added from/to combined_rating
                        #use player_gap because teams can have less players but higher rating depending on who left game

                        if player_gap > 0:
                            all_combos = {}
                            min_gap = 100000

                            for combo in enumerate(list(combinations(team1, abs(player_gap)))):
                                names = []
                                combined_rating = 0
                                print("pause_update() - This is a combo (num, player_id(s)): ", combo)
                                for player_id in combo[1]:
                                    names.append(self.participants[player_id][0])
                                    combined_rating += self.participants[player_id][1]
                                    print("names:", names) #tracking
                                    print("combined_rating:", combined_rating) #tracking

                                all_combos[combo[0]] = [names, (rating_gap - combined_rating)]
                                if abs(combined_rating - rating_gap) < min_gap:
                                    min_gap = abs(combined_rating - rating_gap)
                                    min_combo = names

                            print("This is the min_combo:", min_combo) #testing
                            print("This is the min_gap:", min_gap) #testing

                        else:
                            all_combos = {}
                            min_gap = 100000

                            for combo in enumerate(list(combinations(team2, abs(player_gap)))):
                                names = []
                                combined_rating = 0
                                print("pause_update() - These are the player_ids for this combination:", combo)
                                for player_id in combo[1]:
                                    names.append(self.participants[player_id][0])
                                    combined_rating += self.participants[player_id][1]
                                    print("names:", names) #tracking
                                    print("combined_rating:", combined_rating) #tracking
                                    
                                all_combos[combo[0]] = [names, (combined_rating+rating_gap)]
                                if abs(combined_rating + rating_gap) < min_gap:
                                    min_gap = abs(combined_rating + rating_gap)
                                    min_combo = names

                            print("This is the min_combo after if/else:", min_combo) #testing
                            print("This is the min_gap after if/else:", min_gap) #testing
                            
                        print("This is min_combo right before /spectate:", min_combo)
                        for name in min_combo:
                            self.game_msg("/move " + name + " spec")
                            for k, v in self.participants.items():
                                if name in v:
                                    self.game_state["forced_to_sit"][k] = v
                        self.game_msg("Game now resuming... appropriate players will spectate for equal team size")
                        self.game_msg("and minimal gap in ratings...")
                        time.sleep(3)
                        self.game_msg("/pause")
                        self.game_state["is_paused"] = False
                        self.game_state["is_shutdown"] = False
                        #need to adjust self.game_state["holdpen_count"] based on remaining players; holdpen_limit adjusted in half_time_checks()
                        self.game_state["holdpen_count"] = 2*(len(self.game_state["responded_team1"]) + len(self.game_state["responded_team2"])) 
                        print("all_combos:", all_combos) #tracking
                else:
                    #my stance is to not upload this game - simply suspend players that left
                    self.game_msg("1 or more teams has less than 2 players.  Shutting game down.")
                    time.sleep(3)
                    self.game_state["is_paused"] = False
                    self.game_state["is_shutdown"] = True
                    
        return pause_update_checks

    def half_time_check(self, line): 
        """
        Summary:
        Checks replay file to see if half time has been reached.  If yes, will start the next half.
    
        Parameters: 
        self.game_state["is_half"] (bool): Has half time been reached?

        Return: 
        None
        """
        if line[:5] == "timer" and int(line.split(" ")[1]) <= 2000:
            self.game_state["has_started"] = True
            print("half_time_check() - self.game_state['has_started']:", self.game_state['has_started'])
            print("half_time_check() - self.game_state['has_started']:", line)
    
        if self.game_state["has_started"] == True:
            if self.game_state["has_halves"] == True:
                if self.game_state["is_half"] == False:
                    if line[:5] == "timer" and int(line.split(" ")[1]) > ((((self.game_state["time_length"]*60))*1000) - 3000):
                        time.sleep(5)
                        print("half_time_check() - self.game_state['time_length']", self.game_state["time_length"])
                        self.game_msg("/half " + str(self.game_state["time_length"]) + " 99")
                        self.game_state["is_half"] = True

    def overtime_check(self, line):
        """
        Summary:
        Checks replay file to see if half time has been reached.  If yes, will start the next half.
    
        Parameters: 
        self.game_state["is_overtime"] (bool): is the game in overtime?

        Return: 
        None
        """
        
        if line[:32] == "message *** Overtime Started ***":
            self.game_state["is_overtime"] = True

    def shutdown_check(self, line):
        """
        Summary:
        Checks replay file to see if half time has been reached.  If yes, will start the next half.
    
        Parameters: 
        self.game_state["is_half"] (bool): Has half time been reached?

        Return: 
        None
        """
        
        if line[:25] == "message *** Game Over ***":
            print("'Game Over' found, shutting the game down.") #tracking
            self.game_state["is_shutdown"] = True
            self.game_state["is_uploadable"] = True
            self.game_msg("Thanks for playing, please remain as the server is being shut down.")

    def prevent_ref_boot(self):
        """ 
        Summary:
        Keeps referee from an AFK boot due to inactivity during the game. 
    
        Parameters: 
        None 
    
        Return: 
        None
        """
        #connect to game application
        game_app = Application(backend="uia").connect(class_name="LWJGL")

        #send msg    
        game_app.window(title="Armor Critical").type_keys("{DOWN}")
        game_app.window(title="Armor Critical").type_keys("{UP}")
        game_app.window(title="Armor Critical").type_keys("{LEFT}")
        game_app.window(title="Armor Critical").type_keys("{RIGHT}")

    def run_game(self):
        """ 
        Summary:
        Performs all necessary functions to referee the actual game. 

        Parameters: 
        self.username (string): username of the referee
        self.game_state["has_halves"] (bool): is there half-time or not?
        self.game_state["time_length"] (int): length of half if there are halves

        Return: 
        None
        """
        #initialize variables
        self.map_min = self.map_key[self.elected_map]["map_min"]
        self.map_max = self.map_key[self.elected_map]["map_max"]
        
        self.game_state = {"all_players_dict" : {}, #dictionary to contain all players in the server
                           "rdy_to_start" : False, #bool --> is the game ready to start?
                           "teams_confirmed" : False, #bool --> have teams been confirmed after initial /teams command?
                           "is_paused" : False, #bool --> is the game paused?
                           "has_paused" : False, #bool --> has the game been paused?
                           "is_half" : False, #bool --> has the game boots are bad. 
                           "has_halves" : self.map_key[self.elected_map]["has_halves"],
                           "time_length" : self.map_key[self.elected_map]["time_length"],
                           "has_started" : False,
                           "is_overtime" : False, #bool --> is the game in overtime?
                           "is_shutdown" : False, #bool --> has the game has been shutdown?
                           "is_uploadable" : False, #bool --> should the game be uploaded?
                           "i" : 0,
                           "matchmaking_checks" : 0,
                           "locked_count" : 0,
                           "holdpen_count" : 0,
                           "responded_team1" : [],
                           "responded_team2" : [],
                           "left_early" : {},
                           "forced_to_sit" : {}}
        
        #Finds the most recent file in the replays directory
        time.sleep(7)
        replay_files = glob.glob(paths["replays_dir"]+"/*.rec")
        self.latest_file = max(replay_files, key=os.path.getctime)

        #Initial commands to run upon entering the game (turn switching off & specall)
        self.initial_commands()

        # Core code of manage_game
        # Every 3 seconds reads the latest entries after the previous read, checking for trigger words -- allows game management
        ## file read until the game shuts down.
        ## while the file is being read, each line will be checked for changes in game state
        ## when the game state changes, an action is triggered

        while self.game_state["rdy_to_start"] == False:
            time.sleep(3)
            fo = open(self.latest_file)
            data = fo.readlines()
            fo.close()

            #Checks that need to be conducted regularly
            for line in data[0+self.game_state["i"]:]:
                self.player_check(line)

            self.matchmaking_update()
            self.rdy_to_start_check()

            self.game_state["i"] = len(data)

        while self.game_state["teams_confirmed"] == False:
            self.make_teams()
            time.sleep(3)
            team1, team2 = self.teams_check()

        while self.game_state["is_shutdown"] == False:
            time.sleep(3) #3 second pause between file reads & game state checks
            fo = open(self.latest_file)
            data = fo.readlines()
            fo.close()

            #Checks that need to be conducted regularly
            for line in data[0+self.game_state["i"]:]:
                player_responses, pause_update_checks = self.pause_check(line)
                if self.game_state["is_paused"] == True:
                    break

                self.half_time_check(line)

                if self.game_state["is_overtime"] == False:
                    self.overtime_check(line)

                self.shutdown_check(line)
                if self.game_state["is_shutdown"] == True:
                    break

            while self.game_state["is_paused"] == True:
                time.sleep(3) #3 second pause between file reads & game state checks
                fo = open(self.latest_file)
                data = fo.readlines()
                fo.close()

                #Checks that need to be conducted regularly
                for line in data[0+self.game_state["i"]:]:
                    player_responses = self.unpause_check(line, player_responses)

                pause_update_checks = self.pause_update(pause_update_checks, player_responses, team1, team2)

                self.game_state["i"] = len(data) 

            self.game_state["i"] = len(data)
            self.prevent_ref_boot()

        self.game_msg("/shutdown")

    def upload_game(self, cta_logins):
        """
        Summary:
        Logic to upload a game to the CTA backend & post link in the lobby.

        Parameters:
        self.driver (WebDriver object): Selenium webdriver instance to control browser
        self.latest_file (string): path to replay file for the game to be uploaded
        self.participants (dict): dictionary containing players set to play during game
        self.game_state["left_early"] (dict): players who left early and as a result will not be included in stats
        self.game_state["forced_to_sit"] (dict): players forced to sit to balance teams after another player left
        self.game_state["is_overtime"] (bool): is the game in overtime?

        Return:
        None
        """
        #open tab to cta backend from self.driver
        self.driver.execute_script("window.open('');")
        time.sleep(3)

        #switch to the tab
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("http://cta.critical-hq.net/backend/login.php")
        time.sleep(3)

        #enter username/password & sign-in
        self.driver.find_element_by_name('username').send_keys(cta_logins[0][0])
        self.driver.find_element_by_name('password').send_keys(cta_logins[0][1])
        self.driver.find_element_by_name('Login').click()

        #upload game
        self.driver.find_element_by_link_text("Upload Stats").click()
        self.driver.find_element_by_name("file").send_keys(self.latest_file)
        self.driver.find_element_by_name("gameType").click()
        self.driver.find_element_by_name("upload").click()

        #review game
        #select referee
        WebDriverWait(self.driver, 120, 1).until(lambda x: x.find_element_by_name("mainRef"))
        Select(self.driver.find_element_by_name("mainRef")).select_by_value(cta_logins[0][0])

        #click overtime if there was an overtime
        if self.game_state["is_overtime"] == True:
            self.driver.find_element_by_name("overtime").click()

        #submit - click "Add Game Info"
        self.driver.find_element_by_name("Submit").click()

        #delete players in self.game_state["left_early"] & self.game_state["forced_to_sit"]
        if len(self.game_state["left_early"]) > 0:
            i = 0
            while i < 5:
                for player in self.game_state["left_early"].values():
                    rows = self.driver.find_elements_by_tag_name("tr")
                    try:
                        for row in rows:
                            if player[0].lower() in row.text.lower():
                                row.find_elements_by_tag_name("img")[0].click()
                                time.sleep(3)
                                self.driver.find_elements_by_tag_name("a")[0].click()
                                time.sleep(3)
                                self.driver.refresh()
                        break
                    except StaleElementReferenceException: 
                        print('StaleElementReferenceException while trying to identify rows, trying to find element again.')
                        i += 1

        if len(self.game_state["forced_to_sit"]) > 0:
            i = 0
            while i < 5:
                for player in self.game_state["forced_to_sit"].values():
                    rows = self.driver.find_elements_by_tag_name("tr")
                    try:
                        for row in rows:
                            if player[0].lower() in row.text.lower():
                                row.find_elements_by_tag_name("img")[0].click()
                                time.sleep(3)
                                self.driver.find_elements_by_tag_name("a")[0].click()
                                time.sleep(3)
                                self.driver.refresh()
                        break
                    except StaleElementReferenceException: 
                        print('StaleElementReferenceException while trying to identify rows, trying to find element again.')
                        i += 1

        #assign wins/losses based on RW & RL
        rows = self.driver.find_elements_by_tag_name("tr")
        num_players = len(self.participants) - len(self.game_state["forced_to_sit"]) - len(self.game_state["left_early"])
        drop_downs = self.driver.find_elements_by_id("tiny")
        i=1

        for row in rows[1:num_players+1]:
            round_win = row.text.split(" ")[-3]
            round_loss = row.text.split(" ")[-2]
            if round_win > round_loss:
                Select(drop_downs[i]).select_by_value("1")
                i+=2
            else:
                Select(drop_downs[i]).select_by_value("0")
                i+=2

        #submit changes
        self.driver.find_element_by_name("statsSubmit").click()

        #go to 'Review Games'
        self.driver.find_element_by_link_text("Review Games").click()

        #change status to approved
        Select(self.driver.find_element_by_class_name("styled")).select_by_value("1")

        #submit game
        self.driver.find_element_by_name("reviewGamesSubmit").click()

        #store link to send to lobby
        link = self.driver.find_elements_by_tag_name("a")[8].get_attribute('href')

        #close the active tab
        self.driver.close()
        time.sleep(3)

        #switch back to the first tab
        self.driver.switch_to.window(self.driver.window_handles[0])

        return link

if __name__ == "__main__":
    #open armor critical
    autoref = AutoRef()
    autoref.open_ac(ac_logins["A"][0], ac_logins["A"][1])
    time.sleep(5)

    #manage launch
    autoref.manage_launch()
    
    #create game
    autoref.create_game()
    time.sleep(5)
    
    #refresh game list & enter the game
    autoref.enter_game()
    
    #run the game
    autoref.run_game()

    #upload game if self.game_state["is_uploadable"] is true
    if autoref.game_state["is_uploadable"] == True:
        link = autoref.upload_game(cta_logins)
        autoref.chat_msg(link)
    else:
        autoref.chat_msg("Game was not completed and will not be uploaded.")
