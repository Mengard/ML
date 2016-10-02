import numpy as np
import matplotlib.pyplot as plt

r = np.loadtxt("save.txt")

idx = np.where(r == -1)[0] # when we died
diff = idx[1:] - idx[:-1]  # time before dying
avgd = [np.average(diff[i:i+100]) for i in range(len(diff)-100)]
plt.subplot(311)
plt.plot(idx, range(len(idx)))
plt.title("Death over time")
plt.xlabel("time")
plt.ylabel("cumulated death")

plt.subplot(312)
plt.plot(range(len(diff)), diff)
plt.title("Death frequency")
plt.xlabel("death number")
plt.ylabel("time alive")

plt.subplot(313)
plt.plot(range(len(avgd)), avgd)
plt.title("Averaged death frequency")
plt.xlabel("death number")
plt.ylabel("time alive")

plt.show()