
primes.py - basic code to show prime calculation
primes_timed.py - show how long each call to test n takes, plots blue/red output
primes_processes.py - control nbr processes and size of data blocks that are sent to control execution speed
primes2.py - show that checking for even nbrs helps, steping by 2 is a big improvement, only dereference the external library once, move the sqrt until after the early exit
primes_queue1.py - use a Process and a Queue to send work out
primes_queue2.py - use a map_async (not a map) and a Queue to distribute work

primes_processespernumber1.py - spawn processes per partial range to check for large primes
primes_processespernumber2.py - do same with Manager and Value to communicate state
