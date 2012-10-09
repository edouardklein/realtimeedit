from numpy import * #FIXME:Normaliser les imports de numpy et scipy
import scipy.linalg
import os
import sys
class GradientDescent:
   def alpha( self, t ):
      raise NotImplementedError, "Cannot call abstract method"
   theta_0=array([])
   Threshold = 'a'
   T = -1
   sign = 0
   def run( self, f_grad, f_proj=None, b_norm=False ): #grad is a function of theta
      theta = self.theta_0.copy()
      best_theta = theta.copy()
      best_norm = 1000000.#FIXME:Il faudrait mettre plus l'infini
      best_iter = 0
      t=-1
      while True:#Do...while loop
         t += 1
         DeltaTheta = self.sign * self.alpha( t ) * f_grad( theta )
         norm = scipy.linalg.norm( DeltaTheta )
         if b_norm and  norm > 0.:
             DeltaTheta /= scipy.linalg.norm( DeltaTheta )
         theta = theta + DeltaTheta
         if f_proj:
             theta = f_proj( theta )
         sys.stderr.write("Norme du gradient : "+str(norm)+", pas : "+str(self.alpha(t))+", iteration : "+str(t)+"\n")
         if norm < best_norm:
             best_norm = norm
             best_theta = theta.copy()
             best_iter = t
         if norm < self.Threshold or (self.T != -1 and t >= self.T):
             break
      sys.stdout.write("Gradient de norme : "+str(best_norm)+", a l'iteration : "+str(best_iter)+"\n")
      return best_theta
