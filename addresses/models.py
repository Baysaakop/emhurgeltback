from django.db import models

class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.city.name + ", " + self.name

class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.city.name + ", " + self.district.name + ", " + self.section + ", " + self.address
