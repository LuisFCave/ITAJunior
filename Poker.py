import pandas as pd
import random
class baralho:
    def __init__(self, tipo):
        self.tipo = tipo
        self.baralho = pd.DataFrame(index=["Espadas", "Paus", "Copas", "Ouro"], columns=list(range(1, 14)))
        if self.tipo == "mesa":
            self.baralho = self.baralho.fillna(1)
        else:
            self.baralho = self.baralho.fillna(0)
    def reset(self):
        if self.tipo == "mesa":
            for x in self.baralho.index:
                for y in self.baralho.columns:
                    if self.baralho[y][x] == 0:
                        self.baralho.loc[x, y] = 1
        else:
            for x in self.baralho.index:
                for y in self.baralho.columns:
                    if self.baralho[y][x] == 1:
                        self.baralho.loc[x, y] = 0

    def opcoes_pinta(self):
        result = []
        for x in self.baralho.index:
            amount = 0
            for a in self.baralho.columns:
                if self.baralho[a][x] != 0:
                    amount += 1
            if amount > 0:
                result = result + [x]
        return result

    def opcoes_numero(self, pinta):
        result = []
        for a in self.baralho.columns:
            if self.baralho[a][pinta] == 1:
                result = result + [a]
        return result

    def add_carta(self, numero, pinta):
        self.baralho.loc[pinta, numero] = 1

    def remove_carta(self, numero, pinta):
        self.baralho.loc[pinta, numero] = 0
    def mesclar(self, baralho):
        for i in self.baralho.columns:
            for j in self.baralho.index:
                if baralho[i][j] == 1:
                    self.baralho.loc[j, i] = 1
class player:
    def __init__(self, tipo):
        self.tipo = tipo
        self.baralho = baralho(self.tipo)
        self.pontos = 0
    def print_situation(self):
        print(self.baralho.baralho)
    def get_cards(self):
        global baralho_mesa
        pinta = random.choice(baralho_mesa.opcoes_pinta())
        numero = random.choice(baralho_mesa.opcoes_numero(pinta))
        baralho_mesa.remove_carta(numero, pinta)
        self.baralho.add_carta(numero, pinta)
    def level(self):
        baralho = self.baralho.baralho
        #Straight Flush 1
        for x in baralho.index:
            i = 10
            if baralho[i][x] == 1 and baralho[i + 1][x] == 1 and baralho[i + 2][x] == 1 and baralho[i + 3][x] == 1 and baralho[1][x] == 1:
                return [1,i]
            for i in baralho.columns[:-5]:
                if baralho[i][x] == 1 and baralho[i+1][x] == 1 and baralho[i+2][x] == 1 and baralho[i +3][x] == 1 and baralho[i+4][x] == 1:
                    return [1,i]
        #Four of a kind 2
        trios = 0
        trio_carta = 0
        duplas = 0
        dupla_carta = 0
        dupla_carta2 = 0
        for i in baralho.columns:
            result = 0
            for x in baralho.index:
                if baralho[i][x] == 1:
                    result += 1
            if result == 4:
                return [2, i]
            if result == 3:
                trios += 1
                trio_carta = i
            if result == 2:
                duplas += 1
                if duplas == 2:
                    dupla_carta2 = i
                else:
                    dupla_carta = i
        #Full House 3
        if trios == 1 and duplas == 1:
            return [3, trio_carta, dupla_carta]
        #Flush 4
        for x in baralho.index:
            cards = []
            for i in baralho.columns:
                if baralho[i][x] == 1:
                    cards = cards + [i]
            if len(cards) >= 5:
                return [4] + cards
        #Straight 5
        lista = [0 for _ in range(len(baralho.columns))]
        for i in baralho.columns[:-5]:
            for x in baralho.index:
                if baralho[i][x] == 1:
                    lista[i] = 1
        if lista[0] == 1 and lista[-1] == 1 and lista[-2] == 1 and lista[-3] == 1 and lista[-4] == 1:
            return [5, 10]
        count = 0
        for x in range(1,len(lista[:-5])):
            if lista[x] == 1 and lista[x-1] == 1 and lista[x-2] == 1 and lista[x-3] == 1 and lista[x-4] == 1:
                return [5, x + 1]
        #Three of a kind 6
        if trios == 1 and duplas == 0:
            return [6, trio_carta]
        #Two pair 7
        if trios == 0 and duplas == 2:
            return [7, dupla_carta, dupla_carta2]
        #One pair 8
        if trios == 0 and duplas == 1:
            return [8, dupla_carta]
        else:
            big = 0
            for x in baralho.columns:
                for a in baralho.index:
                    if baralho[x][a] == 1:
                        if x > big:
                            big = x
            return [9, big]
def get_winner(result1, result2):
    if result1[0] > result2[0]:
        return 1
    elif result1[0] < result2[0]:
        return 2
    elif result1[0] == result2[0]:
        if result1[0] == 4:
            #grande pika
            return 0
        if result1[0] == 3:
            if result1[1] == result2[1]:
                if result1[2] > result2[2]:
                    return 1
                if result1[2] < result2[2]:
                    return 2
                else:
                    return 0
            elif result1[1] > result2[1]:
                return 1
            else:
                return 2
        if result1[0] == 7:
            return 0
        else:
            if result1[1] > result2[1]:
                return 1
            if result1[1] == result2[1]:
                return 0
            else:
                return 2

global pool
global pool1
baralho_mesa = baralho("mesa")
main = player("main")
pool1 = 0
pool = 0
def play():
    global main
    global pool
    global pool1
    p1 = player("player")
    p2 = player("player")
    for x in range(2):
        p1.get_cards()
        p2.get_cards()
    for x in range(5):
        main.get_cards()
    p1.baralho.mesclar(main.baralho.baralho)
    p2.baralho.mesclar(main.baralho.baralho)

    result = get_winner(p1.level(), p2.level())
    p1.baralho.reset()
    p2.baralho.reset()
    main.baralho.reset()
    baralho_mesa.reset()
    if result != 0:
        pool += 1
        if result == 1:
            pool1 += 1
    if pool != 0:
        print(str(pool1*100/pool) + "%")
    else:
        print("No")
for _ in range(10000):
    play()

#SUGOU

