# Imports
import random
from dataclasses import dataclass

@dataclass
class State:
    dmzfirewall: int = 0
    firewall: int = 0
    password: bool = False
    updates: bool = False
    serverpatch: bool = False
    usertraining: bool = False
    honeypot: bool = False
    ips: bool = False
    ids: bool = False



def decision(probability):
    return not (random.random() < probability)

# Variables
turncount = 10
# Defenses
firewall = [0.2, 0.3, 0.4, 0.5]
dmzfirewall = [0.2, 0.3, 0.4, 0.5]
updates = 0.3
passwordreq = 0.1
ids = 0.1
ips = 0.2
serverpatch = 0.1
usertraining = 0.1
# One time get out of jail for server\
clients = [0.2, 0.2, 0.2]
# Net seqmentation can only go to one client
netsegmentation = "" # Example: netsegmentation = 'A' for client A
orderOfClientAttack = [1, 2, 3]

max_budget = 0
testCount = 100
budget = 50

listState = []
for q in range(4):  # ------------------------------# DMZ firewall      $0, $2, $4, $8
    for w in range(4):  # --------------------------# Firewall          $0, $2, $4, $8
        for e in range(2):  # ----------------------# passwords         $2
            for r in range(2):  # ------------------# updates           $2
                for t in range(2):  # --------------# serverpatch       $6
                    for y in range(2):   # ---------# usertraining      $4 per
                        for u in range(2):  # ------# honeypot          $10
                            for i in range(3):   # -# ids               $8, $12
                                moneySpent = 0
                                if q != 0:
                                    moneySpent += (2**q)   # This is 2 to the power of q, giving us 2,4,8.
                                if w != 0:
                                    moneySpent += (2**w)   # This is 2 to the power of w, giving us 2,4,8.
                                if e == 1:
                                    moneySpent += 2
                                if r == 1:
                                    moneySpent += 2
                                if t == 1:
                                    moneySpent += 6
                                if y == 1:
                                    moneySpent += 4
                                if u == 1:
                                    moneySpent += 10
                                if i == 1:
                                    moneySpent += 8
                                if i == 2:
                                    moneySpent += 12
                                if moneySpent >= max_budget:
                                    max_budget = moneySpent
                                if moneySpent < budget:
                                    if i == 0:
                                        listState.append(State(q, w, bool(e), bool(r), bool(t), bool(y), bool(u), False,
                                                               False))

                                    if i == 1:
                                        listState.append(State(q, w, bool(e), bool(r), bool(t), bool(y), bool(u), True,
                                                               False))
                                    if i == 2:
                                        listState.append(State(q, w, bool(e), bool(r), bool(t), bool(y), bool(u), False,
                                                               True))

# curState = listState[0]

data = []

print(listState.__sizeof__())
print('Max budget is: ' + str(max_budget))
for curState in listState:
    clients = [0.1, 0.1, 0.1]
    wins = 0
    # curState = listState[0]
    for tests in range(testCount):
        clients = [0.1, 0.1, 0.1]
        x = 0
        curClientAttack = 0
        random.shuffle(orderOfClientAttack)
        win = False
        while x < turncount:
            # Randomize the order of attach.
            # We will keep the client as A to simplify this test.
            # Getting into the LAN
            while x < turncount:
                specialist = 0.0
                if ids:
                    specialist = 0.1
                if ips:
                    specialist = 0.2
                else:
                    specialist = 0.0
                if decision(specialist):
                    if decision(firewall[curState.firewall]):
                        x += 1
                        clientsTotal = clients
                        if curState.updates:
                            clientsTotal[0] += updates
                            clientsTotal[1] += updates
                            clientsTotal[2] += updates
                        if curState.password:
                            clientsTotal[0] += passwordreq
                            clientsTotal[1] += passwordreq
                            clientsTotal[2] += passwordreq
                        if curState.usertraining:
                            clientsTotal[0] += usertraining
                        while x < turncount:
                            specialist = 0.0
                            if ids:
                                specialist = 0.1
                            if ips:
                                specialist = 0.2
                            else:
                                specialist = 0.0
                            if decision(specialist):
                                if orderOfClientAttack[curClientAttack] != 1:
                                    if decision(clientsTotal[1]):
                                        curClientAttack += 1
                                        x += 1
                                    else:
                                        x += 1
                                else:
                                    if decision(clientsTotal[0]):
                                        x += 1
                                        while x < turncount:
                                            specialist = 0.0
                                            if ids:
                                                specialist = 0.1
                                            if ips:
                                                specialist = 0.2
                                            else:
                                                specialist = 0.0
                                            if decision(specialist):
                                                dmztotal = 0
                                                dmztotal = dmzfirewall[curState.dmzfirewall]

                                                if curState.serverpatch:
                                                    dmztotal += serverpatch
                                                if decision(dmztotal):
                                                    x += 1
                                                    if curState.honeypot:
                                                        curState.honeypot = False
                                                        x += 1
                                                    else:
                                                        win = True
                                                        wins += 1
                                                        x = turncount
                                                else:
                                                    x += 1
                                            else:
                                                x += 1
                                    else:
                                        x += 1
                            else:
                                x += 1
                    else:
                        x += 1

    winRatio = wins / testCount
    data.append((curState, winRatio))


print("Client Total: " + str(clientsTotal[0]))
print("firewall: " + str(firewall[0]))
print(win)
# if win:
#     print("WIN")
# else:
#     print("LOST")

f = open("data.txt", "w")
for info in data:
    f.write(str(info) + '\n')
f.close()


