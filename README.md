# auto_referee

This is a script to automate referee duties for Armor Critical.

Duties include:
<li>-Creating game matches based on player requests</li>
-Confirming the appropriate number of players have arrived
-Starting the game
-Pausing the game when requested
-Identifying half time and swapping teams & score accordingly
-Accurately uploading game results once the game has concluded & posting the link to players

Script is based on a Windows10 system, using Python 3.7.4 with Selenium as the prominent library.
 -Reads .rec file (essentially a .txt file) that is automatically generated upon game entry & receives live game updates from the authoritative server 
  in order to interpret game environment & make necessary commands
