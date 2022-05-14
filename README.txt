Tennis dataset contains information about ATP Men's tennis. It consist of the ff columns:

date - 1 January 2017 to 21 November 2021
year - 2017 to 2021
tournament - different tournaments
series - ATP250 or grand slam etc
court - indoor or outdoor
surface - hard, clay, grass
round - 1st round to the final
best_of - 3 or 5
winner - winner name of every match
loser - loser name of every match
wrank - ATP ranking of match winner at the time of play
lrank - ATP ranking of match loser at the time of play
wpts - ATP points of match winner at the time of play
lpts - ATP points of match loser at the time of play
w1 - games by match winner in set 1
l1 - games by match loser in set 1
w2 - games by match winner in set 2
l2 - games by match loser in set 2
w3 - games by match winner in set 3
l3 - games by match loser in set 3
w4 - games by match winner in set 4
l4 - games by match loser in set 4
w5 - games by match winner in set 5
l5 - games by match loser in set 5
wsets - number of sets the match winner won in a match
lsets - number of sets the match loser won in a match
status - whether the match was completed, retired etc.
win_counts - total number of matches a player won 
tsets - total number of sets played in a match

Top10 dataset contains the above columns and the following:

s1win - total number of set 1 won by a player (winner)
s1loss - total number of set 1 lost by a player (winner)
s1win(%) - set 1 win percentage by a player

Note: The above cols have been included to answer the research question " What is the likelihood (in terms of percentage) that the player who won the match would have won the first set as well?" 

Grandslam dataset includes the below columns:

s4win - total number of set 4 won by a player (winner)
s4loss - total number of set 4 lost by a player (winner)
s4win(%) - set 4 win percentage by a player

Note: The above cols have been included to answer the research question " What is the likelihood (in terms of percentage) that the player who won the match would have won the penultimate set as well?" The penultimate set is limited to set 4 of best of 5 matches, with the 2021 top 10 ranked players in the grand slam series.

 


