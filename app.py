from flask import Flask , render_template , request , jsonify
import prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API escuchando las solicitudes POST y prediciendo sentimientos
@app.route('/predict' , methods = ['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status' : 'error',
                    'message' : 'Reseña vacía'}
    
    else:

        # Llamando al método predict del módulo prediction.py
        sentiment , path = prediction.predict(review)
        response = {'status' : 'success',
                    'message' : 'Listo',
                    'sentiment' : sentiment,
                    'path' : path}

    return jsonify(response)


# Creando una API para guardar la resela, el usuario hace clic en el botón Guardar
@app.route('/save' , methods = ['POST'])
def save():

    # Extrayendo la fecha, nombre del producto, reseña, sentimiento asociado a los datos JSON
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # Creando una variable final separada por comas
    data_entry = date + "," + product + "," + review + "," + sentiment

    # Abriendo el archivo en modo "append"
    f =  open ('./static/assets/datafiles/uspdated_product_dataset.csv', 'a')
    # Añadiendo los datos en el archivo
    f.write(data_entry + '\n')
    # Regresando un mensaje de éxito
    return jsonify({'status' : 'success' , 
                    'message' : 'Datos ingresados'})


if __name__  ==  "__main__":
    app.run(debug = True)
