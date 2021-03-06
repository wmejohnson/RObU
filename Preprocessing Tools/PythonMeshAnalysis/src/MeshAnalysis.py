# William Johnson
# Mesh Preprocessing for RObU
# Reads a .obj and returns a .ro

import numpy
from scipy.sparse import coo_matrix

def import_mesh(filename):
    vertices = numpy.array([0, 0, 0], ndmin=2)
    for line in open(filename, "r"):
	vals = line.split()
	if vals[0] == "v":
	    v = map(float, vals[1:])
	    v = numpy.array(v, ndmin=2)
            vertices = numpy.concatenate((vertices, v), axis=0)
    return vertices[1:]

def construct_mass_matrix(vertices):
    S = numpy.rot90(vertices)
    z, y, x = (S[0], S[1], S[2])
    mass_matrix = numpy.zeros((len(z), len(x), len(y)))
    #print "mass matrix shape"+str(numpy.shape(mass_matrix))
    #account for negative indicies, center in the matrix
    z = z + (numpy.shape(mass_matrix)[0]/2)
    x = x + (numpy.shape(mass_matrix)[1]/2)
    y = y + (numpy.shape(mass_matrix)[2]/2)
    #iterate through each zplane
    for i in range(len(z)):
        xplane = numpy.array([])
        yplane = numpy.array([])
        for item in z:
            #if the item is on the current plane
            if item == i:
                #get the (x, y) coodinate for the mass on that plane
                xplane = numpy.append(xplane, numpy.array([x[i]]))
                yplane = numpy.append(yplane, numpy.array([y[i]]))
        data = numpy.ones_like(xplane)
        #define the plane using coo_matrix and tehe x and y coords obtained
        plane = coo_matrix((data, (xplane, yplane)), shape=(len(z), len(z))).todense()
        #set the mass matrix as this depth to the plane of mass created
        #print numpy.shape(plane)
        mass_matrix[i] = plane        
    return mass_matrix

def construct_stiffness_matrix(mass_matrix, k):
    stiffenss_matrix = mass_matrix 
    return stiffness_matrix

def construct_matrices(vertices, mass, k):
    mm = construct_mass_matrix(vertices)
    sm = construct_stiffness_matrix(mm, k)
    mm = mm * mass
    return (mm, sm)

def get_eigen_vals(mass_matrix, stiffness_matrix):
    return numpy.linalg.eigvals(mass_matrix)  

def get_freqs(eigen_vals):
    return 

def get_damps(freqs, internal_friction):
    return

def get_amps(freqs, eigen_vals):
    return

def write_file(filename, freqs, damps, amps):
    fileout = open("../output/"+filename+".ro", "w")
    fileout.write("nactive_freq:\n")
    fileout.write(str(len(freqs))+"\n")
    fileout.write("frequencies:\n")
    for freq in freqs:
	fileout.write(str(freq)+"\n")
    for damp in damps:
	fileout.write(str(damp)+"\n")
    for amp in amps:
	fileout.write(str(amp)+"\n")
    fileout.write("END\n")

def main():    
    internal_friction = 1
    k = 2000
    mass = 1
    vertices = import_mesh("test.obj") 
    m, k = construct_matrices(vertices, mass, k)
    print m 
    eigen_vals = get_eigen_vals(m, k) 
    print eigen_vals
    #freqs = get_freqs(eigen_vals)
    #damps = get_damps(freqs, internal_friction)
    #amps = get_amps(freqs, eigen_vals)
    #write_file("test", freqs, damps, amps)

#main()
