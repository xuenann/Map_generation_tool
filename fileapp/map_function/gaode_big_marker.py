from myproject import settings
import os



def read_gaode_big_marker_config():
    '''
    读取高德海量点标记配置文件

    :return: 高德海量点标记配置字典,{'start':'','end':''}
    '''
    try:
        config_file=os.path.join(settings.BASE_DIR, 'fileapp', 'templates', 'gaode_big_marker')
        map_config={}
        with open(os.path.join(config_file,'start.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('start',f.read())
        with open(os.path.join(config_file,'mid.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('mid',f.read())
        with open(os.path.join(config_file,'end.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('end',f.read())
    except Exception as e:
        print(e)
    
    return map_config
    

def to_gaode_big_marker(map_config,map_data,new_file_path):
    '''
    生成高德地图海量点标记 html文件

    :param map_config: 高德地图海量点标记配置字典,{'start':'','end':''}
    :param map_data: 地图数据,{'lat':lat,'lon':lon}
    :param new_file_path: 新文件路径
    :return: (是否成功,错误信息)
    '''
    try:
        marker_data = ''
        for i,item in enumerate(map_data):
            if 'marker_column' not in item:
                item.setdefault('marker_column','')
            marker_data += f"[{item['lon']},{item['lat']}],\n"
        
        with open(new_file_path,'w', encoding='utf-8') as f:
            f.write(map_config['start']+settings.GAODE_API_KEY+map_config['mid']+marker_data+map_config['end'])
    except Exception as e:
        print(e)
        return (False,e)
    
    return (True,'')
   