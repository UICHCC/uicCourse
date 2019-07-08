from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
# Create your views here.
from course.models import Course, ValidDivisionMajorPair, CourseType, Division
from voting.models import QuickVotes, UserTaggingCourse


def report(request):
    content = dict()
    content['course_type'] = CourseType.objects.all().count()
    content['course_amount'] = Course.objects.all().count()
    content['review_q'] = QuickVotes.objects.all().count()
    content['review_t'] = UserTaggingCourse.objects.all().count()
    content['major_amount'] = ValidDivisionMajorPair.objects.all().count() - 1
    content['division_amount'] = Division.objects.all().count() - 1
    return render(request, 'report/index.html', {'content': content})


def dependency_graph_api(request):
    # data = serializers.serialize("xml", Course.objects.all())
    node_id = 0
    edge_id = 0
    graph = {'graph': {'nodes': [], 'links': []}}
    all_course = Course.objects.all()
    all_major = ValidDivisionMajorPair.objects.all()
    all_division = Division.objects.all()
    for division in all_division:
        graph['graph']['nodes'].append({'id': node_id,
                                        'category': 'division',
                                        'name': division.division_en,
                                        # 'value': 100,
                                        'symbolSize': 100,
                                        'label': {'normal': {'show': True, 'fontSize': 20}},
                                        'itemStyle': {'color': '#c23531'}})
        node_id += 1
    for major in all_major:
        graph['graph']['nodes'].append({'id': node_id,
                                        'category': 'major',
                                        'name': major.major.major_en_abbr,
                                        # 'value': 50,
                                        'symbolSize': 50,
                                        'label': {'normal': {'show': True, 'fontSize': 16}},
                                        'itemStyle': {'color': '#2f4554'}})
        node_id += 1
        graph['graph']['links'].append({'id': edge_id,
                                        'source': get_id_by_name(graph, major.division.division_en),
                                        'target': get_id_by_name(graph, major.major.major_en_abbr)})
        edge_id += 1
    for course in all_course:
        graph['graph']['nodes'].append({'id': node_id,
                                        'category': 'course',
                                        'name': course.course_id+' '+course.course_name_en,
                                        # 'value': 10,
                                        'label': {'normal': {'show': True, 'fontSize': 12}},
                                        'symbolSize': 10,
                                        'itemStyle': {'color': '#61a0a8'}})
        node_id += 1
        for required_major in course.course_major_take.all():
            graph['graph']['links'].append({'id': edge_id,
                                            'source': get_id_by_name(graph, required_major.major.major_en_abbr),
                                            'target': get_id_by_name(graph, course.course_id+' '+course.course_name_en)})
            edge_id += 1
    for course in all_course:
        for requested_course in Course.objects.filter(course_pre_request=course):
            graph['graph']['links'].append({'id': edge_id,
                                            'source': get_id_by_name(graph, course.course_id+' '+course.course_name_en),
                                            'target': get_id_by_name(graph, requested_course.course_id+ ' '+requested_course.course_name_en)})
            edge_id += 1
    # return HttpResponse("Unavailable")
    return JsonResponse(graph)


def get_id_by_name(dictionary, name):
    for node_item in dictionary['graph']['nodes']:
        if node_item['name'] == name:
            return node_item['id']
    return False
