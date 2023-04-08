import logging

def check_time_correctness(time : list) -> bool:
    try: 
        for i in range(len(time)):
            if (i / 2) == 0:
                if int(time[i]) >= 0 and int(time[i])<= 23:
                    continue
                else:
                    return False
            else:
                if int(time[i]) >= 0 and int(time[i]) <= 59:
                    continue
                else:
                    return False
        return True
    except ValueError: 
        return False
    except Exception as e:
        logging.error(f"Error in check_time_correctness: {e}")
        return False
    
def separate_times(time : list) -> list:
    times = []
    if len(time) >= 2:
        time1 = time[0] + ':' + time[1]
        times.append(time1)
        if len(time) >= 4:
            time2 = time[2] + ':' + time[3]
            times.append(time2)
        if len(time) == 6: 
            time3 = time[4] + ':' + time[5]
            times.append(time3)
    return times
