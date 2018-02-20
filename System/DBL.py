import argparse

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Write weather data")
    parser.add_argument('-l', help='location to write final data', type=str, default='')
    parser.add_argument('-m', help='mode (read serial/aggregate values)', type=str, default='')
    args = parser.parse_args()
    
    if 'read' in args.m or 'ser' in args.m:
        text = 'Reading serial input from: {0} - at {1}'
        print(text)
    elif 'agg' in args.m:
        text = 'aggregating values in {0}, last run: {1}'
        print(text)
    else:
        print('not known mode, please specify...')
