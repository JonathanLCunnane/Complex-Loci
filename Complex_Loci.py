import matplotlib.pyplot as plt

if __name__ == "__main__":
    plt.show()
    x = list(range(-20, 20))
    y = [0.3*num**3-num**2+2*(num)+15 for num in x]
    plt.axis([min(x), max(x), min(y), max(y)])
    plt.plot(x, y)
    plt.show()