import numpy
import matplotlib
import matplotlib.pyplot
from itertools import product            

#test per controllare che il punto point sia abbastanza distante dai suoi vicini
def test_point(point, r, generated_points, grid_size, points, cell_side, neighbours_range):
    point_coordinates = tuple(int(i//cell_side) for i in point)
    neighbours = []
    #per ogni possibile cella vicina
    for x in neighbours_range:
        neighbour_coordinates = tuple(point_coordinates[index] + y for index, y in enumerate(x))
        #se una o più coordinate sono fuori dal range della griglia, la cella è fuori dal dominio della griglia
        #e viene scartata
        if not all(0 <= i < grid_size for i in neighbour_coordinates):
            continue
        #se esiste un punto in quella cella della griglia
        if points[neighbour_coordinates] != -1:
            #viene salvato l'indice del punto in quella cella
            neighbours.append(points[neighbour_coordinates])
    #per ogni vicino esistente
    for i in neighbours:
        close_point = generated_points[i]
        distance = 0
        #calcolo della distanza fra due punti
        for x in range(len(point)):
            distance += pow((close_point[x] - point[x]), 2)
        #se la distanza è inferiore a r*r, il punto è troppo vicino al vicino preso in esame, dunque va scartato
        if distance < pow(r, 2):
            return False
    #se nessun punto esistente è troppo vicino a quello generato, allora quest'ultimo è da considerarsi valido
    return True

#implementazione per formula generale per conversione da coordinate sferiche a cartesiane:
#https://en.wikipedia.org/wiki/N-sphere#Spherical_coordinates
#https://stackoverflow.com/questions/20133318/n-sphere-coordinate-system-to-cartesian-coordinate-system
def convert_coords(rho, angles):
    a = numpy.concatenate((numpy.array([2*numpy.pi]), angles))
    si = numpy.sin(a)
    si[0] = 1
    si = numpy.cumprod(si)
    co = numpy.cos(a)
    co = numpy.roll(co, -1)
    coords = si*co*rho
    return numpy.asarray(coords)

def create_point(point, k, r, grid_size, cell_side, points, generated_points, l, neighbours_range):
    #k tentativi di generazione di un punto
    for _ in range(k):
        #distanza/raggio generato casualmente
        rho = numpy.sqrt(numpy.random.uniform(r*r, 4 * r * r))
        #angoli generati casualmente
        angles = numpy.random.random_sample(len(point)-1)*numpy.pi*2
        #conversione da coordinate polari/sferiche a cartesiane
        pt = convert_coords(rho, angles)
        #somma per rendere i valori delle coordinate relativi al punto di riferimento
        pt = tuple(z + point[index] for index, z in enumerate(pt))
        #se una o più coordinate sono fuori dal range della griglia, scarta il punto generato
        if not all(0 <= j < l for j in pt):
            continue
        #test per vedere se il punto è distante abbastanza dai suoi vicini
        if test_point(pt, r, generated_points, grid_size, points, cell_side, neighbours_range):
            return pt
    #se nessun punto è stato generato, si restituisce false
    return False

#r = valore di distanza minima tra i punti, k = numero di tentativi di posizionamento di punti intorno al punto di 
#riferimento attuale, n = numero di dimensioni del piano, l = limite numerico per le dimensioni del piano 
def poisson_point_set(r, k, n, l):
    #lunghezza lato della cella nella griglia
    cell_side = r/numpy.sqrt(n)
    #dimensione griglia
    grid_size = int(l/cell_side)+1
    #coordinate di ogni cella nella griglia
    coordinates = [i for i in product(range(grid_size), repeat=n)]
    #implementazione dell'array n-dimensionale descritto da R. Bridson:
    #dizionario avente come chiavi le tuple di coordinate prodotte alla riga precedente
    #e come valori -1 inizialmente, interi positivi successivamente (indice del punto)
    points = {c: -1 for c in coordinates}
    #viene scelto un punto in modo casuale e messo nella lista dei punti generati,
    #nel dizionario e nella lista dei punti attivi
    generated_points = [tuple(numpy.random.uniform(0, l) for _ in range(n))]
    first = tuple(int(i//cell_side) for i in generated_points[0])
    points[first] = 0
    active_points = [0]
    #intervallo per la generazione delle celle adiacenti, spostato qua per generarlo una volta sola
    interval = [i for i in range(-len(first), len(first)+1)]
    neighbours_range = [p for p in product(interval, repeat=len(first))]
    #finche ci sono punti attivi
    while len(active_points) != 0:
        #se ne sceglie uno
        active_pt = numpy.random.choice(active_points)
        #si usa il punto scelto come riferimento e se ne creano altri a partire da questo
        point = create_point(generated_points[active_pt], k, r, grid_size, cell_side, points, generated_points, l, neighbours_range)
        #se viene creato un punto
        if point:
            #si aggiunge al dizionario, ai punti attivi, e ai punti generati
            generated_points.append(point)
            point_index = len(generated_points) - 1
            active_points.append(point_index)
            points[tuple(int(i//cell_side) for i in point)] = point_index
        #se non viene creato un punto, si rimuove il punto di riferimento attuale dai punti attivi
        else:
            active_points.remove(active_pt)
    #se si vuole generare un esempio bidimensionale
    if(n == 2):
        colors = matplotlib.cm.rainbow(numpy.linspace(0, 1, len(generated_points)))
        matplotlib.pyplot.scatter(*zip(*generated_points), color=colors, alpha=0.6, lw=0)
        matplotlib.pyplot.xlim(0, l)
        matplotlib.pyplot.ylim(0, l)
        matplotlib.pyplot.axis("on")
        matplotlib.pyplot.show()
    #se si vuole generare un esempio tridimensionale
    if(n == 3):
        colors = matplotlib.cm.rainbow(numpy.linspace(0, 1, len(generated_points)))
        fig = matplotlib.pyplot.figure()
        ax = fig.add_subplot(projection="3d")
        ax.scatter(*zip(*generated_points), color=colors, alpha=0.6, lw=0)
        matplotlib.pyplot.show()

 #test       
#if __name__ == '__main__':
    #poisson_point_set(*r*, *k*, *n*, *square_grid_dimension*)