import mesa

import pandas as pd
import networkx as nx
from mesa.discrete_space import Network
from agents import State, PenggunaMediaSosial
import random   

def banyak_pengguna(model, state):
    return sum(1 for a in model.grid.all_cells.agents if a.state is state)


def number_suspectible(model):
    return banyak_pengguna(model, State.SUSCEPTIBLE)


def number_believe(model):
    return banyak_pengguna(model, State.BELIEVE)


def number_deny(model):
    return banyak_pengguna(model, State.DENY)

def number_cured(model):
    return banyak_pengguna(model, State.CURED)

class FakeNewsModel(mesa.Model):
    """
    Model penyebaran berita palsu di media sosial.
    """
    def __init__(self, p_infl=0.05, seed=None):
        """
        Args:
            p_infl:
            Nilai float (0.0 - 1.0) yang merepresentasikan "kekuatan tambahan" yang dimiliki 
            oleh agen Influencer. Nilai ini ditambahkan ke probabilitas dasar agen 
            saat melakukan aksi (share, education, atau convince).
        """
        super().__init__(seed=seed) 
        self.p_infl = p_infl  # Tambahan probabilitas untuk agen berpengaruh

        try:
            hubungan = pd.read_csv("hubungan_sc1.csv") # <---- ubah line ini
        except FileNotFoundError:
            print("Error: File CSV tidak ditemukan. Harap jalankan 'generate_data.py' terlebih dahulu.")
            return
        
        graph = nx.from_pandas_edgelist(hubungan, source='source', target='target')
        self.grid = Network(graph, capacity=1, random=self.random)

        PenggunaMediaSosial.create_agents(
            model=self,
            n=100,
            state=State.SUSCEPTIBLE,
            is_influential = False,
            prob_share = 0,
            prob_skeptic = 0,
            prob_educate = 0,
            prob_convince = 0,
            cell = list(self.grid.all_cells),
        )
        
        self.datacollector = mesa.DataCollector(
            {
                "Susceptible": number_suspectible,
                "Believe": number_believe,
                "Deny": number_deny,
                "Cured": number_cured,
                #"R over S": self.resistant_susceptible_ratio,
            }
        )

        try:
            agent_data = pd.read_csv("data_pengguna_sc1.csv") # <---- ubah line ini
        except FileNotFoundError:
            print("Error: File CSV tidak ditemukan. Harap jalankan 'generate_data.py' terlebih dahulu.")
            return

        for i, (_, row) in zip(self.agents, agent_data.iterrows()):
            i.state = State[row['initial_state']]
            i.is_influential = row['is_influential']
            i.prob_share = row['prob_share']
            i.prob_skeptic = row['prob_skeptic']
            i.prob_educate = row['prob_educate']
            i.prob_convince = row['prob_convince']

    def step(self):
        self.agents.shuffle_do("step")
        # collect data
        self.datacollector.collect(self)

        
        
if __name__ == "__main__":
    #tes model
    model = FakeNewsModel(0,4)
    for i in model.agents:
        print(f"Agen ID: {i.unique_id}, State: {i.state}, Influential: {i.is_influential}, prob_share: {i.prob_share}, prob_skeptic: {i.prob_skeptic}, prob_educate: {i.prob_educate}, prob_convince: {i.prob_convince}")
