import time

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

global messageSend
global received_main
global received_aux
global products


class Main_Agents(Agent):
    class behavior(FSMBehaviour):
        async def on_start(self):
            print("behavior main started")

        async def on_end(self):
            print("behavior main ended")

    class sending(State):
        async def run(self):
            agents = ["m1@jabberx.io", "m2@jabberx.io", "m3@jabberx.io"]
            messageSend
            for agent in agents:
                msg = Message(to=agent)
                # Set the "inform" FIPA performative
                msg.set_metadata("performative", "inform")
                msg.body = messageSend
                await self.send(msg)
                print("message sent")
                time.sleep(0.5)
                self.set_next_state("waiting")

    class waiting(State):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                global received_main
                received_main = msg
                print(f'received the following message: {msg.body}')
                time.sleep(0.5)
                self.set_next_state("sending")
            else:
                print("no message received after 5 seconds")

    async def setup(self):
        fsm = self.behavior()
        fsm.add_state(name="sending", state=self.sending(), initial=True)
        fsm.add_state(name="waiting", state=self.waiting())

        fsm.add_transition(source="sending", dest="waiting")
        fsm.add_transition(source="waiting", dest="sending")

        self.add_behaviour(fsm)


class Auxilary_Agents(Agent):
    class behavior(FSMBehaviour):
        async def on_start(self):
            print("behavior aux started")

        async def on_end(self):
            print("behavior aux ended")

    class sending(State):
        async def run(self):
            msg = Message(to="ap@jabberx.io")
            # Set the "inform" FIPA performative
            msg.set_metadata("performative", "inform")
            msg.body = f'the received message was: {received_aux.body}'
            await self.send(msg)
            print("message sent")
            time.sleep(0.5)
            self.set_next_state("waiting")

    class waiting(State):
        async def run(self):
            msg = await self.receive(timeout=50)
            if msg:
                global received_aux
                received_aux = msg
                products.append(received_aux.body)
                print(f'received the following message: {msg.body}')
                time.sleep(0.5)
                self.set_next_state("sending")
            else:
                print("no message received after 5 seconds")

    async def setup(self):
        fsm = self.behavior()
        fsm.add_state(name="sending", state=self.sending())
        fsm.add_state(name="waiting", state=self.waiting(), initial=True)

        fsm.add_transition(source="sending", dest="waiting")
        fsm.add_transition(source="waiting", dest="sending")

        self.add_behaviour(fsm)


messageSend = "iphone12"
main_agent = Main_Agents("ap@jabberx.io", "mdps")
auxilary_agent1 = Auxilary_Agents("m1@jabberx.io", "mdps")
futureAux1 = auxilary_agent1.start()
futureAux1.result()

auxilary_agent2 = Auxilary_Agents("m2@jabberx.io", "mdps")
futureAux2 = auxilary_agent2.start()
futureAux2.result()

auxilary_agent3 = Auxilary_Agents("m3@jabberx.io", "mdps")
futureAux3 = auxilary_agent3.start()
futureAux3.result()

main_agent_future = main_agent.start()
main_agent_future.result()
products = []
while main_agent.is_alive():
    try:
        time.sleep(5)
        if(len(products) >= 2):
            products = [] = ""
            auxilary_agent1.stop()
            auxilary_agent2.stop()
            auxilary_agent3.stop()
            main_agent.stop()
    except KeyboardInterrupt:
        auxilary_agent1.stop()
        auxilary_agent2.stop()
        auxilary_agent3.stop()
        main_agent.stop()
        break
