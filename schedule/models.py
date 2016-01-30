from __future__ import unicode_literals

from django.db import models
from response.templates import ok_response, error_response, invalid_data
from django.core.validators import MinValueValidator, MaxValueValidator


class Faculty(models.Model):
    name = models.CharField(blank=True, default='', max_length=300)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all():
        res = [{'id': _faculty.id, 'name': _faculty.name} for _faculty in Faculty.objects.all()]
        return ok_response(res)

    def get_groups(self):
        q = self.groups.all()
        if not q:
            return ok_response([])
        res = dict()
        for group in q:
            if group.degree.name not in res:
                res[group.degree.name] = []
            res[group.degree.name].append(group.json())
        return ok_response([res])


class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Group(models.Model):
    faculty = models.ForeignKey(Faculty, related_name='groups')
    name = models.CharField(blank=True, default='', max_length=300)
    degree = models.ForeignKey(Degree, default=1, related_name='degree')

    def __unicode__(self):
        return '%s: %s' % (self.faculty, self.name)

    def json(self):
        return {'id': self.id,
                'name': self.name}

    def get_schedule(self):
        q = self.classes.all()
        if not q:
            return ok_response([])
        res = dict()
        for obj in q:
            if obj.week not in res:
                res[obj.week] = [[] for x in range(7)]
            res[obj.week][obj.day].append(
                {'id': obj.id,
                 'num': obj.num,
                 'start': obj.start,
                 'end': obj.end,
                 'name': obj.name,
                 'type': obj.type,
                 'teachers': [teacher.json() for teacher in obj.teachers.all()],
                 'classrooms': [classroom.json() for classroom in obj.classrooms.all()]}
            )
        return ok_response([{'weeks':res}])

    def update_schedule(self, schedule):
        objects = []
        if type(schedule) is not dict:
            return invalid_data
        schedule = schedule.get('weeks', None)
        if schedule is None or type(schedule) is not dict:
            return invalid_data
        for week in schedule:
            days = schedule[week]
            if len(days) < 7 or type(days) is not list:
                return invalid_data
            for _day in range(len(days)):
                day = days[_day]
                if type(day) is not list:
                    print 'q4'
                    return invalid_data
                for _class in day:
                    if type(_class) is not dict:
                        print 'q3'
                        return invalid_data
                    try:
                        num = int(_class['num'])
                        week = int(week)
                        day = int(_day)
                        start = int(_class['start'])
                        end = int(_class['end'])
                        name = _class['name']
                        teachers = [Teacher.objects.get(id=int(_teacher)) for _teacher in _class['teachers']]
                        classrooms = [Classroom.objects.get(id=int(_classroom)) for _classroom in _class['classrooms']]
                        _type = int(_class['type'])
                    except:
                        print _class
                        return invalid_data
                    if num < 0 or week < 0 or _type < 0:
                        return invalid_data
                    if day < 0 or day > 6:
                        return invalid_data
                    if start < 0 or end < 0 or start > 60*24 or end > 60*24:
                        return invalid_data
                    if len(name) > 500 or not (type(name) is str or type(name) is unicode):
                        return invalid_data
                    objects.append([num, week, day, start, end, name, teachers, classrooms, _type])
        self.classes.all().delete()
        for obj in objects:
            num, week, day, start, end, name, teachers, classrooms, _type = obj
            obj = Class(group=self, num=num, week=week, day=day, start=start, end=end, name=name, type=_type)
            obj.save()
            for t in teachers:
                obj.teachers.add(t)
            for c in classrooms:
                obj.classrooms.add(c)
            obj.save()
            self.classes.add(obj)
        return ok_response([])


'''
group = models.ForeignKey(Group, related_name='classes')
num = models.PositiveIntegerField()
week = models.PositiveIntegerField()
day = models.PositiveIntegerField(validators=[MaxValueValidator(6)])  # 7 days
start = models.PositiveIntegerField(validators=[MaxValueValidator(60*24)])  # 1440 minutes
end = models.PositiveIntegerField(validators=[MaxValueValidator(60*24)])
name = models.CharField(max_length=500)
teachers = models.ManyToManyField(Teacher)
classrooms = models.ManyToManyField(Classroom)
type = models.PositiveIntegerField()
'''



class Teacher(models.Model):
    name = models.CharField(max_length=500)
    surname = models.CharField(max_length=500)
    middle_name = models.CharField(max_length=500)

    def __unicode__(self):
        return '%s %s %s' % (self.surname, self.name, self.middle_name)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'middle_name': self.middle_name}


class Classroom(models.Model):
    name = models.CharField(max_length=300)
    faculty = models.ForeignKey(Faculty, related_name='_faculty')

    def __unicode__(self):
        return '%s %s' % (self.name, self.faculty.name)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'faculty': self.faculty.name,
                'faculty_id': self.faculty.id}


class Class(models.Model):
    group = models.ForeignKey(Group, related_name='classes')
    num = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    day = models.PositiveIntegerField(validators=[MaxValueValidator(6)])  # 7 days
    start = models.PositiveIntegerField(validators=[MaxValueValidator(60*24)])  # 1440 minutes
    end = models.PositiveIntegerField(validators=[MaxValueValidator(60*24)])
    name = models.CharField(max_length=500)
    teachers = models.ManyToManyField(Teacher)
    classrooms = models.ManyToManyField(Classroom)
    type = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Classes'

    def modify(self, data):
        res = dict()
        if 'num' in data:
            try:
                num = int(data['num'])
                if num >= 0:
                    self.num = num
                    res['num'] = True
                else:
                    res['num'] = False
            except:
                res['num'] = False
        if 'week' in data:
            try:
                week = int(data['week'])
                if week >= 0:
                    self.week = week
                    res['week'] = True
                else:
                    res['week'] = False
            except:
                res['week'] = False
        if 'type' in data:
            try:
                type = int(data['type'])
                if type >= 0:
                    self.type = type
                    res['type'] = True
                else:
                    res['type'] = False
            except:
                res['type'] = False
        if 'day' in data:
            try:
                day = int(data['day'])
                if 0 <= day <= 6:
                    self.day = day
                    res['day'] = True
                else:
                    res['day'] = False
            except:
                res['day'] = False
        if 'start' in data:
            try:
                start = int(data['start'])
                if 0 <= start <= 60*24:
                    self.start = start
                    res['start'] = True
                else:
                    res['start'] = False
            except:
                res['start'] = False
        if 'end' in data:
            try:
                end = int(data['end'])
                if 0 <= end <= 60*24:
                    self.end = end
                    res['end'] = True
                else:
                    res['end'] = False
            except:
                res['end'] = False
        if 'name' in data:
            try:
                name = data['name']
                if len(name) <= 500:
                    self.name = data['name']
                    res['name'] = True
                else:
                    res['name'] = False
            except:
                res['name'] = False
        if 'teachers' in data:
            try:
                teachers = [Teacher.objects.get(id=teacher_id) for teacher_id in data['teachers']]
                self.teachers.clear()
                for teacher in teachers:
                    self.teachers.add(teacher)
                res['teachers'] = True
            except:
                res['teachers'] = False
        if 'classrooms' in data:
            try:
                classrooms = [Classroom.objects.get(id=teacher_id) for teacher_id in data['classrooms']]
                self.classrooms.clear()
                for classroom in classrooms:
                    self.classrooms.add(classroom)
                res['classrooms'] = True
            except:
                res['classrooms'] = False
        self.save()
        if False in res.values():
            return error_response(51, res)
        if not res:
            return ok_response([])
        return ok_response([res])
