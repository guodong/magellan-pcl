# from grpc_server import serve
from compiler import compile
from deployer.pit2dataplane import *
import os

if __name__ == '__main__':

    #app_dir = 'D:/CZU/PengCheng/magellan-pcl/apps/l2'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    app_dir = dir_path + '/apps/l2'
    dp_file = app_dir + '/on_packet.mag'
    offline_file = app_dir + '/offline.py'
    out_dir = 'out'
    ds_file = app_dir + '/ds.json'
    print(ds_file)
    portTag, pipeline = compile(dp_file, ds_file)

    '''
    for table in pipeline:
        print("inputs: " + str(table.schema.inputs))
        print("outputs: " + str(table.schema.outputs))
        print(str(table.entries))
    '''

    ds = DatastoreProxy('topologies/l2.json')
    fg = FlowRulesGenerator(ds)

    fg.accept_new_pit(portTag, pipeline)
    fg.dump()

    
    # t = Thread(target=serve, args=(fp)).start()
    # serve()


