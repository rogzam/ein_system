import argparse

parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()

if args.a == 'magic.name':
        
    print ('You nailed it!')


