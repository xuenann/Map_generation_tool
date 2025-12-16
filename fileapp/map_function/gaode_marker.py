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
        with open(os.path.join(config_file,'end.txt'),'r', encoding='utf-8') as f:
            map_config.setdefault('end',f.read())
    except Exception as e:
        print(e)
    
    return map_config
    

def to_gaode_market(map_config,map_data,new_file_path):
    '''
    生成高德地图marker html文件

    :param map_config: 高德地图marker配置字典,{'start':'','end':''}
    :param map_data: 地图数据,{'lat':lat,'lon':lon}
    :param new_file_path: 新文件路径
    :return: (是否成功,错误信息)
    '''
    try:
        middle = ''
        for i,item in enumerate(map_data):
            middle += ("{ icon: 'https://a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-"+str(i+1)+".png'," +
                        " position: [" + str(item['lon']) + "," + str(item['lat']) + "]},")
        
        with open(new_file_path,'w', encoding='utf-8') as f:
            f.write(map_config['start']+middle+map_config['end'])
    except Exception as e:
        print(e)
        return (False,e)
    
    return (True,'')
   