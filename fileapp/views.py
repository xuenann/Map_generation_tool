from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from datetime import datetime
from . import tomap
import shutil


@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def upload_file(request):
    """接收用户选择的文件并保存到以IP地址命名的文件夹，每个用户只能保存一个文件"""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # 获取用户IP地址
            user_ip = request.META.get('REMOTE_ADDR', 'unknown_ip')
            
            # 创建保存文件的目录（如果不存在）
            base_dir = os.path.dirname(__file__)
            save_dir = os.path.join(base_dir, 'uploads', user_ip)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 删除该目录下已存在的所有文件
            for filename in os.listdir(save_dir):
                file_path = os.path.join(save_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            # 使用原始文件名保存，不添加时间戳
            new_filename = uploaded_file.name
            
            # 保存文件到服务器
            file_path = os.path.join(save_dir, new_filename)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            return JsonResponse({
                'filename': new_filename,
                'original_filename': uploaded_file.name,
                'size': uploaded_file.size,
                'user_ip': user_ip,
                'saved_path': file_path,
                'message': '文件已成功保存'
            })
    return JsonResponse({'error': 'No file received'})

@csrf_exempt
def upload_folder(request):
    """接收文件夹并将所有文件保存到以IP地址命名的文件夹，每个用户只能保存一个文件夹"""
    if request.method == 'POST':
        files = request.FILES.getlist('folder')
        if files:
            # 获取用户IP地址
            user_ip = request.META.get('REMOTE_ADDR', 'unknown_ip')
            
            # 提取根文件夹名称
            root_folder_name = None
            if files:
                # 第一个文件的路径通常包含根文件夹名称
                first_file_path = files[0].name
                if '\\' in first_file_path:  # Windows路径分隔符
                    root_folder_name = first_file_path.split('\\')[0]
                elif '/' in first_file_path:  # Unix路径分隔符
                    root_folder_name = first_file_path.split('/')[0]
                else:
                    # 如果没有路径分隔符，说明只有一个文件，没有文件夹结构
                    root_folder_name = 'uploaded_folder'
            
            # 创建基础保存目录（如果不存在）
            base_dir = os.path.dirname(__file__)
            base_save_dir = os.path.join(base_dir, 'uploads', user_ip)
            if not os.path.exists(base_save_dir):
                os.makedirs(base_save_dir)
            
            # 删除该目录下已存在的所有文件夹
            import shutil
            for item in os.listdir(base_save_dir):
                item_path = os.path.join(base_save_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            
            # 处理每个文件
            saved_files = []
            
            # 使用原始根文件夹名称保存，不添加时间戳
            folder_name = root_folder_name
            
            for file in files:
                # 获取相对路径和文件名
                relative_path = file.name
                
                # 提取目录部分
                dir_part = os.path.dirname(relative_path)
                
                # 创建完整的保存路径
                if dir_part and dir_part != root_folder_name:  # 确保目录部分不是根文件夹本身
                    # 如果有目录结构，保持原结构
                    file_save_dir = os.path.join(base_save_dir, folder_name, dir_part)
                    if not os.path.exists(file_save_dir):
                        os.makedirs(file_save_dir)
                    file_path = os.path.join(file_save_dir, os.path.basename(relative_path))
                else:
                    # 如果没有目录结构或目录部分就是根文件夹，直接保存到基础目录
                    file_save_dir = os.path.join(base_save_dir, folder_name)
                    if not os.path.exists(file_save_dir):
                        os.makedirs(file_save_dir)
                    file_path = os.path.join(file_save_dir, os.path.basename(relative_path))
                
                # 保存文件
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                # 记录保存的文件信息
                saved_files.append({
                    'original_path': relative_path,
                    'new_filename': os.path.basename(relative_path),
                    'size': file.size,
                    'saved_path': file_path
                })
            
            return JsonResponse({
                'user_ip': user_ip,
                'total_files': len(saved_files),
                'folder_name': folder_name,
                'saved_files': saved_files,
                'message': '文件夹中的文件已成功保存'
            })
    return JsonResponse({'error': 'No folder received'})

@csrf_exempt
def submit_input(request):
    """接收用户输入的内容"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('input', '')
            if user_input:
                # 这里可以添加处理用户输入的逻辑
                print(f"后端收到用户输入: {user_input}")
                return JsonResponse({
                    'received_input': user_input,
                    'message': '输入内容已成功接收'
                })
            return JsonResponse({'error': 'No input received'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'})
    return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def generate_map(request):
    """处理前端发送的选项和文件信息，将.csv文件后缀改为.html"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 打印前端发送的选项
            ignore_first_row = data.get('ignore_first_row', 'yes')
            coordinate_system = data.get('coordinate_system', 'wgs84')
            map_type = data.get('map_type', 'gaode_marker')
            file_path = data.get('file_path', '')
            folder_path = data.get('folder_path', '')
            longitude_column = data.get('longitude_column', '')
            latitude_column = data.get('latitude_column', '')
            marker_column = data.get('marker_column', '')
            sort_column = data.get('sort_column', '')

            print(f"后端收到生成地图请求:")
            print(f"  是否忽略第一行: {ignore_first_row}")
            print(f"  选择的坐标系: {coordinate_system}")
            print(f"  选择的地图类型: {map_type}")
            print(f"  上传的文件: {file_path}")
            print(f"  上传的文件夹: {folder_path}")
            print(f"  经度列: {longitude_column}")
            print(f"  纬度列: {latitude_column}")
            if marker_column:
                print(f"  标记列: {marker_column}")
            if sort_column:
                print(f"  排序列: {sort_column}")
            
            # 获取用户IP地址
            user_ip = request.META.get('REMOTE_ADDR', 'unknown_ip')
            base_dir = os.path.dirname(__file__)
            upload_dir = os.path.join(base_dir, 'uploads', user_ip)
            
            generated_files = []
            
            # 处理文件复制和后缀修改
            if file_path:
                # 构建原始文件路径
                original_file_path = os.path.join(upload_dir, file_path)
                
                # 检查原始文件是否存在
                if os.path.exists(original_file_path):
                    # 构建新的.html文件路径
                    file_name, file_ext = os.path.splitext(original_file_path)
                    new_file_path = file_name + '.html'

                    # 生成地图文件
                    ret,e,generated_files = tomap.generate_map('file',original_file_path,new_file_path,data,user_ip)

                    if ret is False:
                        return JsonResponse({
                            'message': f'地图生成失败！错误信息: {e}',
                            'generated_files': generated_files
                        })
                    
                    # 添加到生成文件列表
                    # generated_files.append({
                    #     'name': os.path.basename(new_file_path),
                    #     'url': f'/uploads/{user_ip}/{os.path.basename(new_file_path)}'
                    # })
                    
                    return JsonResponse({
                        'message': f'地图生成成功！文件已生成: {os.path.basename(new_file_path)}',
                        'new_file_path': new_file_path,
                        'generated_files': generated_files
                    })
                else:
                    return JsonResponse({
                        'message': f'地图生成成功！但原始文件不存在: {original_file_path}',
                        'generated_files': generated_files
                    })
            
            # 处理文件夹复制和所有文件后缀修改
            elif folder_path:
                # 获取原始文件夹路径
                # 注意：前端返回的是文件列表，需要找到原始文件夹名称
                # 这里假设文件夹上传时，上传的文件中包含原始文件夹名称
                # 我们需要从已上传的文件中找到原始文件夹名称
                import shutil
                
                # 查找原始文件夹
                original_folder = None
                for item in os.listdir(upload_dir):
                    item_path = os.path.join(upload_dir, item)
                    if os.path.isdir(item_path):
                        original_folder = item
                        break
                
                if original_folder:
                    original_folder_path = os.path.join(upload_dir, original_folder)
                    new_folder_path = original_folder_path + '_map'
                    
                    # 创建整个文件夹
                    os.makedirs(new_folder_path, exist_ok=True)
                    
                    # 生成地图文件
                    ret,e,generated_files = tomap.generate_map('folder',original_folder_path,new_folder_path,data,user_ip)

                    
                    return JsonResponse({
                        'message': f'地图生成成功！{e}',
                        'new_folder_path': new_folder_path,
                        'modified_files': data['folder_path'],
                        'total_modified': len(data['folder_path']),
                        'generated_files': generated_files
                    })
                else:
                    return JsonResponse({
                        'message': '地图生成成功！但没有找到上传的文件夹',
                        'generated_files': generated_files
                    })
            
            else:
                return JsonResponse({
                    'message': '地图生成成功！但没有上传文件或文件夹',
                    'generated_files': generated_files
                })
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})
