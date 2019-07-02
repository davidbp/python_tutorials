import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_commandline():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('-n', '--name', type=str,   required=True,  help='Person name')
    parser.add_argument('-a',  '--age', type=int,   required=False,  help='Age of the person.')
    parser.add_argument( '-ec', '--ever_convicted',    type=str2bool,  required=False,  help='Boolean stating if the person has been convicted previously.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":  
    exp_args = parse_commandline()
    print("\n\tPerson name:", exp_args.name)
    print("\tAge:", exp_args.age)
    print("\tConvicted:", exp_args.ever_convicted)
