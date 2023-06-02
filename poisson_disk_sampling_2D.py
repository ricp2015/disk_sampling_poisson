import numpy as np
import matplotlib.pyplot as plt
import matplotlib

#numero massimo di punti candidati intorno a un punto di riferimento
k = 30
#distanza minima tra i punti
r = 1.7
width, height = 60, 45
#lunghezza lato cella
a = r/np.sqrt(2)
#numero di celle nella direzione x o y della griglia
nx, ny = int(width / a) + 1, int(height / a) + 1
#lista delle coordinate nella griglia
coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
#dizionario delle celle: come chiave pongo la coordinata della cella, come valore
#l'indice delle coordinate del punto di quella cella (None se nessun punto è presente)
cells = {coords: None for coords in coords_list}

#restituisce le coordinate della cella di pt
def get_cell_coords(pt):
    return int(pt[0] // a), int(pt[1] // a)

#restituisce l'indice dei punti nelle celle vicine alla cella di coordinate coords
def get_neighbours(coords):
    #coordinate da controllare perchè potrebbero contenere punti più vicini di r
    #rispetto alla cella di coordinate coords
    dxdy = [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1),
            (2, -1), (-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1),
            (1, 1), (2, 1), (-1, 2), (0, 2), (1, 2), (0, 0)]
    neighbours = []
    for dx, dy in dxdy:
        neighbour_coords = coords[0] + dx, coords[1] + dy
        #se non è fuori dalla griglia
        if not (0 <= neighbour_coords[0] < nx and 0 <= neighbour_coords[1] < ny):
            continue
        neighbour_cell = cells[neighbour_coords]
        #se la cella contiene un punto, la mette nella lista dei vicini
        if neighbour_cell is not None:
            neighbours.append(neighbour_cell)
    return neighbours

#Il punto pt è valido se non è più vicino di r rispetto a qualsiasi altro punto:
#dunque controlla le celle vicine
def point_valid(pt):
    #coordinate della cella di pt
    cell_coords = get_cell_coords(pt)
    #ciclo sui punti nelle celle vicine a quella di pt
    for idx in get_neighbours(cell_coords):
        #punto vicino
        nearby_pt = samples[idx]
        #distanza quadratica tra il punto pt e il punto vicino
        distance2 = (nearby_pt[0]-pt[0]) ** 2 + (nearby_pt[1]-pt[1])**2
        #se i punti sono troppo vicino, restituisce False dato che pt non è valido
        if distance2 < r * r:
            return False
    #tutti i punti vicini sono stati testati, pt è valido
    return True

#Disegna al massimo k punti a partire da refpt (punto attivo), in un anello di raggio
#interno r, e raggio esterno 2r. Se nessuno di loro è valido, restituisce False,
#altrimenti il punto (pt).
def get_point(k, refpt):
    i = 0
    while i < k:
        i += 1
        #coordinata x
        rho = np.sqrt(np.random.uniform(r*r, 4 * r * r))
        #coordinata y
        theta = np.random.uniform(0, 2 * np.pi)
        #punto candidato, da verificare la sua validità
        pt = refpt[0] + rho * np.cos(theta), refpt[1] + rho * np.sin(theta)
        #se fuori dal dominio
        if not (0 <= pt[0] < width and 0 <= pt[1] < height):
            continue
        #se il punto è valido, restituisce pt
        if point_valid(pt):
            return pt
    #nessun candidato è valido
    return False

#scelgo un punto a caso per iniziare
pt = (np.random.uniform(0, width), np.random.uniform(0, height))
samples = [pt]
#il primo sample è indicizzato a 0 nella lista dei sample
cells[get_cell_coords(pt)] = 0
#è attivo, cioè sto cercando dei punti vicino a lui
active = [0]
nsamples = 1
#finchè sono presenti punti nella lista dei punti attivi
while active:
    #sceglie a caso un punto di riferimento dalla lista dei punti attivi
    idx = np.random.choice(active)
    refpt = samples[idx]
    #prova a scegliere un nuovo punto a partire dal punto di riferimento
    pt = get_point(k, refpt)
    #se il punto è valido, aggiunge alla lista dei sample e lo segna come attivo
    if pt:
        samples.append(pt)
        nsamples += 1
        active.append(len(samples)-1)
        cells[get_cell_coords(pt)] = len(samples) - 1
    #se nessun punto vicino a quello di riferimento è valido, lo rimuovo dalla lista dei punti attivi
    else:
        active.remove(idx)

colors = matplotlib.cm.rainbow(np.linspace(0, 1, nsamples))
plt.scatter(*zip(*samples), color=colors, alpha=0.6, lw=0)
plt.xlim(0, width)
plt.ylim(0, height)
plt.axis("on")
plt.show()
