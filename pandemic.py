import math
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

HEALTHY = 0
CONTAGIOUS = 1
IMMUNE = 2
color = ['b.','r.','g.']

class Person():
   def __init__(self,i):
      # Public
      self.index = i
      self.age = 30
      self.state = HEALTHY
      self.T_incubation = 10 #days
      self.T0 = 0 # infection day
      self.x = random.random()
      self.y = random.random()
      
      # Private 
      self._vx = 0.1*(random.random()-0.5)
      self._vy = 0.1*(random.random()-0.5)
      
   def move(self):
      self.x = self.x + self._vx*random.random()
      self.y = self.y + self._vy*random.random()
      if self.x > 1 or self.x < 0:
         self._vx = -self._vx
      if self.y > 1 or self.y < 0:
         self._vy = -self._vy
      self.x = max(min(self.x, 1),0)
      self.y = max(min(self.y, 1),0)

   def check_immunity(self, day):
      if (self.state == CONTAGIOUS) and (day > (self.T0 + self.T_incubation)):
         self.state = IMMUNE

      
class DistanceMatrix():
   def __init__(self,n):
      self._n = n
      self.vx = np.zeros((n))
      self.vy = np.zeros((n))
   
   def update(self,i,x,y):
      self.vx[i] = x
      self.vy[i] = y
      
   def get_hits(self):
      distance  = np.zeros((self._n,self._n))
      for i in range(self._n):
         for j in range(self._n):
            distance[i,j] = math.sqrt((self.vx[i] - self.vx[j])**2 + (self.vy[i] - self.vy[j])**2)
      a = []
      for i in range(self._n):
         for j in range(self._n):
            if (distance[i,j] < 0.08) and (i != j):
               a.append([i,j])
      return(a)         
      
class ContactMatrix():
   def __init__(self,n):
      self.n = n
      self.distance_matrix = np.zeros((n,n))
      self.contact_matrix = np.zeros((n,n))
      
   def update(self,i,x,y):
      pass
      # self.distance_matrix =  
      
class Pandemic():
   def __init__(self):
      self.n = 100          # persons
      self.T_duration = 100 # days
      self.person = []
      for i in range(self.n):
         self.person.append(Person(i))
      self.person[0].state = CONTAGIOUS
   
   def run(self):
      d = DistanceMatrix(self.n)
      for day in range(self.T_duration):
         # Calculate
         for person in self.person:
            person.move()
            person.check_immunity(day)
            d.update(person.index,person.x,person.y)
         hits = d.get_hits()
         for i,j in hits:
            if (self.person[i].state == HEALTHY) and (self.person[j].state == CONTAGIOUS):
               self.person[i].state = CONTAGIOUS
               self.person[i].T0 = day
            if (self.person[j].state == HEALTHY) and (self.person[i].state == CONTAGIOUS):
               self.person[j].state = CONTAGIOUS
               self.person[j].T0 = day
         # Plot
         for person in self.person:
            if hasattr(person, 'previous'):
               person.previous.remove()
            person.previous, = plt.plot(person.x,person.y,color[person.state])
         plt.pause(0.001)
      plt.show()
            
if __name__ == '__main__':
   pandemic = Pandemic()
   pandemic.run()
   