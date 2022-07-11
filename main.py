import tkinter as tk
from tkinter import ttk
import threading
from random import random, randint
from time import sleep
from random import randint
from math import sqrt
import matplotlib.pyplot as plt


root = tk.Tk() # On crée la fenêtre.
root.title("Robots") # On lui donne un titre.
root.iconname("Robots") # On lui donne un titre.
root.resizable(False, False) # On l'empêche d'être redimensionnée.

button = tk.Button(root, text="Lancer", command=lambda: Canvas())
button.pack(side=tk.BOTTOM)

devils = []
angels = []
neutrals = []

dataCollectList = []

def createAgents(quantité, agentType, canvas):
    for i in range(quantité):
        position_x, position_y = randint(0, 300), randint(0, 300)
        if agentType == "Devil":
            devils.append(canvas.create_oval(position_x, position_y, position_x+20, position_y+20, fill="red"))
        if agentType == "Angel":
            angels.append(canvas.create_oval(position_x, position_y, position_x + 20, position_y + 20, fill="green"))
        if agentType == "Neutral":
            neutrals.append(canvas.create_oval(position_x, position_y, position_x + 20, position_y + 20, fill="grey"))



def Canvas():
    canvas = tk.Canvas(root, width=500, height=500, bg="grey")
    canvas.pack(side=tk.RIGHT)

    global water
    water = canvas.create_oval(300, 300, 10+50, 10+200, fill="blue")

    createAgents(6, "Devil", canvas)
    createAgents(6, "Angel", canvas)
    createAgents(10, "Neutral", canvas)

    thread = threading.Thread(target=dataCollect)
    thread.daemon = True
    thread.start()

    for devil in devils:
        thread = threading.Thread(target = MoveAgent, args = (canvas, devil, 5, 5, "Devil"))
        thread.daemon = True
        thread.start()
    for angel in angels:
        thread = threading.Thread(target = MoveAgent, args = (canvas, angel, 5, 5, "Angel"))
        thread.daemon = True
        thread.start()
    for neutral in neutrals:
        thread = threading.Thread(target=MoveAgent, args=(canvas, neutral, 5, 5, "Neutral"))
        thread.daemon = True
        thread.start()




def MoveAgent(canvas, agent, local_x_speed, local_y_speed, agentType):
    thirst = False
    thirstTimer = 0
    avoidZoneSize = 60

    local_x_speed *= random()
    local_y_speed *= random()
    if randint(0, 1) == 1:
        local_x_speed *= -1
    if randint(0, 1) == 1:
        local_y_speed *= -1

    if agentType == "Devil":
        evadeZone = canvas.create_oval(0, 0, avoidZoneSize, avoidZoneSize)

    while True:
        (leftPos, topPos, rightPos, bottomPos) = canvas.coords(agent)
        if agentType == "Devil":
            (avoidZoneLeftPos, avoidZoneTopPos, avoidZoneRightPos, avoidZoneBottomPos) = canvas.coords(evadeZone)

            (agentCenterX, agentCenterY) = ((leftPos + rightPos)/2, (topPos + bottomPos)/2)
            (avoidZoneCenterX, avoidZoneCenterY) = ((avoidZoneLeftPos + avoidZoneRightPos)/2, (avoidZoneTopPos + avoidZoneBottomPos)/2)

            canvas.move(evadeZone, agentCenterX - avoidZoneCenterX, agentCenterY - avoidZoneCenterY)

        if leftPos <= 0 or rightPos >= 500:
            local_x_speed = -local_x_speed
        if topPos <= 0 or bottomPos >= 500:
            local_y_speed = -local_y_speed

        if random() <= 0.01:
            thirst = True
            if agentType == "Devil":
                canvas.itemconfig(agent, fill="pink")
            elif agentType == "Angel":
                canvas.itemconfig(agent, fill="yellow")
            elif agentType == "Neutral":
                canvas.itemconfig(agent, fill="white")

        if thirst:
            thirstTimer += 1
            overlapping_agents = canvas.find_overlapping(leftPos,topPos,rightPos,bottomPos)
            for overlapping_agent in overlapping_agents:
                if overlapping_agent == water:
                    thirst = False
                    thirstTimer = 0
                    if agentType == "Devil":
                        canvas.itemconfig(agent, fill="red")
                    elif agentType == "Angel":
                        canvas.itemconfig(agent, fill="green")
                    elif agentType == "Neutral":
                        canvas.itemconfig(agent, fill="grey")
            if thirstTimer > 150:
                canvas.delete(agent)
                if agent in devils:
                    devils.remove(agent)
                    canvas.delete(evadeZone)
                elif agent in angels:
                    angels.remove(agent)
                return

        if agentType == "Angel":
            for devil in devils:
                try:
                    (leftPosDevil, topPosDevil, rightPosDevil, bottomPosDevil) = canvas.coords(devil)
                    devilX = (leftPosDevil+rightPosDevil)/2
                    devilY = (bottomPosDevil+rightPosDevil)/2
                    X = (leftPos+rightPos)/2
                    Y = (bottomPos+topPos)/2

                    if sqrt((devilX - X)**2 + (devilY - Y)**2) < avoidZoneSize :
                        canvas.move(agent, local_x_speed * 2, local_y_speed * 2)
                except ValueError:
                    pass

        if agentType == "Neutral":
            overlapping_agents = canvas.find_overlapping(leftPos, topPos, rightPos, bottomPos)
            for overlapping_agent in overlapping_agents:
                if overlapping_agent in angels:
                    agentType = "Angel"
                    if agent in neutrals:
                        neutrals.remove(agent)
                    angels.append(agent)
                    if thirst:
                        canvas.itemconfig(agent, fill="yellow")
                    else:
                        canvas.itemconfig(agent, fill="green")
                    break
                if overlapping_agent in devils:
                    agentType = "Devil"
                    if agent in neutrals:
                        neutrals.remove(agent)
                    devils.append(agent)
                    evadeZone = canvas.create_oval(0, 0, avoidZoneSize, avoidZoneSize)
                    if thirst:
                        canvas.itemconfig(agent, fill="pink")
                    else:
                        canvas.itemconfig(agent, fill="red")
                    break

        canvas.move(agent, local_x_speed, local_y_speed)

        sleep(0.02)

def dataCollect():
    while True:
        dataCollectList.append({"Angels": len(angels), "Devils": len(devils), "Neutral": len(neutrals)})
        sleep(0.02)


root.mainloop() # On démarre la fenêtre.
print("Fenêtre fermée. Génération du graphe.")

angelData = []
devilData = []
neutralData = []

for i in dataCollectList:
    angelData.append(i["Angels"])
    devilData.append(i["Devils"])
    neutralData.append(i["Neutral"])

plt.stackplot(range(len(dataCollectList)), [angelData, devilData, neutralData], labels = ["Anges", "Diables", "Neutres"], colors = ["green", "red", "grey"])
plt.legend()
plt.xlabel("Temps (images)")
plt.ylabel("Population")
plt.title("Graphe des populations")
#print(dataCollectList)
plt.show()