from numpy import * #FIXME:Normaliser les imports de numpy et scipy
import scipy
from GradientDescent import *


## function being optimized : x->x^2
class TestGD( GradientDescent ):
    def alpha( self, t ):
        return 1./(10*t+1)
    theta_0 = array( [1067] )
    Threshold = 0.001
    T = 100
    sign = -1

def grad( theta ):
    return 2*theta[0]

x = 0
print "Vanilla :"
test = TestGD()
x = test.run( grad )
print x    

print "Normalise :"
test = TestGD()
#test.T = -1
x = test.run( grad,b_norm=True )
print x    

print "Projete et normalise"
test = TestGD()
#test.T = -1
def proj( x ):
    if x == 0:
        return array([1.])
    return x / scipy.linalg.norm( x )
x = test.run( grad, f_proj=proj, b_norm=True )
print x    

print "Vanilla projete"
test = TestGD()
#test.T = -1
x = test.run( grad, f_proj=proj )
print x    

## function being optimized : x->||x||_2
class TestGD2( GradientDescent ):
    def alpha( self, t ):
        return 1./(t+1)
    theta_0 = array( [1067,455,-660] )
    Threshold = 0.001
    T = 100
    sign = -1

def grad( theta ):
    return 2*theta

print "Vanilla :"
test = TestGD2()
x = test.run( grad )
print x    

print "Normalise :"
test = TestGD2()
#test.T = -1
x = test.run( grad,b_norm=True )
print x    

print "Projete et normalise"
test = TestGD2()
#test.T = -1
def proj( x ):
    if scipy.linalg.norm( x ) == 0:
        return array([1.,0.,0.])
    return x / scipy.linalg.norm( x )
x = test.run( grad, f_proj=proj, b_norm=True )
print x

print "Vanilla projete"
test = TestGD2()
#test.T = -1
x = test.run( grad, f_proj=proj )
print x    


print "Projete et normalise (2eme type)"
test = TestGD2()
#test.T = -1
def proj2( x ):
    if scipy.linalg.norm( x ) == 0:
        return array([1.,0.,0.])
    x[0] = 1.
    return x
x = test.run( grad, f_proj=proj2, b_norm=True )
print x

print "Vanilla projete (2eme type)"
test = TestGD2()
#test.T = -1
x = test.run( grad, f_proj=proj2 )
print x    


