import gspread
from google.oauth2.service_account import Credentials
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
import datetime
import os


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("daily-sales-455107-35b447e52c4c.json", scopes=scope)
client = gspread.authorize(creds)


SHEET_ID = "1GP4NzH0tA2J9rRK_AbAhLnauHZmNKdKH_l1MkCDNHjU"  
sheet = client.open_by_key(SHEET_ID).sheet1  

menu = {
    "ccs-m": 350,  
    "ccs-l": 750,  
    "tcs-m": 280,  
    "tcs-l": 700,
    "dcs-m": 100,
    "dcs-l": 100,
    "bf-m": 100,
    "bf-l": 100,


    
}

sales = []
total_sales = 0 

class SalesApp(App):
    def build(self):
        self.layout = RelativeLayout()
        
     
        
        self.content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label = Label(text="Selected Items:", font_size=18, bold=True)
        self.content.add_widget(self.label)
        
        self.item_input = TextInput(multiline=True, opacity=0.7, background_color=(1, 1, 1, 0.5))
        self.content.add_widget(self.item_input)
        
        self.quantity_label = Label(text="Selected Quantities:", font_size=18, bold=True)
        self.content.add_widget(self.quantity_label)
        
        self.quantity_input = TextInput(multiline=False, opacity=0.7, background_color=(1, 1, 1, 0.5))
        self.content.add_widget(self.quantity_input)
        
        
        self.product_buttons_layout = GridLayout(cols=3, spacing=5, size_hint_y=None)
        self.product_buttons_layout.bind(minimum_height=self.product_buttons_layout.setter('height'))

        for item in menu.keys():
            btn = Button(
                text=item.upper(), 
                font_size=12, 
                background_color=(0.2, 0.6, 0.8, 0.8),
                size_hint_y=None,
                height=30,
                on_press=self.add_product
            )
            self.product_buttons_layout.add_widget(btn)

        self.content.add_widget(self.product_buttons_layout)

        
        self.quantity_buttons_layout = GridLayout(cols=5, spacing=5, size_hint_y=None)
        self.quantity_buttons_layout.bind(minimum_height=self.quantity_buttons_layout.setter('height'))

        for quantity in range(1, 11):  
            btn = Button(
                text=str(quantity), 
                font_size=12, 
                background_color=(0.6, 0.2, 0.8, 0.8),
                size_hint_y=None,
                height=30,
                on_press=self.add_quantity
            )
            self.quantity_buttons_layout.add_widget(btn)

        self.content.add_widget(self.quantity_buttons_layout)
        
        self.button = Button(text="Add to Order", font_size=16, on_press=self.add_to_order, background_color=(1, 0.84, 0, 0.5))
        self.content.add_widget(self.button)
        
        self.order_total_label = Label(text="Order Total: $0.00", font_size=18, bold=True)
        self.content.add_widget(self.order_total_label)
        
        self.sales_summary = Label(text="Total Sales: $0.00", font_size=16)
        self.content.add_widget(self.sales_summary)
        
        self.excel_button = Button(text="Open Sales Report", font_size=14, on_press=self.open_excel, background_color=(1, 0.84, 0, 0.5))
        self.content.add_widget(self.excel_button)
        
        self.layout.add_widget(self.content)
        
        return self.layout

    def add_product(self, instance):
        """Add selected product to the item input field."""
        item_text = instance.text.lower()
        current_text = self.item_input.text.strip()
        
        if current_text:
            self.item_input.text = f"{current_text}, {item_text}"
        else:
            self.item_input.text = item_text

    def add_quantity(self, instance):
        """Add selected quantity to the quantity input field."""
        quantity_text = instance.text
        current_text = self.quantity_input.text.strip()
        
        if current_text:
            self.quantity_input.text = f"{current_text}, {quantity_text}"
        else:
            self.quantity_input.text = quantity_text

    def add_to_order(self, instance):
        self.animate_button(instance)  
        
        items = self.item_input.text.strip().lower().split(',')
        quantities = self.quantity_input.text.strip().split(',')
        
        if len(items) != len(quantities):
            self.order_total_label.text = "Mismatched item and quantity count!"
            return
        
        order_total = 0
        order_entries = []
        
        for i in range(len(items)):
            item = items[i].strip()
            quantity = quantities[i].strip()
            
            if not quantity.isdigit():
                self.order_total_label.text = "Invalid Quantity!"
                return
            
            quantity = int(quantity)
            
            if item in menu:
                price = menu[item]
                total_price = price * quantity
                sales.append((item, quantity, total_price))
                order_total += total_price
                order_entries.append((item, quantity, total_price))
            else:
                self.order_total_label.text = f"Item '{item}' Not In Menu."
                return
        
        global total_sales
        total_sales += order_total
        
        self.order_total_label.text = f"Order Total: ${order_total:.2f}"
        self.sales_summary.text = f"Total Sales: ${total_sales:.2f}"
        
        for entry in order_entries:
            self.save_to_google_sheets(*entry)  
        
        self.item_input.text = ""
        self.quantity_input.text = ""
    
    def save_to_google_sheets(self, item, quantity, total_price):
        """Save sales data to Google Sheets in real-time."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, item, quantity, total_price])
    
    def open_excel(self, instance):
        filename = "sales_summary.csv"
        if os.path.exists(filename):
            os.system(f"start {filename}")  
        else:
            self.sales_summary.text = "Sales report not found!"
    
    def animate_button(self, button):
        anim = Animation(size_hint=(1.2, 1.2), duration=0.1) + Animation(size_hint=(1, 1), duration=0.1)
        anim.start(button)

if __name__ == "__main__":
    SalesApp().run()
