from django.utils import simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from Utils.models import ModelMapDictionary

def setData(request):
    print "Setting data"
    jsonobj = JsonDataObject()
    if request.method == 'POST':
        try:
            modelmapid      = request.POST.get('model_map_id', None)
            obj_id          = request.POST.get('obj_id', None)
            value           = request.POST.get('value', None)
            row             = ModelMapDictionary.objects.get(id=modelmapid)
            model_name      = row.model_name
            app_label       = row.app_name
            attribute_name  = row.attribute_name
            print "Saving",row,model_name,app_label,attribute_name
            
            model_type = ContentType.objects.get(app_label=app_label, model=model_name)
            inst = model_type.model_class().objects.get(id=obj_id)
            setattr(inst, attribute_name, value)
            inst.save()
            
            jsonobj.success = 1 
                    #code
        except Exception as e:
            print "Error",e.strerror
            jsonobj.success = 0
            jsonobj.errormessage=e.strerror
        return jsonobj.getJsonHttpResponse()
    return jsonobj.getJsonHttpResponse()

class JsonDataObject(object):
    def __init__(self):
        self.success = 0
        self.errormessage = ""
        self.attributeDictionary = {}
    def getJsonString(self):
        self.attributeDictionary["success"] = self.success
        self.attributeDictionary["errormessage"] = self.errormessage
        return simplejson.dumps(self.attributeDictionary)
    def getJsonHttpResponse(self):
        return HttpResponse(self.getJsonString())

