from django.db import models
from django.conf import settings

# Language Master
class Language(models.Model):    
    # Language id field
    # id = models.AutoField(primary_key=True,unique=True,blank=False)
    # Language name field
    name = models.CharField(max_length=20)
    # Language Code 
    code = models.CharField(max_length=4,blank=True,default=None)
    # Language Status field
    status = models.BooleanField(default=True)
    # Language date added field
    date_added = models.DateTimeField(auto_now_add=True)
    # Language date updated field
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # return language data by id if id not found its return False
    def getLanguagebyId(self, id = None):        
        if id:   
            try:
                returnData = Language.objects.get(id = id)
                return returnData
            except:
                return False
        else:
            return False

# country and country_mapping_language normalize 
class Country(models.Model):
     # Country field Status
    status = models.BooleanField(default=True)
    # Date added field
    date_added = models.DateTimeField(auto_now_add=True)
    # date updated field
    date_updated = models.DateTimeField(auto_now=True)
    # model return name
    def __str__(self):
        return str(self.id)

    # model function return data by country id
    def getCountrybyId(self, id = None):
        if id:
            try:
                returnData = Country.objects.get(id = id)
                return returnData
            except:
                return False
        else:
            return False    

class CountryMappingLanguage(models.Model):
    # Foriegn Key set Country ID
    country_foriegn = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="country_id",null=False)
    # Foriegn Key Langauge ID
    langauge = models.ForeignKey(Language,on_delete=models.CASCADE,related_name="langauge_id",null=False)
    # Country_Name
    country = models.CharField(max_length=50,blank=False)
    # Date added field
    date_added = models.DateTimeField(auto_now_add=True)
    # date updated field
    date_updated = models.DateTimeField(auto_now=True)
    # model return name
    def __str__(self):
        return self.country

    # model function return data by state id
    def getCountryMappingbyId(self, id = None):
        if id:
            try:
                returnData = CountryMappingLanguage.objects.get(id = id)
                return returnData
            except:
                return False
        else:
            return False
    # Delete Entries before entering new entries
    def deleteCountryMappingByForiegnId(self, foriegn_id = 0):
        if foriegn_id:
            status = CountryMappingLanguage.objects.filter(country_foriegn_id = foriegn_id).delete()
            return status
        else:
            return False        


# state and state_mapping_language normalize 
class State(models.Model):
    # country foriegn key
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=False)
     # State field Status
    status = models.BooleanField(default=True)
    # Date added field
    date_added = models.DateTimeField(auto_now_add=True)
    # date updated field
    date_updated = models.DateTimeField(auto_now=True)
    # model return name
    def __str__(self):
        return str(self.id)

    # model function return data by state id
    def getStatebyId(self, id = None):
        if id:
            try:
                returnData = State.objects.get(id = id)
                return returnData
            except:
                return False
        else:
            return False    

class StateMappingLanguage(models.Model):
    # Foriegn Key set    
    state_foriegn = models.ForeignKey(State,on_delete=models.CASCADE,related_name="state_id",null=False)
    # Foriegn Key Langauge ID
    state_langauge = models.ForeignKey(Language,on_delete=models.CASCADE,related_name="state_langauge_id",null=False)        
    # State_Name
    state = models.CharField(max_length=50,blank=False)
    # Date added field
    date_added = models.DateTimeField(auto_now_add=True)
    # date updated field
    date_updated = models.DateTimeField(auto_now=True)
    # model return name
    def __str__(self):
        return self.state

    # model function return data by state id
    def getStateMappingbyId(self, id = None):
        if id:
            try:
                returnData = StateMappingLanguage.objects.get(id = id)
                return returnData
            except:
                return False
        else:
            return False
    
    # Delete Entries before entering new entries
    def deleteStateMappingByForiegnId(self, foriegn_id = 0):
        if foriegn_id:
            status = StateMappingLanguage.objects.filter(state_foriegn_id = foriegn_id).delete()
            return status
        else:
            return False        


# from auditlog.registry import auditlog
# auditlog.register(Language)
# auditlog.register(Country)
# auditlog.register(CountryMappingLanguage)
# auditlog.register(State)
# auditlog.register(StateMappingLanguage)