import discord
from discord.ext import commands
import os, random
from model import *
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

user_context = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

async def mostrar_info_animal(ctx, tipo, confidence_score):
    datos_m = {
        "perro": {
            "Comida": ["pueden comer pollo, res, salmón, atún, zanahoria, calabaza y purina"],
            "Vacunas": ["Vacunas recomendadas: Polivalente, Rabia, Moquillo canino, Hepatitis infecciosa canina y Leptospirosis"],
            "Cuidado": ["Deben comer 2 veces al día y salir a pasear 90 minutos diarios."]
        },
        "gatos": {
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
    tipo = tipo.strip().lower()
    datos_m = {k.lower(): v for k, v in datos_m.items()}  
    print(f"Confidence Score: {confidence_score}")
    print(f"Tipo detectado: {tipo}")
    print(f"Está en datos_m?: {tipo in datos_m}")
    if confidence_score > 0.90 and tipo in datos_m:
        await ctx.send(f"El animal detectado es **{tipo}**.")
        await ctx.send("Escribe **1** si quieres saber sobre la alimentación, **2** sobre vacunación, y **3** sobre higiene y cuidado.")
        await ctx.send("RECUERDA QUE TODA ESTA INFORMACIÓN ES RECOMENDABLE QUE LA CONSULTES CON UN VETERINARIO.")

        def check_msg(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', timeout=30.0, check=check_msg)
            print(f"Mensaje recibido: {msg.content}")  # Para depuración
            opcion = int(msg.content)

            if opcion == 1:
                await ctx.send(f"Alimentación: {datos_m[tipo]['Comida'][0]}")
            elif opcion == 2:
                await ctx.send(f"Vacunación: {datos_m[tipo]['Vacunas'][0]}")
            elif opcion == 3:
                await ctx.send(f"Cuidado: {datos_m[tipo]['Cuidado'][0]}")
            else:
                await ctx.send("Respuesta no válida. Escribe 1, 2 o 3.")
        except asyncio.TimeoutError:
            await ctx.send("No respondiste a tiempo. Por favor, vuelve a intentarlo.")
        except ValueError:
            await ctx.send("La respuesta debe ser un número (1, 2 o 3).")

    else:
        await ctx.send("No se puede confirmar con suficiente certeza qué animal es.")


# Ahora tu comando check llama directamente a esa función
@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        os.makedirs("./img", exist_ok=True)

        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            await attachment.save(f"./img/{file_name}")
            image_path = f"./img/{file_name}"

            class_name, confidence_score = animales(image_path)

            response_message = f"**Predicción:** {class_name}\n**Confianza:** {confidence_score:.2f}"
            await ctx.send(response_message)

            await mostrar_info_animal(ctx, class_name.strip(), confidence_score)
    else:
        await ctx.send("No ingresaste ninguna imagen.")


bot.run()