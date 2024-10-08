from typing import Any
from django import forms

from .models import *

class TerminosYCondicionesForm(forms.Form):

    consentimiento = forms.BooleanField(label="He leído esta información sobre la investigación y acepto participar.")

    def __init__(self, user=None, *args, **kwargs):
        self.user = user    
        super().__init__(*args, **kwargs)

    def save(self):
        return        
    

class CodigoForm(forms.Form):
    dni = forms.CharField(label="Ingrese los últimos 3 números del DNI del paciente", min_length=3, max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Ingrese el primer nombre del paciente", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get('dni')
        nombre = cleaned_data.get('nombre')
        codigo = f'{self.user.username}-{dni}-{nombre}'
        try:
            _ = Cpqol.objects.get(
                user=self.user,
                codigo=codigo
            )
            self.add_error('dni', "Ya posee un CPQOL con esta combinación de DNI y NOMBRE")
        except:
            pass
            
        return cleaned_data
    


    def save(self):
        dni = self.cleaned_data.get('dni')
        nombre = self.cleaned_data.get('nombre')
        codigo = f'{self.user.username}-{dni}-{nombre}'
        cpqol_instance = Cpqol.objects.create(
            user=self.user,
            codigo=codigo
        )
        return cpqol_instance


class BaseForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user        
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control h5'})


    def save(self, cpqol, atributo):
        instance = super().save(commit=True)
        setattr(cpqol, atributo, instance)
        cpqol.save()
        return instance


class TutorForm(BaseForm):
    class Meta:
        model = Tutor
        fields = '__all__'
        widgets = {
            'estado_salud': forms.RadioSelect,
        }

class PacienteForm(BaseForm):
    class Meta:
        model = Paciente
        fields = '__all__'


class SentimientosForm(BaseForm):
    class Meta:
        model = Sentimientos
        fields = '__all__'
        widgets = {
            "hacer_cosas": forms.RadioSelect,
            "uno_mismo": forms.RadioSelect,
            "motivacion": forms.RadioSelect,
            "oportunidades": forms.RadioSelect,
            "aspecto_fisico": forms.RadioSelect,
        }


class RelacionesForm(BaseForm):
    class Meta:
        model = Relaciones
        fields = '__all__'
        widgets = {
            "con_gente": forms.RadioSelect,
            "otros_chichos": forms.RadioSelect,
            "con_adultos": forms.RadioSelect,
            "con_amigos": forms.RadioSelect,
            "aceptacion_otros_chicos": forms.RadioSelect,
            "aceptacion_adultos": forms.RadioSelect,
            "aceptacion_gente": forms.RadioSelect,
            "cosas_nuevas": forms.RadioSelect,
            "comunicacion_conocidos": forms.RadioSelect,
            "comunicacion_extranios": forms.RadioSelect,
            "comunicacion_otros_con_el": forms.RadioSelect,
            "comunicacion_tecnologia": forms.RadioSelect,
        }        

class FamiliaForm(BaseForm):
    class Meta:
        model = Familia
        fields = '__all__'
        widgets = {
            "apoyo_flia": forms.RadioSelect,
            "viaje_flia": forms.RadioSelect,
            "aceptacion_flia": forms.RadioSelect,
        }                

class ParticipacionForm(BaseForm):
    class Meta:
        model = Participacion
        fields = '__all__'
        widgets = {
            "recreativas": forms.RadioSelect,
            "deportivas": forms.RadioSelect,
            "eventos_sociales": forms.RadioSelect,
            "en_su_comunidad": forms.RadioSelect,
        }                        

class EscuelaForm(BaseForm):
    class Meta:
        model = Escuela
        fields = '__all__'
        widgets = {
            "otros_chicos_escuela": forms.RadioSelect,
            "como_lo_integran": forms.RadioSelect,
            "profesores": forms.RadioSelect,
            "otros_alumnos": forms.RadioSelect,
            "otros_docentes": forms.RadioSelect,
            "mismo_trato": forms.RadioSelect,
            "participacion_colegio": forms.RadioSelect,
        }                

class SaludForm(BaseForm):
    class Meta:
        model = Salud
        fields = '__all__'
        widgets = {
            "hacer_cosas_solo": forms.RadioSelect,
            "movilidad": forms.RadioSelect,
            "independencia": forms.RadioSelect,
            "moverse_dentro_barrio": forms.RadioSelect,
            "transporte": forms.RadioSelect,
            "brazos_y_manos": forms.RadioSelect,
            "piernas": forms.RadioSelect,
            "vestirse": forms.RadioSelect,
            "beber": forms.RadioSelect,
            "ir_al_banio": forms.RadioSelect,
        }              

class DolorForm(BaseForm):
    class Meta:
        model = Dolor
        fields = '__all__'
        widgets = {
            "salud_gral": forms.RadioSelect,
            "suenio": forms.RadioSelect,
            "cuanto_dolor": forms.RadioSelect,
            "nivel_dolor": forms.RadioSelect,
            "nivel_incomodidad": forms.RadioSelect,
            "como_afecta": forms.RadioSelect,
            "impedimentos": forms.RadioSelect,
            "no_disfrutar_dia": forms.RadioSelect,
        }             

class ServiciosForm(BaseForm):
    class Meta:
        model = Servicios
        fields = '__all__'
        widgets = {
            "acceso_tratamiento": forms.RadioSelect,
            "acceso_terapia": forms.RadioSelect,
            "acceso_atencion_medica": forms.RadioSelect,
            "acceso_pediatria": forms.RadioSelect,
            "acceso_ayuda_aprendizaje": forms.RadioSelect,
        }                    










