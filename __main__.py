import display
import signal

def main(): 
    display.run()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, display.sendToSleep)
    signal.signal(signal.SIGTERM, display.sendToSleep)
    main()
