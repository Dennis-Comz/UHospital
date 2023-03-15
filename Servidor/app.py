import json
from flask_restful import Api
from flask import Flask, request
from flask_cors import CORS
from Appointment import Appointment
from Doctor import Doctor
from Medicine import Medicine
from Nurse import Nurse
from Patient import Patient

app = Flask(__name__)
CORS(app)
api = Api(app)

patients, doctors, nurses, medicines, sessions, appointments, appointmentsAccep = list(), list(), list(), list(), list(), list(), list()

@app.route('/', methods = ['GET'])
def home():
    return 'API FUNCIONA'

@app.route('/login', methods = ['POST'])
def postLogin():
    content = request.get_json()
    username = content['username']
    password = content['password']
    
    if (username == 'admin' and password == '1234'):
            return {'path': 'admin'}
    else:        
        for value in patients:
            if username == value.name and password == value.password:
                sessions.append(value)            
                return {'path': 'paciente'}
        for value in doctors:
            if username == value.name and password == value.password:
                sessions.append(value)
                return {'path': 'doctor'}
        for value in nurses:
            if username == value.name and password == value.password:
                sessions.append(value)
                return {'path': 'enfermera'}
    
    return {'dato': 'NO'}

@app.route('/add-patient', methods = ['POST'])
def postAddPatient():
    content = request.get_json()
    name = content['name']
    lastname = content['lastname']
    birthday = content['birthday']
    gender = content['gender']
    password = content['password']
    phone = content['phone']
    
    patients.append(Patient(name,lastname,birthday,gender,password,phone))
    return {'message':'REGISTRADO CORRECTAMENTE'}

@app.route('/load-patients', methods=['POST'])
def postLoadPatients(): 
    content = request.get_json()
    for patient_ in content['result']:
        patients.append(Patient(patient_['Nombre'],patient_['Apellido'],patient_['Fecha'],patient_['Sexo'],patient_['Contraseña'], patient_['Teléfono']))

    return {'message': 'patients cargados'}
    
@app.route('/load-doctors', methods=['POST'])
def postLoadDoctors():
    content = request.get_json()
    contador = 0
    global name 
    global lastname
    global birthday
    global gender
    global phone
    for i in range(0, len(content['result'])):
        for value in content['result'][i]:
            # print(value + str(contador))
            if contador == 0:
                name = content['result'][i][str(value)]
                # print(name)
            elif contador == 1:
                lastname = content['result'][i][str(value)]
                # print(lastname)
            elif contador == 2:
                birthday = content['result'][i][str(value)]
                # print(birthday)
            elif contador == 3:
                gender = content['result'][i][str(value)]
                # print(gender)
            elif contador == 4:
                password = content['result'][i][str(value)]
                # print(password)
            elif contador == 5:
                especialidad = content['result'][i][str(value)]
            elif contador == 6:
                phone = content['result'][i][str(value)]
                # print(phone)
            contador += 1
            if contador > 6:
                contador = 0
                doctors.append(Doctor(name,lastname,birthday,gender,password,especialidad,phone))
    
    return {'message': 'doctors cargados'}

@app.route('/load-nurses', methods=['POST'])
def postLoadNurses(): 
    content = request.get_json()
    contador = 0
    global name 
    global lastname
    global birthday
    global gender
    global phone
    for i in range(0, len(content['result'])):
        for value in content['result'][i]:
            # print(value + str(contador))
            if contador == 0:
                name = content['result'][i][str(value)]
                # print(name)
            elif contador == 1:
                lastname = content['result'][i][str(value)]
                # print(lastname)
            elif contador == 2:
                birthday = content['result'][i][str(value)]
                # print(birthday)
            elif contador == 3:
                gender = content['result'][i][str(value)]
                # print(gender)
            elif contador == 4:
                password = content['result'][i][str(value)]
                # print(password)
            elif contador == 5:
                phone = content['result'][i][str(value)]
                # print(phone)
            contador += 1
            if contador == 6:
                contador = 0
                nurses.append(Patient(name,lastname,birthday,gender,password,phone))
            
    return {'message': 'nurses cargados'}

@app.route('/load-medicines', methods=['POST'])
def postLoadMedicines():
    content = request.get_json()
    for i in content['result']:
        if i['Nombre'] != '':
            name = i['Nombre']
            price = i['Precio']
            description = i['Descripcion'] 
            quantity = i['Cantidad']
            
            medicines.append(Medicine(name,price,description,quantity))
    
    return {'message': 'medicines cargados'}
                   
# Getters de patients y nurses
@app.route('/cantidadpatients', methods=['GET'])
def getCantidadpatients():
    return {'cantidad': str(len(patients))}

@app.route('/datospatients', methods=['GET'])
def getDatospatients():
    results = json.dumps([obj for obj in patients])
    jsdata = json.dumps({"results": results})
    return jsdata

@app.route('/cantidadnurses', methods=['GET'])
def getCantidadnurses():
    return {'cantidad': str(len(nurses))}
    
@app.route('/datosnurses', methods=['GET'])
def getDatosnurses():
    results = [obj.to_dict() for obj in nurses]
    jsdata = json.dumps({"results": results})
    return jsdata

# Getters de doctors
@app.route('/cantidaddoctors', methods=['GET'])
def getCantidaddoctors():
    return {'cantidad': str(len(doctors))}

@app.route('/datosdoctors', methods=['GET'])
def getDatosdoctors():
    results = [obj.to_dict() for obj in doctors]
    jsdata = json.dumps({"results": results})
    return jsdata

# Getters de medicines
@app.route('/cantidadmedicines', methods=['GET'])
def getCantidadmedicines():
    return {'cantidad': str(len(medicines))}

@app.route('/datosmedicines', methods=['GET'])
def getDatosmedicines():
    results = [obj.to_dict() for obj in medicines]
    jsdata = json.dumps({"results": results})
    return jsdata

@app.route('/cerrarSesion', methods=['GET'])
def postCerrarSesion():
    sessions.clear()
    return {'message': 'Sesion Cerrada'}

@app.route('/configuracion', methods=['GET'])
def getConfiguracion():
    results = [obj.to_dict() for obj in sessions]
    jsdata = json.dumps({"results": results})
    return jsdata

@app.route('/cita', methods=['POST'])
def postCita():
    content = request.get_json()
    fecha = content['fecha']
    hora = content['hora']
    motivo = content['motivo']
    username = content['username']

    appointments.append(Appointment(username, fecha, hora, motivo))
    return {'message': 'Cita Generada', 'username': username}
    
@app.route('/cantidadCitas', methods=['GET'])
def getCantidadCitas():
    return {'cantidad': str(len(appointments))}

@app.route('/datosCitas', methods=['GET'])
def getDatosCitas():
    results = [obj.to_dict() for obj in appointments]
    jsdata = json.dumps({"results": results})
    return jsdata

@app.route('/citasAceptadas', methods=['POST'])
def postCitasAceptadas():
    content = request.get_json()
    numero = content['No']
    fecha = content['Fecha']
    hora = content['Hora']
    motivo = content['Motivo']
    doctor = content['Doctor']
    
    appointments.append(Appointment(numero,fecha,hora,motivo,doctor))
    return {'message': 'Cita Aceptada'}

@app.route('/aceptadas', methods=['GET'])
def getAceptadas():
    results = [obj.to_dict() for obj in appointments]
    jsdata = json.dumps({"results": results})
    return jsdata

@app.route('/actualizar', methods=['POST'])
def postActualizar():
    content = request.get_json()
    name = content['nombre']
    lastname = content['apellido']
    username = content['usuario']
    password = content['password']
    fechaNac = content['fechaNac']
    oldUser = content['oldUsuario']
    
    for i in range(0, len(patients)):
        if patients[i].username == oldUser:
            patients[i].name = name
            patients[i].lastname = lastname
            patients[i].username = username
            patients[i].password = password
            patients[i].birthday = fechaNac
            return {'message': 'Actualizado'}
    for i in range(0, len(nurses)):
        if nurses[i].username == oldUser:
            nurses[i].name = name
            nurses[i].lastname = lastname
            nurses[i].username = username
            nurses[i].password = password
            nurses[i].birthday = fechaNac
            return {'message': 'Actualizado'}
    for i in range(0, len(doctors)):
        if patients[i].username == oldUser:
            doctors[i].name = name
            doctors[i].lastname = lastname
            doctors[i].username = username
            doctors[i].password = password
            doctors[i].birthday = fechaNac
            return {'message': 'Actualizado'}
    
        
if __name__ == '__main__':
    app.run(host= '192.168.0.11')
    app.run(debug=True)