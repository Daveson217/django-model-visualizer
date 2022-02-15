from pprint import pprint
from django.shortcuts import render
from django.views.generic.base import TemplateView
from pages.models import Article
from django.http import JsonResponse


# Create your views here.
class RelationalModelVisualizerView(TemplateView):
    template_name = "relational_model_visualizer.html"
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)                    
        return self.render_to_response(context)

def get_database_model_data(request):
    """This view returns a dictionary containing all the models, fields, and options given a set of models
    """    
    instance = Article()
    def get_fields_and_properties(models: list) -> dict:
    
        database_model_data = {} 
        """ STRUCTURE OF database_model_data dictionary
        database_model_data  = {
            'model1' : {
                'field1': {
                    'option1': 'value1',
                    'option2': 'value12',
                },
                'field2': {
                    'option1': 'value1',
                    'option2': 'value12',
                }
            },
            
            'model2' : {
                'field1': {
                    'option1': 'value1',
                    'option2': 'value12',
                },
                'field2': {
                    'option1': 'value1',
                    'option2': 'value12',
                }
            },
            
        }"""
        
        ALLOWED_FIELD_OPTIONS = [
            'null', 'blank', 'choices', 'db_column', 'db_index', 'db_tablespace', 'default',
            'editable', 'help_text', 'primary_key', 'unique', 
            'unique_for_date', 'unique_for_month', 'unique_for_year', 'verbose_name', 
            # 'error_messages', 'validators'
        ]
        
        for model in models:            
            fields = [field for field in model._meta.fields] # List of fields in model     
            property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]     
            database_model_data[model.__name__] = {} # Add a particular model to dictionary
                
            for field in fields + property_names:
                # Add fields as keys to database_model_data and dictionary of attributes and values as values                
                database_model_data[model.__name__][str(field)] = dict([attr, getattr(field, attr)] for attr in dir(field) if not attr.startswith('_') and not callable(getattr(field, attr)))                                        
                
                new_field_option_dict = {} # Dictionary of all the options initialized on a field e.g models.CharField(max_length=50, unique=True)
                for option in ALLOWED_FIELD_OPTIONS:
                    if option in database_model_data[model.__name__][str(field)].keys(): # Check if key exists i.e. was passed as an argument when initializing the field
                        # Key exists, continue                       
                        new_field_option_dict[option] = database_model_data[model.__name__][str(field)][option]
                new_field_option_dict['className'] = repr(field)
                database_model_data[model.__name__][str(field)] = new_field_option_dict  # Replace the options dictionary with the newly created one           
            
                
        return database_model_data
    #pprint(get_fields_and_properties([Article]))
    return JsonResponse(get_fields_and_properties([Article]), safe=False)
    #model = models[0]
    #field_names = [f.name for f in model._meta.fields]
    #print(model._meta.fields, '\n')
    #property_names = [name for name in dir(model) if isinstance(getattr(model, name), property)]   
    #print(property_names)              
    #return dict((name, getattr(instance, name)) for name in field_names + property_names)