from experta import *


class MyFact(KnowledgeEngine):
    type_vehicule = ''
    vehicule = ''
    rules = []
    os = ''
    phone = ''
    resultat = ''

    @Rule(Fact(number_wheels=4), Fact(motor='yes'))
    def Automobile(self):
        self.type_vehicule = 'Automobile'
        self.declare(Fact(type_vehicule=self.type_vehicule))
        self.rules.append("number_wheels = 4 AND motor = yes")
        print('Automobile rule is used')

    @Rule(Fact(number_wheels=P(lambda number_wheels: number_wheels < 4)))
    def Cycle(self):
        self.type_vehicule = 'Cycle'
        self.resultat = 'Cycle'
        self.declare(Fact(type_vehicule=self.type_vehicule))
        self.rules.append("number_wheels <= 4 ")
        print('Cycle rule is used')

    @Rule(Fact(type_vehicule='Cycle'), Fact(number_wheels=2), Fact(motor='no'))
    def Bicycle(self):
        self.vehicule = 'Bicycle'
        self.resultat = 'Bicycle'
        self.rules.append(
            "type_vehicule = Cycle AND number_wheels = 2 AND motor = no")
        print('Bicycle rule is used')

    @Rule(Fact(type_vehicule='Cycle'), Fact(number_wheels=2), Fact(motor='yes'))
    def Motorcycle(self):
        self.vehicule = 'Motorcycle'
        self.resultat = 'Motorcycle'
        self.rules.append(
            "type_vehicule = Cycle AND number_wheels = 2 AND motor = yes")
        print('Motorcycle rule is used')

    @Rule(Fact(type_vehicule='Cycle'), Fact(number_wheels=3), Fact(motor='yes'))
    def Tricycle(self):
        self.vehicule = 'Tricycle'
        self.resultat = 'Tricycle'
        self.rules.append(
            "type_vehicule = Cycle AND number_wheels = 3 AND motor = yes")
        print('Tricycle rule is used')

    @Rule(Fact(type_vehicule='Automobile'), Fact(number_doors=2), Fact(size='small'))
    def SportCar(self):
        self.vehicule = 'SportCar'
        self.resultat = 'SportCar'
        self.rules.append(
            "type_vehicule = Automobile AND number_doors = 2 AND motor = yes AND size = small")
        print('SportCar rule is used')

    @Rule(Fact(type_vehicule='Automobile'), Fact(number_doors=4), Fact(size='medium'))
    def Sedan(self):
        self.vehicule = 'Chevrolet'
        self.resultat = 'Chevrolet'
        self.rules.append(
            "type_vehicule = Automobile AND number_doors = 4 AND motor = yes AND size = medium")
        print('Sedan rule is used')

    @Rule(Fact(type_vehicule='Automobile'), Fact(number_doors=3), Fact(size='medium'))
    def MiniVan(self):
        self.vehicule = 'MiniVan'
        self.resultat = 'MiniVan'
        self.rules.append(
            "type_vehicule = Automobile AND number_doors = 3 AND motor = yes AND size = medium")
        print('MiniVan rule is used')

    @Rule(Fact(type_vehicule='Automobile'), Fact(number_doors=4), Fact(size='large'))
    def SUV(self):
        self.vehicule = 'Sport_Utility_Vehicule'
        self.resultat = 'Sport_Utility_Vehicule'
        self.rules.append(
            "type_vehicule = Automobile AND number_doors = 4 AND motor = yes AND size = large")
        print('Sport_Utility_Vehicule rule is used')

    # ******************************************************************************************************************

    @Rule(Fact(brand='Apple'))
    def ios(self):
        self.os = 'iOS'
        self.declare(Fact(os=self.os))
        self.rules.append("os = iOS")
        print('iOS rule is used')

    @Rule(NOT(Fact(brand='Apple')))
    def android(self):
        self.os = 'Android'
        self.declare(Fact(os=self.os))
        self.rules.append("os = Android")
        print('Android rule is used')

    @Rule(Fact(os='iOS'), Fact(brand='Apple'), Fact(ram=4),
          Fact(stockage=P(lambda stockage: stockage >= 64)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 100000) & P(lambda price: price <= 125000)))
    def iPhone12(self):
        self.phone = 'iPhone 12'
        self.resultat = 'iPhone 12'
        self.rules.append(
            "brand = Apple AND ram=4 AND (stockage>=64 AND stockage<=256) AND (price>=100000 AND price <=125000)")
        print('iPhone 12 rule is used')

    @Rule(Fact(os='iOS'), Fact(brand='Apple'), Fact(ram=4),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 512)),
          Fact(price=P(lambda price: price >= 130000) & P(lambda price: price <= 160000)))
    def iPhone13(self):
        self.phone = 'iPhone 13'
        self.resultat = 'iPhone 13'
        self.rules.append(
            "brand = Apple AND ram=4 AND (stockage>=128 AND stockage<=512) AND (price>=130000 AND price <=160000)")
        print('iPhone 13 rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Samsung'), Fact(ram=4),
          Fact(stockage=P(lambda stockage: stockage >= 64)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 29000) & P(lambda price: price <= 65000)))
    def samsung_s9(self):
        self.phone = 'Samsung S9'
        self.resultat = 'Samsung S9'
        self.rules.append(
            "brand = Samsung AND ram=4 AND (stockage>=64 AND stockage<=128) AND (price>=29000 AND price <=65000)")
        print('Samsung_S9 rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Samsung'),
          Fact(ram=P(lambda ram: ram >= 12) & P(lambda ram: ram <= 16)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 512)),
          Fact(price=P(lambda price: price >= 110000) & P(lambda price: price <= 190000)))
    def samsung_s21_ultra(self):
        self.phone = 'Samsung S21 Ultra'
        self.resultat = 'Samsung S21 Ultra'
        self.rules.append(
            "brand = Samsung AND (ram>=12 AND ram<=16) AND (stockage>=128 AND stockage<=512) AND (price>=110000 AND price <=190000)")
        print('Samsung_S21_Ultra rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Huawei'),
          Fact(ram=P(lambda ram: ram >= 6) & P(lambda ram: ram <= 8)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 512)),
          Fact(price=P(lambda price: price >= 36000) & P(lambda price: price <= 94000)))
    def huawei_p30_pro(self):
        self.phone = 'Huawei P30 Pro'
        self.resultat = 'Huawei P30 Pro'
        self.rules.append(
            "brand = Huawei AND (ram>=6 AND ram<=8) AND (stockage>=128 AND stockage<=512) AND (price>=36000 AND price <=9400)")
        print('Huawei_P30_Pro rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Huawei'),
          Fact(ram=8),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 512)),
          Fact(price=P(lambda price: price >= 96000) & P(lambda price: price <= 190000)))
    def huawei_p40_pro(self):
        self.phone = 'Huawei P40 Pro'
        self.resultat = 'Huawei P40 Pro'
        self.rules.append(
            "brand = Huawei AND ram=8 AND (stockage>=128 AND stockage<=512) AND (price>=96000 AND price <=190000)")
        print('Huawei_P40_Pro rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Oppo'),
          Fact(ram=P(lambda ram: ram >= 8) & P(lambda ram: ram <= 12)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 102000) & P(lambda price: price <= 120000)))
    def oppo_reno5_pro(self):
        self.phone = 'Oppo Reno5 Pro'
        self.resultat = 'Oppo Reno5 Pro'
        self.rules.append(
            "brand = Oppo AND (ram>=8 AND ram<=12) AND (stockage>=128 AND stockage<=256) AND (price>=102000 AND price <=120000)")
        print('Oppo_Reno5_Pro rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Poco'),
          Fact(ram=P(lambda ram: ram >= 6) & P(lambda ram: ram <= 8)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 38000) & P(lambda price: price <= 41000)))
    def poco_x3_pro(self):
        self.phone = 'Poco X3 Pro'
        self.resultat = 'Poco X3 Pro'
        self.rules.append(
            "brand = Poco AND (ram>=6 AND ram<=8) AND (stockage>=128 AND stockage<=256) AND (price>=38000 AND price <=41000)")
        print('Poco X3 Pro rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Poco'),
          Fact(ram=P(lambda ram: ram >= 6) & P(lambda ram: ram <= 8)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 42000) & P(lambda price: price <= 50000)))
    def poco_f3(self):
        self.phone = 'Poco F3'
        self.resultat = 'Poco F3'
        self.rules.append(
            "brand = Poco AND (ram>=6 AND ram<=8) AND (stockage>=128 AND stockage<=256) AND (price>=42000 AND price <=50000)")
        print('Poco F3 rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Redmi'),
          Fact(ram=P(lambda ram: ram >= 6) & P(lambda ram: ram <= 8)),
          Fact(stockage=P(lambda stockage: stockage >= 64)
               & P(lambda stockage: stockage <= 128)),
          Fact(price=P(lambda price: price >= 36000) & P(lambda price: price <= 43000)))
    def xiaomi_redmi_note_10_pro(self):
        self.phone = 'Redmi Note 10 Pro'
        self.resultat = 'Redmi Note 10 Pro'
        self.rules.append(
            "brand = Redmi AND (ram>=6 AND ram<=8) AND (stockage>=64 AND stockage<=128) AND (price>=36000 AND price <=43000)")
        print('Redmi Note 10 Pro rule is used')

    @Rule(Fact(os='Android'), Fact(brand='Xiaomi'),
          Fact(ram=P(lambda ram: ram >= 8) & P(lambda ram: ram <= 12)),
          Fact(stockage=P(lambda stockage: stockage >= 128)
               & P(lambda stockage: stockage <= 256)),
          Fact(price=P(lambda price: price >= 131000) & P(lambda price: price <= 167000)))
    def xiaomi_12_pro(self):
        self.phone = 'Xiaomi 12 Pro'
        self.resultat = 'Xiaomi 12 Pro'
        self.rules.append(
            "brand = Xiaomi AND (ram>=8 AND ram<=12) AND (stockage>=128 AND stockage<=256) AND (price>=131000 AND price <=167000)")
        print('Xiaomi 12 Pro rule is used')
