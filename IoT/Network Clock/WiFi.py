from micropython import const
from machine import UART, Pin
from utime import sleep_ms, ticks_ms


tx_buffer_size = const(1024)
rx_buffer_size = const(2048)

default_timeout = const(2000)


class wifi():
    
    def __init__(self):
        
        self.uart = UART(0,
                         baudrate = 115200,
                         bits = 8,
                         parity = None,
                         stop = 1,
                         tx = Pin(0),
                         rx = Pin(1),
                         txbuf = tx_buffer_size,
                         rxbuf = rx_buffer_size)
        
        self.rxd = bytearray(rx_buffer_size)
        
        self.STA_mode = const(1)
        self.AP_mode = const(2)
        self.STA_AP_mode = const(3)
        
        self.single_connection = const(0)
        self.multi_connection = const(1)
        
        sleep_ms(100)
        self.test()
        self.get_firmware_version()
        
        
    def send_cmd(self, cmd, ack, print_res = False, timeout = default_timeout):
        self.rxd = []
        
        try:
            self.uart.write(cmd + "\r\n")
        except:
            print("Error sending command!")
            
        t = ticks_ms()
        while ((ticks_ms() - t) < timeout):
            pass
        
        try:
            self.rxd = self.uart.read()            
            
        except:
            print("Error reading response!")
        
        if(self.rxd != None):
            try:
                self.rxd = self.rxd.decode('utf-8')
            
                if(print_res == True):
                    print(self.rxd)
                    
                if(self.rxd.find(ack) >= 0):
                    return True
                
            except:
                return False

        return False
    
    
    def test(self, echo = False):
        self.send_cmd("AT", "OK", echo)
        
        
    def reset(self):
        self.uart.write("AT+RST\r\n", 40000)
        
        
    def get_firmware_version(self, echo = True):
        return self.send_cmd("AT+GMR", "OK", echo)
    
    
    def factory_reset(self):
        return self.send_cmd("AT+RESTORE", "OK", False)
    
    
    def scan(self, echo = True):
        return self.send_cmd("AT+CWLAP", "OK", echo, 6000)
    
    
    def set_mode(self, mode, echo = False):
        return self.send_cmd(("AT+CWMODE_CUR=" + str(mode)), "OK", echo)
    
    
    def get_mode(self, echo = False):
        self.send_cmd("AT+CWMODE?", "OK", echo)
        m = self.rxd.find(":")
        m = int(self.rxd[(m + 1) : (m + 2)])
        return m
    
    
    def set_connections(self, mode, echo = False):        
        return self.send_cmd(("AT+CIPMUX=" + str(mode)), "OK", echo)
    
    
    def get_connections(self, echo = False):
        self.send_cmd("AT+CIPMUX?", "OK", echo)
        m = self.rxd.find(":")
        m = int(self.rxd[(m + 1) : (m + 2)])
        return m
    
    
    def set_SSID_password(self, SSID, PW, echo = False):
        return self.send_cmd("AT+CWJAP_CUR=\""+ SSID +"\",\""+ PW +"\"", "OK", echo, 20000)
    
    
    def get_connection_status(self, echo = False):
        m = -1
        self.send_cmd("AT+CWJAP?", "OK", echo)
        try:
            m = self.rxd.find("No AP")
        except:
            print("Error!")
        if(m < 0):
            return True
        else:
            return False
 
 
    def get_IP(self, echo = False):
        self.send_cmd("AT+CIFSR", "OK", echo)
        ap_ip = self.search(":APIP,", '"')
        ap_mac = self.search(":APMAC,", '"')
        sta_ip = self.search(":STAIP,", '"')
        sta_mac = self.search(":STAMAC,", '"')
        
        return ap_ip, ap_mac, sta_ip, sta_mac
    
    
    def close_connection(self, echo = False):
        return self.send_cmd("AT+CIPCLOSE", "CLOSED", echo)
        
        
    def search(self, s, e):
        m = self.rxd.find(s)
        l = len(s)
        l += 1
        temp = self.rxd[(m + l) : ]
        n = temp.find(e)
        return temp[0 : n]
    
    
    def http_get(self, _url, header = "", http_ver = "1.1", port = 80, timeout = 10000, echo = False):
        m = _url.find("/") 
        url =  _url[0 : m]
        path = _url[m : ]
        raw = "GET "
        raw = raw + path
        raw = raw + " HTTP/" + http_ver + "\r\n"
        raw = raw + "Host: " + url + "\r\n"
        raw = raw + header + "\r\n"
        self.send_cmd("AT+CIPSTART=\"TCP\",\""+ url +"\","+ str(port), "OK", echo, timeout)
        self.send_cmd(("AT+CIPSENDEX=" + str(len(_url) + 25)), ">", echo)
        return self.send_cmd(raw, "CLOSED", (timeout / 2))
    
    
    def http_post(self, _url, header = "", content = '', content_info = "", http_ver = "1.1", port = 80, timeout = 10000, echo = False):
        content_length = len(content)
        m = _url.find("/") 
        url =  _url[0 : m]
        path = _url[m : ]
        raw = "POST "
        raw = raw + path
        raw = raw + " HTTP/" + http_ver + "\r\n"
        raw = raw + "Host: " + url + "\r\n"
        raw = raw + header + "\r\n"
        raw = raw + content_info + str(content_length) + "\r\n"
        raw = raw + "\r\n" + content + "\r\n\r\n"
        str_length = len(raw)
        self.send_cmd("AT+CIPSTART=\"TCP\",\""+ url +"\","+ str(port), "OK", echo, timeout)
        self.send_cmd(("AT+CIPSENDEX=" + str(str_length)), ">", echo)
        self.send_cmd((raw +"\r\n"), "OK", (timeout / 2))
        return self.send_cmd("AT+CIPCLOSE", "CLOSED", (timeout / 2))
        
    
    def requested_data(self, string):
        if(string != None):
            n1 = string.find("{")
            msg_string = string[n1 : ]
            length = len(msg_string)
            msg_string = string[n1 : (n1 + length - 8)]
            
        return msg_string