import argparse
import numpy as np
import cv2


def calc_error(values, start, end):

    mean = sum(values[start:end+1])/(end - start + 1)

    error = 0
    for value in values[start:end+1]:
        error += np.power((value - mean), 2)

    return error


def main(argv):

    [path,b] = vars(args).values()

    file = open(path, 'r')
    values = []

    while(True):
        value_in_str = file.readline()
        if len(value_in_str) > 0:
            values.append(int(value_in_str))
        else:
            break

    n_values = len(values)

    varianza = np.zeros((b, n_values))
    x = np.zeros((b, n_values))

    for i in range(b):
        for j in range(n_values):
            if i==0:
                start = 0
                end = j
                varianza[i,j] = calc_error( values, start, end)
            else:
                if (j > i):
                    v_min = np.power(10,6)
                    for k in range(j):
                        start_bin_0 = 0
                        end_bin_0 = k
                        start_bin_1 = end_bin_0 + 1
                        end_bin_1 = j
                        v = varianza[i - 1][k] + calc_error( values, start_bin_1, end_bin_1)
                        if ( v < v_min):
                            v_min = v
                            x[i][j] = k

                        varianza[i, j] = v_min


    print('varianza: ' + str(varianza[b-1, n_values-1]))

    for i in range(b-1):
        if i == 0:
            end = n_values+1
            start = int(x[b-1, n_values-1] + 1)

        else:
            end = start - 1
            start = int(x[b-1-i,end] + 1)

        print(values[start:end+1])

    print(values[0:start])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", nargs='?', type=str, default="input.txt")
    parser.add_argument("-b", nargs='?', type=int, default=6)
    args = parser.parse_args()
    main(args)
