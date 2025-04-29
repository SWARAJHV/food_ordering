# import speech_recognition as sr
# import pyttsx3
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
#
# # Initialize voice engine
# engine = pyttsx3.init()
#
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()
#
# def listen():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         command = r.recognize_google(audio)
#         print("You said:", command)
#     except sr.UnknownValueError:
#         print("Sorry, I did not catch that.")
#         return ""
#     return command.lower()
#
# # Example usage
# speak("Welcome to Zomato voice ordering!")
# command = listen()
#
# if "list restaurants" in command:
#     # Launch Zomato
#     driver = webdriver.Chrome()
#     driver.get("https://www.zomato.com/")
#     speak("Opening Zomato. Listing restaurants nearby.")
#
#     time.sleep(7)  # wait for page and JS to load
#
#     # Scroll down to load more content (optional)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)
#
#     # Scrape restaurant names (update this selector if Zomato changes their HTML)
#     restaurant_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-result-type="ResCard_Name"]')
#
#     if not restaurant_elements:
#         speak("Sorry, I could not find any restaurants on the page.")
#     else:
#         speak("Here are some restaurants near you:")
#         for r in restaurant_elements[:5]:
#             name = r.text.strip()
#             if name:
#                 print(name)
#                 speak(name)
#
# # After this, you can extend: listen for food item names -> click them -> proceed to payment page.


import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print("You said:", command)
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
    return command.lower()

# Example usage
speak("Welcome to Zomato voice ordering!")
command = listen()

driver = webdriver.Chrome()

if "list restaurants" in command:
    # Launch Zomato
    driver.get("https://www.zomato.com/")
    speak("Opening Zomato. Listing restaurants nearby.")

    time.sleep(7)  # wait for page and JS to load

    # Scroll down to load more content (optional)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Scrape restaurant names
    restaurant_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-result-type="ResCard_Name"]')

    if not restaurant_elements:
        speak("Sorry, I could not find any restaurants on the page.")
    else:
        speak("Here are some restaurants near you:")
        for r in restaurant_elements[:5]:
            name = r.text.strip()
            if name:
                print(name)
                speak(name)

elif "order" in command and "from" in command:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import re
    match = re.search(r"order (.+) from (.+)", command)
    if match:
        food_item = match.group(1)
        restaurant_name = match.group(2)
        speak(f"Ordering {food_item} from {restaurant_name}")

        driver = webdriver.Chrome()
        driver.get("https://www.swiggy.com/")
        speak(f"Searching for {restaurant_name} on Zomato.")
        time.sleep(5)

        try:
            # Wait for search icon to appear and click it
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search for restaurant, cuisine or a dish']"))
            )
            search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search for restaurant, cuisine or a dish']")
            search_box.click()
            search_box.send_keys(restaurant_name)
            search_box.submit()

            time.sleep(5)

            # Click the first restaurant result (update this if Zomato changes layout)
            first_result = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/rest']"))
            )
            first_result.click()

            speak(f"Opened {restaurant_name}. Now you can manually place your order for {food_item}.")
        except Exception as e:
            print("Error:", e)
            speak("Sorry, I couldn't find the restaurant or complete the search.")


else:
    speak("Sorry, I didn't understand your command.")
