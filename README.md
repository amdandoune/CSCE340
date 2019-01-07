# CSCI-340-Term-Project

This project is a program that simulates some aspects of operating systems. The whole simulation is based on the text inputs that the program receives from user.
The program implements preemptive priority CPU-scheduling. Higher numbers mean higher priority. All I/O-queues are FCFS.
The program simulates contiguous memory management with “best fit” approach.
Each process in the program is represented by its own PCB. We do not want to move around the whole PCBs. All PCBs are stored in a process table and we move around only a small part of its data in the stimulation. 
