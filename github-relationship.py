import requests
import json
import networkx as nx
import matplotlib.pyplot as plt

followersStored = {}

def getFollowers(username):
    if username not in followersStored:
        followersStored[username] = json.loads(requests.get('https://api.github.com/users/' + username + '/followers').text)
    return followersStored[username]

flatten = lambda s: reduce(list.__add__, s)

getRelationshipFromFollowers = lambda username, followers, deepth=1: \
    map(
        lambda follower: (follower['login'], username),
        followers
    ) + (
        [] if deepth <= 1 else \
        flatten(map(
            lambda follower: getRelationshipFromFollowers(follower['login'], getFollowers(follower['login']), deepth - 1),
            followers
        ))
    )

def draw(relationship):
    g = nx.DiGraph()
    g.add_edges_from(relationship)
    nx.draw(
        g,
        with_labels=True, font_family='Times New Roman',
        node_size=200, node_color='c', alpha=0.2,
        edge_color='c'
    )
    plt.show()

drawRelationship = lambda username, deepth=1: draw(getRelationshipFromFollowers(username, getFollowers(username), deepth))

## ======= Here you go ======= ##
drawRelationship(u'arrowrowe', 2)
