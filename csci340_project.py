# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 17:05:05 2018

@author: Abderrahman Dandoune
"""

# cmd used: python3 csci340_project.py

class Ram:
    def __init__(obj, size):
        obj.size = size

class Disk:
    def __init__(obj, num):
        obj.num = num

class Process_Cycle:
    def __init__(obj, ram_size, num_hard_disk):
        obj.ram_size = ram_size
        obj.num_hard_disk = num_hard_disk
        obj.temp_pid = 0
        obj.pid = 0
        obj.total_mem_used = 0
        obj.process_table = []
        obj.ready_queue = []
        obj.io_queues = []
        obj.free_memory = [ {'start': 0, 'end':ram_size - 1} ]
        i = 0
        while i < obj.num_hard_disk:
            obj.io_queues.append([])
            i += 1 
        
    def get_memory_address(obj, num_addr): 
        mem_size_list = []
        s = -1
        e = -1
        i = 0
        while i<len(obj.free_memory):
            start = obj.free_memory[i]['start']
            end = obj.free_memory[i]['end']
            size = end-start+1
            if( size >= num_addr ):
                mem_size_list.append( {'index': i, 'size':size} )
            i += 1
            
        if( len(mem_size_list) > 0 ):
            mem_size_list.sort(key = lambda x: x['size'])
            size = mem_size_list[0]['size']
            index = mem_size_list[0]['index']
            diff = size - num_addr
            if( diff == 0 ):
                s = obj.free_memory[index]['start']
                e = obj.free_memory[index]['end']
                del obj.free_memory[index]
                
            elif( diff > 0 ):
                s = obj.free_memory[index]['start']
                e = obj.free_memory[index]['end']-diff
                obj.free_memory[index]['start'] = e+1
        
        return s, e
    
    
    def free_memory_address(obj, process):
        s = process['memory_range_s']
        e = process['memory_range_e']
        freed = False
        i = 0
        while i < len(obj.free_memory):
            if( obj.free_memory[i]['end'] == s-1):
                obj.free_memory[i]['end'] = e
                if (i+1 < len(obj.free_memory)):
                    if( obj.free_memory[i]['end'] == obj.free_memory[i+1]['start']-1 ):
                        obj.free_memory[i+1]['start'] = obj.free_memory[i]['start']
                        del obj.free_memory[i]
                freed = True
                break
                
            elif( obj.free_memory[i]['start'] == e+1 ):
                obj.free_memory[i]['start'] = s
                freed = True
                break
            
            i += 1
        if(not freed):
            obj.free_memory.append( {'start':s, 'end':e} )
            obj.free_memory.sort(key = lambda x: x['start'])
        #print(obj.free_memory)
    
    def add_rq(obj, pid, priority):
        process = {'PID':pid,'priority':priority,'file_name':''}
        obj.ready_queue.append(process)
        obj.ready_queue.sort(key = lambda x: x['priority'], reverse=True)
    
    
    def move_rq_io(obj, hard_disk, file_name):
        try:
            obj.temp_pid = obj.ready_queue[0]['PID']
            obj.ready_queue[0]['file_name'] = file_name
            obj.io_queues[hard_disk].append(obj.ready_queue[0])
            del obj.ready_queue[0]
            obj.ready_queue.sort(key = lambda x: x['priority'], reverse=True)
            print('Process of PID:',obj.temp_pid,'has been moved from CPU to I/O queue of Hard Disk #', hard_disk,'\n')
        except IndexError:
            print("\nThe CPU & Ready Queue have no processes.")
            pass
        except ValueError:
            print("\nThere is an invalid value.")
            pass
        except:
            print("\nUnexpected error")
            raise
            pass
        
        try:
            i = 0
            while i < len(obj.process_table):
                if( obj.process_table[i]['PID'] == obj.temp_pid):
                    obj.process_table[i]['file_name'] == file_name
                    obj.process_table[i]['hard_disk'] == hard_disk
                    break
                i += 1
        except IndexError:
            print("\nThe Process Table has no processes.")
        except ValueError:
            print("\nThere is an invalid value.")
        except:
            print("\nUnexpected error")
            raise
    
    
    def move_io_rq(obj, hard_disk):
        try:
            obj.temp_pid = obj.io_queues[hard_disk][0]['PID']
            obj.io_queues[hard_disk][0]['file_name'] = ''
            obj.ready_queue.append(obj.io_queues[hard_disk][0])
            del obj.io_queues[hard_disk][0]
            obj.ready_queue.sort(key = lambda x: x['priority'], reverse=True)
            print('Process of PID:',obj.temp_pid,'has been moved from Hard Disk #', hard_disk,'to Ready Queue.\n')
        except IndexError:
            print("\nThe Hard Drive has no processes.")
            pass
        except ValueError:
            print("\nThere is an invalid value.")
            pass
        except:
            print("\nUnexpected error")
            raise
            pass
        
        try:
            i = 0
            while i < len(obj.process_table):
                if( obj.process_table[i]['PID'] == obj.temp_pid):
                    obj.process_table[i]['file_name'] == ''
                    obj.process_table[i]['hard_disk'] == -1
                    break
                i += 1
        except IndexError:
            print("\nThe Process Table has no processes.")
        except ValueError:
            print("\nThere is an invalid value.")
        except:
            print("\nUnexpected error")
            raise
    
    def remove_rq(obj, pid_d):
        try:
            i = 0
            while i < len(obj.ready_queue):
                if( obj.ready_queue[i]['PID'] == pid_d):
                    del obj.ready_queue[i]
                    print('Process of PID:',pid_d,'has been terminated')
                    break
                i += 1
        except IndexError:
            print("\nThe CPU & Ready Queue has no processes.")
        except ValueError:
            print("\nThere is an invalid value.")
        except:
            print("\nUnexpected error")
            raise
        
    
    def create_process(obj, priority, memory_size):
        try:
            obj.pid += 1
            hd = -1
            file_name = ''
            obj.total_mem_used += memory_size
            start = 0
            end = 0
            # check memory range
            start, end = obj.get_memory_address(memory_size)
            if( start != -1 and end != -1 ):
                pcb = {'PID':obj.pid,'priority':priority,'memory_size':memory_size,'hard_disk':hd,'file_name':file_name,'memory_range_s':start,'memory_range_e':end}
                obj.process_table.append(pcb)
                obj.add_rq(obj.pid, priority)
            else:
                print('\nThere is not enough space in memory.')
        except IndexError:
            print("\nThe Process Table has Index Error.")
        except ValueError:
            print("\nThere is an invalid value.")
        except:
            print("\nUnexpected error")
            raise 
    
    
    def terminate_CPU_process(obj):
        try:
            pid_dp = obj.ready_queue[0]['PID']
            i = 0
            while i < len(obj.process_table):
                if( obj.process_table[i]['PID'] == pid_dp):
                    obj.free_memory_address(obj.process_table[i])
                    obj.total_mem_used -= obj.process_table[i]['memory_size']
                    del obj.process_table[i]
                    break
                i += 1
                
            obj.remove_rq(pid_dp)
        except IndexError:
            print("\nThe CPU has no processes.")
        except ValueError:
            print("\nThere is an invalid value.")
        except:
            print("\nUnexpected error")
            raise        
        
    
    #################################################
    
    def show_current_process_ready_queue(obj):
        print('\n*************CPU & Ready Queue Processes***********')
        i = 0
        while i < len(obj.ready_queue):
            if (i == 0):
                print('***************CPU Process*************')
                print('PID:', obj.ready_queue[i]['PID'])
                print('Priority:', obj.ready_queue[i]['priority'])
                print('***************Ready Queue*************') 
    
            else:
                print('------Ready Queue Process',i,'------')
                print('PID:', obj.ready_queue[i]['PID'])
                print('Priority:', obj.ready_queue[i]['priority'])
            i += 1
        print('***************Ready Queue End*************')
        print('*************CPU & Ready Queue Processes End***********\n')
        
    
    def show_processes_on_hd_waiting_processes(obj): 
        j = 0
        while j < obj.num_hard_disk:
            print('\n***************I/O Queues for HD',j,'*************')
            i = 0
            while i <  len(obj.io_queues[j]):
                if (i == 0):
                    print('***************Hard Drive',j,'*************')
                    print('PID:', obj.io_queues[j][i]['PID'])
                    print('File:', obj.io_queues[j][i]['file_name'])
                    print('**************End Hard Drive',j,'*************')
                    
                else:
                    print('------I/O Queue',j,'Process',i,'------')
                    print('PID:', obj.io_queues[j][i]['PID'])
                    print('File:', obj.io_queues[j][i]['file_name'])
                i += 1
            print('*************End of I/O Queues for HD',j,'***********\n')
            j += 1
        
    
    def show_memory_state(obj): 
        
        print('\n*********Memory State*************')
        i = 0
        while i < len(obj.process_table):
            print('***************PCB of Index',i,'*************')
            print('PID:', obj.process_table[i]['PID'])
            print('Priority:', obj.process_table[i]['priority'])
            print('Memory Size:', obj.process_table[i]['memory_size'],'Bytes')
            print('Range Memory Addresses:', obj.process_table[i]['memory_range_s'],'-', obj.process_table[i]['memory_range_e'])
            i += 1
        print('*********End of Memory State*************')
        print('Total Memory Used:',obj.total_mem_used,'Bytes /',obj.ram_size,'Bytes\n')
        print('Free address holes range: ',obj.free_memory,'\n')
        
#################################################################

def simulation(pc):
    while True:
        arg = input("").split()
        # Check command values and run appropriate functions
        if(len(arg) == 0):
            continue
        elif(arg[0] == 'q'):
            break
        elif(arg[0] == 'A'):
            exp = False
            try:
                if( len(arg) >= 3 ):
                    arg[1] = int(arg[1])
                    arg[2] = int(arg[2]) 
                else:
                    exp = True
                    print("\nThis command takes 3 arguments.")
            
            except IndexError:
                exp = True
                print("\nThis command takes 3 arguments.")
            except ValueError:
                exp = True
                print("\nThere is an invalid value in arg 2 or arg 3.")
            except:
                exp = True
                print("\nUnexpected error")
                raise
            
            if(not exp):
                # create function to do work.
                #‘A’ input means that a new process has been created. 
                #This process has a priority priority and requires memory_size bytes of memory.
                if(pc.ram_size > 0 and pc.ram_size <= 4000000000):
                    if( pc.total_mem_used+arg[2] <= pc.ram_size ):
                        if(arg[2]>0):
                            pc.create_process(arg[1], arg[2])
                        else:
                            print('Memory size should be greater than one.')
                    else:
                        print('Memory Size is too big or Memory is Full.')
                else:
                        print('Memory Size between 1 Byte and 4 Billion Bytes.')
                
        elif(arg[0] == 't'):
            # The process that is currently using the CPU terminates. 
            if( len(arg) >= 1 ):
                pc.terminate_CPU_process()
            else:
                exp = True
                print("\nThis command takes 1 argument.")
            
        elif(arg[0] == 'd'):
            exp = False
            try:
                if( len(arg) >= 3 ):
                    arg[1] = int(arg[1])
                else:
                    exp = True
                    print("\nThis command takes 3 arguments.")
                
            except IndexError:
                exp = True
                print("\nThis command takes 3 arguments.")
            except ValueError:
                exp = True
                print("\nThere is an invalid value in arg 2.")
            except:
                exp = True
                print("\nUnexpected error")
                raise
            
            if(not exp):
                if(arg[1]>=0 and arg[1]<pc.num_hard_disk):
                    pc.move_rq_io(arg[1], arg[2])
                else:
                    print('The drive number should be between 0 and', pc.num_hard_disk-1) 
        
        elif(arg[0] == 'D'):
            exp = False
            try:
                if( len(arg) >= 2 ):
                    arg[1] = int(arg[1])
                else:
                    exp = True
                    print("\nThis command takes 2 arguments.")
            
            except IndexError:
                exp = True
                print("\nThis command takes 2 arguments.")
            except ValueError:
                exp = True
                print("\nThere is an invalid value in arg 2.")
            except:
                exp = True
                print("\nUnexpected error")
                raise
            
            if(not exp):
                # create function to do work.
                # The hard disk #number has finished the work for one process.
                if(arg[1]>=0 and arg[1]<pc.num_hard_disk):
                    pc.move_io_rq(arg[1])
                else:
                    print('The drive number should be between 0 and', pc.num_hard_disk-1)        
        
        elif(arg[0] == 'S'):
            if( len(arg) >= 2 ):
                if(arg[1] == 'r'):
                    # create function to do work.
                    # Shows a process currently using the CPU and processes waiting in the ready-queue. 
                    pc.show_current_process_ready_queue()
                    
                elif(arg[1] == 'i'):
                    # create function to do work.
                    # Shows what processes are currently using the hard disks and what processes are waiting to use them. 
                    pc.show_processes_on_hd_waiting_processes()
                    
                elif(arg[1] == 'm'):
                    # create function to do work.
                    # Shows the state of memory.
                    pc.show_memory_state()
                    
                else:
                    print("\nThere is an invalid value in arg 2.")
            else:
                    exp = True
                    print("\nThis command takes 2 arguments.")
        else:
            print('\nInvalid command Entered')

#################################################################   
def main():
    ex = False # ex is to detect exceptions
    while True:
        ex = False
        try:
            ram_size = int(input("How much RAM memory is there on the simulated computer? "))
            if(ram_size>0 and ram_size<=4000000000):
                r = Ram(ram_size)
            else:
                print('Memory Size between 1 Byte and 4 Billion Bytes.')
                ex = True
        except IOError as e:
            ex = True
            errno, strerror = e.args
            print("\nI/O error({0}): {1}".format(errno,strerror))
        except ValueError:
            ex = True
            print("\nNo valid integer in line.")
        except:
            ex = True
            print("\nUnexpected error")
            raise
        
        if(not ex):
            break
            
    while True:
        ex = False
        try:
            num_hard_disk = int(input("How many hard disks does the simulated computer have? "))
            if(num_hard_disk>0):
                d = Disk(num_hard_disk)
            else:
                    print('The drive number should be a positive number grater than 0.')
                    ex = True
        except IOError as e:
            ex = True
            errno, strerror = e.args
            print("\nI/O error({0}): {1}".format(errno,strerror))
        except ValueError:
            ex = True
            print("\nNo valid integer in line.")
        except:
            ex = True
            print("\nUnexpected error")
            raise
            
        if(not ex):
            break
    
    pc = Process_Cycle(r.size, d.num)
    simulation(pc)
    
#################################################################
if __name__ == '__main__':
    main()
#################################################################  