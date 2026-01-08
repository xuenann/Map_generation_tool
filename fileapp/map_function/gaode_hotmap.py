from myproject import settings
import os



def read_gaode_hotmap_config(data):
    '''
    读取高德地图热力图配置文件

    :return: 高德地图热力图配置字典,{'start':'','end':''}
    '''
    try:
        config_file=os.path.join(settings.BASE_DIR, 'fileapp', 'templates', 'gaode_hotmap')
        map_config={}
        with open(os.path.join(config_file,'start.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('start',f.read())

        if data['hotmap_style']=='2d':
            with open(os.path.join(config_file,'mid_2d.txt'),'r', encoding='utf-8') as f:
                map_config.setdefault('mid',f.read())
        elif data['hotmap_style']=='3d':
            with open(os.path.join(config_file,'mid_3d.txt'),'r', encoding='utf-8') as f:
                map_config.setdefault('mid',f.read())

        with open(os.path.join(config_file,'end.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('end',f.read())
    except Exception as e:
        print(e)
    
    return map_config
    

def to_gaode_hotmap(map_config,map_data,new_file_path):
    '''
    生成高德地图热力图 html文件

    :param map_config: 高德地图热力图配置字典,{'start':'','end':''}
    :param map_data: 地图数据,{'lat':lat,'lon':lon,count_column:}
    :param new_file_path: 新文件路径
    :return: (是否成功,错误信息)
    '''
    try:
        hotmap_data = ''
        for i,item in enumerate(map_data):
            if 'count_column' not in item:
                item.setdefault('count_column',1)
            hotmap_data += f"{'{'}'lng':{item['lon']},'lat':{item['lat']},'count':{item['count_column']}{'}'},\n"
        
        with open(new_file_path,'w', encoding='utf-8') as f:
            f.write(map_config['start']+settings.GAODE_API_KEY+map_config['mid']+hotmap_data+map_config['end'])
    except Exception as e:
        print(e)
        return (False,e)
    
    return (True,'')
   