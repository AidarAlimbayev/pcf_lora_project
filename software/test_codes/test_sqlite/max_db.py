from audioop import maxpp
from email import message
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from urllib.parse import DefragResult
from django.db import models
from django.forms import RegexField
from datetime import date

Animal_list = (
    [1, 'Cow'],
    [2, 'Horse'],
    [3, 'Goat']
)

class Error(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField("Error")

    class Meta:
        verbose_name = ("Error")
        verbose_name_plural = ("Errors")

    def __str__(self):
        return self.name

class ErrorMessage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(Error, verbose_name="Error", on_delete=CASCADE, blank=True)
    message = models.TextField("Error message", blank=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message



class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=50)
    country = models.CharField("Country", max_length=50)
    email = models.EmailField("Email", max_length=254)
    site = models.URLField("Site", max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"

    def __str__(self):
        return self.name


class EquipmentType(models.Model):
    id = models.AutoField('Equipment type', primary_key=True)
    name = models.CharField("Type of equipment",
                            max_length=150, default='Scales')

    class Meta:
        verbose_name = "Equipment Type"
        verbose_name_plural = "Equipment Types"

    def __str__(self):
        return self.name

  #  def get_absolute_url(self):
  #      return reverse("EquipmentType_detail", kwargs={"pk": self.pk})


class ResponsiblePerson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=150)
    position = models.CharField("Position", max_length=150, blank=True)
    email = models.EmailField("Email", max_length=254)
    office = models.CharField("Office", max_length=6, blank=True)
    phone = models.CharField("Phone", max_length=16)
    work_phone = models.CharField("Work phone", max_length=8, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Responsible Person"
        verbose_name_plural = "Responsible Persons"

    def __str__(self):
        return self.name

   # def get_absolute_url(self):
   #     return reverse("ResponsiblePerson_detail", kwargs={"pk": self.pk})


class TechnicalContact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=150)
    position = models.CharField("Position", max_length=150, blank=True)
    email = models.EmailField("Email", max_length=254)
    office = models.CharField("Office", max_length=6, blank=True)
    phone = models.CharField("Phone", max_length=16)
    work_phone = models.CharField("Work phone", max_length=8, blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Technical Contact"
        verbose_name_plural = "Technical Contacts"

    def __str__(self):
        return self.name

 #   def get_absolute_url(self):
  #      return reverse("TechnicalContact_detail", kwargs={"pk": self.pk})


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    type_of_equipment = models.ManyToManyField(
        EquipmentType, verbose_name="Type of equipment")
    name = models.CharField("Model", max_length=50)
    description = models.TextField("Description", blank=True)
    serial_number = models.CharField(
        "Serial number", max_length=100, unique=True)
    manufacturer = models.ForeignKey(
        Manufacturer, verbose_name="Manufacturer", on_delete=models.CASCADE
    )
    manual = models.FileField("Manual", upload_to='manual/', blank=True)
    #inventory_number = models.CharField(
    #    "Inventory number", max_length=20, unique=True)
    photo = models.ImageField("Photo", null=True, blank=True)
    #service = models.ForeignKey(
    #    Service, verbose_name="Service", on_delete=models.CASCADE
    #    blank=True)
    responsible_person = models.ManyToManyField(
        ResponsiblePerson, verbose_name="Responsible Person", blank=True)
    technical_contact = models.ManyToManyField(
        TechnicalContact, verbose_name="Technical Contact", blank=True)
    slug = models.SlugField("url", max_length=150, unique=True)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"

    def __str__(self):
        return self.name


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(
        Equipment, verbose_name="equipment", on_delete=models.CASCADE)
    last_service = models.DateField("last service", default=date.today)
    next_service = models.DateField(
        'Next service', null=False, help_text="Please use following format: <em>YYYY-MM-DD</em>.", blank=True)
    spares = models.CharField("Spares", max_length=150, blank=True)
    what_is_done = models.TextField("What is done", blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return str(self.equipment)


class Locality(models.Model):
    id = models.AutoField(primary_key=True)
    locality = models.CharField("Locality", max_length=150)

    class Meta:
        verbose_name = "Locality"
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.locality


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    locality = models.ForeignKey(
        Locality, max_length=150, verbose_name="Locality", null=True,
        on_delete=models.SET_NULL, blank=True
    )
    location = models.CharField("Location", max_length=150, blank=True)  # primary_key = True,
    department = models.CharField(
        'Departament', max_length=64, null=True, blank=True)
    

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):  # unicode?
        return f"{self.locality} - {self.location}"


class Node(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=50, unique=True)
    equipment = models.ForeignKey(
        Equipment, verbose_name="Equipment", on_delete=models.CASCADE
    )
    location = models.ManyToManyField(Location, verbose_name="location")
    error = models.ForeignKey(Error, on_delete=CASCADE, blank=True)
    message = models.ForeignKey(ErrorMessage, on_delete=CASCADE, blank=True)
    
    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"

    def __str__(self):
        return self.name


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(
        Node, verbose_name="Node", on_delete=models.CASCADE
    )
    time = models.DateTimeField('Time', auto_now=True)
    checked = models.BooleanField("Checked", default=False)
    mailWasSent = models.BooleanField("Inform", default=False)

    class Meta:
        verbose_name = ("Notification")
        verbose_name_plural = ("Notifications")

    def __str__(self):
        return str(self.node)

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, verbose_name="Equipment", on_delete=CASCADE)
    event_date = models.DateTimeField("Event Date", auto_now=True)
    boot_id = models.PositiveIntegerField("BootId")
    uptime = models.PositiveIntegerField("Uptime")
    last_shutdown = models.TextField ("Last Shutdown", max_length=50)
    Pcf_Service_Active = models.BooleanField("Daemon active status", default=True)
    Pcf_Service_Enabled = models.BooleanField("Daemon enable status", default=True)
    voltage = models.IntegerField("Voltage", blank=True)
    error = models.ForeignKey(Error, on_delete=CASCADE, blank=True)
    message = models.ForeignKey(ErrorMessage, on_delete=CASCADE, blank=True)
    memory = models.TextField("Memory", blank=True) 

    def __str__(self):
        return str(self.equipment)

class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    animal_type = models.TextField("Animal Type", choices=Animal_list, default=1)
    RIFDNumber = models.TextField("RFID Number", max_length=150)
    burn_date = models.DateField("Date of burn", blank=True)
    age = models.PositiveSmallIntegerField("Age", blant=True, default=0)
    weight = models.FloatField("Weight")
    painted_status = models.BooleanField("Painted status", default=False)
    druged_status = models.BooleanField("Druged status", default=False)
    last_painted_date = models.DateField("Last Painted Date", auto_now=True, blank=True)
    last_druged_date = models.DateField("Last Druged Date", auto_now=True, blank=True)
    painted_id = models.PositiveSmallIntegerField("Painted Number", default='0')
    druged_id = models.PositiveSmallIntegerField("Druged Number", default='0')

    def __str__(self):
        return self.RIFDNumber

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animals"


class Weighing(models.Model):
    id = models.AutoField(primary_key=True)
    RIFDNumber = models.ForeignKey(Animal, on_delete=CASCADE)
    model = models.ForeignKey(Equipment, "Model", max_length=50, on_delete=CASCADE)
    event_date_time = models.DateTimeField("Event date and time")
    real_weight = models.FloatField("Real weight, kg")
    estimated_value = models.FloatField("Real weight, kg")
    uncorrect_value = models.BooleanField("Uncorrect Value", default=False)
    deviation_mean = models.FloatField("Deviation avarage")
    deviation_last = models.FloatField("Deviation Last")
    animal = models.ForeignKey(Animal, verbose_name="Animal Type", blank=True, on_delete=CASCADE)

    def __str__(self):
        return self.real_weight

class Feeder(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=CASCADE)
    animal = models.ForeignKey(Animal, on_delete=CASCADE)
    event_date_time = models.DateTimeField("Event date and time")
    real_weight = models.FloatField("Real weight, kg")
    estimated_value = models.FloatField("Estimated value, kg")
    start_time = models.TimeField("Start time", auto_now=True)
    end_time = models.TimeField("End time", blank=True)
    average = models.FloatField("Average, kg")

    def __str__(self):
        return str(self.equipment)

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Color", max_length=20)
    description = models.TextField("Description", blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Recipe", max_length=150)
    description = models.TextField("Description", blank=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Medicine", max_length=20)
    description = models.TextField("Description", blank=True)

    def __str__(self):
        return self.name

class Sprayer(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=CASCADE)
    animal = models.ForeignKey(Animal, on_delete=CASCADE)
    event_date_time = models.DateTimeField("Event date and time")
    color = models.ForeignKey(Color, on_delete=CASCADE)
    sprinkled = models.BooleanField("Sprinkled", default=False)
    planned_date = models.DateField("Planned date", blank=True)
    count = models.PositiveSmallIntegerField("Count", blank=True)

    def __str__(self):
        return str(self.equipment)

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=CASCADE)
    animal = models.ForeignKey(Animal, on_delete=CASCADE)
    event_date_time = models.DateTimeField("Event date and time")
    medicine = models.ForeignKey(Medicine, default="Green")
    sprinkled = models.BooleanField("Sprinkled", default=False)
    planned_date = models.DateField("Planned date", blank=True)
    count = models.PositiveSmallIntegerField("Count", blank=True)
 
    def __str__(self):
        return str(self.equipment)

class Mixer(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=CASCADE)
    animal = models.ForeignKey(Animal, on_delete=CASCADE)
    event_date_time = models.DateTimeField("Event date and time")
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    sprinkled = models.BooleanField("Sprinkled", default=False)
    planned_date = models.DateField("Planned date", blank=True)
    count = models.PositiveSmallIntegerField("Count", blank=True)
 
    def __str__(self):
        return str(self.equipment)
