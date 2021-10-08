import random
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

class Bird:

	def __init__(self, x_alls, p_alls, t_alls, gen):

		self.x_alls = x_alls
		self.p_alls = p_alls
		self.t_alls = t_alls

		self.del_x = 0.05
		self.del_p = 0.001
		self.del_t = 0.005
		self.K = 3 #minimum beak size

		self.gen = gen #M/F

	def __str__(self):
		return "\n".join([self.gen, str(self.x_alls), str(self.p_alls), str(self.t_alls)])

	def choosiness(self):

		choosy = 0
		for allele in flatten(self.p_alls): choosy += allele*self.del_p
		return np.round(choosy,3)

	def ornament_contrib(self):

		contrib = 0
		for allele in flatten(self.t_alls): contrib += allele*self.del_t
		return np.round(contrib,3)

	def beak_size(self):

		b_len = 0
		for allele in flatten(self.x_alls): b_len += allele*self.del_x
		b_len = self.K + np.round(b_len,3)
		return b_len

	def fitness(self):

		b_len = self.beak_size()

		min_b_size = self.K
		max_b_size = self.K + 2*len(self.x_alls)*self.del_x
		std_dev = 0.5 #can be used to change degree of divergent selection

		min_contri = normal_dist(b_len, min_b_size, std_dev)
		max_contri = normal_dist(b_len, max_b_size, std_dev)
		return min_contri + max_contri

	def not_reach_maturity(self):

		delta = 0.01
		if self.gen == 'F': return delta

		t = self.ornament_contrib()
		return delta + (t/(1-t))

	def mate(self, other, gen):

		if(self.gen == other.gen): print("Mating error: different genders required!")

		new_x_alls = mate_loci(self.x_alls, other.x_alls)
		new_p_alls = mate_loci(self.p_alls, other.p_alls)
		new_t_alls = mate_loci(self.t_alls, other.t_alls)

		#note that gender of the offspring is pre-decided
		#since numbers of each need to be maintained equal in the simulation
		return Bird(new_x_alls, new_p_alls, new_t_alls, gen)

def flatten(l):
    return [item for sublist in l for item in sublist]

def mate_loci(l1, l2):

	n, new_l = len(l1), list()
	if n != len(l2): print("Mating error: no. of loci unequal!")

	for i in range(n):
		alls1, alls2 = l1[i], l2[i]
		chosen_all1 = random.choice(alls1)
		chosen_all2 = random.choice(alls2)
		new_l.append([chosen_all1, chosen_all2])

	return new_l

def normal_dist(x , mean , sd):
	prob_density = np.exp(-0.5*(((x-mean)/sd)**2))/(sd*np.sqrt(2*np.pi))
	return prob_density
