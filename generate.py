import pandas as pd
import networkx as nx
import random


# --- KONFIGURASI UMUM ---
N_AGENTS = 100
N_INITIAL_INFECTED = 5
P_INFLUENTIAL = 0.1  # 10% agen adalah influencer
AVG_CONNECTIONS = 3  # Parameter m untuk Barabasi-Albert

# Fungsi Helper untuk membuat atribut random normal
def get_normal_attrs():
    return {
        "p_inf": round(random.uniform(0.02, 0.10), 4),       # Daya sebar
        "p_resist": round(random.uniform(0.05, 0.20), 4),    # Daya tolak
        "p_vace": round(random.uniform(0.01, 0.05), 4),      # Daya vaksin (normal)
        "p_cure": round(random.uniform(0.005, 0.02), 4)      # Daya sembuh
    }

print("=== MEMULAI GENERATE DATA SKENARIO ===")

# ==========================================
# SKENARIO 1: BELIEVER ADALAH HUB (BANYAK RELASI)
# ==========================================
print("\n[1/2] Men-generate Skenario 1: Targeted Attack (Hubs)...")

# 1. Buat Jaringan Dulu untuk tahu siapa Hub-nya
G1 = nx.barabasi_albert_graph(N_AGENTS, AVG_CONNECTIONS)

# 2. Cari 5 Node dengan derajat (koneksi) tertinggi
node_degrees = sorted(G1.degree, key=lambda x: x[1], reverse=True)
top_hubs = [n for n, d in node_degrees[:N_INITIAL_INFECTED]]
print(f"   -> Top 5 Hubs yang akan menjadi BELIEVE: {top_hubs}")

# 3. Buat Data Pengguna
data_sc1 = []
for i in range(N_AGENTS):
    attrs = get_normal_attrs()
    
    # LOGIKA KHUSUS SKENARIO 1:
    # Jika i adalah salah satu top hub, dia BELIEVE. Sisanya SUSCEPTIBLE.
    if i in top_hubs:
        state = "BELIEVE"
    else:
        state = "SUSCEPTIBLE"
        
    data_sc1.append({
        "agent_id": i,
        "initial_state": state,
        "is_influential": (random.random() < P_INFLUENTIAL),
        "prob_share": attrs["p_inf"],
        "prob_skeptic": attrs["p_resist"],
        "prob_educate": attrs["p_vace"],
        "prob_convince": attrs["p_cure"]
    })

# Simpan File Skenario 1
pd.DataFrame(data_sc1).to_csv("data_pengguna_sc1.csv", index=False)
pd.DataFrame(list(G1.edges()), columns=["source", "target"]).to_csv("hubungan_sc1.csv", index=False)
print("   -> File 'data_pengguna_sc1.csv' dan 'hubungan_sc1.csv' berhasil dibuat.")


# ==========================================
# SKENARIO 2: ATRIBUT P_VACE RENDAH (PASIF)
# ==========================================
print("\n[2/2] Men-generate Skenario 2: Low Vaccination (Pasif)...")

# 1. Buat Jaringan (Bisa beda topologi, tapi metode sama)
G2 = nx.barabasi_albert_graph(N_AGENTS, AVG_CONNECTIONS)

# 2. Pilih 5 node acak untuk menjadi BELIEVE (karena fokusnya bukan posisi, tapi atribut)
initial_infected_sc2 = random.sample(range(N_AGENTS), N_INITIAL_INFECTED)

# 3. Buat Data Pengguna
data_sc2 = []
for i in range(N_AGENTS):
    attrs = get_normal_attrs()
    
    if i in initial_infected_sc2:
        state = "BELIEVE"
    else:
        state = "SUSCEPTIBLE"
    
    # LOGIKA KHUSUS SKENARIO 2:
    # prob_educate dibuat SANGAT RENDAH untuk SEMUA ORANG
    # Misal: 0.0001 - 0.001 (Hampir tidak pernah memvaksinasi orang lain)
    low_p_vace = round(random.uniform(0.001, 0.010), 5)

    data_sc2.append({
        "agent_id": i,
        "initial_state": state,
        "is_influential": (random.random() < P_INFLUENTIAL),
        "prob_share": attrs["p_inf"],
        "prob_skeptic": attrs["p_resist"],
        "prob_educate": low_p_vace,  # <-- INI YANG DIUBAH
        "prob_convince": attrs["p_cure"]
    })

# Simpan File Skenario 2
pd.DataFrame(data_sc2).to_csv("data_pengguna_sc2.csv", index=False)
pd.DataFrame(list(G2.edges()), columns=["source", "target"]).to_csv("hubungan_sc2.csv", index=False)
print("   -> File 'data_pengguna_sc2.csv' dan 'hubungan_sc2.csv' berhasil dibuat.")

print("\n=== SELESAI ===")