import unicodedata

from django.db import models


# Create your models here.
class Proyecto(models.Model):
    codigo = models.CharField(max_length=20)
    numero_proyecto = models.CharField(max_length=50)
    short_url = models.CharField(max_length=20)
    congresistas = models.TextField(blank=True)

    # migrate from date as string
    fecha_presentacion = models.DateField(null=False)
    titulo = models.TextField(blank=True)
    expediente = models.URLField(max_length=200, blank=True)
    pdf_url = models.URLField(max_length=200, blank=True)
    seguimiento_page = models.URLField(max_length=200, blank=True)

    # migrate from timestamp field
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)

    # > v1.1.1
    proponente = models.TextField(null=True, blank=True, default='')
    grupo_parlamentario = models.TextField(blank=True, default='')
    iniciativas_agrupadas = models.TextField(null=True, blank=True, default='')
    nombre_comision = models.TextField(null=True, blank=True, default='')
    titulo_de_ley = models.TextField(null=True, blank=True, default='')
    numero_de_ley = models.TextField(null=True, blank=True, default='')


class Seguimientos(models.Model):
    """Keep records regarding each project (seguimiento). This info is shown
    in the ``seguimiento_page``. For example: http://bit.ly/1uSXA5X
    It has a many-to-one relationship with model ``Proyecto`` a foreign key.
    """
    fecha = models.DateField(blank=True)
    evento = models.TextField(blank=True)
    proyecto = models.ForeignKey(Proyecto)


class Expedientes(models.Model):
    """Keep records regarding events in Expediente page. This info is shown
    in the ``seguimiento_page``. For example: http://bit.ly/1uSXA5X
    It has a many-to-one relationship with model ``Proyecto`` a foreign key.
    """
    fecha = models.DateField(blank=True)
    evento = models.TextField(blank=True)
    pdf_url = models.URLField(blank=True)
    proyecto = models.ForeignKey(Proyecto)


class Slug(models.Model):
    """A translation table between a Congresista name and a slug to be used
    as hiperlink."""
    nombre = models.CharField(max_length=200)
    ascii = models.CharField(max_length=200, help_text='nombre sin caracteres escpeciales')
    slug = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.ascii = unicodedata.normalize('NFKD', self.nombre).encode('ascii', 'ignore').decode('utf-8')
        super(Slug, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
