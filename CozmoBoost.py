# imports
import speech_recognition as sr
import requests
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
import cozmo
import time
import webbrowser
import asyncio
from cozmo.util import degrees, speed_mmps, distance_mm


# variables
now = datetime.now()
hour = int(now.strftime('%I')) # this gives 12 hour time 
minute = int(now.strftime('%M')) # This gives the minute
am_pm = str(now.strftime('%p')) # this gives both and am and pm
day = str(now.strftime('%A'))
voice_data = '' 
voice_data2 = ''
voice_data4 = ''
joinn = ""
joinn2 = ""

url = "https://weather.com/weather/today/l/33.52,-86.80?par=google&temp=c" # change the link from weather.com for you your country
url2 = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?"

r = sr.Recognizer()

# Tutourial found for the voice commands at : https://www.youtube.com/watch?v=x8xjj6cR9Nc&t=867s&ab_channel=TraversyMedia
def record_audio():
    global voice_data
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            print('Please try again')
        except sr.RequestError:
            print('Sorry, my speech service is down')
        return voice_data


def respond(robot: cozmo.robot.Robot):
    global hour, minute, am_pm, voice_data, voice_data2, joinn, voice_data4, url
    if "help" in voice_data:
        robot.say_text("opening my voice command list").wait_for_completed()
        url3 = "https://amall022.wixsite.com/cozmoboost"
        webbrowser.get().open(url3) # this opens to the website with the list of commands
    if 'move forward by ' in voice_data:
        voice_data, voice_data2 = voice_data.split('by')
        voice_data3 = voice_data2.split("mm")
        x = joinn.join(voice_data3)
        distance_forward = int(x)
        print(x)
        robot.drive_straight(distance_mm(distance_forward), speed_mmps(100)).wait_for_completed()
        print("Command: move forward")
    if 'move back by' in voice_data:
        voice_data, voice_data4 = voice_data.split('by')
        voice_data5 = voice_data4.split("mm")
        y = joinn2.join(voice_data5)
        potato = int(y)
        potato = -(potato**1)
        print(potato)
        robot.drive_straight(distance_mm(potato), speed_mmps(100)).wait_for_completed()
        print("Command: move back")
    
    if "stack" in voice_data:
        #code found at: https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/04_cubes_and_objects/05_cube_stack.py
        print("it worked?")
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=30) # cozmo looks for cubes for both cubes for 30 seconds
        look_around.stop()

        if len(cubes) < 2:
            print("unable to find both cubes")
        else:
            current_action = robot.pickup_object(cube[0], num_retries=3) # picks up the first cube
            current_action.wait_for_completed()
            if current_action.has_failed:
                print("oh no it failed")
                return
        
            #stacking attempts to stack both cubes
            current_action = robot.place_on_object(cubes[1], num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                return
    if 'time' in voice_data:
        print("telling time")
        if hour in range(1,12) and minute in range(0,60) and am_pm == "AM": # For am time 
            both = str(datetime.now().strftime('%I %M A M')) #This converts it into a readable string for cozmo. 
            robot.say_text(both, use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed() #This tells cozmo to read variable both 
            print("Command: Saying time")
        elif hour in range(1,12) and minute in range(0,60) and am_pm == "PM": # For pm tme/.
            both1 = str(datetime.now().strftime('%I %M P M'))
            robot.say_text(f"the time is {both1}", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if 'turn right' in voice_data:
         robot.turn_in_place(degrees(90)).wait_for_completed()
    if 'turn left' in voice_data:
         robot.turn_in_place(degrees(-90)).wait_for_completed()
    if 'weather' in voice_data:
        # webscraping tutorial found at: https://www.youtube.com/watch?v=xKukOMtPWwk&ab_channel=johangodinho
        print("telling weather")
        var = requests.get(url)
        soup1 = BeautifulSoup(var.content, 'html.parser')
        weather = soup1.find('span', class_="CurrentConditions--tempValue--3KcTQ").text
        print(weather)
        robot.say_text(f"the current temperature is {weather}", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if 'active covid cases' in voice_data:
        page = requests.get(url2)
        soup2 = BeautifulSoup(page.content, 'html.parser')
        activecases = soup2.find('div', class_= "number-table-main").text
        activecases = activecases.strip()
        cozmo_active_cases = str(activecases)
        robot.say_text(f"There are currently {cozmo_active_cases} active Covid 19 cases", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if "total cases" in voice_data:
        page = requests.get(url2)
        soup2 = BeautifulSoup(page.content, 'html.parser')
        totalcases = soup2.find('div', class_= "maincounter-number").text
        totalcases = totalcases.strip()
        cozmo_total_cases = str(totalcases)
        robot.say_text(f"The Worlds total Covid 19 cases is {cozmo_total_cases}", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if "covid deaths" in voice_data:
        page = requests.get(url2)
        soup2 = BeautifulSoup(page.content, 'html.parser')
        deaths = soup2.findAll('div', class_= "maincounter-number")
        covid_death = deaths[1] # finds which "maincounter-number" we want
        y = str(covid_death)
        covid_deaths2 = y.replace('<div class="maincounter-number">', "").replace("<span>", "").replace("</span>", "").replace("</div>", "")
        covid_deaths2 = covid_deaths2.strip()
        cozmo_total_deaths = str(covid_deaths2)
        robot.say_text(f"The current deaths from covid 19 is {cozmo_total_deaths}", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if "recovered" in voice_data:
        page = requests.get(url2)
        soup2 = BeautifulSoup(page.content, 'html.parser')
        recovered = soup2.findAll('div', class_= "maincounter-number")
        covid_recovered = recovered[2]
        z = str(covid_recovered)
        covid_recovered2 =  z.replace('<div class="maincounter-number" style="color:#8ACA2B ">', "").replace("<span>", "").replace("</span>", "").replace("</div>", "")
        covid_recovered2 = covid_recovered2.strip()
        robot.say_text(f"Currently {covid_recovered2} people have recovered from covid", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
    if 'shut down'in voice_data:
        robot.say_text("Voice commands is now shutting down", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
        exit()

# code found at: https://github.com/hunter-heidenreich/Cozmo-Scripts/blob/master/structured-tutorials/009-face_images.py
# tutorial found at: https://www.youtube.com/watch?v=sUa3aF0dN_8&t=566s&ab_channel=CreatingHunterH

def setup_position(robot: cozmo.robot.Robot):
    if robot.lift_height.distance_mm > 45:
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()

def cozmo_boost_face(robot: cozmo.robot.Robot):
    setup_position(robot)
    raw_images = [('C:\\Users\\Alexa\\OneDrive\\Desktop\\Year 10\\EPM\\logo.jpg', Image.BICUBIC)]
    face_images = []
    for name, mode in raw_images:
        img = Image.open(name)
        resize = img.resize(cozmo.oled_face.dimensions(), mode)
        face = cozmo.oled_face.convert_image_to_screen_data(resize, invert_image=True)
        face_images.append(face)

    num_loops = 10
    duration = 2
    for _ in range(num_loops):
        for image in face_images:
            robot.display_oled_face_image(image, duration * 1000.0)
            time.sleep(duration)



def begin_speech(robot: cozmo.robot.Robot):
    robot.say_text("How can I be of service", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()

cozmo.run_program(cozmo_boost_face)
cozmo.run_program(begin_speech)


time.sleep(1)
while 1:
    print('Please say something')
    voice_data = record_audio()
    print(voice_data)
    cozmo.run_program(respond)

