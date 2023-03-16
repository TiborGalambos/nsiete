import numpy as np
import plotly.express as px

def dataset_Flower(m=10, noise=0.0):
    # Inicializujeme matice
    X = np.zeros((m, 2), dtype='float')
    Y = np.zeros((m, 1), dtype='float')

    a = 1.0
    pi = 3.141592654
    M = int(m/2)

    for j in range(2):
        ix = range(M*j, M*(j+1))
        t = np.linspace(j*pi, (j+1)*pi, M) + np.random.randn(M)*noise
        r = a*np.sin(4*t) + np.random.randn(M)*noise
        X[ix] = np.c_[r*np.sin(t), r*np.cos(t)]
        Y[ix] = j

    return X, Y

def MakeBatches(dataset, batchSize, shuffle:bool):
    # Set obsahuje 2 mnoziny - X, Y
    X, Y = dataset

    # Zistime celkovy pocet vzoriek
    m, nx = X.shape
    _, ny = Y.shape

    if shuffle:
        idx = np.arange(len(X))
        np.random.shuffle(idx)
        X = X[idx]
        Y = Y[idx]

    # Vysledny zoznam
    result = []

    # Ak je batchSize = 0, berieme celu mnozinu
    if (batchSize <= 0):
        batchSize = m

    # Celkovy pocet davok sa zaokruhluje nahor
    steps = int(np.ceil(m / batchSize))
    for i in range(steps):
        # Spocitame hranice rezu
        mStart = i * batchSize
        mEnd = min(mStart + batchSize, m)

        # Vyberame data pre aktualny rez - chceme dodrzat rank
        minibatchX = X[mStart:mEnd, :]
        minibatchY = Y[mStart:mEnd, :]

        assert (len(minibatchX.shape) == 2)
        assert (len(minibatchY.shape) == 2)

        # Pridame novu dvojicu do vysledneho zoznamu
        result.append((np.expand_dims(minibatchX, axis=-1), np.expand_dims(minibatchY, axis=-1)))

    return result


def draw_dataset(x, y):
    fig = px.scatter(x=x[0], y=x[1], color=y[0], width=700, height=700)
    fig.show()


if __name__ == '__main__':
    x,y = dataset_Flower(128)
    draw_dataset(x.T, y.T)
    dataset = MakeBatches((x,y),32)
    for mini_batch in dataset:
        print(mini_batch[0].shape)
