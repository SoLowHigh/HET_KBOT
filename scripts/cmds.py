from . import temperature

def help(message):
      with open('docs/help', 'r') as f_cmd:
            help_text = f_cmd.read()
      return help_text

def weather(city):
      weather_temperature = temperature.main(city)
      return weather_temperature