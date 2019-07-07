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
    graph = {'graph': {'nodes': [], 'edges': []}}
    course_node = Course.objects.all()
    all_major = ValidDivisionMajorPair.objects.all()
    all_division = Division.objects.all()
    for division in all_division:
        if division.division_en_abbr == "MISC":
            pass
        graph['graph']['nodes'].append({'id': node_id, 'type': 'division', 'label': division.division_en})
        node_id += 1
    for major in all_major:
        if major.division.division_en_abbr == "MISC":
            pass
        graph['graph']['nodes'].append({'id': node_id, 'type': 'major', 'label': major.major.major_en})
        node_id += 1
        graph['graph']['edges'].append({'id': edge_id, 'source': get_id_by_name(graph, major.division.division_en), 'target': get_id_by_name(graph, major.major.major_en)})
        edge_id += 1
    # return HttpResponse("Unavailable")
    return JsonResponse(graph)


def get_id_by_name(dictionary, name):
    for node_item in dictionary['graph']['nodes']:
        if node_item['label'] == name:
            return node_item['id']
    return False
