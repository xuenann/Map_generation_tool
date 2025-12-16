from myproject import settings
import os



def read_baidu_market_config():
    '''
    读取百度地图marker配置文件

    :return: 百度地图marker配置字典,{'start':'','end':''}
    '''
    try:
        config_file=os.path.join(settings.BASE_DIR, 'fileapp', 'templates', 'baidu_marker')
        map_config={}
        with open(os.path.join(config_file,'start.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('start',f.read())
        with open(os.path.join(config_file,'end.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('end',f.read())
    except Exception as e:
        print(e)
    
    return map_config


def to_baidu_market(map_config,map_data,new_file_path):
    '''
    生成百度地图marker html文件

    :param map_config: 百度地图marker配置字典,{'start':'','end':''}
    :param map_data: 地图数据列表,每个元素为一个字典,{'marker_column':'','lon':'','lat':''}
    :param new_file_path: 新文件路径,包含文件名
    :return: (True,'') 或 (False,错误信息)
    '''
    middle=''
    data=[]
    lng_list,lat_list=[],[]
    try:
        for item in map_data:
            if 'marker_column' not in item:
                data.append('{title:"",point:"'+f'{item["lon"]},{item["lat"]}"'+'}')
            else:
                data.append('{ title :"'+f'{item["marker_column"]}", point: "{item["lon"]},{item["lat"]}"'+'}')
            lng_list.append(item['lon'])
            lat_list.append(item['lat'])
        middle='var markerArr = [' + ','.join(data) + '];\n'
        middle+='function map_init() {\nvar map = new BMap.Map("map");\n'
        middle+=f'var point = new BMap.Point({(max(lng_list)+min(lng_list))/2},{(max(lat_list)+min(lat_list))/2});\n'

        with open(new_file_path,'w', encoding='utf-8') as f:
            f.write(map_config['start']+middle+map_config['end'])
    except Exception as e:
        print(e)
        return (False,e)
    
    return (True,'')

