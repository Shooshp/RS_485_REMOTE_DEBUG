import Rs_485

Power_Source = Rs_485.Rs485Communication()

counter = 0

while 1:
    command = 'Write counter: %d ' % (counter)
    Power_Source.write_and_read(command.encode())
    counter += 1
