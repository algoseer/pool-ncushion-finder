from shot import Point, Board
import sys

from pylab import *

def get_all_shots(last_bank = None, n = 3):
  if n == 0:
    return ['']
  all_shots = []

  for bank in 'LURD':
    if bank != last_bank:
      future_shots = get_all_shots(last_bank = bank, n = n-1)
      all_shots.extend([bank+f for f  in future_shots])

  return all_shots
    

if __name__ == '__main__':

    all_shots = get_all_shots()

    #Define a new board
    b = Board()

    b.visualize()
    title('Click red ball positions')
    pts = ginput(2)
    s = Point(pts[0][0], pts[0][1])
    t = Point(pts[1][0], pts[1][1])
    
    close()

    n=1
    figure(figsize=(20,10))

    #Iterate and find shot options
    
    for seq in all_shots:
      print(seq)
      pt = b.findShot(s,t, edges=[s for s in seq])

      if pt:
        subplot(4,4,n)
        b.visualize(s,t, pt)
        title(seq)
        n+=1

    show()
