import pandas as pd
import random
def play():
    class baralho:
        def __init__(self, tipo):
            self.tipo = tipo
            self.baralho = pd.DataFrame(index=["Espadas", "Paus", "Copas", "Ouro"], columns=list(range(1, 14)))
            if self.tipo == "mesa":
                self.baralho = self.baralho.fillna(1)
            else:
                self.baralho = self.baralho.fillna(0)

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
    class player:
        def __init__(self, tipo):
            self.tipo = tipo
            self.baralho = baralho(self.tipo)
            self.pontos = 0
        def print_situation(self):
            print(self.baralho.baralho)
        def get_points(self):
            self.pontos = 0
            num = 0
            for pinta in self.baralho.baralho.index:
                for numero in self.baralho.baralho.columns:
                    if self.baralho.baralho[numero][pinta] == 1:
                        if numero == 1:
                            self.pontos += 1
                            num += 1
                        elif numero >= 10:
                            self.pontos += 10
                        else:
                            self.pontos += numero
            if num >= 1 and self.pontos + 10 == 21:
                self.pontos = 21
        def get_cards(self):
            global baralho_mesa
            pinta = random.choice(baralho_mesa.opcoes_pinta())
            numero = random.choice(baralho_mesa.opcoes_numero(pinta))
            baralho_mesa.remove_carta(numero, pinta)
            self.baralho.add_carta(numero, pinta)
            self.get_points()
    global baralho_mesa
    baralho_mesa = baralho("mesa")
    voce = player("player")
    casa = player("casa")
    #Pegar cartas iniciais
    casa.get_cards()
    print("Carta da CASA")
    casa.print_situation()
    casa.get_cards()
    voce.get_cards()
    voce.get_cards()
    print("SUAS cartas")
    voce.print_situation()
    print(f"Voce tem {voce.pontos} pontos")
    pegar = input("Você quer pegar mais uma carta ? (y/n)")
    while pegar.lower() == "y":
        voce.get_cards()
        print("SUAS cartas")
        voce.print_situation()
        print(f"Voce tem {voce.pontos} pontos")
        if voce.pontos > 21:
            print("Você Perdeu! \n\n\n")
            break
        pegar = input("Você quer pegar mais uma carta ? (y/n)")
    if voce.pontos <= 21:
        while casa.pontos < voce.pontos:
            casa.get_cards()
            print("Cartas da CASA")
            casa.print_situation()
            print(f"A casa tem {casa.pontos} pontos")
            if casa.pontos >=21:
                print("Você Venceu!! \n\n\n")
                break
            elif casa.pontos == voce.pontos:
                print("Empatou!!")
                break

play()
