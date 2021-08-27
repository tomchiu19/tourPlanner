import sys
import pandas as pd
import numpy as np

def main(input_file, output_file):
    data = pd.read_json(sys.argv[1], lines=True, compression='gzip')

    #print(data)

    data.to_csv(output_file + '.csv', index=False)


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
