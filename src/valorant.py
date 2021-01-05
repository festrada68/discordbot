import requests
import cchardet
from bs4 import BeautifulSoup

class Player():
    def __init__(self,player):
        self.usrname = player # player name with id, ex: player#7024
        self.player_stats = None
        self.agents = None
        self.weapons = None

        self.__url = self.get_url(self.usrname)
        self.__res = None
        self.request(self.__url)

        self.__soup = self.parse(self.__res)
        self.tags(self.__soup)

    def get_url(self,player):
        index = player.find('#')
        player_name = player[0:index]
        if(player_name.find(' ') == True):
            space_index = player_name.find(' ')
            player_name = player[0:space_index] + '%20' + player[space_index+1:index]
        player_id = '%23'+player[index+1:]
        url = f'https://tracker.gg/valorant/profile/riot/{player_name}{player_id}/overview?playlist=competitive'
        return url

    def request(self,url):
        session = requests.Session()
        res = session.get(url = url, data={'body':'div'})
        self.__res = res
        res.close()

    def parse(self,res):
        soup = BeautifulSoup(res.text,'lxml') 
        return soup

    def tags(self,soup):
        agent_tag1 = soup('div',attrs = {'class':'agent'}) # this is for agent names/imgs
        if(not agent_tag1):
            raise ValueError("Player does not exist.")
        else:
            agent_tag2 = soup('div',attrs = {'class':'text'}) # this is for agent stats, time played, etc..
            self.agents = Agent(agent_tag1,agent_tag2) # uses composition 

            weapon_tag = soup('div',attrs = {'class':'weapon'})
            self.weapons = Weapon(weapon_tag) # uses composition
            player_stat_tag0 = soup.find('img',attrs = {'class':'valorant-rank-icon'}).get('src')
            player_stat_tag1 = soup.find_all('span',attrs = {'class':'valorant-highlighted-stat__value'})
            player_stat_tag2 = soup.find_all('div',attrs={'class':"numbers"})
            player_stat_tag3 = soup.find_all('span',attrs={'class':"value"})[3:] # this gets all numbers in comp ov, and weapon kill numbers
            self.player_stats = Player_Stats(player_stat_tag0,player_stat_tag1,player_stat_tag2)

    def __str__(self):
        return f"This is {self.usrname}"


class Attributes():
    def __init__(self):
        self.names = []
        self.imgs = []

class Player_Stats():
    def __init__(self,stat_tag0,stat_tag1,stat_tag2):
        self.rank_img = stat_tag0
        self.rank = stat_tag1[0].text
        self.KAD = stat_tag1[1].text
    
        self.dmgprnd = stat_tag2[0].text
        self.KD = stat_tag2[1].text
        self.hshot = stat_tag2[2].text
        self.win = stat_tag2[3].text
        self.totalwins = stat_tag2[4].text
        self.totalkills = stat_tag2[5].text
        self.totalhshots = stat_tag2[6].text
        self.deaths = stat_tag2[7].text
        self.assists = stat_tag2[8].text
        self.scoreprnd = stat_tag2[9].text
        self.killprnd = stat_tag2[10].text
        self.firstbld = stat_tag2[11].text
        self.ACE = stat_tag2[12].text
        self.clutches = stat_tag2[13].text
        self.flawless = stat_tag2[14].text
        self.mostkills = stat_tag2[15].text


class Agent(Attributes):
    def __init__(self,agent_tag1,agent_tag2):
        super().__init__()
        self.__agent_tag1 = agent_tag1
        self.__agent_tag2 = agent_tag2
        self.agent_stats = []
        self.get_len()
        self.get_names()
        self.get_imgs()
        self.get_stats(self.__agent_tag2)
    def get_len(self):
        return len(self.__agent_tag1)

    def get_imgs(self):
        for i in self.__agent_tag1:
            self.imgs.append(i.find('img',attrs={'class':'agent__icon'}).get('src'))

    def get_names(self):
        for i in self.__agent_tag1:
            self.names.append(i.find('span',attrs={'class':'agent__name'}).text)
    def print_names(self):
        for x in range(self.get_len()):
            print(f'{self.names[x]} =  {self.imgs[x]}')

    def get_stats(self,tag):
        for agent in range(self.get_len()):
            stat = []
            for i in range(4):
                if(agent != 0):
                    stat.append(tag[(agent*4)+i].text)
                else:
                    stat.append(tag[i].text)
            self.agent_stats.append(stat) # this function gets the agent time played(0), win%(1),K/D(2),dmg/rnd(3)
                                          # puts it into a 2d list, with the # of rows = # of agents, and cols with stat above
class Weapon(Attributes):
    def __init__(self,weapon_tag):
        super().__init__()
        self.__weapon_tag = weapon_tag
        self.Kills =[]
        self.stats = []
        self.get_names()
        self.get_kills()
        self.get_stats(self.__weapon_tag)
        self.get_imgs(self.__weapon_tag)
    def get_len(self):
        return len(self.__weapon_tag)

    def get_names(self):
        for i in self.__weapon_tag:
            self.names.append(i.find('div',attrs={'class':'weapon__name'}).text)
    def get_kills(self):
        for i in self.__weapon_tag:
            self.Kills.append(i.find('span',attrs={'class':'value'}).text)
    def get_stats(self,weapon_tag):
        for weapon in weapon_tag:
            data = []
            n = weapon.find('div',attrs ={'class':'weapon__accuracy-hits'}).text.split()
            for x in n:
                data.append(x)
            self.stats.append(data)
    def get_imgs(self,tag):
        for i in tag:
            self.imgs.append(i.find('img',attrs={'class':'weapon__silhouette'}).get('src'))

    def print_data(self):
        for x in range(self.get_len()):
            print(f'{self.names[x]} =  {self.Kills[x]}')
