# Imports 
#imports
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


#variables
now = datetime.now()
hour = int(now.strftime('%I')) # this gives 12 hour time 
minute = int(now.strftime('%M')) # This gives the minute
am_pm = str(now.strftime('%p')) # this gives both and am and pm
day = str(now.strftime('%A'))
voice_assistant = False
#begin_data
voice_data = '' 
voice_data2 = ''
voice_data4 = ''
joinn = ""
joinn2 = ""

url = "http://www.bom.gov.au/places/sa/adelaide/"
url2 = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?"

r = sr.Recognizer()
'''
def beign_audio():
    global begin_speech
    with sr.Microphone() as source1
    audio1 = r.listen(source1)
    try:
        begin_speech = r.recognize_google(audio1)
    except sr.UnknownValueError:
        print('please try again')
    except sr.RequestError:
        print("sorry my speech service is down")
    return begin_speech'''

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
    global hour, minute, am_pm, voice_data, voice_data2, joinn, voice_data4
    if "help" in voice_data:
        robot.say_text("opening my voice command list").wait_for_completed()
        url3 = "http://www.bom.gov.au/places/sa/adelaide/"
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
    '''if "wheelie" in voice_data:
        print("it worked?")
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    cube = None

    try:
        cube = robot.world.wait_for_observed_light_cube(timeout=30) #this waits for cozmo to spot one of cubes
        print("Found cube", cube)

    except asyncio.TimeoutError:
        print("Didn't find a cube :-(")

    finally:
        look_around.stop()
        # whether we find it or not, we want to stop the behavior
        
    if cube is None:
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail) #if the cube is not found 
        return
    
    print("Yay, found cube")
    cube.set_lights(cozmo.lights.green_light.flash())
    anim = robot.play_anim_trigger(cozmo.anim.Triggers.BlockReact)
    anim.wait_for_completed()
    action = robot.pop_a_wheelie(cube, num_retries=2)
    action.wait_for_completed()'''
    # code found at 
    if "stack" in voice_data:
        print("it worked?")
        look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=15) 
        look_around.stop()

        if len(cubes) < 2:
            print("unable to find both cubes")
        else:
            current_action = robot.pickup_object(cube[0], num_retries=3) # picks up the first cube
            current_action.wait_for_completed()
            if current_action.has_failed:
                failreason = current_action.failure_reason
                print(failreason)
                return
        
        #stacking cubes

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
        print("telling weather")
        global day, url
        var = requests.get(url) 
        soup = BeautifulSoup(var.content, 'html.parser') 
        weather = soup.find('li', class_="airT") # finds the text within the class
        climate = soup.find('dd', class_="summary")
        string_weather = str(weather)
        the_climate = str(climate) # converts to string
        replaceclimate = the_climate.replace('<dd class="summary">', "").replace(".</dd>", "") # removes the tags 
        replaceweather = string_weather.replace('<li class="airT">', "").replace("</li>", "")
        print(replaceclimate)
        print(replaceweather)
        str(weather)
        robot.say_text(f"the current temperature is {replaceweather} and it is {replaceclimate}", use_cozmo_voice=False, voice_pitch=0.8, duration_scalar=0.6).wait_for_completed()
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
    robot.say_text("How can I be of service").wait_for_completed()


#$cozmo.run_program(cozmo_boost_face)
#time.sleep(5)
#cozmo.run_program(begin_speech)


time.sleep(1)
while 1:
    print('Please say something')
    voice_data = record_audio()
    print(voice_data)
    cozmo.run_program(respond)

