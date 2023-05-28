import numpy as np
import matplotlib.pyplot as plt
import matplotlib

#numero massimo di punti candidati intorno a un punto di riferimento
k = 30
#distanza minima tra i punti
r = 7.5
width, height, depth = 60, 60, 60
#lunghezza lato cella
a = r/np.sqrt(3)
#numero di celle nella direzione x o y della griglia
nx, ny, nz = int(width / a) + 1, int(height / a) + 1, int(depth / a) + 1
#lista delle coordinate nella griglia
coords_list = [(ix, iy, iz) for ix in range(nx) for iy in range(ny) for iz in range(nz)]
#dizionario delle celle: come chiave si pone la coordinata della cella, come valore
#l'indice delle coordinate del punto di quella cella (None se nessun punto è presente)
cells = {coords: None for coords in coords_list}

#restituisce le coordinate della cella di pt
def get_cell_coords(pt):
    return int(pt[0] // a), int(pt[1] // a), int(pt[2] // a)

#restituisce l'indice dei punti nelle celle vicine alla cella di coordinate coords
def get_neighbours(coords):
    #coordinate da controllare perchè potrebbero contenere punti più vicini di r
    #rispetto alla cella di coordinate coords
    dxdydz = [(ix, iy, iz) for ix in range(-2, 3) for iy in range(-2, 3) for iz in range(-2, 3)]
    neighbours = []
    for dx, dy, dz in dxdydz:
        neighbour_coords = coords[0] + dx, coords[1] + dy, coords[2] + dz
        #se non è fuori dalla griglia
        if not (0 <= neighbour_coords[0] < nx and 0 <= neighbour_coords[1] < ny and 0 <= neighbour_coords[2] < nz):
            continue
        neighbour_cell = cells[neighbour_coords]
        #se la cella contiene un punto, la mette nella lista dei vicini
        if neighbour_cell is not None:
            neighbours.append(neighbour_cell)
    return neighbours

#il punto pt è valido se non è più vicino di r rispetto a qualsiasi altro punto:
#dunque controlla le celle vicine
def point_valid(pt):
    #coordinate della cella di pt
    cell_coords = get_cell_coords(pt)
    #cicla sui punti nelle celle vicine a quella di pt
    for idx in get_neighbours(cell_coords):
        #punto vicino
        nearby_pt = samples[idx]
        #distanza quadratica tra il punto pt e il punto vicino
        distance2 = (nearby_pt[0]-pt[0]) ** 2 + (nearby_pt[1]-pt[1])**2 + (nearby_pt[2]-pt[2]) ** 2
        #se i punti sono troppo vicini, restituisce False dato che pt non è valido
        if distance2 < r * r:
            return False
    #tutti i punti vicini sono stati testati, pt è valido
    return True

#disegna al massimo k punti a partire da refpt (punto attivo), in un anello di raggio
#interno r, e raggio esterno 2r. Se nessuno di loro è valido, restituisce False,
#altrimenti il punto (pt).
def get_point(k, refpt):
    i = 0
    while i < k:
        i += 1
        rho = np.sqrt(np.random.uniform(r*r, 4 * r * r))
        #genera 2 angoli
        sigma = np.random.uniform(0, 2 * np.pi)
        theta = np.random.uniform(0, 2 * np.pi)
        #punto candidato, da verificare la sua validità
        pt = refpt[0] + rho * np.cos(sigma) * np.sin(theta), refpt[1] + rho * np.sin(sigma) * np.sin(theta),\
            refpt[2] + rho * np.cos(theta)
        #se fuori dal dominio
        if not (0 <= pt[0] < width and 0 <= pt[1] < height and 0 <= pt[2] < depth):
            continue
        #se il punto è valido, restituisce pt
        if point_valid(pt):
            return pt
    #nessun candidato è valido
    return False

#sceglie un punto a caso per iniziare
pt = (np.random.uniform(0, width), np.random.uniform(0, height), np.random.uniform(0, depth))
samples = [pt]
#il primo sample è indicizzato a 0 nella lista dei sample
cells[get_cell_coords(pt)] = 0
#è attivo, cioè sta cercando dei punti vicino a lui
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
    #se nessun punto vicino a quello di riferimento è valido, lo rimuove dalla lista dei punti attivi
    else:
        active.remove(idx)

colors = matplotlib.cm.rainbow(np.linspace(0, 1, nsamples))
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(*zip(*samples), color=colors, alpha=0.6, lw=0)

plt.show()