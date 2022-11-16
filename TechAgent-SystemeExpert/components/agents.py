import time
import json
# from sklearn.metrics import auc
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

global received_main
global received_aux_1
global messageSend
# global products_Founded
products_Founded = []
# global interactions
interactions = []
# print("out products_Founded @:", hex(id(products_Founded)))
global stopTime
global stock1
global stock2
global stock3
global validate_Achat
global validate_magasin

file = open("./components/stock_first.json")
stock1 = json.load(file)

file = open("./components/stock_second.json")
stock2 = json.load(file)

file = open("./components/stock_third.json")
stock3 = json.load(file)


class Main_Agents(Agent):
    class behavior(FSMBehaviour):
        async def on_start(self):
            global interactions
            interactions.append("Main agent : behavior started")
            print("behavior main started")

        async def on_end(self):
            global interactions
            interactions.append("Main agent : behavior ended")
            print("behavior main ended")

    class sending(State):
        async def run(self):
            global validate_Achat
            global validate_magasin
            global interactions
            if(validate_Achat == False):
                agents = ["m1@jabberx.io",
                          "m2@jabberx.io", "m3@jabberx.io"]
                for agent in agents:
                    msg = Message(to=agent)
                    # Set the "inform" FIPA performative
                    msg.set_metadata("performative", "inform")
                    msg.body = messageSend
                    await self.send(msg)
                    interactions.append("Main agent : sent the message")
                    print("message sent")
                    time.sleep(0.5)
                    self.set_next_state("waiting")
            else:
                agent = f"m{validate_magasin}@jabberx.io"
                msg = Message(to=agent)
                # Set the "inform" FIPA performative
                msg.set_metadata("performative", "inform")
                msg.body = messageSend
                await self.send(msg)
                interactions.append("Main agent : sent the message")
                print("message sent")
                time.sleep(0.5)
                self.set_next_state("waiting")

    class waiting(State):
        async def run(self):
            global interactions
            msg = await self.receive(timeout=50)
            if msg:
                global received_main
                received_main = msg
                interactions.append(
                    f"Main agent : received the following message: {msg.body}")
                print(f'received the following message: {msg.body}')
                time.sleep(0.5)
                self.set_next_state("final_state")
            else:
                interactions.append(
                    "Main agent : no message received after 10 seconds")
                print("no message received after 10 seconds")

    class final_state(State):
        async def run(self):
            global interactions
            interactions.append("Main agent : is done!")
            print("main agent is done!")
            global stopTime
            stopTime = True
            self.kill()

    async def setup(self):
        fsm = self.behavior()
        fsm.add_state(name="sending", state=self.sending(), initial=True)
        fsm.add_state(name="waiting", state=self.waiting())
        fsm.add_state(name="final_state", state=self.final_state())

        fsm.add_transition(source="sending", dest="waiting")
        fsm.add_transition(source="waiting", dest="sending")
        fsm.add_transition(source="waiting", dest="final_state")

        self.add_behaviour(fsm)


class Auxilary_Agents(Agent):
    name = ""

    def agent_name(self, name):
        self.name = name

    class behavior(FSMBehaviour):
        name = ""

        def agent_name(self, name):
            self.name = name

        async def on_start(self):
            global interactions
            interactions.append(f"Annex agent{self.name} : behavior started")
            print("behavior aux started")

        async def on_end(self):
            global interactions
            interactions.append(f"Annex agent{self.name} : behavior ended")
            print("behavior aux ended")

    class sending(State):
        name = ""

        def agent_name(self, name):
            self.name = name

        def checkStock(self, stock):
            global interactions
            global products_Founded
            products = messageSend.split(";")
            phones = products[0].rsplit(":")
            phone = phones[-1]
            chargers = products[1].rsplit(":")
            cache = products[2].rsplit(":")
            ecouteurs = products[-1].rsplit(":")
            phone1 = next(z for z in stock if z["Name"] == phone)
            print(phone1)
            if(int(phone1["stock"]) >= 1):
                products_Founded.append(phone1)
                print(products_Founded)
            if(chargers[-1] == "yes"):
                charger = next(z for z in stock if z["Name"] == "chargeur")
                if(int(charger["stock"]) >= 1):
                    products_Founded.append(charger)
            if(cache[-1] == "yes"):
                cach = next(z for z in stock if z["Name"] == "cache")
                if(int(cach["stock"]) >= 1):
                    products_Founded.append(cach)
            if(ecouteurs[-1] != "no"):
                ecouteur = next(z for z in stock if z["Name"] == "ecouteurs")
                if(int(ecouteur.get(ecouteurs[-1]).get("stock")) >= 1):
                    ecoute = {}
                    ecoute['Name'] = 'ecouteurs'
                    ecoute["type"] = str(ecouteurs[-1])
                    ecoute["stock"] = ecouteur.get(ecouteurs[-1]).get("stock")
                    ecoute["prix"] = ecouteur.get(ecouteurs[-1])["prix"]
                    ecoute["magasin"] = ecouteur["magasin"]
                    products_Founded.append(ecoute)

        def updatestock(self, stock):
            products = messageSend.split(";")
            res = {}
            phones = products[0].split(":")
            if(phones[-1] == 'yes'):  # on met a jour le stock de phones[1]
                phone1 = next(z for z in stock if z["Name"] == phones[1])
                res = [i for i in stock if not (i['Name'] == phones[1])]
                phone1["stock"] = str(int(int(phone1["stock"])-1))
                res.append(phone1)

            charger = products[1].split(":")
            if(charger[-1] == 'yes'):  # on met a jour le stock des chargeurs
                chargeur = next(z for z in stock if z["Name"] == "chargeur")
                res = [i for i in stock if not (i['Name'] == "chargeur")]
                chargeur["stock"] = str(int(int(chargeur["stock"])-1))
                res.append(chargeur)

            caches = products[2].split(":")
            if(caches[-1] == 'yes'):  # on met a jour le stock des caches
                cache = next(z for z in stock if z["Name"] == "cache")
                res = [i for i in stock if not (i['Name'] == "cache")]
                cache["stock"] = str(int(int(cache["stock"])-1))
                res.append(cache)

            ecouteurs = products[3].split(":")
            if(ecouteurs[-1] == 'yes'):  # on met a jour le stock des ecouteurs precis
                ecouteur = next(z for z in stock if z["Name"] == "ecouteurs")
                res = [i for i in stock if not (i['Name'] == "ecouteurs")]
                normalOne = ecouteur.pop(ecouteurs[1])
                normalOne["stock"] = str(int(int(normalOne["stock"])-1))
                ecouteur[ecouteurs[1]] = normalOne
                res.append(ecouteur)
            return res

        async def run(self):

            global messageSend
            global validate_Achat
            global interactions
            global stock1
            global stock2
            global stock3
            if(self.name == "m1"):
                try:
                    if(validate_Achat == False):
                        self.checkStock(stock1)
                    else:
                        res = self.updatestock(stock1)
                        final = json.dumps(res, indent=2)
                        with open("./components/stock_first.json", "w") as f:
                            f.write(final)
                        interactions.append(
                            f"Annex agent{self.name} : update done !")
                        print("update done !")

                except StopIteration:
                    pass

            if(self.name == "m2"):
                try:
                    if(validate_Achat == False):
                        self.checkStock(stock2)
                    else:
                        res = self.updatestock(stock2)
                        final = json.dumps(res, indent=2)
                        with open("./components/stock_second.json", "w") as f:
                            f.write(final)
                        interactions.append(
                            f"Annex agent{self.name} : update done !")
                        print("update done !")
                except StopIteration:
                    pass

            if(self.name == "m3"):
                try:
                    if(validate_Achat == False):
                        self.checkStock(stock3)
                    else:
                        res = self.updatestock(stock3)
                        final = json.dumps(res, indent=2)
                        with open("./components/stock_third.json", "w") as f:
                            f.write(final)
                        interactions.append(
                            f"Annex agent{self.name} : update done !")
                        print("update done !")
                except StopIteration:
                    pass

            msg = Message(to="ap@jabberx.io")
            # Set the "inform" FIPA performative
            msg.set_metadata("performative", "inform")
            msg.body = f"{self.name} : a termine le check du stock"
            await self.send(msg)
            interactions.append(f"Annex agent{self.name} : message sent !")
            print("message sent")

            time.sleep(0.5)
            self.set_next_state("final_state")
            # self.set_next_state("waiting")

    class waiting(State):

        name = ""

        def agent_name(self, name):
            self.name = name

        async def run(self):
            global interactions
            msg = await self.receive(timeout=50)
            if msg:
                print("l'agent est : ", self.name)
                global received_aux_1
                received_aux_1 = msg
                interactions.append(f"{self.name} : received {msg.body}")
                print(f'received the following message: {msg.body}')
                time.sleep(0.5)
                self.set_next_state("sending")
            else:
                interactions.append(
                    f"{self.name} : no message received after 10 seconds")
                print("no message received after 10 seconds")

    class final_state(State):
        name = ""

        def agent_name(self, name):
            self.name = name

        async def run(self):
            global interactions
            interactions.append(f"{self.name} : is done")
            print("auxi agent is done!")
            time.sleep(2)
            self.kill()

    async def setup(self):
        fsm = self.behavior()
        fsm.agent_name(self.name)
        sending = self.sending()
        sending.agent_name(self.name)
        fsm.add_state(name="sending", state=sending)
        wating = self.waiting()
        wating.agent_name(self.name)
        fsm.add_state(name="waiting", state=wating, initial=True)
        finalState = self.final_state()
        finalState.agent_name(self.name)
        fsm.add_state(name="final_state", state=finalState)

        fsm.add_transition(source="sending", dest="final_state")
        fsm.add_transition(source="waiting", dest="sending")
        #fsm.add_transition(source = "sending", dest = "final_state")

        self.add_behaviour(fsm)


class Agents:
    def chechStore(self, checkStore):
        global validate_Achat
        global products_Founded
        # print("in chechStore products_Founded @:", hex(id(products_Founded)))
        global messageSend
        global stopTime
        global interactions
        validate_Achat = False
        stopTime = False
        messageSend = checkStore

        main_agent = Main_Agents("ap@jabberx.io", "mdps")

        auxilary_agent1 = Auxilary_Agents("m1@jabberx.io", "mdps")
        auxilary_agent1.agent_name("m1")
        futureAux1 = auxilary_agent1.start()
        futureAux1.result()

        auxilary_agent2 = Auxilary_Agents("m2@jabberx.io", "mdps")
        auxilary_agent2.agent_name("m2")
        futureAux2 = auxilary_agent2.start()
        futureAux2.result()

        auxilary_agent3 = Auxilary_Agents("m3@jabberx.io", "mdps")
        auxilary_agent3.agent_name("m3")
        futureAux3 = auxilary_agent3.start()
        futureAux3.result()

        main_agent_future = main_agent.start()
        main_agent_future.result()

        while main_agent.is_alive():
            try:
                time.sleep(0.5)

                if stopTime == True:
                    break
            except KeyboardInterrupt:
                main_agent.stop()
                auxilary_agent1.stop()
                auxilary_agent2.stop()
                auxilary_agent3.stop()

                break
        print(interactions)
        return interactions, products_Founded

    def validation_achat(self, achat, magasin):
        global validate_Achat
        global messageSend
        global stopTime
        global validate_magasin
        global interactions
        validate_magasin = magasin
        validate_Achat = True
        stopTime = False
        messageSend = achat

        main_agent = Main_Agents("ap@jabberx.io", "mdps")

        auxilary_agent1 = Auxilary_Agents("m1@jabberx.io", "mdps")
        auxilary_agent1.agent_name("m1")
        futureAux1 = auxilary_agent1.start()
        futureAux1.result()

        auxilary_agent2 = Auxilary_Agents("m2@jabberx.io", "mdps")
        auxilary_agent2.agent_name("m2")
        futureAux2 = auxilary_agent2.start()
        futureAux2.result()

        auxilary_agent3 = Auxilary_Agents("m3@jabberx.io", "mdps")
        auxilary_agent3.agent_name("m3")
        futureAux3 = auxilary_agent3.start()
        futureAux3.result()

        main_agent_future = main_agent.start()
        main_agent_future.result()

        while main_agent.is_alive():
            try:
                time.sleep(0.5)

                if stopTime == True:
                    break
            except KeyboardInterrupt:
                main_agent.stop()
                auxilary_agent1.stop()
                auxilary_agent2.stop()
                auxilary_agent3.stop()

                break
        print(interactions)
        return interactions


# if __name__ == '__main__':
#     agents = Agents()

#     products_Founded = []
#     interactions = []

#     print("in __main__ products_Founded @:", hex(id(products_Founded)))

#     i, p = agents.chechStore(
#         "phone :Samsung S9; chargeur :yes; cache :yes; ecouteurs :sans fil")

#     print("\n\nFirst\nfounded:", p)

#     products_Founded = []
#     interactions = []

#     agents.chechStore(
#         "phone :iPhone 13; chargeur :yes; cache :yes; ecouteurs :sans fil")

#     print("\n\nSecond\nfounded:", products_Founded)

#     agents.validation_achat(
#         "phone :iPhone 12:yes; chargeur :yes; cache :yes; ecouteurs :sans fil:yes", 1)
