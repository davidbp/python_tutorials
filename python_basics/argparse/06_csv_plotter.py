import pandas as pd
import argparse

# python -c "import pandas as pd; aux=pd.read_csv('input_csv.csv'); print(aux)"


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def build_argument_parser():
    parser = argparse.ArgumentParser(description="Pretty printer csv")
    parser.add_argument('-f', '--file', type=str, metavar='', required=True, help='Input csv file to be printed')
    parser.add_argument('-H', '--head', type=str2bool, metavar='', required=False, help='Wheather to print only the head of the csv or not (default=False)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = build_argument_parser()
    df = pd.read_csv(args.file)

    if args.head == True:
        print("\n")
        print(df.head())
        print("\n")
    else:
        print("\n")
        print(df)
        print("\n")
