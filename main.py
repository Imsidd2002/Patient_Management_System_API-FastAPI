
import json
from fastapi import FastAPI, Path , HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

app = FastAPI()


#pydantic class for patient
class Patient(BaseModel):
    id : Annotated[str, Field(...,description='ID of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city : Annotated[str , Field(...,description='City where you reside')]
    age : Annotated[int, Field(...,gt=0,lt=120,description='Age of the patient')]
    gender : Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height : Annotated[float,Field(...,gt=0,description='Height of the patient in mtrs')]
    weight : Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]

    #as we are computing bmi and verdict on our own we have to use computed_field from python and use it as a constructor
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height **2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
            
#pydantic class if user wants to update the data as the original pydantic class had ...(req) attributes      
class PatientUpdate(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str] , Field(default=None)]
    age : Annotated[Optional[int], Field(gt=0,lt=120,default=None)]
    gender : Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height : Annotated[Optional[float],Field(gt=0, default = None)]
    weight : Annotated[Optional[float],Field(gt=0, default = None)]
    

#loading out patients.json
def load_data():
    with open("patients.json", "r") as file:
        data =  json.load(file)
        return data

#saving new patient into our json file that is used for the post route
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

#routes
@app.get("/")
def hello():
    return {"message": "Patients Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patients records."}

@app.get("/view")
def view():
    data = load_data()
    return data


"""
Path => As patient id is in string format("P001") the user may not know this so we can use Path function which helps providing metadata, validation rulese adn documentation hints for path parameters in your endpoint

HttpException => special buit in exception class in Fast used to return custom HTTP error responses by providing custom error msg and a also proper status code along with extra headers(optional)

(...) => means the path parameter is reqiured

"""

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description= 'ID of the pateint in DB',example= 'P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404, detail='Patient not found')


"""
Query => a utility function in Fast to declare , validate and document query parameter in API endpoints allows to set default values, keep validation rules and also add metadata

"""

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight and BMI'), order : str = Query('asc',description= 'Sort in ascending or descending order')):

    valid_fields = ['height','weight','BMI']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code= 400 , detail=f'Invalid fields choose from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and dsc')
    
    data = load_data()
    sort_order =True if order == 'desc' else False
    sorted_data = sorted(data.values(),key= lambda x :x.get(sort_by,0),reverse= sort_order)
    return sorted_data 


@app.post('/create')
def create_patient(patient : Patient):
    #load existing data
    data = load_data()
    
    #check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400 , detail='Patient already exists')
    
    #add new patient to the db
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    #save into json
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id : str,patient_update : PatientUpdate):
    #loading data
    data = load_data()
    
    #checking if the patient exists or not
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient id not found')
    
    #loading the data about the asked pateint
    existing_patient_info = data[patient_id]
    
    #converting pydantic obj to dic using model_dump
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    #looping through the updated and doing changes in the real data
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    """the work here was done but in our data as we change height or weight the bmi and verdict also changes so to solve this challenge
    we will do the following things
    existing_patient_info > pydantic obj > updated bmi + verdict > pydantic obj to dict using model_dump
    """
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])
    #add this dictionary to data
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Patient Updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id : str):
    data = load_data()
    
    #check if patient is present or not
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'meassage':'Patient Deleted'})