import math
import datetime
import random
import matplotlib.pyplot as plt

HEALTHY = 0
CONTAGIOUS = 1
IMMUNE = 2
color = ['b.','r.','g.']

class Person():
   def __init__(self):
      # Public
      self.age = 30
      self.state = HEALTHY
      self.T_incubation = 5 #days
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
         self.person.append(Person())
   
   def run(self):
      for i in range(self.T_duration):
         for person in self.person:
            if hasattr(person, 'previous'):
               person.previous.remove()
            person.move()
            person.previous, = plt.plot(person.x,person.y,color[person.state])
         
         plt.pause(0.001)
      plt.show()
            
if __name__ == '__main__':
   pandemic = Pandemic()
   pandemic.run()
   