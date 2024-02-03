import matplotlib.pyplot as plt


y=[20,90,50,70]
x=["shreya","vrushika","mahek","prerna"]
plt.ylabel("Percentages")
plt.xlabel("Student names")
c=["r","g","b","y"]
plt.bar(x,y,color=c,edgecolor="b")
plt.show()