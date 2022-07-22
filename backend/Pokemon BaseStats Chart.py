import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')


pokedata = pd.read_csv("/Users/cheikhounagueye/Desktop/Radar Chart/pokedex_(Update_05.20).csv")
pokedata.head()

attributes=["hp", "attack", "defense", "special_attack", "special_defense", "speed"]

x = pokedata[pokedata["name"] == "Charizard"]

pokemon=[x['hp'].values[0],x['attack'].values[0],x['defense'].values[0],x['sp_attack'].values[0],x['sp_defense'].values[0],x['speed'].values[0]]


angles=np.linspace(0,2*np.pi,len(attributes), endpoint=False)
print(angles)


angles=np.concatenate((angles,[angles[0]]))
attributes.append(attributes[0])
pokemon.append(pokemon[0])


fig=plt.figure(figsize=(8,8))
ax=fig.add_subplot(111, polar=True)
ax.plot(angles,pokemon, 'o-', color='g', linewidth=.5)
ax.fill(angles, pokemon, alpha=0.25, color='g')
ax.set_thetagrids(angles * 180/np.pi, attributes)
plt.legend()
