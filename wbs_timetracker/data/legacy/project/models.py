from django.db import models


class Employees(models.Model):
    login = models.CharField(unique=True, max_length=255)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    project_leader = models.IntegerField()
    daily_rate = models.FloatField()
    time_preference = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'employees'

    @staticmethod
    def from_request(request):
        """
        gets the employee from a request

        :param request:
        :return: the employee for the logged in user
        :rtype: Employees
        """
        return Employees.objects.using(
            request.parser_context.get('kwargs').get('project_id')
        ).get(
            login=request.user.username
        )


class WorkEffort(models.Model):
    workpackage = models.ForeignKey('Workpackage', models.DO_NOTHING, db_column='fid_wp')
    employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='fid_emp')
    rec_date = models.DateTimeField()
    effort = models.FloatField()
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_effort'


class Workpackage(models.Model):
    string_id = models.CharField(max_length=255)
    fid_project = models.IntegerField()
    """be aware, that this is a ForeignKey, which is not implemented as such, since there is no Model for the referencing table"""
    resp_employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='fid_resp_emp')
    parent = models.ForeignKey('Workpackage', null=True, db_column='fid_parent')
    parent_order_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    bac = models.FloatField()
    ac = models.FloatField()
    ev = models.FloatField()
    etc = models.FloatField()
    eac = models.FloatField()
    cpi = models.FloatField()
    bac_costs = models.FloatField()
    ac_costs = models.FloatField()
    etc_costs = models.FloatField()
    wp_daily_rate = models.FloatField()
    release_date = models.DateTimeField(blank=True, null=True)
    is_toplevel_wp = models.IntegerField(blank=True, null=True)
    is_inactive = models.IntegerField(blank=True, null=True)
    start_date_calc = models.DateTimeField(blank=True, null=True)
    start_date_wish = models.DateTimeField(blank=True, null=True)
    end_date_calc = models.DateTimeField(blank=True, null=True)
    allocated_employees = models.ManyToManyField(
        Employees,
        through='WpAllocation',
        related_name='allocated_workpackages'
    )

    class Meta:
        managed = False
        db_table = 'workpackage'
        unique_together = (('parent', 'parent_order_id'), ('string_id', 'fid_project'),)

    def __unicode__(self):
        return '{string_id} {workpackage_name}'.format(string_id=self.string_id, workpackage_name=self.name)


class WpAllocation(models.Model):
    workpackage = models.ForeignKey(Workpackage, models.DO_NOTHING, db_column='fid_wp')
    employee = models.ForeignKey(Employees, models.DO_NOTHING, db_column='fid_emp')

    class Meta:
        managed = False
        db_table = 'wp_allocation'
        unique_together = (('workpackage', 'employee'),)
