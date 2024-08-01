from django.shortcuts import render
from django.http import JsonResponse


'数据统计页面'
def chart_list(request):
    return render(request, 'chart_list.html')

'构造柱状图的数据'
def chart_bar(request):
    # 数据可以去数据库中获取
    legend = ["xiaoxiao", "xiaoxiao520"]
    series_list = [
        {
            "name": 'xiaoxiao',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": 'xiaoxiao520',
            "type": 'bar',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)

'构造饼图的数据'
def chart_pie(request):
    db_data_list = [
        {"value": 2048, "name": 'IT开发部门'},
        {"value": 1735, "name": '秘书部门'},
        {"value": 580, "name": '运营部'},
        {"value": 580, "name": '后勤保障部'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ["上海", "浙江"]
    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '浙江',
            "type": 'line',
            "stack": 'Total',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


