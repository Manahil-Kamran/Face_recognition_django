from django import template
from dashboard.models import FaceCoding

register = template.Library()

@register.simple_tag
def get_face_image_url(person):
    if person is None:
        return None
    
    try:
        print("person tracking",person)
        face_coding = FaceCoding.objects.filter(person=person).first()
        print("face coding",face_coding.img_url
              )
        if face_coding and face_coding.img_url:
            return face_coding.img_url
        return None
    except Exception as e:
        # Log the error or handle it as needed
        return None
