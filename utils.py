import serial
ser = serial.Serial("/dev/ttyUSB0")

def read_button(fd):
  ioctl(fd, RD_PBUTTONS)
  value = os.read(fd, 4); # read 4 bytes and store in red var
  if(debug):
  	print("red 0x%X"%int.from_bytes(value, 'little'))
  value = int.from_bytes(value, 'little')
  return value
  

def first_b_pres(fd):
  value = 0
  while(value == 0):
    val_read = read_button(fd)
    if(val_read == 0xE):      
      value = 4
    elif(val_read == 0xD):
      value = 3
    elif(val_read == 0xB):
      value = 2
    elif(val_read == 0x7):
      value = 1
  
  return value

def read_switch(fd):
  ioctl(fd, RD_SWITCHES)
  value = os.read(fd, 4); # read 4 bytes and store in red var
  if(debug):
  	print("red 0x%X"%int.from_bytes(value, 'little'))
  value = int.from_bytes(value, 'little')
  return value
  

def check_swirch(fd):
  val = 0
  val_read = read_switch(fd)
  if (val_read == 0x1):
  	val = 1
  return val

def set_green_leds(fd, data):
  ioctl(fd, WR_GREEN_LEDS)
  retval = os.write(fd, data.to_bytes(4, 'little'))

def set_red_leds(fd, data):
  ioctl(fd, WR_RED_LEDS)
  retval = os.write(fd, data.to_bytes(4, 'little'))

def to_seg(num):
  if(num == 0):
    return 0xC0
  elif(num == 1):
    return 0xF9
  elif(num == 2):
    return 0xA4
  elif(num == 3):
    return 0xB0
  elif(num == 4):
    return 0x99
  elif(num == 5):
    return 0x92
  elif(num == 6):
    return 0x82
  elif(num == 7):
    return 0xF8
  elif(num == 8):
    return 0x80
  elif(num == 9):
    return 0x90
  else:
    print("Error: invalid digit")
    return -1


def ret_dig(num, pos):
  return num // 10**pos % 10


def send_r_disp(fd, data):
  ioctl(fd, WR_R_DISPLAY)
  retval = os.write(fd, data.to_bytes(4, 'little'))
  print("wrote %d bytes"%retval)
  
  
def r_disp(num, fd):
  if(num > 9999 or num < 0 or str(num).isdigit() == 0):
    print("Error: this number cannot be displayed")
    return -1
  else:
    data = 0
    digit = [0 for i in range(4)] 
    for i in range (4):
      digit[i] = to_seg(ret_dig(num, i))
      print("0x%X" %digit[i])
      if(digit[i] != -1):
        data += digit[i] * 256**i

      last_r_disp_data[i] = digit[i]
    
    print("0x%X" %data)
    send_r_disp(fd, data)
    
    return 0


def r_disp_digit(num, pos, fd):
  if(num > 9999 or num < 0 or str(num).isdigit() == 0):
    print("Error: this number cannot be displayed")
    return -1
  else:
    data = 0
    digit = last_r_disp_data.copy()
    digit[pos] = to_seg(ret_dig(num, 0))
    for i in range (4):
      print("0x%X" %digit[i])
      if(digit[i] != -1):
        data += digit[i] * 256**i

    last_r_disp_data[pos] = digit[pos]
    
    print("0x%X" %data)
    send_r_disp(fd, data)
    return 0

def ret_pos():
    #pygame.time.wait(500)	
    res = ser.readline()
    
    value = float(res.decode())
    print(value, end="\n")
    if(value > 0 and value < 15):
        count = 1
    elif(value >= 15 and value < 30):
        count = 2
    elif(value >= 30 and value < 45):
        count = 3
    elif(value >= 45 and value < 60):
        count = 4
    else: 	
        count = 0
	
    return count