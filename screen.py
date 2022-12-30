class Screen:

    def start_screen( display, display_name ):

        # clear screen
        display.fill(1)
        display.fill(0)

        display.text(display_name, 0, 0, 1)
        display.text('Hello :)', 0, 20, 1)
        display.text('Start...', 0, 40, 1)

        display.show()

    def clear_screen( display, display_name ):

        # clear screen
        display.fill(1)
        display.fill(0)

        display.text(display_name, 0, 0, 1)

        display.show()

    def print_screen_dht11( display, temp, humidity, ip, datetime ):
        display.text('T:{}C'.format(temp), 0, 10, 1)
        display.text('H:{:.0f}%'.format(humidity), 0, 20, 1)
        display.text('ip:{}'.format(ip), 0, 30, 1)
        display.text('i:{}'.format(datetime), 0, 40, 1)
        display.show()

    def print_screen_error( display, error ):
        display.text( error, 0, 40, 1)
        display.show()

    def show_ip(display, ip):
        display.text('ip:{}'.format(ip), 0, 30, 1)
        display.show()
