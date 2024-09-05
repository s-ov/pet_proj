from django.db import models


class NodeMotor(models.Model):
    """
        The class represents nodes motors.
    """

    SYMBOL_CHOICES = [
        ('▲', 'Трикутник'),
        ('✳', 'Зірка'),
    ]
    
    power = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    round_per_minute = models.PositiveSmallIntegerField(default=0)
    connection = models.CharField(max_length=1, choices=SYMBOL_CHOICES, default='▲',)
    amperage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Двигун вузла'
        verbose_name_plural = 'Двигуни'

    def __str__(self):
        return str(self.power)


class Node(models.Model):
    """
        The class for nodes creation.
    """

    NODE_TYPES = [
        ('Засувка', 'Засувка'),
        ('Засувка загружна', 'Засувка загружна'),
        ('Засувка вигружна', 'Засувка вигружна'),
        ('Kонвеєр', 'Kонвеєр'),
        ('Норія', 'Норія'),
        ('Пробовідбірник', 'Пробовідбірник'),
        ('Вент. аспіраційний', 'Вент. аспіраційний'),
        ('Вент. аераційний', 'Вент. аераційний'),
        ('Сепаратор очистки', 'Сепаратор очистки'),
        ('Клапан перекидний', 'Клапан перекидний'),
        ('Клапан 3-х ходовий', 'Клапан 3-х ходовий'),
        ('Вентилятор', 'Вентилятор'),
        ('Вентилятор даховий', 'Вентилятор даховий'),
        ('Шнек зачисний', 'Шнек зачисний'),
    ]
    name = models.CharField(max_length=25, choices=NODE_TYPES)
    index = models.CharField(unique=True, max_length=10)
    level = models.ForeignKey('work_tower.WorkTowerLevel', 
                              on_delete=models.PROTECT, 
                              related_name='nodes', 
                              blank=True, null=True)
    motor = models.ForeignKey('NodeMotor', 
                              on_delete=models.PROTECT, 
                              related_name='nodes',
                              blank=True, null=True)
    mcc = models.ForeignKey('mcc.MotorControlCenter', 
                            on_delete=models.CASCADE, 
                            related_name='mcc', 
                            blank=True, null=True)
    
    class Meta:
        verbose_name = 'Вузол'
        verbose_name_plural = 'Вузли'

    def __str__(self):
        return f'{self.name}_{self.index}'
