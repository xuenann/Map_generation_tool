import csv
from . import coordinate_transform
import os
from .map_function import gaode_marker,baidu_marker,gaode_line


coordinate_func_dict={
        'wgs84_gaode_marker':coordinate_transform.wgs84_to_gcj02,
        'bd09_gaode_marker':coordinate_transform.bd09_to_gcj02,
        'mapbar_gaode_marker':coordinate_transform.mapbar_to_gcj02,
        'wgs84_baidu_marker':coordinate_transform.wgs84_to_bd09,
        'gcj02_baidu_marker':coordinate_transform.gcj02_to_bd09,
        'mapbar_baidu_marker':coordinate_transform.mapbar_to_bd09,
    }

config_func_dict={
        'gaode_marker':gaode_marker.read_gaode_market_config,
        'baidu_marker':baidu_marker.read_baidu_market_config,
        'gaode_line':gaode_line.read_gaode_line_config,
}

map_func_dict={
        'gaode_marker':gaode_marker.to_gaode_market,
        'baidu_marker':baidu_marker.to_baidu_market,
        'gaode_line':gaode_line.to_gaode_line,
}


def generate_map(f_type,file_path,new_file_path,data,user_ip):
    '''
    生成地图文件

    :param f_type: 文件类型，file或folder
    :param file_path: 文件路径或文件夹路径
    :param new_file_path: 新文件路径或新文件夹路径
    :param data: 地图配置数据
    :param user_ip: 用户IP地址，用于生成文件路径
    :return: 
        : ret: 生成地图文件是否成功
        : msg: 生成地图文件的消息
        : generated_files: 生成的地图文件列表
    '''
    generated_files=[]
    for k in list(data.keys()):
            if data[k]=='':
                del data[k]

    print(data)
    # 读取地图配置文件
    map_config=config_func_dict[data['map_type']]()
    
    # 处理文件
    if f_type == 'file':
        # 处理数据
        
        ret,map_data=deal_data(file_path,data)
        if ret is False:
            return ret,map_data,''

        # 生成地图文件
        ret,msg=map_func_dict[data['map_type']](map_config,map_data,new_file_path)
        if ret is False:
            return ret,msg,''

        # 生成文件列表
        generated_files.append({
                        'name': os.path.basename(new_file_path),
                        'url': f'/uploads/{user_ip}/{os.path.basename(new_file_path)}'
                    })
        return True,'',generated_files

    # 处理文件夹
    elif f_type == 'folder':
        err_msg=[]
        for file_name in os.listdir(file_path):
            # 处理数据
            ret,map_data=deal_data(os.path.join(file_path,file_name),data)
            if ret is False:
                err_msg.append(f'{file_name}:{map_data}')
                continue
            
            # 生成地图文件
            file_name, file_ext = os.path.splitext(file_name)
            new_file_name = file_name + '.html'
            # 生成地图文件
            ret,msg=map_func_dict[data['map_type']](map_config,map_data,os.path.join(new_file_path,new_file_name))
            if ret is False:
                err_msg.append(f'{file_name}:{msg}')
                continue

            generated_files.append({
                                'name': new_file_name,
                                'url': f'/uploads/{user_ip}/{os.path.basename(new_file_path)}/{new_file_name}'
                            })

        return ret,f'共处理{len(os.listdir(file_path))}个文件，成功{len(generated_files)}个，失败{len(err_msg)}个\n'+ \
                            '\n'.join(err_msg),generated_files



def deal_data(file_path,data):
    '''
    处理数据，将数据转换为地图数据

    :param file_path: 文件地址
    :param data: 用户选择的地图类型、坐标系统、是否忽略表头、纬度索引、经度索引
    :return: (是否成功,地图数据)  [{'lat':lat,'lon':lon,,},{},,]
    '''
    map_data=[]

    index_list={k:int(v) for k,v in data.items() if k.endswith('column')}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            if data['ignore_first_row'] == 'yes':
                next(reader)
            for row in reader:
                lat,lon=coordinate_func_dict.get(
                    f"{data['coordinate_system']}_{data['map_type']}",lambda x,y:(x,y))(
                                float(row[index_list['latitude_column']]),
                                float(row[index_list['longitude_column']])) 

                map_data.append({'lat':lat,'lon':lon} | {k:row[index_list[k]] for k in index_list if k not in ['latitude_column','longitude_column']})
                
        if len(map_data)==0:
            return (False,'数据为空')

        # 如果需要排序
        if 'sort_column' in data:
            map_data.sort(key=lambda x:x['sort_column'])

        return (True,map_data)
    except Exception as e:
        print(e)
        return (False,e)
                

