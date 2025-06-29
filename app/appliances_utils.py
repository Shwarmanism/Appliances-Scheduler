class AppliancesCatalog():
    appliances = [
        # ❄️ Air Conditioner
        {"category": "Air Conditioner", "type": "Floor Stand, Non-Inverter", "capacity": "2.00 HP", "wattage": 1700, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Floor Stand, Non-Inverter", "capacity": "3.00 HP", "wattage": 2550},

        {"category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "1.00 HP", "wattage": 800, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "1.50 HP", "wattage": 1100, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "2.00 HP", "wattage": 1450, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "2.50 HP", "wattage": 1800, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "1.00 HP", "wattage": 950, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "1.50 HP", "wattage": 1300, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "2.00 HP", "wattage": 1600, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "2.50 HP", "wattage": 2000, "prefix" : "AC-NI"},

        {"category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "1.00 HP", "wattage": 850, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "1.50 HP", "wattage": 1150, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "2.00 HP", "wattage": 1500, "prefix" : "AC-I"},
        {"category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "0.50 HP", "wattage": 500, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "0.75 HP", "wattage": 650, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "1.00 HP", "wattage": 900, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "1.50 HP", "wattage": 1250, "prefix" : "AC-NI"},
        {"category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "2.00 HP", "wattage": 1600, "prefix" : "AC-NI"},

        # 🌬️ Cooling / Air Movement
        {"category": "Cooling", "type": "Air Cooler", "capacity": "125 W", "wattage": 125, "prefix" : "CL"},
        {"category": "Cooling", "type": "Air Cooler", "capacity": "300 W", "wattage": 300, "prefix" : "CL"},
        {"category": "Cooling", "type": "Electric Fan", "capacity": "Stand, 16\"", "wattage": 65, "prefix" : "CL"},
        {"category": "Cooling", "type": "Electric Fan", "capacity": "Desk, 12\"", "wattage": 50, "prefix" : "CL"},
        {"category": "Cooling", "type": "Electric Fan", "capacity": "Wall, 16\"", "wattage": 60, "prefix" : "CL"},
        {"category": "Cooling", "type": "Electric Fan", "capacity": "Ceiling, 18\"", "wattage": 75, "prefix" : "CL"},
        {"category": "Cooling", "type": "Industrial Fan", "capacity": "500 W", "wattage": 500, "prefix" : "CL"},
        {"category": "Cooling", "type": "Exhaust Fan", "capacity": "12\"", "wattage": 40, "prefix" : "CL"},

        # 🧺 Laundry
        {"category": "Laundry", "type": "Washing Machine", "capacity": "Top Load, 6kg", "wattage": 400, "prefix" : "LA"},
        {"category": "Laundry", "type": "Washing Machine", "capacity": "Top Load, 10kg", "wattage": 600, "prefix" : "LA"},
        {"category": "Laundry", "type": "Washing Machine", "capacity": "Front Load, 7kg", "wattage": 800, "prefix" : "LA"},
        {"category": "Laundry", "type": "Washing Machine", "capacity": "Front Load, 11kg, Inverter", "wattage": 1000, "prefix" : "LA"},
        {"category": "Laundry", "type": "Spin Dryer", "capacity": "Single Tub", "wattage": 200, "prefix" : "LA"},
        {"category": "Laundry", "type": "Clothes Dryer", "capacity": "5kg", "wattage": 1500, "prefix" : "LA"},
        {"category": "Laundry", "type": "Flat Iron", "capacity": "Dry", "wattage": 1000, "prefix" : "LA"},
        {"category": "Laundry", "type": "Flat Iron", "capacity": "Steam", "wattage": 1200, "prefix" : "LA"},

        # 🍳 Kitchen
        {"category": "Kitchen", "type": "Refrigerator", "capacity": "Single Door, 6 cu. ft.", "wattage": 120, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Refrigerator", "capacity": "Two Door, 12 cu. ft., Inverter", "wattage": 150, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Chest Freezer", "capacity": "7 cu. ft.", "wattage": 180, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Upright Freezer", "capacity": "8 cu. ft.", "wattage": 200, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Rice Cooker", "capacity": "0.6L, 300W", "wattage": 300, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Rice Cooker", "capacity": "1.0L, 500W", "wattage": 500, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Induction Cooker", "capacity": "1200W", "wattage": 1200, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Electric Stove", "capacity": "1500W", "wattage": 1500, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Oven Toaster", "capacity": "650W", "wattage": 650, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Microwave Oven", "capacity": "700W", "wattage": 700, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Electric Kettle", "capacity": "1500W", "wattage": 1500, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Blender", "capacity": "1.00L, 300W", "wattage": 300, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Coffee Maker", "capacity": "600W", "wattage": 600, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Food Processor", "capacity": "600W", "wattage": 600, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Water Dispenser", "capacity": "Hot & Cold", "wattage": 580, "prefix" : "KI"},
        {"category": "Kitchen", "type": "Dish Dryer", "capacity": "300W", "wattage": 300, "prefix" : "KI"},

        # 🧼 Cleaning
        {"category": "Cleaning", "type": "Vacuum Cleaner", "capacity": "Standard", "wattage": 600, "prefix" : "CLE"},
        {"category": "Cleaning", "type": "Pressure Washer", "capacity": "1000W", "wattage": 1000, "prefix" : "CLE"},
        {"category": "Cleaning", "type": "Robot Vacuum", "capacity": "30W", "wattage": 30, "prefix" : "CLE"},

        # 💡 Lighting
        {"category": "Lighting", "type": "LED Bulb", "capacity": "5W", "wattage": 5, "prefix" : "LIG"},
        {"category": "Lighting", "type": "LED Bulb", "capacity": "9W", "wattage": 9, "prefix" : "LIG"},
        {"category": "Lighting", "type": "LED Bulb", "capacity": "12W", "wattage": 12, "prefix" : "LIG"},
        {"category": "Lighting", "type": "Fluorescent Lamp", "capacity": "18W", "wattage": 18, "prefix" : "LIG"},
        {"category": "Lighting", "type": "Incandescent Bulb", "capacity": "40W", "wattage": 40, "prefix" : "LIG"},
        {"category": "Lighting", "type": "Incandescent Bulb", "capacity": "60W", "wattage": 60, "prefix" : "LIG"},
        {"category": "Lighting", "type": "Night Light", "capacity": "1W", "wattage": 1, "prefix" : "LIG"},
        {"category": "Lighting", "type": "Chandelier", "capacity": "5 bulbs x 9W", "wattage": 45, "prefix" : "LIG"},

        # 📱 Gadgets
        {"category": "Electronics", "type": "Desktop Computer", "capacity": "Standard", "wattage": 400, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Laptop", "capacity": "Standard", "wattage": 65, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Wi-Fi Router", "capacity": "Standard", "wattage": 10, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Mobile Phone Charger", "capacity": "Standard", "wattage": 5, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Tablet Charger", "capacity": "Standard", "wattage": 10, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Smart TV", "capacity": "32\"", "wattage": 50, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Smart TV", "capacity": "55\"", "wattage": 120, "prefix" : "ELE"},
        {"category": "Electronics", "type": "CRT TV", "capacity": "21\"", "wattage": 90, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Gaming Console", "capacity": "Standard", "wattage": 200, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Home Theater", "capacity": "Standard", "wattage": 250, "prefix" : "ELE"},
        {"category": "Electronics", "type": "Projector", "capacity": "Standard", "wattage": 300, "prefix" : "ELE"},

        # 🛏️ Bedroom / Wellness
        {"category": "Wellness", "type": "Air Purifier", "capacity": "Standard", "wattage": 50, "prefix" : "WL"},
        {"category": "Wellness", "type": "Air Purifier with Humidifier", "capacity": "Standard", "wattage": 75, "prefix" : "WL"},
        {"category": "Wellness", "type": "Aroma Diffuser", "capacity": "Standard", "wattage": 10, "prefix" : "WL"},
        {"category": "Wellness", "type": "Electric Blanket", "capacity": "Standard", "wattage": 60, "prefix" : "WL"},
        {"category": "Wellness", "type": "Dehumidifier", "capacity": "Standard", "wattage": 300, "prefix" : "WL"},
        {"category": "Wellness", "type": "Massage Chair", "capacity": "Standard", "wattage": 150, "prefix" : "WL"},
        {"category": "Wellness", "type": "Sleep Sound Machine", "capacity": "Standard", "wattage": 10, "prefix" : "WL"}
    ]
        
    def get_appliance_by_type(cls, selected_type):
        for appliance in cls.appliances:
            if appliance['type'] == selected_type:
                return appliance.get("prefix", "AP")
            return "AP"

