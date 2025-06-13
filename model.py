from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

def animales(img):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(img).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return(class_name[2:], confidence_score)






def tipo_m(tipo):
    global confidence_score, respuesta_usuario

async def tipo_f(tipo, ctx, bot):
    datos_m = {
        "Perros": {
            "Comida": ["pueden comer pollo, res, salmón, atún, zanahoria, calabaza y purina"],
            "Vacunas": ["Vacunas recomendadas: Polivalente, Rabia, Moquillo canino, Hepatitis infecciosa canina y Leptospirosis"],
            "Cuidado": ["Deben comer 2 veces al día y salir a pasear 90 minutos diarios."]
        },
        "Gatos": {
            "Comida": ["pueden comer pollo, res, salmón, atún y purina"],
            "Vacunas": ["Vacunas recomendadas: Panleucopenia felina, Rinotraqueitis, Calcivirosis, Leucemia felina, Rabia"],
            "Cuidado": ["Juguetes para exploración, espacio para afilar sus uñas."]
        },
        "Conejos": {
            "Comida": ["Hojas verdes de zanahoria, apio, espinacas, heno, zanahorias y frutas como premios"],
            "Vacunas": ["Vacunas recomendadas: Mixomatosis, Hemorragia vírica del conejo (RHDV)"],
            "Cuidado": ["Interacción social, ejercicio y hábitat adecuado."]
        }
    }

    if confidence_score > 0.50:
        await ctx.send(f"El animal detectado es {tipo}")
        await ctx.send("Escribe 1 si quieres saber sobre la alimentación, 2 sobre vacunación, y 3 sobre higiene y cuidado.")
        await ctx.send("RECUERDA QUE TODA ESTA INFORMACIÓN ES RECOMENDABLE QUE LA CONSULTES CON UN VETERINARIO.")

        def check(m):
            return m.author == ctx.author

        mensaje = await bot.wait_for('message', check=check)
        respuesta_usuario = int(mensaje.content)

        if tipo in datos_m:  
            if respuesta_usuario == 1:
                await ctx.send(f"Información sobre alimentación: {datos_m[tipo]['Comida'][0]}")
            elif respuesta_usuario == 2:
                await ctx.send(f"Información sobre vacunación: {datos_m[tipo]['Vacunas'][0]}")
            elif respuesta_usuario == 3:
                await ctx.send(f"Información sobre cuidado: {datos_m[tipo]['Cuidado'][0]}")
            else:
                await ctx.send("Respuesta no válida. Ingresa 1, 2 o 3.")
        else:
            await ctx.send("No reconozco ese animal en la base de datos.")
    else:
        await ctx.send("No te puedo decir qué es esa imagen.")


