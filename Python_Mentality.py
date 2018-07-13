#Kim, Matthew
#6/30/18
#NBA Hackathon Basketball Analysis

import csv

##Write category names
with open('Python_Mentality_Q1_BBALL.csv',"ab") as output:
        writer = csv.writer(output)
        writer.writerow(['Game_ID','Plaer_ID','Player_Plus/Minus'])


def getPlayers():
    with open('lineup.csv') as f:
        readcode = csv.reader(f)
        players = [r for r in readcode]
        players.pop(0)
    return players

#print getPlayers()

def getEvents():
    with open('playbyplay.csv') as p:
        readcode = csv.reader(p)
        events = [r for r in readcode]
        events.pop(0)
        #get rid of header
    return events

class Court:
##  takes in set of players, stores it to see if active
    def __init__(self,players,game,period,team1,team2):
        self.game=game
        self.period=period
        self.players = players
        self.team1 = team1
        self.team2 = team2
    def __iter(self):
        return iter([self.players,self.game,self.period,self.team1,self.team2])
    def substitute(self,player1,player2):
        if player1 in court.players:
            self.players.remove(player1)
            self.players.add(player2)
            return Court(self.players,self.game,self.period,self.team1,self.team2)
        else:
            court.players.add(player1)
            return Court(self.players,self.game,self.period,self.team1,self.team2)
        
def new_period(court,num):
    court.players.clear()
    court.period = num
    return court
        
class Player:
    def __init__(self, player_id, team_id, plusminus):
        self.player_id= player_id
        self.team_id= team_id
        self.plusminus=plusminus
    def __iter__(self):
        return iter([self.player_id,self.team_id,self.plusminus])
def add(Player,num):
    Player.plusminus = Player.plusminus + num
    
def subtract(Player,num):
    Player.plusminus = Player.plusminus - num

def findteams(players,num1,num2):
    for x in range(num1,num2):
        team1 = players[0][3]
        if players[x][3] != team1:
            team2 = players[x][3]
    return (team1,team2)

def createPlayers(sampleset,players,num1,num2,startpm):
    for x in range(num1,num2):
        courtplayer = Player(players[x][2],players[x][3],startpm)
        sampleset.add(courtplayer)
    return sampleset

def createSet(sampleset,players,num1,num2):
    for x in range(num1,num2):
        sampleset.add(players[x][2])
    return sampleset

def getOnCourt(sampleset):
    oncourt = set()
    for player in sampleset:
        oncourt.add(player.player_id)
    return oncourt

def freethrow(events,eventnum,players):
##copies the players on the court during the foul event, then does plusminus
    numfouls = int(events[eventnum][9])
    foul = 0
    for x in range(1,10):
        if foul == numfouls:
            break
        if int(events[eventnum + x][2]) == 3:
            if int(events[eventnum +x][7]) == 1:
                for player in players:
                    if player.team_id == events[eventnum+x][10]:
                        add(player,1)
                    else:
                        subtract(player,1)
            foul = foul+1

def score(events,eventnum,players):
##adds plusminusf ro teams
    for playeroncourt in players:
        if playeroncourt.team_id == events[eventnum][10]:
            add(playeroncourt,int(events[eventnum][7]))
        else:
            subtract(playeroncourt,int(events[eventnum][7]))
            
def substitute(bench,benchids,events,eventnum,players):
##subs players in court.players adds them to bench
##benchids just stores the player ids in the bench. Easier to search
    if events[eventnum][12] not in benchids:
        for player in players:
            if player.player_id == events[eventnum][11]:
                bench.add(player)
                players.add(Player(events[eventnum][12],player.team_id,0))
                players.remove(player)
                benchids.add(events[eventnum][11])
                break
    else:
        for player in players:
            if player.player_id == events[eventnum][11]:
                bench.add(player)
                players.remove(player)
                benchids.add(events[eventnum][11])
                break
        for sub in bench:
            if sub.player_id == events[eventnum][12]:
                players.add(sub)
                bench.remove(sub)
                benchids.discard(events[eventnum][12])
                break

def calculate():
    events = getEvents()
##   [Game_id 0
##    Event_Num 1  Event_Msg 2
##    Period 3     WCTime 4
##    PCTime 5     Action 6
##    Option1 7    Option2 8
##    Option3 9    Teamid 10
##    Person1 11    Person2 12
##    Team_id_type 13]
    players = getPlayers()
##    [Game id 0
##     Period 1    Person id 2
##     Team id 3   Status 4]
    period = 1
    increment = 0
    initial = set()
    eventnum = 0
    game_id = events[eventnum][0]
    team1 = findteams(players,increment,increment+10)[0]
    team2 = findteams(players,increment,increment+10)[1]
    createPlayers(initial,players,increment,increment+10,0)
    oncourt = getOnCourt(initial)
    court = Court(initial, game_id, period, team1,team2)
    bench = set()
    benchids = set()
    while eventnum < len(events):
        if events[eventnum][0] == game_id:
    ##score
            if int(events[eventnum][3]) == period:
                if int(events[eventnum][2]) == 1:
                    score(events,eventnum,court.players)
    ##substitue
                if int(events[eventnum][2]) == 8:
                    substitute(bench,benchids,events,eventnum,court.players)
    #freethrow
                if ((int(events[eventnum][2]) == 6) and (int(events[eventnum][9]) !=0)):
                    freethrow(events,eventnum,court.players)
                eventnum = eventnum + 1
    ##new period
            else:
                bench = bench.union(court.players)
                for player in court.players:
                    if player.player_id not in benchids:
                        benchids.add(player.player_id)
                court = new_period(court,period +1)
                increment = increment + 10
                newteam1 = findteams(players,increment,increment+10)[0]
                newteam2 = findteams(players,increment,increment+10)[1]
                nextset = set()
                playerset = set()
                for x in range(increment,increment+10):
                    if players[x][2] in benchids:
                        for player in bench:
                            if player.player_id == players[x][2]:
                                playerset.add(player)
                                bench.remove(player)
                                benchids.discard(player.player_id)
                                break
                    else:
                        playerset.add(Player(players[x][2],players[x][3],0))
                period = int(events[eventnum+1][3])
                court = Court(playerset,game_id,period,newteam1,newteam2)
                bench = bench - court.players
                for player in court.players:
                    if player.player_id in benchids:
                        benchids.remove(player.player_id)
     ##new game                       
        elif events[eventnum][0] != game_id:
            with open('Python_Mentality_Q1_BBALL.csv',"ab") as output:
                writer = csv.writer(output)
                for player in bench:
                    writer.writerow([court.game,str(player.player_id), str(player.plusminus)])
                for player in court.players:
                    writer.writerow([court.game,str(player.player_id), str(player.plusminus)])
            game_id = events[eventnum+1][0]
            increment = increment +10
            newteam1 = findteams(players,increment,increment+10)[0]
            newteam2 = findteams(players,increment,increment+10)[1]
            bench.clear()
            court.players.clear()
            benchids.clear()
            period = 1
            court = Court(set(),game_id,period,newteam1,newteam2)
            eventnum = eventnum + 1
    with open('Python_Mentality_Q1_BBALL.csv',"ab") as output:
        writer = csv.writer(output)
        for player in bench:
            writer.writerow([court.game,str(player.player_id), str(player.plusminus)])
        for player in court.players:
            writer.writerow([court.game,str(player.player_id), str(player.plusminus)])
print calculate()


    
   


