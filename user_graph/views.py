from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import User
from users.views import login
from django.conf import settings

import networkx as nx
import matplotlib.pyplot as plt


@login_required
def user_graph(request):

    if(not request.user.is_superuser):
        return redirect(login)

    # Graph creation

    users = User.objects.all()
    DG = nx.DiGraph()

    for user in users:

        DG.add_node(user.username, **{
            "uuidNormal": str(user.uuidNormal),
            "uuidAdmin": str(user.uuidAdmin),
            "invite": str(user.invite)
        })

        for node, data in DG.nodes(data=True):
            if DG.nodes[user.username]["invite"] == data.get("uuidNormal"):
                DG.add_edge(node, user.username, **{"type":"normal"})
            elif DG.nodes[user.username]["invite"] == data.get("uuidAdmin"):
                DG.add_edge(node, user.username, **{"type":"admin"})

    # Graph printing configurations

    pos = nx.planar_layout(DG)
    #edge_labels = dict([((u,v,),d['type']) for u,v,d in DG.edges(data=True)])
    admin_edges = [(u,v) for u,v,d in DG.edges(data=True) if d.get("type") == "admin"]
    #edge_colors = ['red' if edge in admin_edges else 'blue' for edge in DG.edges()]
    edge_colors = []
    for edge in DG.edges():
        edge_colors.append('red') if edge in admin_edges else edge_colors.append('blue')

    # Labels under nodes

    right_pos = {}
    for node in DG.nodes():
        new_pos = [pos[node][0]+0.10, pos[node][1]-0.03]
        right_pos[node] = new_pos

    # Graph printing

    plt.figure(figsize=(10,10)) 
    nx.draw_networkx_edges(DG, pos, arrowstyle="->", edge_color=edge_colors, width=2, arrowsize=20, alpha=0.6)
    #nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)
    nx.draw_networkx_nodes(DG, pos, node_size=500)
    nx.draw_networkx_labels(DG, right_pos,font_size=14)
    plt.savefig(settings.MEDIA_ROOT + "/user_graph.png")
    
    return render(request, 'user_graph.html', {})
