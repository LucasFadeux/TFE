import numpy as np
import matplotlib.pyplot as plt

# Paramètres à modifier (doit être impair en pratique)
f_multi = 15

# Paramètres généraux
f_sin = 50
t = np.linspace(0, 1/f_sin, 2000, endpoint=False)

# Définition des couleurs
Vert = (162/255, 175/255, 146/255)
Bleu = (64/255, 116/255, 155/255)
 
# Calcul des trois signaux sinusoïdaux déphasés
sin_wave = np.sin(2 * np.pi * f_sin * t)
sin_wave_120 = np.sin(2 * np.pi * f_sin * t - 2 * np.pi / 3)
sin_wave_240 = np.sin(2 * np.pi * f_sin * t - 4 * np.pi / 3)

# Paramètres pour le signal triangulaire
f_tri = f_multi * f_sin
signal_tri = 2 * (np.abs(((t + (1 / (4 * f_tri))) * f_tri) % 1 - 0.5) - 0.5) * 2.02 + 1.01

# Génération des signaux PWM pour chaque phase
pwm_signal = np.where((sin_wave > 0) & (sin_wave > signal_tri), 1,
                      np.where((sin_wave > 0) & (sin_wave <= signal_tri), 0,
                               np.where((sin_wave <= 0) & (sin_wave > signal_tri), 0, -1)))
pwm_signal_120 = np.where((sin_wave_120 > 0) & (sin_wave_120 > signal_tri), 1,
                          np.where((sin_wave_120 > 0) & (sin_wave_120 <= signal_tri), 0,
                                   np.where((sin_wave_120 <= 0) & (sin_wave_120 > signal_tri), 0, -1)))
pwm_signal_240 = np.where((sin_wave_240 > 0) & (sin_wave_240 > signal_tri), 1,
                          np.where((sin_wave_240 > 0) & (sin_wave_240 <= signal_tri), 0,
                                   np.where((sin_wave_240 <= 0) & (sin_wave_240 > signal_tri), 0, -1)))

# Visualisation des signaux
plt.figure(figsize=(12, 8))

def plot_with_fill(ax, phase, pwm, color, label):
    ax.plot(t, phase, color=Bleu, label=label)
    ax.fill_between(t, 0, pwm, where=(pwm >= 0), color=color, step='post', alpha=0.9)
    ax.fill_between(t, 0, pwm, where=(pwm <= 0), color=color, step='post', alpha=0.9)
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.75)
    ax.legend()

# Signaux sinusoïdaux et PWM
ax1 = plt.subplot(3, 1, 1)
plot_with_fill(ax1, sin_wave, pwm_signal, Vert, 'Phase 1 Sinusoïdal (50 Hz)')

ax2 = plt.subplot(3, 1, 2)
plot_with_fill(ax2, sin_wave_120, pwm_signal_120, Vert, 'Phase 2 Sinusoïdal (50 Hz)')

ax3 = plt.subplot(3, 1, 3)
plot_with_fill(ax3, sin_wave_240, pwm_signal_240, Vert, 'Phase 3 Sinusoïdal (50 Hz)')

# Paramètres communs
for ax in plt.gcf().axes:
    ax.set_xlabel('Temps (s)')
    ax.set_ylabel('Amplitude')
    ax.grid(False)
    ax.yaxis.set_ticklabels([])

plt.tight_layout()
plt.show()