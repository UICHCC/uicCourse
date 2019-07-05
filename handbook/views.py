from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from course.models import ValidDivisionMajorPair, Division
from .models import HandbookEntity

# Create your views here.


def handbook(request):
    all_majors = ValidDivisionMajorPair.objects.all().order_by('division__division_en_abbr')
    all_divisions = Division.objects.all().exclude(division_en_abbr='MISC')
    all_ay = {}
    for c_major in all_majors:
        major_abbr = "{}".format(str(c_major.major.major_en_abbr))
        all_ay[major_abbr] = HandbookEntity.objects.order_by('-admission_year').filter(major=c_major).values(
            'admission_year').distinct()
    return render(request, 'handbook/index.html', {'all_majors': all_majors,
                                                   'all_divisions': all_divisions,
                                                   'all_ay': all_ay})


def handbook_content(request, r_major, admission_year):
    is_valid = True
    handbook_info = {}
    query_major = {}
    try:
        query_major = ValidDivisionMajorPair.objects.get(major__major_en_abbr=r_major)
        handbook_info_temp = HandbookEntity.objects.filter(major=query_major, admission_year=admission_year)
        for entity in handbook_info_temp:
            if entity.study_semester in handbook_info:
                handbook_info[entity.study_semester].append(entity)
            else:
                handbook_info[entity.study_semester] = [entity]
    except ObjectDoesNotExist:
        is_valid = False
    return render(request, 'handbook/content.html', {'major': query_major,
                                                     'admission_year': admission_year,
                                                     'handbook_info': handbook_info,
                                                     'is_valid': is_valid})
