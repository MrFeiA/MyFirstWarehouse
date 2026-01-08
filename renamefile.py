import re
import os
import sys


class RenameFile:
    def __init__(self):
        self.r = '^\d{1,3}-.+$'
        self.excluded_files = self._get_excluded_files()

    def _get_excluded_files(self):
        """获取需要排除的文件列表"""
        excluded = set()

        # 排除自身脚本文件
        if '__file__' in globals():
            script_name = os.path.basename(__file__)
            excluded.add(script_name)

        # 排除编译后的exe文件
        if getattr(sys, 'frozen', False):
            exe_filename = os.path.basename(sys.executable)
            excluded.add(exe_filename)

        # 排除隐藏文件和系统文件
        for file in os.listdir('.'):
            if file.startswith('.') or file.startswith('~'):
                excluded.add(file)

        return excluded

    def list_filename(self):
        """获取已编号文件的编号列表"""
        list_file_nums = []
        for file in os.listdir('.'):
            if os.path.isfile(file):
                if re.match(self.r,file):
                    try:
                        list_file_nums.append(int(file.split('-')[0]))
                    except Exception as e:
                        print(f"文件编号错误，错误代码是：{e}")
        return list_file_nums

    def max_name_file(self):
        """获取最大编号 为后续重命名做准备"""
        max_list = self.list_filename()
        if len(max_list)>0:
            max_name = max(max_list) + 1
        else:
            max_name = 1
        return max_name

    def rename_file(self,max_name):
        """重命名的方法"""
        list_dir = os.listdir('.')
        for file in list_dir:
            if file in self.excluded_files or not os.path.isfile(file):
                continue
            elif not re.match(self.r,file):
                new_file = f"{max_name}-{file}"
                os.rename(file,new_file)
                max_name += 1


if __name__ == "__main__":
    rf = RenameFile()
    n = rf.max_name_file()
    rf.rename_file(n)


