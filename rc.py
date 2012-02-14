#!/usr/bin/env python2

from __future__ import division
from datetime import datetime

from awrap import TextWidget, GraphWidget, Timer

# Retrieve all available widgets defined in rc.lua

battery_widget = TextWidget("battery_widget")
cpu_widget = GraphWidget("cpu_widget")
mem_widget = GraphWidget("mem_widget")
date_widget = TextWidget("date_widget")

# # # BATTERY CHARGE FUNCTION # # #

def battery():
    """Display power manager information"""
    battery_widget.text(" -- BATTERY -- ")

# # # CPU AND MEMORY LOAD FUNCTION # # #

prev_work_jiffies = prev_total_jiffies = 0

def cpu_mem_usage():
    """
    Display current CPUs and Memory usage
    """

    # CPU LOAD
    try:
        # Retrieve previous saved cpu jiffies    
        global prev_work_jiffies, prev_total_jiffies

        # Retrive main information about CPU load
        # For a reference about the topic, see:
        # 1. http://stackoverflow.com/questions/3017162
        #    /how-to-get-total-cpu-usage-in-linux-c
        # 2. http://www.linuxhowtos.org/System/procstat.htm

        with open('/proc/stat') as f:
            cpu_jiffies = map(int, f.readline().split(' ')[2:9])

            # Calculate the current number of jiffies
            curr_work_jiffies = sum(cpu_jiffies[0:3])
            curr_total_jiffies = sum(cpu_jiffies)
        
            # Check for previous jiffies
            if prev_work_jiffies != 0:
                # Calculate the percentage of usage
                cpu_usage = ( curr_work_jiffies - prev_work_jiffies ) / \
                            ( curr_total_jiffies - prev_total_jiffies )
                # Display percentage
                cpu_widget.add_value(cpu_usage)

            # Update previous jiffies for next call
            prev_work_jiffies = curr_work_jiffies
            prev_total_jiffies = curr_total_jiffies
    except:
        pass

    # MEMORY USAGE
    try:
        # Retrieve actual memory usage
        # see: /proc/meminfo

        with open('/proc/meminfo') as f:
            i = 0
            total_memory = used_memory = 0

            for line in f:
                # Read the int value from the line
                int_value = int(line.split(":")[1][:-4].lstrip())

                if i == 0:
                    # Update total_memory
                    total_memory = used_memory = int_value
                elif i < 4:
                    # Read only first four lines!!!
                    # Subtract MemFree, Buffers and Cached from used_memory

                    used_memory -= int_value
                else:
                    # Display memory usage and break loop!
                    mem_widget.add_value(used_memory / total_memory)
                    break
                    
                # Next line
                i += 1
    except Exception, e:
        print e

# # # DATE TIME FUNCTION # # #

def date():
    """
    Display current datetime information
    """
    
    date_widget.text(datetime.today().strftime("%a %b %d, %H:%M "))

# # # NETWORK LOAD FUNCTION # # #

# TODO

# # # FILESYSTEM USAGE # # #

# TODO

# # # MAIN HERE # # #

if __name__ == "__main__":
    
    # Define timer
    battery_timer = Timer(30)
    cpu_mem_timer = Timer(1)
    date_timer = Timer(60)
    
    # Attach functions to each timer
    battery_timer.add_signal("battery", battery)
    cpu_mem_timer.add_signal("cpu_mem", cpu_mem_usage)
    date_timer.add_signal("date", date)

    # Starts all the timers
    battery_timer.start()
    cpu_mem_timer.start()
    date_timer.start()
