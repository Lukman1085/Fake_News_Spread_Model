import mesa

import pandas as pd
import networkx as nx
from mesa.discrete_space import CellCollection, Network
import random   
from enum import Enum

class State(Enum):
    SUSCEPTIBLE = 0
    BELIEVE = 1  # "Infected" di paper
    DENY = 2       # "Vaccinated" di paper
    CURED = 3   

class PenggunaMediaSosial(mesa.discrete_space.FixedAgent):
    """
    prob_share: Seberapa aktif agent BELIEVE membagikan info yang dia percaya?
    prob_skeptic: Seberapa kritis/pintar agent SUSPECTIBLE ini menolak berita dari agent BELIEVE?
    prob_educate: Seberapa aktif agent DENY mengedukasi orang yang rentan?
    prob_convince: Seberapa jago agent DENY menyadarkan orang yang sudah terlanjur percaya(BELIEVE)?
    """
    def __init__(self, model, 
                state, 
                is_influential, 
                prob_share, 
                prob_skeptic, 
                prob_educate, 
                prob_convince,
                cell):
        super().__init__(model)
        self.state = state
        self.is_influential = is_influential
        self.prob_share = prob_share
        self.prob_skeptic = prob_skeptic
        self.prob_educate = prob_educate
        self.prob_convince = prob_convince
        self.cell = cell

    def spread_fake_news(self,model):
        prob = self.prob_share
        # Jika influencer, tambahkan bonusnya
        if self.is_influential:
            prob += model.p_infl
        for agent in self.cell.neighborhood.agents:
            if (agent.state is State.SUSCEPTIBLE) and (
                self.random.random() < prob
            ):
                agent.state = State.BELIEVE if self.random.random() >= agent.prob_skeptic else State.DENY

    def aggaints_fake_news(self,model):
        prob_vace = self.prob_educate
        # Jika influencer, tambahkan bonusnya
        if self.is_influential:
            prob_vace += model.p_infl

        for agent in self.cell.neighborhood.agents:
            if agent.state is State.SUSCEPTIBLE:

                if self.random.random() < prob_vace:
                    agent.state = State.DENY

            elif agent.state is State.BELIEVE:
                prob_cure = self.prob_convince
                
                # Jika influencer, tambahkan bonusnya
                if self.is_influential:
                    prob_cure += model.p_infl

                if self.random.random() < prob_cure:
                    agent.state = State.CURED
            else:
                pass

    def step(self):
        """
        Logika yang dijalankan agen setiap timestep.
        Agen yang "Believe" dan "Deny" adalah yang aktif.
        """
            
        if self.state == State.BELIEVE:
            self.spread_fake_news(self.model)
        if self.state == State.DENY:
            self.aggaints_fake_news(self.model)
        