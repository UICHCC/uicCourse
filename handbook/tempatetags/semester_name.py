from django import template
register = template.Library()

semester_name = {1: 'Year 1 Semester 1',
                 2: 'Year 1 Semester 2',
                 3: 'Year 2 Semester 1',
                 4: 'Year 2 Semester 2',
                 5: 'Year 3 Semester 1',
                 6: 'Year 3 Semester 2',
                 7: 'Year 4 Semester 1',
                 8: 'Year 4 Semester 2'}


@register.simple_tag
def semester_name(semester):
    return semester_name[semester]
