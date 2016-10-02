import random
import numpy as np

class Sarsa:
	def __init__(self, logic, epsilon, alpha, gamma, actions):
		self.Q = {} # state-action dictionary
		self.epsilon = epsilon # used for epsilon-greedy choice
		self.alpha = alpha # used for diminished returns, "the sooner the better"
		self.gamma = gamma # learning rate, importance given to new data
		self.actions = actions # needs to know which actions are possible for greedy action choice

	def Qget(self, state, action):
		return self.Q.get((state, action), 0.0)
		
	def learn(self, old_state, old_action, new_state, new_action, reward):
		self.epsilon = self.epsilon + (1 - self.epsilon) * 0.0001
		# the closer gamma is from 1, the more memories will be overwritten by new data
		# the closer gamme is from 0, the more memories will stay the same as the old data
		forget = (self.gamma) *  self.Qget(old_state, old_action) # how much will be forgotten
		learn  = (self.gamma) * (self.Qget(new_state, new_action) + reward) # how much will be learn
		self.Q[(old_state, old_action)] = self.Qget(old_state, old_action) - forget + self.alpha * learn # update value 
	
	def choose_action(self, state):
		# epsilon-greedy is an algorithm that will chose the best action when random() > epsilon, else random move
		# the closer epsilon is from 1, the more the algorithm will chose the best action
		# the closer epsilon is from 0, the more the algorithm will chose a random action
		if random.random() > self.epsilon: # random action
			action = random.choice(self.actions)
		else : # looking for best action
			Qs = [self.Qget(state, action) for action in self.actions]
			action = self.actions[random.choice(np.where(Qs == np.max(Qs))[0])] # random choice between the best actions if ties occur
		return action