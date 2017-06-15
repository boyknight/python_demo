# -*- encoding: utf-8 -*-

import os.path
import shutil
import zipfile

if __name__ == "__main__":

    source_root_dir = os.getcwd()
    output_root_dir = os.path.join(source_root_dir, "output")

    # 初始化输出目录
    if os.path.exists(output_root_dir):
        shutil.rmtree(output_root_dir)

    os.makedirs(output_root_dir)
    os.chdir(output_root_dir)

    file_count = 0

    # 扫描所有zip文件
    all_files = os.walk(source_root_dir)
    for (root_path, dirs, file_names) in all_files:
        for file_name in file_names:
            file_full_path = os.path.join(root_path, file_name)

            file_full_path_splitted = os.path.split(file_full_path)

            file_name_split = file_name.split(".")

            if root_path != output_root_dir and len(file_name_split) > 1 and file_name_split[-1].lower() == "zip":
                
                print("正在处理: {}".format(file_name))

                # 创建滤镜目录
                filter_dir = os.path.join(output_root_dir, file_name_split[0])
                os.makedirs(filter_dir)

                json_file_content = '''{
    "filterList": [
        {
            "name": "stSticker",
            "type": "stSticker",
            "data": {
                "audio": "",
                "folderName": "stSticker",
                "triggerType": 0,
                "file": "''' + file_name + '''"
            }
        }
    ]
}'''

                json_file_path = os.path.join(filter_dir, "config.json")

                # 创建config.json文件
                with open(json_file_path, "w") as f:
                    f.write(json_file_content)

                # 创建stSticker目录
                sticker_path = os.path.join(filter_dir, "stSticker")
                os.makedirs(sticker_path)

                # 复制zip文件到stSticker目录
                sticker_file_path = os.path.join(sticker_path, file_name)
                shutil.copy(file_full_path, sticker_file_path)

                # 生成最终zip文件
                final_zip_file_path = os.path.join(output_root_dir, file_name)

                with zipfile.ZipFile(final_zip_file_path, 'w', zipfile.ZIP_DEFLATED) as target_file:
                    for dirpath, dirnames, filenames in os.walk(filter_dir):
                        for filename in filenames:
                            zip_file_path = os.path.join(dirpath, filename)
                            rel_path = os.path.relpath(zip_file_path, start=output_root_dir)
                            target_file.write(rel_path)

                # 删除滤镜目录
                shutil.rmtree(filter_dir)

                print("正在生成: {}".format(final_zip_file_path))
                print("")
                file_count += 1

    print("全部完成{}个文件".format(file_count))
