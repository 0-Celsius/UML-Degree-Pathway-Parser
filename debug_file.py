import timeit
import os 
DEBUG_MODE = True
DEBUG_LOG_TEXT_FILE_LOCATION = os.path.join(os.getcwd() , "debug_log.txt")


def debug_print(*args, **kwargs):
    if DEBUG_MODE == 'True':
        with open(f"{DEBUG_LOG_TEXT_FILE_LOCATION}", "a") as w_file:
            try:
                msg = ' '.join(map(str, args))
                w_file.write(msg)
                w_file.write('\n')
                print(msg, **kwargs)
            except Exception as e:
                w_file.write(f"!!!! \t\t exception: {e}")
                print(f"exception: {e}")
                return

        

def time_taken(function):
    print(f'#time_taken::: Testing function: \"{function.func_name}\"')
    t_t = timeit.timeit(function, number=1)
    print(f'#time_taken::: Time taken to run \"{function.func_name}\": {t_t:.3f} seconds')
    
    
if __name__ == '__main__':
    print("running Debug_file !")