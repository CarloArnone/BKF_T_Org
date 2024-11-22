import pandas as pd
import random

class Player:
    def __init__(self, name, proficiency, time_played = 0, points_scored = 0, team_name = "Rest"):
        self.name = name              # Player's name
        self.proficiency = proficiency  # Player's proficiency
        self.time_played = time_played  # Time played by the player
        self.points_scored = points_scored  # Points scored by the player
        self.team_name = team_name
    def __repr__(self):
        return f"Name: {self.name}, Proficiency: {self.proficiency}, Time Played: {self.time_played}, Points Scored: {self.points_scored}"

class Team:
    def __init__(self, team_name):
        self.members = []  # List to hold team members
        self.average_score = 0  # Average score of the team
        self.team_name = team_name  # Name of the team
        self.total_proficiency = 0

    def add_member(self, player):
        self.members.append(player)
        self.update_average_score()
        self.update_total_proficiency(player.proficiency)  # Update total proficiency when a member is added

    def update_average_score(self):
        if self.members:
            total_score = sum(player.points_scored for player in self.members)
            self.average_score = total_score / len(self.members)
        else:
            self.average_score = 0

    def update_total_proficiency(self, proficiency):
        self.total_proficiency += proficiency  # Update total proficiency with the new member's proficiency

    def pretty_print(self):
        print(f"Team Name: {self.team_name}")
        print(f"Average Score: {self.average_score:.2f}")
        print(f"Total Proficiency: {self.total_proficiency}")
        print("Members:")
        for member in self.members:
            print(f"  - {member}")

def extract_players_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Create Player objects from the DataFrame
    players = []
    for row in df.itertuples(index=False):
        player = Player(
            name=row[0],                # Column A (index 0) for names
            proficiency=row[1],         # Column B (index 1) for proficiency
            # Default values for time_played and points_scored
        )
        players.append(player)
    
    return players

def arrange_teams_with_remaining_people_OV(players, team_size, num_teams):
    # Sort players based on time played
    players_to_select = players.copy()
    players_to_select.sort(key=lambda x: x.time_played)

    #reclusterize players
    #TODO

    number_of_players_to_select = team_size * num_teams

    selected_players = []
    while len(selected_players) < number_of_players_to_select:
        if len(players_to_select) == 0:
            print("Not Enough players to form the teams")
            return
        
        p1 = players_to_select.pop(0)
        selected_players.append(p1)

    selected_players.sort(key=lambda x: x.proficiency, reverse=True) 
    final_selected_players = selected_players.copy()

    teams = [Team(f"Team {i + 1}") for i in range(num_teams)]
    
    for _ in range(len(selected_players)):
        # Find the team with the least total proficiency
        min_team_index = min(range(len(teams)), key=lambda i: teams[i].total_proficiency)
        if len(teams[min_team_index].members) < team_size:
            player = selected_players.pop(0)  # Take the first player from the list
            teams[min_team_index].add_member(player)
        else:
            # Find the team with the fewest members
            min_team_index = min(range(len(teams)), key=lambda i: len(teams[i].members))
            if len(teams[min_team_index].members) < team_size:
                player = selected_players.pop(-1)  # Take the last player from the list
                teams[min_team_index].add_member(player)
            else:
                break

    final_selected_players = [p for p in final_selected_players if p not in selected_players]

    return teams, final_selected_players
        
def match_making(teams):
    matches = []
    if len(teams) % 2 != 0:
        #Not possible situation, can not do the matches 
        print("WTF IS WRONG WITH YOU !!!")
        return
    
    while teams:
        current_team = teams.pop(0)
        most_similar_team_index =  min(range(len(teams)), key=lambda i: abs(current_team.average_score - teams[i].average_score))
        most_similar_team = teams.pop(most_similar_team_index)

        matches.append((current_team, most_similar_team))
    
    return matches
    
def update_time_played(selected_players):
    for player in selected_players:
        player.time_played += GAME_TIMER  # Add the specified minutes to time played

def update_score_of_players(winners):
    for player in winners:
        player.points_scored += WINNING_SCORE_POINTS

def pretty_print_players(players):
    print(f"{'Name':<20} {'Proficiency':<12} {'Time Played':<12} {'Points Scored':<12}")
    print("=" * 56)
    for player in players:
        print(f"{player.name:<20} {player.proficiency:<12} {player.time_played:<12} {player.points_scored:<12}")

def pretty_print_teams(teams):
    for team in teams:
        team.pretty_print()
        print("=" * 70)

def pretty_print_matches(matches):
    print("Matchups:")
    print("=" * 30)
    for match in matches:
        team1 = match[0]
        team2 = match[1]
        print(f"{team1.team_name} (Avg Score: {team1.average_score:.2f}) vs {team2.team_name} (Avg Score: {team2.average_score:.2f})")
    print("=" * 30)

def simulate_winning_turn(matches):
    for match in matches:
            winner = match[random.randint(0, 1)]
            update_score_of_players(winner.members)

#### GRAPHIC INTERFACE OFLINE

EXC_FILE = 'players.xlsx'
TEAM_SIZE = 4               # Specify the number of members per team
FIELDS_NUM = 3            # Number of open fields
NUM_TEAMS= FIELDS_NUM * 2   # Specify the number of teams
WINNING_SCORE_POINTS = 10   # How much you score winning a game
GAME_TIMER = 15             # How long is a game, in minutes


players = extract_players_from_excel(EXC_FILE)



# 
# while True:
#     # Wait for user input to update time played
#     input("Press Enter to add 15 minutes to the time played of each selected player and redo the teams...")
#     
#     teams, selected_players = arrange_teams_with_remaining_people_OV(players, TEAM_SIZE, NUM_TEAMS)
#     # Update time played for selected players
#     update_time_played(selected_players)  # Add 5 minutes
#     
#     pretty_print_players(players)
#     print("\n\n\n")
#     pretty_print_teams(teams)
#     print("\n\n\n")
#     matches = match_making(teams)
#     pretty_print_matches(matches)
# 
#     simulate_winning_turn(matches)