from datetime import datetime
def get_input(filename: str) -> list[str]:
    """Get the input file and return it as a list of strings"""
    with open(filename,'r') as f:
        return f.readlines()
    
def parse_line(line: str) -> list:
    """return a list of information from the line
    [1518-03-19 00:49] falls asleep"""
    time = datetime.strptime(line[1:17],'%Y-%m-%d %H:%M')
    if '#' in line:
        guard_num = line.split('#')[1].split(' ')[0]
        return [time,int(guard_num)]

    if 'asleep' in line:
        print([time,False])
        return [time, False]
    else:
        return [time, True]
    
    
def sleep_tracker(line_list: list, sleep_storage: dict) -> None:
    """Take a parsed line of information and update the dictionary accordingly"""
    pass


if __name__ == '__main__':

    sleep_storage = {}
    

