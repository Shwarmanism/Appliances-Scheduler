class AppliancesCatalog():
    appliances = [
        # ❄️ Air Conditioner
            
        {"id" : 1, "category": "Air Conditioner", "type": "Floor Stand, Non-Inverter", "capacity": "3.00 HP", "wattage": 2550},

        {"id" : 2, "category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "1.00 HP", "wattage": 800, "prefix" : "AC-I"},
        {"id" : 3, "category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "1.50 HP", "wattage": 1100, "prefix" : "AC-I"},
        {"id" : 4, "category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "2.00 HP", "wattage": 1450, "prefix" : "AC-I"},
        {"id" : 5, "category": "Air Conditioner", "type": "Split Type, Inverter", "capacity": "2.50 HP", "wattage": 1800, "prefix" : "AC-I"},
        {"id" : 6, "category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "1.00 HP", "wattage": 950, "prefix" : "AC-NI"},
        {"id" : 7, "category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "1.50 HP", "wattage": 1300, "prefix" : "AC-NI"},
        {"id" : 8, "category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "2.00 HP", "wattage": 1600, "prefix" : "AC-NI"},
        {"id" : 9, "category": "Air Conditioner", "type": "Split Type, Non-Inverter", "capacity": "2.50 HP", "wattage": 2000, "prefix" : "AC-NI"},

        {"id" : 10, "category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "1.00 HP", "wattage": 850, "prefix" : "AC-I"},
        {"id" : 11, "category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "1.50 HP", "wattage": 1150, "prefix" : "AC-I"},
        {"id" : 12, "category": "Air Conditioner", "type": "Window Type, Inverter", "capacity": "2.00 HP", "wattage": 1500, "prefix" : "AC-I"},
        {"id" : 13, "category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "0.50 HP", "wattage": 500, "prefix" : "AC-NI"},
        {"id" : 14, "category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "0.75 HP", "wattage": 650, "prefix" : "AC-NI"},
        {"id" : 15, "category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "1.00 HP", "wattage": 900, "prefix" : "AC-NI"},
        {"id" : 16, "category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "1.50 HP", "wattage": 1250, "prefix" : "AC-NI"},
        {"id" : 17, "category": "Air Conditioner", "type": "Window Type, Non-Inverter", "capacity": "2.00 HP", "wattage": 1600, "prefix" : "AC-NI"},

        # 🌬️ Cooling / Air Movement
        {"id" : 18, "category": "Cooling", "type": "Air Cooler", "capacity": "125 W", "wattage": 125, "prefix" : "CL"},
        {"id" : 19, "category": "Cooling", "type": "Air Cooler", "capacity": "300 W", "wattage": 300, "prefix" : "CL"},
        {"id" : 20, "category": "Cooling", "type": "Electric Fan", "capacity": "Stand, 16\"", "wattage": 65, "prefix" : "CL"},
        {"id" : 21, "category": "Cooling", "type": "Electric Fan", "capacity": "Desk, 12\"", "wattage": 50, "prefix" : "CL"},
        {"id" : 22, "category": "Cooling", "type": "Electric Fan", "capacity": "Wall, 16\"", "wattage": 60, "prefix" : "CL"},
        {"id" : 23, "category": "Cooling", "type": "Electric Fan", "capacity": "Ceiling, 18\"", "wattage": 75, "prefix" : "CL"},
        {"id" : 24, "category": "Cooling", "type": "Industrial Fan", "capacity": "500 W", "wattage": 500, "prefix" : "CL"},
        {"id" : 25, "category": "Cooling", "type": "Exhaust Fan", "capacity": "12\"", "wattage": 40, "prefix" : "CL"},

        # 🧺 Laundry
        {"id" : 26, "category": "Laundry", "type": "Washing Machine", "capacity": "Top Load, 6kg", "wattage": 400, "prefix" : "LA"},
        {"id" : 27, "category": "Laundry", "type": "Washing Machine", "capacity": "Top Load, 10kg", "wattage": 600, "prefix" : "LA"},
        {"id" : 28, "category": "Laundry", "type": "Washing Machine", "capacity": "Front Load, 7kg", "wattage": 800, "prefix" : "LA"},
        {"id" : 29, "category": "Laundry", "type": "Washing Machine", "capacity": "Front Load, 11kg, Inverter", "wattage": 1000, "prefix" : "LA"},
        {"id" : 30, "category": "Laundry", "type": "Spin Dryer", "capacity": "Single Tub", "wattage": 200, "prefix" : "LA"},
        {"id" : 31, "category": "Laundry", "type": "Clothes Dryer", "capacity": "5kg", "wattage": 1500, "prefix" : "LA"},
        {"id" : 32, "category": "Laundry", "type": "Flat Iron", "capacity": "Dry", "wattage": 1000, "prefix" : "LA"},
        {"id" : 33, "category": "Laundry", "type": "Flat Iron", "capacity": "Steam", "wattage": 1200, "prefix" : "LA"},

        # 🍳 Kitchen
        {"id" : 34, "category": "Kitchen", "type": "Refrigerator", "capacity": "Single Door, 6 cu. ft.", "wattage": 120, "prefix" : "KI"},
        {"id" : 35, "category": "Kitchen", "type": "Refrigerator", "capacity": "Two Door, 12 cu. ft., Inverter", "wattage": 150, "prefix" : "KI"},
        {"id" : 36, "category": "Kitchen", "type": "Chest Freezer", "capacity": "7 cu. ft.", "wattage": 180, "prefix" : "KI"},
        {"id" : 37, "category": "Kitchen", "type": "Upright Freezer", "capacity": "8 cu. ft.", "wattage": 200, "prefix" : "KI"},
        {"id" : 38, "category": "Kitchen", "type": "Rice Cooker", "capacity": "0.6L, 300W", "wattage": 300, "prefix" : "KI"},
        {"id" : 39, "category": "Kitchen", "type": "Rice Cooker", "capacity": "1.0L, 500W", "wattage": 500, "prefix" : "KI"},
        {"id" : 40, "category": "Kitchen", "type": "Induction Cooker", "capacity": "1200W", "wattage": 1200, "prefix" : "KI"},
        {"id" : 41, "category": "Kitchen", "type": "Electric Stove", "capacity": "1500W", "wattage": 1500, "prefix" : "KI"},
        {"id" : 42, "category": "Kitchen", "type": "Oven Toaster", "capacity": "650W", "wattage": 650, "prefix" : "KI"},
        {"id" : 43, "category": "Kitchen", "type": "Microwave Oven", "capacity": "700W", "wattage": 700, "prefix" : "KI"},
        {"id" : 44, "category": "Kitchen", "type": "Electric Kettle", "capacity": "1500W", "wattage": 1500, "prefix" : "KI"},
        {"id" : 45, "category": "Kitchen", "type": "Blender", "capacity": "1.00L, 300W", "wattage": 300, "prefix" : "KI"},
        {"id" : 46, "category": "Kitchen", "type": "Coffee Maker", "capacity": "600W", "wattage": 600, "prefix" : "KI"},
        {"id" : 47, "category": "Kitchen", "type": "Food Processor", "capacity": "600W", "wattage": 600, "prefix" : "KI"},
        {"id" : 48, "category": "Kitchen", "type": "Water Dispenser", "capacity": "Hot & Cold", "wattage": 580, "prefix" : "KI"},
        {"id" : 49, "category": "Kitchen", "type": "Dish Dryer", "capacity": "300W", "wattage": 300, "prefix" : "KI"},

        # 🧼 Cleaning
        {"id" : 50, "category": "Cleaning", "type": "Vacuum Cleaner", "capacity": "Standard", "wattage": 600, "prefix" : "CLE"},
        {"id" : 51, "category": "Cleaning", "type": "Pressure Washer", "capacity": "1000W", "wattage": 1000, "prefix" : "CLE"},
        {"id" : 52, "category": "Cleaning", "type": "Robot Vacuum", "capacity": "30W", "wattage": 30, "prefix" : "CLE"},

        # 💡 Lighting
        {"id" : 53, "category": "Lighting", "type": "LED Bulb", "capacity": "5W", "wattage": 5, "prefix" : "LIG"},
        {"id" : 54, "category": "Lighting", "type": "LED Bulb", "capacity": "9W", "wattage": 9, "prefix" : "LIG"},
        {"id" : 55, "category": "Lighting", "type": "LED Bulb", "capacity": "12W", "wattage": 12, "prefix" : "LIG"},
        {"id" : 56, "category": "Lighting", "type": "Fluorescent Lamp", "capacity": "18W", "wattage": 18, "prefix" : "LIG"},
        {"id" : 57, "category": "Lighting", "type": "Incandescent Bulb", "capacity": "40W", "wattage": 40, "prefix" : "LIG"},
        {"id" : 58, "category": "Lighting", "type": "Incandescent Bulb", "capacity": "60W", "wattage": 60, "prefix" : "LIG"},
        {"id" : 59, "category": "Lighting", "type": "Night Light", "capacity": "1W", "wattage": 1, "prefix" : "LIG"},
        {"id" : 60, "category": "Lighting", "type": "Chandelier", "capacity": "5 bulbs x 9W", "wattage": 45, "prefix" : "LIG"},

        # 📱 Gadgets
        {"id" : 61, "category": "Electronics", "type": "Desktop Computer", "capacity": "Standard", "wattage": 400, "prefix" : "ELE"},
        {"id" : 62, "category": "Electronics", "type": "Laptop", "capacity": "Standard", "wattage": 65, "prefix" : "ELE"},
        {"id" : 63, "category": "Electronics", "type": "Wi-Fi Router", "capacity": "Standard", "wattage": 10, "prefix" : "ELE"},
        {"id" : 64, "category": "Electronics", "type": "Mobile Phone Charger", "capacity": "Standard", "wattage": 5, "prefix" : "ELE"},
        {"id" : 65, "category": "Electronics", "type": "Tablet Charger", "capacity": "Standard", "wattage": 10, "prefix" : "ELE"},
        {"id" : 66, "category": "Electronics", "type": "Smart TV", "capacity": "32\"", "wattage": 50, "prefix" : "ELE"},
        {"id" : 67, "category": "Electronics", "type": "Smart TV", "capacity": "55\"", "wattage": 120, "prefix" : "ELE"},
        {"id" : 68, "category": "Electronics", "type": "CRT TV", "capacity": "21\"", "wattage": 90, "prefix" : "ELE"},
        {"id" : 69, "category": "Electronics", "type": "Gaming Console", "capacity": "Standard", "wattage": 200, "prefix" : "ELE"},
        {"id" : 70, "category": "Electronics", "type": "Home Theater", "capacity": "Standard", "wattage": 250, "prefix" : "ELE"},
        {"id" : 71, "category": "Electronics", "type": "Projector", "capacity": "Standard", "wattage": 300, "prefix" : "ELE"},

        # 🛏️ Bedroom / Wellness
        {"id" : 72, "category": "Wellness", "type": "Air Purifier", "capacity": "Standard", "wattage": 50, "prefix" : "WL"},
        {"id" : 73, "category": "Wellness", "type": "Air Purifier with Humidifier", "capacity": "Standard", "wattage": 75, "prefix" : "WL"},
        {"id" : 74, "category": "Wellness", "type": "Aroma Diffuser", "capacity": "Standard", "wattage": 10, "prefix" : "WL"},
        {"id" : 75, "category": "Wellness", "type": "Electric Blanket", "capacity": "Standard", "wattage": 60, "prefix" : "WL"},
        {"id" : 76, "category": "Wellness", "type": "Dehumidifier", "capacity": "Standard", "wattage": 300, "prefix" : "WL"},
        {"id" : 77, "category": "Wellness", "type": "Massage Chair", "capacity": "Standard", "wattage": 150, "prefix" : "WL"},
        {"id" : 78, "category": "Wellness", "type": "Sleep Sound Machine", "capacity": "Standard", "wattage": 10, "prefix" : "WL"}
    ]
        
    @classmethod
    def get_appliance_by_id(cls, appliance_id):
        try:
            appliance_id = int(appliance_id)
        except (ValueError, TypeError):
            return None

        for appliance in cls.appliances:
            if appliance['id'] == appliance_id:
                return appliance
        return None

