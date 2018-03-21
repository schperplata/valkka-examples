import time
from valkka.api2.threads import LiveThread, OpenGLThread
from valkka.api2.chains import BasicFilterchain

livethread=LiveThread( # starts live stream services (using live555)
  name   ="live_thread",
  verbose=False,
  affinity=-1
)

openglthread=OpenGLThread(
  name    ="glthread",
  n720p   =20,   # reserve stacks of YUV video frames for various resolutions
  n1080p  =20,
  n1440p  =0,
  n4K     =0,
  verbose =False,
  msbuftime=100,
  affinity=-1
)

chain=BasicFilterchain( # decoding and branching the stream happens here
  livethread  =livethread, 
  openglthread=openglthread,
  address     ="rtsp://admin:nordic12345@192.168.1.41",
  slot        =1,
  affinity    =-1,
  verbose     =False,
  msreconnect =10000 # if no frames in ten seconds, try to reconnect
)

# create a window
win_id =openglthread.createWindow()

# create a stream-to-window mapping
token  =openglthread.connect(slot=1,window_id=win_id) # present frames with slot number 1 at window win_id

# start decoding
chain.decodingOn()
# stream for 20 secs
time.sleep(20)

chain.decodingOff()

print("bye")
