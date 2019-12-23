#coding=# -*- coding: utf-8 -*-
import os
import sys
import datetime
from app.iclass.utils import get_primary_key
from django.template import Context, Template


def get_field_type(field):

    sfield =  str(field)
    sfield = sfield.split(":")
    ts = sfield[0].split(".")
    field_type =  ts[-1]

    return field_type


def output_view(clazz ,clazz_name, field_list , folder, has_position, foreign_key_gen_select , has_course):
    project = os.path.realpath(os.path.dirname(__file__))
    t_path = os.path.realpath(os.path.join(project, 'templates/view.py'))
    output_path = os.path.realpath(os.path.join(project,"../.." , "iclass", "views", '%s_view.py' % folder))
    print output_path

    template = open(t_path).read()
    t = Template(template)

    data = t.render(Context({
        'clazz': clazz, 
        'clazz_name': clazz_name, 
        'field_list': field_list, 
        "has_position":has_position,
        "folder":folder,
        "foreign_key_gen_select":foreign_key_gen_select,
        "has_course":has_course,
    }))

    fd = open(output_path,"w")
    fd.write(data)
    fd.close()



def output_detail(clazz ,clazz_name, field_list , folder, has_position , foreign_key_gen_select , has_course):
    project = os.path.realpath(os.path.dirname(__file__))
    t_path = os.path.realpath(os.path.join(project, 'templates/new.html'))

    path = os.path.join(project,".." , "templates", folder )
    if not os.path.exists(os.path.join(path)):
        os.makedirs(os.path.join(path))
    output_path = os.path.realpath(os.path.join(path, 'new.html' ))
    print output_path

    template = open(t_path).read()
    t = Template(template)

    data = t.render(Context({
        'clazz': clazz, 
        'clazz_name': clazz_name, 
        'field_list': field_list, 
        "has_position":has_position,
        "folder":folder,
        "foreign_key_gen_select":foreign_key_gen_select,
        "has_course":has_course,
    }))

    #print data
    data = data.replace("===","{%")
    data = data.replace("---","%}")
    data = data.replace("###","{{")
    data = data.replace("***","}}")

    fd = open(output_path,"w")
    fd.write(data)
    fd.close()



def output_list(clazz ,clazz_name, field_list , folder, has_position , foreign_key_gen_select, has_course):
    project = os.path.realpath(os.path.dirname(__file__))
    t_path = os.path.realpath(os.path.join(project, 'templates/list.html'))
  

    path = os.path.join(project,".." , "templates", folder )
    if not os.path.exists(os.path.join(path)):
        os.makedirs(os.path.join(path))
    output_path = os.path.realpath(os.path.join(path, 'list.html' ))
    print output_path
    

    template = open(t_path).read()
    t = Template(template)

    data = t.render(Context({
        'clazz': clazz, 
        'clazz_name': clazz_name, 
        'field_list': field_list, 
        "has_position":has_position,
        "folder":folder,
        "foreign_key_gen_select":foreign_key_gen_select,
        "has_course":has_course,
    }))

    #print data
    data = data.replace("===","{%")
    data = data.replace("---","%}")
    data = data.replace("###","{{")
    data = data.replace("***","}}")

    fd = open(output_path,"w")
    fd.write(data)
    fd.close()


def do_output(model):
    
    """
    说明：
    图像上传: field_name  包括 image 字符串的会自动检测为图像控件
    时间: field_type 等于 DatetimeField 会自动生成时间控件
    poistion 字段：如果包含position 字段，数据不分页
    choices: 如果 module 里面包括choices，自动生成select控件
    foreign_key_gen_select = true|false 外键是否自动生成select 控件
    course: 如果课程中有course会自动生成course autocomplete ,     课程检索: 自动包含
    """

    # modify me here

    local_fields = model._meta.fields
    verbose_name = model._meta.verbose_name

  
    clazz = model._meta.object_name
    folder = model._meta.model_name.lower()

    clazz_name = verbose_name
    foreign_key_gen_select = True

    field_list = []
    has_position = False
    has_course = False

    for field in local_fields:
        #field_dict = {}

        field.field_type = get_field_type(field)
        if "image" in field.name:
            field.image_field = True
        else:
            field.image_field = False

        if "course" in field.name:
            has_course = True
        else:
            has_course = False

        if field.attname == "position":
            has_position = True

        field_list.append(field)

        if hasattr(field,"related_fields"):
            name = field.related_fields[0][0].related.parent_model.__name__
            field.foreign_key_cls = name
            field.foreign_key_datas = "%s_datas" % (name.lower())
        else:
            field.foreign_key_cls = None
            field.foreign_key_datas = None


    output_view(clazz , clazz_name  , field_list , folder, has_position , foreign_key_gen_select  ,has_course)
    output_detail(clazz , clazz_name  , field_list , folder, has_position , foreign_key_gen_select ,has_course)
    output_list(clazz , clazz_name  , field_list , folder, has_position , foreign_key_gen_select ,has_course)





if __name__ == "__main__":
    do_output()



