from django.shortcuts import render

from django.core.exceptions import ObjectDoesNotExist
from course.models import ValidDivisionMajorPair, Division
from .models import HandbookEntity

# Create your views here.

semester_name = {1: 'Year 1 Semester 1',
                 2: 'Year 1 Semester 2',
                 3: 'Year 2 Semester 1',
                 4: 'Year 2 Semester 2',
                 5: 'Year 3 Semester 1',
                 6: 'Year 3 Semester 2',
                 7: 'Year 4 Semester 1',
                 8: 'Year 4 Semester 2'}


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
    handbook_info_unit_sum = {}
    query_major = {}
    try:
        query_major = ValidDivisionMajorPair.objects.get(major__major_en_abbr=r_major)
        handbook_info_temp = HandbookEntity.objects.filter(major=query_major, admission_year=admission_year)
        if not handbook_info_temp.exists():
            is_valid = False
        for entity in handbook_info_temp:
            if semester_name[entity.study_semester] in handbook_info:
                handbook_info['{}'.format(semester_name[entity.study_semester])].append(entity)
                handbook_info_unit_sum['{}'.format(semester_name[entity.study_semester])] += entity.unit
            else:
                handbook_info['{}'.format(semester_name[entity.study_semester])] = [entity]
                handbook_info_unit_sum['{}'.format(semester_name[entity.study_semester])] = entity.unit
    except ObjectDoesNotExist:
        is_valid = False
    return render(request, 'handbook/content.html', {'major': query_major,
                                                     'admission_year': admission_year,
                                                     'handbook_info': handbook_info,
                                                     'is_valid': is_valid,
                                                     'unit': handbook_info_unit_sum})
