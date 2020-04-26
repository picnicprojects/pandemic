import math
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt

HEALTHY = 0
INFECTED = 1
CONTAGIOUS = 2
IMMUNE = 3
color = ['b.','m.','r.','g.']

class Person():
   def __init__(self,i):
      # Public
      self.index = i
      self.state = HEALTHY
      self.T_infected = 5 #days
      self.T_contagious = 20 #days
      self.x = random.random()
      self.y = random.random()
      
      # Private 
      self._vx = 0.01*(random.random()-0.5)
      self._vy = 0.01*(random.random()-0.5)
      
   def move(self):
      self.x = self.x + self._vx
      self.y = self.y + self._vy
      if self.x > 1 or self.x < 0:
         self._vx = -self._vx
      if self.y > 1 or self.y < 0:
         self._vy = -self._vy
      self.x = max(min(self.x, 1),0)
      self.y = max(min(self.y, 1),0)

   def change_state(self, day):
      if (self.state == INFECTED)   and (day > (self.T0 + self.T_infected)):
         self.state = CONTAGIOUS
      if (self.state == CONTAGIOUS) and (day > (self.T0 + self.T_infected + self.T_contagious)):
         self.state = IMMUNE
      
class DistanceMatrix():
   def __init__(self,n):
      self._n = n
      self._x = np.zeros((n))
      self._y = np.zeros((n))
   
   def update(self,i,x,y):
      self._x[i] = x
      self._y[i] = y
      
   def get_hits(self):
      distance  = np.zeros((self._n,self._n))
      for i in range(self._n):
         for j in range(self._n):
            distance[i,j] = math.sqrt((self._x[i] - self._x[j])**2 + (self._y[i] - self._y[j])**2)
      a = []
      for i in range(self._n):
         for j in range(self._n):
            if (distance[i,j] < 0.02) and (i != j):
               a.append([i,j])
      return(a)         
      
class Pandemic():
   def __init__(self):
      self.n = 100          # persons
      self.T_duration = 100 # days
      self.person = []
      for i in range(self.n):
         self.person.append(Person(i))
      self.person[0].state = INFECTED
      self.person[0].T0 = 0
   
   def run(self):
      d = DistanceMatrix(self.n)
      steps_per_day = 10
      for step in range(self.T_duration * steps_per_day):
         day = step / steps_per_day;
         # Calculate
         for person in self.person:
            person.move()
            person.change_state(day)
            d.update(person.index,person.x,person.y)
         hits = d.get_hits()
         for i,j in hits:
            if (self.person[i].state == HEALTHY) and (self.person[j].state == CONTAGIOUS):
               self.person[i].state = INFECTED
               self.person[i].T0 = day
            if (self.person[j].state == HEALTHY) and (self.person[i].state == CONTAGIOUS):
               self.person[j].state = INFECTED
               self.person[j].T0 = day

         # Plot
         if day == int(day):
            for person in self.person:
               if hasattr(person, 'previous'):
                  person.previous.remove()
               person.previous, = plt.plot(person.x,person.y,color[person.state])
            plt.title('day %d' % day)
            plt.pause(0.000001)
      plt.show()
            
if __name__ == '__main__':
   pandemic = Pandemic()
   pandemic.run()
   