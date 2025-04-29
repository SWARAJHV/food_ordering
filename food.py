import speech_recognition as sr
import pyttsx3
import requests
import json
from datetime import datetime
import webbrowser

class VoiceFoodOrderingSystem:
    def __init__(self):
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # User session data
        self.user_data = {
            'cart': [],
            'current_restaurant': None,
            'address': None,
            'preferences': {'vegetarian': False, 'cuisine': None}
        }
        
        # API configurations (mock - replace with actual API keys)
        self.api_config = {
            'zomato': {
                'api_key': 'YOUR_ZOMATO_API_KEY',
                'base_url': 'https://developers.zomato.com/api/v2.1/'
            }
        }
        
        # Supported commands mapping
        self.command_mapping = {
            'search': self.handle_search,
            'order': self.handle_order,
            'cart': self.handle_cart,
            'checkout': self.handle_checkout,
            'status': self.handle_order_status,
            'help': self.show_help,
            'preferences': self.handle_preferences
        }

    def speak(self, text):
        """Convert text to speech"""
        print(f"System: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen to user voice input"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"User: {command}")
            return command
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            self.speak("Sorry, my speech service is down. Please try typing.")
            return None

    def handle_search(self, query):
        """Search for restaurants or menu items"""
        if 'nearby' in query or 'near me' in query:
            self.search_nearby_restaurants()
        elif 'restaurant' in query:
            cuisine = self.extract_cuisine(query)
            self.search_restaurants(cuisine)
        elif 'menu' in query:
            restaurant = self.extract_restaurant(query)
            self.show_menu(restaurant)
        else:
            self.speak("What would you like to search for? Restaurants or menu items?")

    def handle_order(self, query):
        """Handle food ordering commands"""
        if 'add' in query:
            item = self.extract_food_item(query)
            self.add_to_cart(item)
        elif 'remove' in query:
            item = self.extract_food_item(query)
            self.remove_from_cart(item)
        elif 'from' in query:
            restaurant, item = self.extract_restaurant_and_item(query)
            self.order_specific_item(restaurant, item)
        else:
            self.speak("What would you like to order?")

    def search_nearby_restaurants(self):
        """Search nearby restaurants (mock implementation)"""
        # In a real implementation, this would use geolocation and API calls
        self.speak("Here are some nearby restaurants: 1. Empire (Indian) 2. Mainland China (Chinese) 3. McDonald's (Fast Food)")
        
    def search_restaurants(self, cuisine=None):
        """Search restaurants by cuisine"""
        if cuisine:
            self.speak(f"Searching for {cuisine} restaurants...")
            # API call would go here
            self.speak(f"Found these {cuisine} restaurants: 1. China Town 2. Peking Palace")
        else:
            self.speak("What type of cuisine are you looking for?")

    def show_menu(self, restaurant_name):
        """Display menu for a restaurant"""
        # Mock data - replace with actual API call
        menus = {
            'empire': ['Chicken Biryani', 'Veg Biryani', 'Butter Chicken'],
            'mcdonalds': ['Big Mac', 'McChicken', 'French Fries']
        }
        
        if restaurant_name.lower() in menus:
            self.speak(f"Menu for {restaurant_name}: {', '.join(menus[restaurant_name.lower()])}")
        else:
            self.speak(f"Sorry, I couldn't find {restaurant_name}")

    def add_to_cart(self, item):
        """Add item to cart"""
        if item:
            self.user_data['cart'].append(item)
            self.speak(f"Added {item} to your cart. Current cart: {', '.join(self.user_data['cart'])}")
        else:
            self.speak("What would you like to add to your cart?")

    def remove_from_cart(self, item):
        """Remove item from cart"""
        if item in self.user_data['cart']:
            self.user_data['cart'].remove(item)
            self.speak(f"Removed {item}. Current cart: {', '.join(self.user_data['cart'])}")
        else:
            self.speak(f"{item} not found in your cart")

    def handle_cart(self, query=None):
        """Handle cart operations"""
        if not self.user_data['cart']:
            self.speak("Your cart is empty")
        else:
            self.speak(f"Your cart contains: {', '.join(self.user_data['cart'])}")

    def handle_checkout(self, query=None):
        """Process checkout"""
        if not self.user_data['cart']:
            self.speak("Your cart is empty. Add some items first.")
            return
            
        self.speak(f"Ready to checkout with: {', '.join(self.user_data['cart'])}. Proceed with payment?")
        response = self.listen()
        
        if response and ('yes' in response or 'proceed' in response):
            # In a real implementation, this would integrate with payment gateway
            self.speak("Processing payment... Order confirmed! Your food will arrive in 30-40 minutes.")
            self.user_data['cart'] = []  # Clear cart
        else:
            self.speak("Checkout cancelled")

    def handle_order_status(self, query=None):
        """Check order status"""
        # Mock implementation
        self.speak("Your order is being prepared and will arrive in about 25 minutes")

    def show_help(self, query=None):
        """Show available commands"""
        help_text = """
        You can say things like:
        - Search for nearby restaurants
        - Show me Italian restaurants
        - Order pizza from Domino's
        - Add fries to my order
        - What's in my cart?
        - Checkout
        - Order status
        """
        self.speak(help_text)

    def handle_preferences(self, query):
        """Handle user preferences"""
        if 'vegetarian' in query:
            self.user_data['preferences']['vegetarian'] = 'no' not in query
            status = "on" if self.user_data['preferences']['vegetarian'] else "off"
            self.speak(f"Vegetarian preference turned {status}")
        elif 'cuisine' in query:
            cuisine = self.extract_cuisine(query)
            if cuisine:
                self.user_data['preferences']['cuisine'] = cuisine
                self.speak(f"Preferred cuisine set to {cuisine}")

    def extract_cuisine(self, text):
        """Extract cuisine type from text"""
        cuisines = ['indian', 'chinese', 'italian', 'mexican', 'thai', 'american']
        for cuisine in cuisines:
            if cuisine in text:
                return cuisine
        return None

    def extract_restaurant(self, text):
        """Extract restaurant name from text"""
        restaurants = ['empire', 'mcdonalds', 'domino', 'mainland china']
        for restaurant in restaurants:
            if restaurant in text.lower():
                return restaurant.title()
        return None

    def extract_food_item(self, text):
        """Extract food item from text"""
        food_items = ['biryani', 'pizza', 'burger', 'fries', 'pasta']
        for item in food_items:
            if item in text.lower():
                return item
        return None

    def extract_restaurant_and_item(self, text):
        """Extract both restaurant and item from text"""
        parts = text.split(' from ')
        if len(parts) == 2:
            item = self.extract_food_item(parts[0])
            restaurant = self.extract_restaurant(parts[1])
            return restaurant, item
        return None, None

    def process_command(self, command):
        """Process user command and route to appropriate handler"""
        if not command:
            return False
            
        # Check for exit commands
        if 'exit' in command or 'quit' in command or 'stop' in command:
            self.speak("Goodbye! Happy eating!")
            return False
            
        # Route command to appropriate handler
        handled = False
        for keyword, handler in self.command_mapping.items():
            if keyword in command:
                handler(command)
                handled = True
                break
                
        if not handled:
            self.speak("I'm not sure how to help with that. Say 'help' for available commands.")
            
        return True

    def run(self):
        """Main system loop"""
        self.speak("Welcome to Voice Food Ordering! How can I help you today? Say 'help' for options.")
        
        while True:
            command = self.listen()
            if not self.process_command(command):
                break

if __name__ == "__main__":
    system = VoiceFoodOrderingSystem()
    system.run()