from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from WeddingApp.models import Event, Category, CoverImage
import datetime
from weasyprint import HTML

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    pdf_file = HTML(string=html).write_pdf()
    return pdf_file

class GenerateEventCardPdf(View):
    def get(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        category = event.event_category
        cover_image = event.cover_image_id
        additional_fields_list = event.additional_fields
        fields_data = {field['key']: field['value'] for field in additional_fields_list}
        
        # Get category image URL
        category_image_url = ''
        if category.category_image:
            category_image_url = request.build_absolute_uri(category.category_image.url)
    
        # Get Cover image URL
        cover_image_url = ''
        if cover_image:
            category.events_category_type.first()
            cover_image_url = request.build_absolute_uri(cover_image.image.url)

        context = {
                'today': str(datetime.date.today()),
                'event': event,
                'category': category.category_name,
                'additional_fields': fields_data,
                'category_image_url': category_image_url,
                'cover_image_url': cover_image_url, 
        }
        category_name_lower = category.category_name.lower()
        
        if category_name_lower == "birthday":
            template_name = 'events/event_card_birthday.html'
        elif category_name_lower == "wedding":
            template_name = 'events/event_card_wedding.html'
        elif category_name_lower == "inauguration":
            template_name = 'events/event_card_inauguration.html'
        else:
            template_name = 'events/event_card_custom.html'

        pdf = render_to_pdf(template_name, context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")
    



