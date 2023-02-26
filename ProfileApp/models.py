from django.db import models
from django.db.models import Sum, F

class Spare_part(models.Model):
    spid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    price=models.FloatField(default=0.00)
    net = models.IntegerField(default=0)
    picture = models.ImageField(upload_to ='static/SparePart/', default="")
    def __str__(self):
        return self.spid + ":" + self.name + ", " + str(self.price)
    def getSaleAmount(self):
        amount = Samplesale.objects.filter(spare_part=self).aggregate(amount=Sum(F('amount')))
        return amount['amount']

class Admin(models.Model):
    aid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    birthdate = models.DateField(default=None)
    picture = models.ImageField(upload_to='static/admin/', default="")
    password = models.CharField(max_length=255, default="1234")

    def __str__(self):
        return self.aid + ":" + self.name

class Member(models.Model):
    mid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    birthdate = models.DateField(default=None)
    picture = models.ImageField(upload_to='static/member/', default="")
    address = models.TextField(max_length=400, default="")
    tel = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=255, default="1234")
    def __str__(self):
        return self.mid + ":" + self.name
    def getSaleAmount(self):
        amount = Samplesale.objects.filter(member=self).aggregate(amount=Sum(F('amount')))
        return amount['amount']

class Getjop(models.Model):
    gid = models.CharField(max_length=13, primary_key=True, default="")
    details = models.CharField(max_length=100, default="")
    date = models.DateField(default=None)
    name_employer = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.gid + ":" + self.details
    def getSaleAmount(self):
        amount = Samplesale.objects.filter(spare_part=self).aggregate(amount=Sum(F('amount')))
        return amount['amount']

class Assignment(models.Model):
    agid = models.CharField(max_length=13, primary_key=True, default="")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default=None)
    getjop = models.ForeignKey(Getjop, on_delete=models.CASCADE, default=None)
    date = models.DateField(default=None)
    status = models.CharField(max_length=1, default="1")
    def __str__(self):
        return self.agid + " : "  + self.member.name  + " : " + self.getjop.details
    def getStatus(self):
        if self.status == '1':
            return 'ยังไม่ซ่อม'
        elif self.status == '2':
            return 'ซ่อมแล้ว'

class ConfirmsAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, default=None)

class Savejob(models.Model):
    sid = models.CharField(max_length=13, primary_key=True, default="")
    spare_part = models.ForeignKey(Spare_part, on_delete=models.CASCADE, default=None)
    date = models.DateField(default=None)
    status = models.CharField(max_length=1, default="1")
    details = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.sid + " : "  + self.spare_part.name

    def getSavejobDetails(self):
        savejobDetails = SavejobDetails.objects.filter(order=self)
        return savejobDetails
    def getStatus(self):
        if self.status == '1':
            return 'ยังไม่ส่งคืนรถ'
        elif self.status == '2':
            return 'ส่งคืนรถแล้ว'


class SavejobDetails(models.Model):
    savejob=models.ForeignKey(Savejob, on_delete=models.CASCADE, default=None)
    assignment=models.ForeignKey(Assignment, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.savejob.sid + " : " + self.assignment.agid + " " + self.assignment.details



class Samplesale(models.Model): # ตารางสมมุติ เอาไว้เก็บยอดขาย เพื่อเอาไปทำ Dashboard
    spare_part = models.ForeignKey(Spare_part, on_delete=models.CASCADE, default=None)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, default=None)
    getjop = models.ForeignKey(Getjop, on_delete=models.CASCADE, default=None)
    datesale = models.DateField(default=None)
    amount = models.IntegerField(default=0)  #ยอดขาย
    def __str__(self):
        return "Hey: " + str(self.id) + ":" + self.spare_part.name + ", " + str(self.datesale.year) + ", " + str(self.amount)

class Confirms(models.Model):
    savejob = models.ForeignKey(Savejob, on_delete=models.CASCADE, default=None)
