import swiftclient
import subprocess
import datetime
import os


def push(obj, ipv4):

    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

	# Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)
    container = 'whiskcontainer'
 
    with open(obj, 'rb') as f:
        conn.put_object(container, obj, contents=f, content_length=os.path.getsize(obj))
 
    return ("Ok")


def pull(obj, ipv4):
  
    # Swift identifiant
    auth_url = f'http://{ipv4}:8080/auth/v1.0'
    username = 'test:tester'
    password = 'testing'

    # Connect to Swift
    conn = swiftclient.Connection(
    	authurl=auth_url,
    	user=username,
    	key=password,
    	auth_version='1'
	)
    container = 'whiskcontainer'

    file = conn.get_object(container, obj)
    with open("speech.mp3", 'wb') as f:
        f.write(file[1])
        
    conn.close()
    return ("Ok")


def conversion(file):
    args = ["-i", file, "speech.wav",]
    
    subprocess.run(
            ["ffmpeg", '-y'] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

    return "speech.wav"


def main(args):

    ipv4 = args.get("ipv4", "192.168.1.120")

    pull_begin = datetime.datetime.now()
    pull("speech.mp3", ipv4)
    pull_end = datetime.datetime.now()
    
    process_begin = datetime.datetime.now()
    result = conversion("speech.mp3")
    process_end = datetime.datetime.now()
    
    push_begin = datetime.datetime.now()
    push(result, ipv4)
    push_end = datetime.datetime.now()

    args["body"]["wavefilesize"] = os.path.getsize(result)

    args["body"]["conversion"] = {
         "process" : (process_end - process_begin) / datetime.timedelta(seconds=1),
         "pull" : (pull_end - pull_begin) / datetime.timedelta(seconds=1),
         "push" : (push_end - push_begin) / datetime.timedelta(seconds=1)
    }
         

    return  args
    

