import gradio as gr
import math
from datetime import datetime
import requests

# Basic Arithmetic Calculator
def calculator(operation, num1, num2=None):
    try:
        if num2 is None and operation not in ["Square Root", "Cube Root"]:
            return "Error: Second number is required for this operation."

        if operation == "Addition":
            return num1 + num2
        elif operation == "Subtraction":
            return num1 - num2
        elif operation == "Multiplication":
            return num1 * num2
        elif operation == "Division":
            return num1 / num2 if num2 != 0 else "Error: Division by zero!"
        elif operation == "Exponent":
            return num1 ** num2
        elif operation == "Modulus":
            return num1 % num2 if num2 != 0 else "Error: Modulus by zero!"
        else:
            return "Invalid Operation!"
    except Exception as e:
        return f"Error: {str(e)}"

# Logarithm & Exponents
def log_calculator(number, base):
    try:
        return math.log(number, base) if number > 0 and base > 0 and base != 1 else "Error: Invalid values!"
    except Exception as e:
        return f"Error: {str(e)}"

def antilog_calculator(log_value, base):
    try:
        return base ** log_value
    except Exception as e:
        return f"Error: {str(e)}"

def square_root(number):
    return math.sqrt(number) if number >= 0 else "Error: Negative square root!"

def cube_root(number):
    return number ** (1/3)

# BMI & Age Calculators
def calculate_bmi(weight, height):
    try:
        bmi = weight / (height ** 2)
        categories = ["Underweight", "Normal weight", "Overweight", "Obesity"]
        category = categories[0] if bmi < 18.5 else categories[1] if bmi < 24.9 else categories[2] if bmi < 29.9 else categories[3]
        return f"BMI: {bmi:.2f} ({category})"
    except ZeroDivisionError:
        return "Error: Height cannot be zero"

def calculate_age(birthdate):
    try:
        today = datetime.today()
        birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return f"Age: {age} years"
    except ValueError:
        return "Error: Invalid date format! Use YYYY-MM-DD."

# Area Calculator
def calculate_area(shape, dimension_1, dimension_2=0):
    try:
        if shape == "Circle":
            return f"Area: {math.pi * dimension_1**2:.2f} sq units"
        elif shape == "Rectangle":
            return f"Area: {dimension_1 * dimension_2:.2f} sq units"
        elif shape == "Square":
            return f"Area: {dimension_1 ** 2:.2f} sq units"
        else:
            return "Invalid shape"
    except Exception as e:
        return f"Error: {str(e)}"

# Length Converter
def length_converter(value, from_unit, to_unit):
    units = {'m': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001, 'inch': 0.0254, 'foot': 0.3048}
    try:
        converted_value = (float(value) * units[from_unit]) / units[to_unit]
        return f"{value} {from_unit} = {converted_value:.2f} {to_unit}"
    except KeyError:
        return "Error: Invalid units"

# Currency Converter
def currency_converter(amount, from_currency, to_currency):
    api_url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(api_url)
        rates = response.json().get("rates")
        if rates and to_currency in rates:
            converted_amount = amount * rates[to_currency]
            return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        else:
            return "Error: Invalid currency code"
    except Exception as e:
        return f"Error: {str(e)}"

# Time Converter
def time_converter(value, from_unit, to_unit):
    time_units = {'seconds': 1, 'minutes': 60, 'hours': 3600, 'days': 86400}
    try:
        converted_value = (float(value) * time_units[from_unit]) / time_units[to_unit]
        return f"{value} {from_unit} = {converted_value:.2f} {to_unit}"
    except KeyError:
        return "Error: Invalid units"

# Gradio Interface
with gr.Blocks(theme="default") as demo:
    gr.Markdown("# 🔢 Multi-Purpose Calculator & Converter")

    with gr.Accordion("📊 Basic Calculators", open=False):
        with gr.Tab("Arithmetic"):
            gr.Interface(fn=calculator, inputs=[
                gr.Radio(["Addition", "Subtraction", "Multiplication", "Division", "Exponent", "Modulus"], label="Operation"),
                gr.Number(label="First Number"),
                gr.Number(label="Second Number (if needed)")
            ], outputs="text")

        with gr.Tab("BMI Calculator"):
            gr.Interface(fn=calculate_bmi, inputs=[gr.Number(label="Weight (kg)"), gr.Number(label="Height (m)")], outputs="text")

        with gr.Tab("Age Calculator"):
            gr.Interface(fn=calculate_age, inputs=gr.Textbox(label="Birthdate (YYYY-MM-DD)"), outputs="text")

    with gr.Accordion("📐 Advanced Math Functions", open=False):
        with gr.Tab("Logarithm"):
            gr.Interface(fn=log_calculator, inputs=[gr.Number(label="Number"), gr.Number(label="Base")], outputs="text")

        with gr.Tab("Antilogarithm"):
            gr.Interface(fn=antilog_calculator, inputs=[gr.Number(label="Log Value"), gr.Number(label="Base")], outputs="text")

        with gr.Tab("Square Root"):
            gr.Interface(fn=square_root, inputs=gr.Number(label="Number"), outputs="text")

        with gr.Tab("Cube Root"):
            gr.Interface(fn=cube_root, inputs=gr.Number(label="Number"), outputs="text")

    with gr.Accordion("📏 Converters", open=False):
        with gr.Tab("Area Converter"):
            gr.Interface(fn=calculate_area, inputs=[
                gr.Radio(["Circle", "Rectangle", "Square"], label="Shape"),
                gr.Number(label="Dimension 1"),
                gr.Number(label="Dimension 2 (Optional)", value=0)
            ], outputs="text")

        with gr.Tab("Length Converter"):
            gr.Interface(fn=length_converter, inputs=[
                gr.Number(label="Value"),
                gr.Radio(["m", "km", "cm", "mm", "inch", "foot"], label="From Unit"),
                gr.Radio(["m", "km", "cm", "mm", "inch", "foot"], label="To Unit")
            ], outputs="text")

        with gr.Tab("Currency Converter"):
            gr.Interface(fn=currency_converter, inputs=[
                gr.Number(label="Amount"),
                gr.Textbox(label="From Currency (e.g., USD)"),
                gr.Textbox(label="To Currency (e.g., INR)")
            ], outputs="text")

        with gr.Tab("Time Converter"):
            gr.Interface(fn=time_converter, inputs=[
                gr.Number(label="Value"),
                gr.Radio(["seconds", "minutes", "hours", "days"], label="From Unit"),
                gr.Radio(["seconds", "minutes", "hours", "days"], label="To Unit")
            ], outputs="text")

demo.launch()