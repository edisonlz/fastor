#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.utils import importlib
from iclass.utils.gen_code_lib import do_output
import os,sys

class Command(BaseCommand):
    help = '自动代码生成'


    def add_arguments(self, parser):
        


        parser.add_argument('model', nargs='+', type=str)



    def handle(self, *args, **options):
        s = """
            说明：
            图像上传: field_name  包括 image 字符串的会自动检测为图像控件
            时间: field_type 等于 DatetimeField 会自动生成时间控件
            poistion 字段：如果包含position 字段，数据不分页
            choices: 如果 module 里面包括choices，自动生成select控件
            foreign_key_gen_select = true|false 外键是否自动生成select 控件
            course: 如果课程中有course会自动生成course autocomplete ,     课程检索: 自动包含
        """

        if len(args)!=2:
            print "需要两个参数，第一个参数为models路径，第二个参数为类名"
            print "例如： python manage.py gencode iclass.models.base_user BaseUser"
            return 
            
        model = args[0]
        _class = args[1]
        importlib.import_module('%s' % model)

        obj_model = getattr(sys.modules[model], _class) 
        
        print "[gen code]",obj_model
        do_output(obj_model)








            