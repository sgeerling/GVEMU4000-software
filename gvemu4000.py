# -*- coding: utf-8 -*-
"""
@author: gopimn
"""

from models.device import device as dev

# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
# check if this is spending CPU
params = {}
params['period_gtfri'] = 0.4
params['period_gtinf'] = 0.3

def main():
  gvemu = dev(params)
  gvemu.start()
  print("threads started\n") 
  
if __name__== "__main__":
  main()
