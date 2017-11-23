import os                                                       
import sys                                                              
for i in range(0, 10):
  os.system('gcloud compute instances create my-asia-vm{i} --zone asia-southeast1-a --preemptible --image squid-image'.format(i=i)) 
