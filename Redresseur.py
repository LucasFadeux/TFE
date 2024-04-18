import numpy as np
import matplotlib.pyplot as plt

# Paramètres du signal
f = 50  # fréquence à 50 Hz
T = 1/f # Période
t_full = np.linspace(0, 2*T, 5000)  # Vecteur temps
phase_rad = np.deg2rad(120)  # Déphasage en radians

# Define colors in RGB
Vert=(162/255,175/255,146/255)
Bleu=(64/255,116/255,155/255)
Rouge=(224/255,152/255,120/255)

# Génération des signaux des trois phases
signal_1_full = np.sin(2 * np.pi * f * t_full)
signal_2_full = np.sin(2 * np.pi * f * t_full - phase_rad)
signal_3_full = np.sin(2 * np.pi * f * t_full - 2 * phase_rad)

# Calcul des différences de tension entre les phases
U_12 = signal_1_full - signal_2_full
U_21 = signal_2_full - signal_1_full
U_23 = signal_2_full - signal_3_full
U_32 = signal_3_full - signal_2_full
U_31 = signal_3_full - signal_1_full
U_13 = signal_1_full - signal_3_full

# Calcul de Vs
Vs = np.maximum.reduce([np.abs(U_12), np.abs(U_23), np.abs(U_31)])

# Détection des croisements à zéro pour les tensions utilisées pour les annotations
zero_crossings_21 = np.where(np.diff(np.sign(U_21)))[0]
zero_crossings_32 = np.where(np.diff(np.sign(U_32)))[0]
zero_crossings_13 = np.where(np.diff(np.sign(U_13)))[0]

# Fusionner et trier tous les croisements à zéro
all_crossings = np.sort(np.concatenate((zero_crossings_21, zero_crossings_32, zero_crossings_13)))

# Annotations et tracés
plt.figure(figsize=(12, 8))
plt.plot(t_full, signal_1_full, label='Phase 1', color=Vert)
plt.plot(t_full, signal_2_full, label='Phase 2', color=Bleu)
plt.plot(t_full, signal_3_full, label='Phase 3', color=Rouge)
plt.plot(t_full, Vs, label='Vs (Signal redressé)', color='black', linewidth=2)

# Tracé des tensions inverses
plt.plot(t_full, U_21, color='gray', linestyle='--', alpha=0.3)
plt.plot(t_full, U_32, color='gray', linestyle='--', alpha=0.3)
plt.plot(t_full, U_13, color='gray', linestyle='--', alpha=0.3)
plt.plot(t_full, U_12, color='gray', linestyle='--', alpha=0.3)
plt.plot(t_full, U_23, color='gray', linestyle='--', alpha=0.3)
plt.plot(t_full, U_31, color='gray', linestyle='--', alpha=0.3)

# Détection des croisements à zéro pour U12, U23, U31, U21, U32, U13
zero_crossings_12 = np.where(np.diff(np.sign(U_12)))[0]
zero_crossings_23 = np.where(np.diff(np.sign(U_23)))[0]
zero_crossings_31 = np.where(np.diff(np.sign(U_31)))[0]
zero_crossings_21 = np.where(np.diff(np.sign(U_21)))[0]
zero_crossings_32 = np.where(np.diff(np.sign(U_32)))[0]
zero_crossings_13 = np.where(np.diff(np.sign(U_13)))[0]

# Tracer les lignes verticales aux croisements de chaque tension
for crossing in zero_crossings_12:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)
for crossing in zero_crossings_23:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)
for crossing in zero_crossings_31:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)
for crossing in zero_crossings_21:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)
for crossing in zero_crossings_32:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)
for crossing in zero_crossings_13:
    plt.axvline(t_full[crossing], color='black', linestyle='--', alpha=0.5)


# Calcul des croisements entre U21, U32, U13
crossings_21_32 = np.where(np.diff(np.sign(U_21 - U_32)))[0]
crossings_32_13 = np.where(np.diff(np.sign(U_32 - U_13)))[0]
crossings_13_21 = np.where(np.diff(np.sign(U_13 - U_21)))[0]

# Collecte de tous les croisements
all_crossings = np.sort(np.concatenate((crossings_21_32, crossings_32_13, crossings_13_21)))

# Labels dans l'ordre cyclique
labels_cycle = ['U12', 'U13', 'U23', 'U21', 'U31','U32']
index = 0

# Placement des annotations
for crossing in all_crossings:
    plt.text(t_full[crossing], 1.55, labels_cycle[index % len(labels_cycle)], 
             horizontalalignment='center', verticalalignment='center', 
             fontweight='bold', fontsize=12)  # Vous pouvez ajuster la taille de la police selon vos besoins
    index += 1

# Configurations de base du graphiqueJ
plt.title('Redresseur triphasé')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 0.05))  # Positionne la légende en bas au centre
plt.tight_layout()
plt.show()
