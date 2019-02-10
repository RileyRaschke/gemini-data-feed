mkfifo /tmp/messages-in
exec 8<>/tmp/messages-in  # hold the fifo open
ncat -l -U /tmp/messages-out -k --send-only < /tmp/messages-in

echo "test" > /tmp/messages-in

# every client connected to /tmp/messages-out will get "test" message

