import json
from leaderboard import parseMembers, formatLeaderMessage

with open('tests/leaderboard.json', 'r') as f:
    leaderboard = json.load(f)

members = parseMembers(leaderboard["members"])
message = formatLeaderMessage(members)
print(message)
