import subprocess
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy.config as config
import time


import multiprocessing



def addServer_HAproxyCFG(_name, _port, the_be_section):

    server1 = config.Server(name=_name, host="127.0.0.1", port=_port)
    the_be_section.add_server(server1)

def removeServer_HAproxyCFG(_name, the_be_section):
    the_be_section.remove_server(_name)


def addDocker(cmd):
    #cmd[0] is image name
    #cmd[1] is port no
    #subprocess.call(cmd, shell=False)
    print (cmd[0],cmd[1])
    subprocess.run("docker rm "+cmd[0] , shell=True)
    subprocess.run("docker build -t flask-"+cmd[0]+" ." , shell=True)
    subprocess.check_output("docker run --name "+cmd[0]+" -it -p "+cmd[1]+":5000 flask-"+cmd[0] , shell=True)

    #

def removeDocker(cmd):

    subprocess.run("docker stop "+cmd[0] , shell=True)
    subprocess.run("docker rm "+cmd[0] , shell=True)



if __name__ == '__main__':



    cfg_parser = Parser('/etc/haproxy/haproxy.cfg')
    configuration = cfg_parser.build_configuration()

    the_be_section = configuration.backend("My_Web_Servers")

    subprocess.run(" sudo service haproxy restart", shell=True)




    docker_count = 0
    initial_im=0
    initial_port=4500
    docker_list=[]
    while True:
        time.sleep(1)
        cputil= subprocess.check_output("mpstat 1 1| tr ' ' '\n'| tail -n 1", shell=True )

        strCpu=cputil.decode("utf-8").split('\n')[0]

        fltCputil=100-float(strCpu)
        print("CPU Load:",fltCputil)
        n = int(fltCputil/10) + 1
        print("N:",n)
        print(docker_list)

        # if cpu load increases, increase the number of containers
        if (n>docker_count):
            cmd=[]
            newDocsN = n-docker_count
            docker_count = n
            i=0
            while (i<newDocsN):
                initial_im += 1
                initial_port += 1
                str_im = str(initial_im)
                str_port = str(initial_port)
                print(str_im, str_port)
                lis = ["image"+str_im , str_port]
                cmd.append(lis)
                docker_list.append(lis)
                i += 1
            #print(cmd)
            # count = newDocsN #multiprocessing.cpu_count()

            # BUILD AND RUN DOCKER IMAGE
            pool = multiprocessing.Pool()
            pool.map_async(addDocker, cmd)

            #ADD DOCKER IMAGE SERVER TO HAPROXY CONFIG FILE
            for c in cmd:
                addServer_HAproxyCFG(_name=c[0], _port=c[1], the_be_section=the_be_section)

            cfg_render = Render(configuration)
            cfg_render.dumps_to('/etc/haproxy/haproxy.cfg')
            subprocess.run(" sudo service haproxy reload", shell=True)

            #docker_list.append(docker)
            #pool.close()
            #pool.join()


        # if cpu load decreases, decrease the number of containers
        if (n<docker_count and len(docker_list)>0):
            delDocsN = docker_count - n
            docker_count = n
            i = 0
            cmd = []
            while (i < delDocsN):
                initial_im -= 1
                initial_port -= 1
                print ("Removing docker image ", docker_list[len(docker_list)-1])
                lis = docker_list.pop(len(docker_list)-1)
                cmd.append(lis)
                i += 1


            # STOP AND REMOVE DOCKER IMAGE
            pool = multiprocessing.Pool()
            pool.map_async(removeDocker, cmd)

            # DELETE DOCKER IMAGE SERVER FROM HAPROXY CONFIG FILE
            for c in cmd:
                removeServer_HAproxyCFG(_name=c[0], the_be_section=the_be_section)

            cfg_render = Render(configuration)
            cfg_render.dumps_to('/etc/haproxy/haproxy.cfg')
            subprocess.run(" sudo service haproxy reload", shell=True)





# subprocess.run("docker rm image1" , shell=True)
# subprocess.run("docker build -t flask-image1 ." , shell=True)
# subprocess.run("docker rm image2" , shell=True)
# subprocess.run("docker build -t flask-image2 ." , shell=True)
#
# subprocess.check_output("docker run --name image1 -it -p 4500:5000 flask-image1" , shell=True)
#
# subprocess.check_output("docker run --name image2 -it -p 5500:5000 flask-image2" , shell=True)

# cputil= subprocess.check_output("mpstat | tr ' ' '\n'| tail -n 1", shell=True )
#
# strCpu=cputil.decode("utf-8").split('\n')[0]
#
# fltCputil=100-float(strCpu)
#
# print (fltCputil)

cfg_parser = Parser('/etc/haproxy/haproxy.cfg')
configuration = cfg_parser.build_configuration()
# print (configuration.globall)  # the `global` is keyword of Python, so name it `globall`
# print (configuration.globall.options())  # get the 'option ...' config lines
# print (configuration.globall.configs())  # get config lines except 'option ...' ones

frontend_sections = configuration.frontends

frontServerName=None
# Get frontend sections specifics
for fe_section in frontend_sections:
    # Get the name, host, port of the frontend section
    print (fe_section.name, fe_section.host, fe_section.port)
    frontServerName=fe_section.name




the_fe_section = configuration.frontend(frontServerName)

#   Get all the backend configs
usebackends = the_fe_section.usebackends()  # return list(config.UseBackend)
for usebe in usebackends:
    # Get the using backend name, operator, condition
    print (usebe.backend_name, usebe.operator, usebe.backend_condition)
    # Determine if it's `default_backend` line
    print (usebe.is_default)



the_be_section = configuration.backend("My_Web_Servers")
#   Get all the Server lines in backend section
servers = the_be_section.servers()  # return list(config.Server)
print (servers[0])

#   Find the specified Server
# the_server = the_be_section.server("web1.example.com")  # return config.Server
# #   Get the Server name, host, port
# print the_server.name, the_server.host, the_server.port
#
#
#
#
# the_be_section.remove_server("web1.example.com")

# server1 = config.Server(name="web3.example.com", host="192.168.10.9", port="4500")
# the_be_section.add_server(server1)


cfg_render = Render(configuration)
cfg_render.dumps_to('/etc/haproxy/haproxy.cfg')



#
