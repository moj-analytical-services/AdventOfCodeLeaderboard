'''
This script will grab the leaderboard from Advent of Code and post it to Slack
'''

import datetime
import sys
import json
import requests

# You'll need a file ~/secrets.py that defines these
from secrets import LEADERBOARD_ID, SESSION_ID, SLACK_WEBHOOK

# You should not need to change this URL
LEADERBOARD_URL = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(
        datetime.datetime.today().year,
        LEADERBOARD_ID)

def formatLeaderMessage(members):
    """
    Format the message to conform to Slack's API
    """
    message = ""

    # add each member to message
    medals = [':third_place_medal:', ':second_place_medal:', ':trophy:']
    for username, score, stars in members:
        if medals:
            medal = ' ' + medals.pop()
        else:
            medal = ''
        message += f"`{username:>17}` :: {score:>3} points, {stars:>3} stars{medal}\n"

    message += f"\n<{LEADERBOARD_URL}|View Leaderboard Online>"


    return message

def parseMembers(members_json):
    """
    Handle member lists from AoC leaderboard
    """
    # Get member name, score and stars
    members = [(m.get('name', 'unknown'),
                m.get('local_score', 0),
                m.get('stars', 0)
                ) for m in members_json.values()]

    # Sort members by score, descending
    members.sort(key=lambda s: (-s[1], -s[2]))

    return members

def postMessage(message):
    """
    Post the message to to Slack's API in the proper channel
    """
    payload = json.dumps({
        "icon_emoji": ":christmas_tree:",
        "username": "Advent Of Code Leaderboard",
        "text": message
    })

    requests.post(
        SLACK_WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

def main():
    """
    Main program loop
    """
    # make sure all variables are filled
    if LEADERBOARD_ID == "" or SESSION_ID == "" or SLACK_WEBHOOK == "":
        print("Please update script variables before running script.\n\
                See README for details on how to do this.")
        sys.exit(1)

    # retrieve leaderboard
    r = requests.get(
        "{}.json".format(LEADERBOARD_URL),
        cookies={"session": SESSION_ID}
    )
    if r.status_code != requests.codes.ok: #pylint: disable=no-member
        print("Error retrieving leaderboard")
        sys.exit(1)

    # get members from json
    members = parseMembers(r.json()["members"])

    # generate message to send to slack
    message = formatLeaderMessage(members)

    # send message to slack
    postMessage(message)

if __name__ == "__main__":
    main()
