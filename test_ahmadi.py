import psycopg2
from conf import config
from datetime import datetime

def connect(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        db_result = cur.fetchall()
        cur.close()
        return db_result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    res=connect('select * from cam_coord ')
    res_c = connect("select cam.plak,cam.time,cam.cam_num,co.coord_x,co.coord_y from camera cam,cam_coord co where cam.cam_num=co.id and cam.plak='12359-13'")

######################################################
import requests
import urllib,json
def dist_time_osm(x1,y1,x2,y2):
    url = "https://routing.openstreetmap.de/routed-car/route/v1/driving/"\
          +str(x1)+","+str(y1)+";"+str(x2)+","+str(y2)+"?"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    #print(data)
    dist=data['routes'][0]['legs'][0]['distance']
    time=data['routes'][0]['legs'][0]['duration']
    dis_tim=[dist,time]
    return dis_tim

test=dist_time_osm(res[0][1],res[0][2],res[1][1],res[1][2])
##########################################################
total_dist=0
for i in range(len(res_c)-1):
        d_t=dist_time_osm(res_c[i][3],res_c[i][4],res_c[i+1][3],res_c[i+1][4])
        total_dist=total_dist+d_t[0];
        t1 = res_c[i][1]
        t2 = res_c[i+1][1]
        #print(d_t,res_c[i][1],res_c[i+1][1])

        if (t2.hour * 60 + t2.minute)-(t1.hour * 60 + t1.minute) > (d_t[1]/60)+30:
            print("\n","\n","The car with plak='12359-13' is parked---from camera  "+str(res_c[i][2])+" to camera  "+str(res_c[i+1][2]))
print("\n","total distance for car with plak='12359-13' is : ", total_dist)