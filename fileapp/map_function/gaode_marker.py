from myproject import settings
import os



def read_gaode_market_config():
    '''
    读取高德地图marker配置文件

    :return: 高德地图marker配置字典,{'start':'','end':''}
    '''
    try:
        config_file=os.path.join(settings.BASE_DIR, 'fileapp', 'templates', 'gaode_marker')
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
    

def to_gaode_market(map_config,map_data,new_file_path):
    '''
    生成高德地图marker html文件

    :param map_config: 高德地图marker配置字典,{'start':'','end':''}
    :param map_data: 地图数据,{'lat':lat,'lon':lon,gaode_marker_column:}
    :param new_file_path: 新文件路径
    :return: (是否成功,错误信息)
    '''
    try:
        marker_data = ''
        for i,item in enumerate(map_data):
            if 'marker_column' not in item:
                item.setdefault('marker_column','')
            marker_data += (f"{'{'}title:'{item['marker_column']+':'+str(item['lon'])+':'+str(item['lat'])}',\n \
                                text:'{item['marker_column']}',\n \
                                position:[{item['lon']},{item['lat']}] {'}'},\n")
        
        with open(new_file_path,'w', encoding='utf-8') as f:
            f.write(map_config['start']+settings.GAODE_API_KEY+map_config['mid']+marker_data+map_config['end'])
    except Exception as e:
        print(e)
        return (False,e)
    
    return (True,'')
   