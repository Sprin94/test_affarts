from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

class Person(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    gender = models.CharField('Пол', choices=Gender.choices, max_length=6)

    class BloodType(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'
        A_NEGATIVE = 'A-', 'A-'
        B_POSITIVE = 'B+', 'B+'
        B_NEGATIVE = 'B-', 'B-'
        AB_POSITIVE = 'AB+', 'AB+'
        AB_NEGATIVE = 'AB-', 'AB-'
        O_POSITIVE = 'O+', 'O+'
        O_NEGATIVE = 'O-', 'O-'

    blood_type = models.CharField('Группа крови', choices=BloodType.choices, max_length=6)
    is_workless = models.BooleanField('Безработный', null=True)
    is_married = models.BooleanField('В браке')  # поле избыточно т.к. у нас есть таблицы Marriage по которой можно проверить


class Residence(models.Model):
    city = models.CharField(max_length=100) # в боевой БД лучше вынести в отдельную таблицу
    postcode = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    registered_to = models.ForeignKey(Person, related_name='estate', on_delete=models.CASCADE)
    tenant = models.ManyToManyField(Person, through='ResidenceTenant', related_name='residence')


class ResidenceTenant(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    residence = models.ForeignKey(Residence, on_delete=models.CASCADE)


class Marriage(models.Model):
    person_1 = models.ForeignKey(Person, related_name='marriage_1', on_delete=models.CASCADE)
    person_2 = models.ForeignKey(Person, related_name='marriage_2', on_delete=models.CASCADE)
    start = models.DateField()
    finish = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(person_1=models.F('person_2')),
                name='No self',
            ),
        ]

    def clean(self):
        if (
            Marriage.objects.filter(
                models.Q(person_1=self.person_1) | models.Q(person_1=self.person_2) |
                models.Q(person_2=self.person_1) | models.Q(person_2=self.person_2)
            ).filter(models.Q(finish=None)).exclude(person_1=self.person_1, person_2=self.person_2)
        ):
            raise ValidationError('У одного из участников уже есть активный брак')
        if self.person_1 == self.person_2:
            raise ValidationError('Нельзя создать брак между 1 пользователем')


class Action(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='actions')
    description = models.TextField()
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    date = models.DateField()
