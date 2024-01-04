from pymavlink import mavutil
import time
mvk = mavutil.mavlink_connection('tcp:192.168.0.21:5763')
mvk.wait_heartbeat()
mvk.mav.request_data_stream_send(mvk.target_system, mvk.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 5, 1)

def main():
    while(1):
        re = mvk.recv_match()
        print(re)
        time.sleep(0.1)

if __name__ =="__main__":
    main()