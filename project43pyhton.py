import sqlite3
import pandas as pd 
import os
import csv

print('________run_________')

#-------To open the database------
#--- changed the database name to be able to easily distinguish between the .py itself 

dbase = sqlite3.connect('database_group43.db', isolation_level=None)

#---TABLES---

#---Total number of tables are as follows: 

#---Company: These are the (actual customers) companies that use our service 
#---Customer: These are the customers of our customers 
#---CustomerAccount: This table will create a combination of Company-Customer
#---Products: These are the variety of avaliable products provided by our customers  
#---Subscriptions: This table keeps track of subscriptions 
#---Invocie: This table tracks the date, paid/no paid details 
#---Payments: This table keeps track of payments 

#---Table refresher

dbase.execute('''DROP TABLE IF EXISTS Company''')
dbase.execute('''DROP TABLE IF EXISTS Customer''')
dbase.execute('''DROP TABLE IF EXISTS ExchangeRate''')
dbase.execute('''DROP TABLE IF EXISTS Product''')
dbase.execute('''DROP TABLE IF EXISTS CustomerAccount''')
dbase.execute('''DROP TABLE IF EXISTS Quote''')
dbase.execute('''DROP TABLE IF EXISTS Subscription''')
dbase.execute('''DROP TABLE IF EXISTS Invocie''')
dbase.execute('''DROP TABLE IF EXISTS Payment''')



#---Company
 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS Company(
        CompanyID                    INTEGER PRIMARY KEY AUTOINCREMENT,
        Company_Name                 TEXT NOT NULL,
        Company_AddressCountry       TEXT NOT NULL,
        Company_AddressState         TEXT NOT NULL,
        Company_AddressCity          TEXT NOT NULL,
        Company_AddressStreet        TEXT NOT NULL,
        Company_AddressNumber        TEXT NOT NULL,
        Company_AddressPostCode      TEXT NOT NULL,
        Company_VATID                TEXT NOT NULL, 
        Company_BankAccNumber        TEXT NOT NULL,
        Company_BankAccName          TEXT NOT NULL 
    )    
    ''')


#---the code below calls the following functions
#---Deletes Customer table
#---Creates table customer
#---Imports 1000 lines worth of customer data  

dbase.execute('''
    CREATE TABLE IF NOT EXISTS Customer(
        CustomerID                   INTEGER PRIMARY KEY AUTOINCREMENT,
        Customer_Name                TEXT NOT NULL,
        Customer_Surname             TEXT NOT NULL,
        Customer_AddressCountry      TEXT NOT NULL,
        Customer_AddressState        TEXT,
        Customer_AddressCity         TEXT NOT NULL,
        Customer_AddressStreet       TEXT NOT NULL,
        Customer_AddressNumber       TEXT NOT NULL,
        Customer_AddressPostCode     TEXT, 
        Customer_CCNumber            TEXT NOT NULL  
    )    
    ''')





#ExchangeRate   
dbase.execute('''
    CREATE TABLE IF NOT EXISTS ExchangeRate(
        CurrencyCode                TEXT PRIMARY KEY,
        Date                        DATE NOT NULL,
        InEuro                      FLOAT NOT NULL
    )
    ''')


#Product 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        ProductID                   INTEGER PRIMARY KEY AUTOINCREMENT,
        CurrencyCode                CHAR NOT NULL,
        ProductName                 TEXT NOT NULL,
        PriceLocal                  FLOAT NOT NULL,
        CompanyID                   INTEGER NOT NULL, 
        FOREIGN KEY(CurrencyCode) REFERENCES ExchangeRate(CurrencyCode)
        FOREIGN KEY(CompanyID) REFERENCES Company(CompanyID)
    )    
    ''')


#CustomerAccount 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS CustomerAccounts(
        CustomerAccountID           INTEGER PRIMARY KEY AUTOINCREMENT,
        CompanyID                   INTEGER,
        CustomerID                  INTEGER, 
        FOREIGN KEY(CompanyID) REFERENCES Company(CompanyID),
        FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID) 
    )      
    ''')



#Subscription 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS Subscriptions(
        SubscriptionID              INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerAccountID           INTEGER,
        CompanyID                   INTEGER,
        QuoteID                     INTEGER,
        ProductID                   INTEGER,
        Quantity                    INTEGER NOT NULL,
        TotalPriceVATE              FLOAT,
        TotalPriceVATI              FLOAT,
        Acceptance                  BOOLEAN,
        Active                      BOOLEAN,
        StartDate                   DATE,
        EndDate                     DATE,
        FOREIGN KEY(CustomerAccountID) REFERENCES CustomerAccount(CustomerAccountID),
        FOREIGN KEY(CompanyID) REFERENCES Company(CompanyID),
        FOREIGN KEY(ProductID) REFERENCES Product(ProductID),
        FOREIGN KEY(QuoteID) REFERENCES Quote(QuoteID)
    )    
    ''')



#Invoice 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS Invoice(
        InvoiceID                   INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerAccountID           INTEGER
        InvoiceDate                 DATE,
        DueDate                     DATE,
        Paid                        BOOLEAN,      
        CustomerID                  INTEGER,
        TotalDueEuro                FLOAT,
        Paid                        BOOLEAN,
        CompanyID                   INTEGER,
        FOREIGN KEY(CustomerAccountID) REFERENCES CustomerAccount(CustomerAccountID),
        FOREIGN KEY(CompanyID) REFERENCES Ccompanies(CompanyID)
    )    
    ''')


#Payment 
dbase.execute('''
    CREATE TABLE IF NOT EXISTS Payment(
        PaymentID                   INTEGER PRIMARY KEY AUTOINCREMENT,
        InvoiceID                   INTEGER,
        Date                        DATE,
        Amount                      FLOAT,
        FOREIGN KEY(InvoiceID) REFERENCES Invoice(InvoiceID)
    )    
    ''')

#-----------------





#---Functions of INSERT INTO---


#---Company

def record_a_new_company(
        Company_Name,           
        Company_AddressCountry,  
        Company_AddressState, 
        Company_AddressCity,
        Company_AddressStreet,
        Company_AddressNumber,
        Company_AddressPostCode,
        Company_VATID,           
        Company_BankAccNumber,
        Company_BankAccName):
    dbase.execute('''
        INSERT INTO Company(
        Company_Name,           
        Company_AddressCountry,  
        Company_AddressState, 
        Company_AddressCity,
        Company_AddressStreet,
        Company_AddressNumber,
        Company_AddressPostCode,
        Company_VATID,           
        Company_BankAccNumber,
        Company_BankAccName)
        VALUES(?,?,?,?,?,?,?,?,?,?)     
        '''
        ,
        (
        Company_Name,           
        Company_AddressCountry,  
        Company_AddressState, 
        Company_AddressCity,
        Company_AddressStreet,
        Company_AddressNumber,
        Company_AddressPostCode,
        Company_VATID,           
        Company_BankAccNumber,
        Company_BankAccName))

#---

def record_a_new_customer( 
        Customer_Name,           
        Customer_Surname,        
        Customer_AddressCountry, 
        Customer_AddressState,
        Customer_AddressCity,   
        Customer_AddressStreet,  
        Customer_AddressNumber,  
        Customer_AddressPostCode,
        Customer_CCNumber       
        ):
        dbase.execute('''
        INSERT INTO Customer(
        Customer_Name,           
        Customer_Surname,        
        Customer_AddressCountry, 
        Customer_AddressState,
        Customer_AddressCity, 
        Customer_AddressStreet,  
        Customer_AddressNumber,  
        Customer_AddressPostCode,
        Customer_CCNumber)
        VALUES(?,?,?,?,?,?,?,?,?)     
        '''
        ,
        (          
        Customer_Name,           
        Customer_Surname,        
        Customer_AddressCountry, 
        Customer_AddressState,
        Customer_AddressCity,   
        Customer_AddressStreet,  
        Customer_AddressNumber,  
        Customer_AddressPostCode,
        Customer_CCNumber))



def ExchangeRate_recorder( 
        CurrencyCode,
        Date,  
        InEuro,  
        ):
        dbase.execute('''
        INSERT INTO ExchangeRate(
            CurrencyCode,
            Date,  
            InEuro
        )
        VALUES(?,?,?)     
        '''
        ,
        (          
        CurrencyCode,
        Date,        
        InEuro,      ))

def Product_recorder( 
        ProductName,  
        PriceEUR,     
        PriceLocal,   
        ):  
        dbase.execute('''
        INSERT INTO Products(
            ProductName,  
            PriceEUR,     
            PriceLocal,
        )
        VALUES(?,?,?)     
        '''
        ,
        (          
        ProductName,  
        PriceEUR,     
        PriceLocal))


def Quote_recorder( 
        Date,   
        ):  
        dbase.execute('''
        INSERT INTO Quote(
            Date,  
        )
        VALUES(?)     
        '''
        ,
        (          
        Date))


def Subscription_recorder( 
        Quantity, 
        Active,   
        StartDate,
        EndDate,  
        ):  
        dbase.execute('''
        INSERT INTO Quote(
            Quantity, 
            Active,   
            StartDate,
            EndDate, 
        )
        VALUES(?,?,?,?)     
        '''
        ,
        (  
        Quantity, 
        Active,   
        StartDate,
        EndDate,           
        ))






def Invocie_recorder( 
        Date, 
        DueDate,   
        Paid,
        ):  
        dbase.execute('''
        INSERT INTO Invoice(
            Date, 
            DueDate,   
            Paid, 
        )
        VALUES(?,?,?)     
        '''
        ,
        ( 
        Date, 
        DueDate,   
        Paid,
        ))


def Invocie_recorder( 
        Date, 
        Amount,
        ):  
        dbase.execute('''
        INSERT INTO Invoice(
            Date, 
            Amount,   
        )
        VALUES(?,?)     
        '''
        ,
        ( 
        Date, 
        Amount,
        ))


#---Filling the database 
#---You will need to populate your database to be able to test your code 

#---create a variable to be able to write down all the companies at once
Company_List=(

    ('Meta','USA','LA','San diego','FB street','368','1020','1364763834','128361726317823', 'Bank of America'),
    ('Microsoft','USA','LA','San diego','MSFT street','369','1021','1364763835','128361726317824', 'Bank of America'),
    ('Google','USA','LA','San diego','GOOGL street','370','1022','1364763836','128361726317824', 'Bank of America'),
    ('Nvidia','USA','LA','San diego','NVDA street','371','1023','1364763837','128361726317825', 'Bank of America'),
    ('Tesla','USA','TX','Houston','TSLA street','372','1024','1364763838','128361726317826', 'Bank of America'),
    ('Oracle','USA','LA','San diego','ORCL street','373','1025','1364763839','128361726317827', 'Bank of America'),
    ('Apple','USA','LA','San diego','AAPL street','374','1026','1364763840','128361726317828', 'Bank of America'),
    ('Spotify','Sweden','Stockholm','Stockholm','Syndrome street','375','1027','1364763841','SE128361726317823', 'Bank of Sweden'),
    ('Uber','USA','LA','San diego','UBER street','376','1028','1364763842','128361726317829', 'Bank of America'),
    ('Lyft','USA','LA','San diego','LYFT street','377','1029','1364763843','128361726317830', 'Bank of America'),
    ('Netflix','USA','LA','San diego','NFLX street','378','1030','1364763844','128361726317831', 'Bank of America'),
    ('Klarna','Sweden','Stockholm','Stockholm','Syndrome street','379','1031','1364763845','SE128361726317824', 'Bank of Sweden'),
    ('Dell','USA','LA','San diego','DELL street','380','1032','1364763846','128361726317832', 'Bank of America'),
    ('UCLA','USA','LA','San diego','UCLA street','381','1033','1364763847','128361726317833', 'Bank of America')
    )

#--- to import data in bulk 

for Company_Name, Company_AddressCountry,Company_AddressState, Company_AddressCity,Company_AddressStreet,Company_AddressNumber,Company_AddressPostCode,Company_VATID, Company_BankAccNumber, Company_BankAccName in Company_List:
    record_a_new_company(Company_Name, Company_AddressCountry,Company_AddressState, Company_AddressCity,Company_AddressStreet,Company_AddressNumber,Company_AddressPostCode,Company_VATID, Company_BankAccNumber,Company_BankAccName)
print('companies imported')





Customer_List=(
    ('Wat', 'Myring', 'Thailand', None, 'Watthana Nakhon', 'Fordem', '54659', '34230', '56022266748153064'),
    ('Brook', 'Riby', 'Portugal', 'Viseu', 'Oliveirinha', 'South', '4', '3430-393', '3536866970807559'),
    ('Laureen', 'Hearsum', 'Indonesia', None, 'Margotuhu Kidul', 'Lakewood', '2664', None, '675967718400894959'),
    ('Kristal', 'Trenaman', 'Peru', None, 'Iberia', 'Londonderry', '666', None, '4911927251141051246'),
    ('Thayne', 'Blunsen', 'Colombia', None, 'Chipaque', 'Barnett', '02', '251808', '4041591408090802'),
    ('Marlyn', 'Guiso', 'Indonesia', None, 'Banjaranyar', 'Jay', '29311', None, '3543136510685001'),
    ('Camille', 'Garrard', 'Argentina', None, 'Loreto', 'Harper', '3', '3483', '3556920445064893'),
    ('Glenda', 'Aitchison', 'Canada', 'Ontario', 'Amherstburg', 'Talisman', '7', 'N9V', '56022103672145941'),
    ('Lenora', 'Birnie', 'Sweden', 'Jönköping', 'Habo', 'Ryan', '4111', '566 24', '6382656959235858'),
    ('Hercule', 'Scollan', 'Finland', None, 'Längelmäki', 'Hansons', '87', '35400', '337941027101905'),
    ('Constantine', 'Ferrarello', 'Indonesia', None, 'Gawanan', 'Independence', '6', None, '30391983169217'),
    ('Kacie', 'Courage', 'Sweden', 'Västmanland', 'Västerås', 'Hintze', '3140', '721 19', '5602249221856159091'),
    ('Heindrick', 'Harvison', 'Colombia', None, 'Combita', 'Pepper Wood', '31', '150208', '4405412890894504'),
    ('Julietta', 'Brockie', 'Thailand', None, 'Si Narong', 'Fallview', '03840', '34000', '56022343096833660'),
    ('Selby', 'Chidlow', 'Indonesia', None, 'Sukabumi', 'Lighthouse Bay', '35718', None, '3561611257886860'),
    ('Lottie', 'Everil', 'Indonesia', None, 'Bojongnangka', 'Burning Wood', '8', None, '3550982996750961'),
    ('Sherm', 'Caroli', 'China', None, 'Muzi', 'Northfield', '5959', None, '201894388602867'),
    ('Pryce', 'Ratcliffe', 'Indonesia', None, 'Babantar', 'Marquette', '23', None, '5452721688390965'),
    ('Chaim', 'Dwire', 'Russia', None, 'Krasnogvardeyets', 'Sugar', '40854', '102469', '633484956762995641'),
    ('Ginny', 'Kleewein', 'Belarus', None, 'Loyew', 'Rieder', '05', None, '3580430987534600'),
    ('Janaya', 'Fidelus', 'Philippines', None, 'Tartaro', 'Mcbride', '17', '2307', '5602217254492698'),
    ('Hinda', 'Pointing', 'Brazil', None, 'Igaraçu do Tietê', 'Victoria', '27', '17350-000', '3559947835151565'),
    ('Georgie', 'Drydale', 'Indonesia', None, 'Sukamaju', 'Dryden', '546', None, '4017958478018379'),
    ('Edlin', 'Dondon', 'Gambia', None, 'Bambali', 'Bayside', '08209', None, '4844360692236524'),
    ('Kinna', 'Earey', 'Senegal', None, 'Richard-Toll', 'Nobel', '71', None, '30343069592978'),
    ('Skye', 'McKenzie', 'Russia', None, 'Mikhaylovka', 'Melrose', '6', '613384', '677176040570466176'),
    ('Rube', 'Denkin', 'Colombia', None, 'La Vega', 'Crowley', '6', '253618', '3562613075614812'),
    ('Cami', 'Chedzoy', 'Poland', None, 'Dobra', 'Eastlawn', '4', '72-210', '56022432164640295'),
    ('Wilma', 'Dickins', 'Russia', None, 'Yakovlevskoye', 'Meadow Valley', '6', '242791', '3530266712583608'),
    ('Milly', 'Fetter', 'China', None, 'Huilong', 'Huxley', '5', None, '56022256309173676'),
    ('Wolfy', 'Elmar', 'Morocco', None, 'Sefrou', 'David', '4289', None, '5048370158132514'),
    ('Dario', 'Hourstan', 'Indonesia', None, 'Ransiki', 'Victoria', '9312', None, '3575345830534424'),
    ('Dix', 'Sloley', 'South Korea', None, 'Hwasun', 'Village Green', '8', None, '56022167124316459'),
    ('Tracy', 'Joret', 'China', None, 'Dongzaogang', 'Barnett', '21', None, '5419864711673304'),
    ('Brinna', 'Deniset', 'Portugal', 'Santarém', 'Praia do Ribatejo', 'Sachtjen', '93', '2260-100', '201575688220191'),
    ('Deina', 'Gotfrey', 'Indonesia', None, 'Nambak Tengah', 'Wayridge', '0706', None, '3567333995704206'),
    ('Abigael', 'Mizzen', 'Mexico', 'Mexico', 'Pueblo Nuevo', 'Starling', '46760', '52332', '5602225643695954'),
    ('Candi', 'Lardier', 'Poland', None, 'Naprawa', 'Weeping Birch', '65909', '34-721', '4913430467328313'),
    ('Esdras', 'Steagall', 'Sweden', 'Västra Götaland', 'Västra Frölunda', 'Bay', '7', '421 62', '677180565486944662'),
    ('Albert', 'Sworder', 'Nicaragua', None, 'Siuna', 'Farwell', '9264', None, '374288345247075'),
    ('Nicolette', 'Hunting', 'Russia', None, 'Abakan', 'Toban', '60763', '655131', '3565467293060630'),
    ('Egon', 'Toffoloni', 'Estonia', None, 'Aseri', 'Gulseth', '1', None, '3588931576237754'),
    ('Hersch', 'Schuster', 'Somalia', None, 'Oodweyne', 'Sundown', '50', None, '5100148077134349'),
    ('Brodie', 'Dewey', 'Finland', None, 'Loimaan Kunta', 'Grover', '3', '32560', '3559202651403181'),
    ('Kale', 'Crocetti', 'Czech Republic', None, 'Kněžpole', 'Spaight', '32825', '793 51', '3588885507577763'),
    ('Teresa', 'Oldfield', 'China', None, 'Longshan', 'Sachs', '52958', None, '3571204484460549'),
    ('Nolana', 'Somner', 'Russia', None, 'Uritsk', 'Sheridan', '83', '663594', '3554708707117794'),
    ('Ellie', 'Neljes', 'Azerbaijan', None, 'Nardaran', 'Arkansas', '88946', None, '201452204927933'),
    ('Jared', 'Olohan', 'United Kingdom', 'England', 'Langley', 'Pleasure', '790', 'SG4', '6390061290884532'),
    ('Yanaton', 'Sutch', 'China', None, 'Chimen', 'Mariners Cove', '8', None, '3530356964425796'),
    ('Kailey', 'Vicar', 'China', None, 'Nanzhang Chengguanzhen', 'Carberry', '70642', None, '4911050409449812722'),
    ('Donnajean', 'Cogin', 'United States', 'Ohio', 'Columbus', 'Scott', '22824', '43210', '3586875364154246'),
    ('Genny', 'Teliga', 'Indonesia', None, 'Pamakayo', 'Pepper Wood', '67388', None, '3567578430638886'),
    ('Martita', 'Mobius', 'Bosnia and Herzegovina', None, 'Bileća', 'Mcbride', '4', None, '67061351923950119'),
    ('Claretta', 'Tille', 'Belarus', None, 'Haradok', 'Fisk', '649', None, '3584847045278936'),
    ('Myra', 'Brydone', 'Ukraine', None, 'Zachepylivka', 'Ramsey', '31098', None, '5602225197960465'),
    ('Shandeigh', 'Banks', 'French Polynesia', None, 'Vaitape', 'Stang', '28', None, '3547694320565306'),
    ('Allyson', 'Leacock', 'Spain', 'Galicia', 'Ferrol', 'Sachtjen', '7', '15490', '4844579386999721'),
    ('Athene', 'Beig', 'Ivory Coast', None, 'Arrah', 'Oneill', '3', None, '6333678952307203'),
    ('Robby', 'Spottiswood', 'Indonesia', None, 'Bamban', 'Crest Line', '509', None, '3551348526680558'),
    ('Albertina', 'Falcus', 'China', None, 'Yidian', 'Merchant', '85046', None, '6304362730554205'),
    ('Vaughan', 'Phillis', 'Poland', None, 'Miechów Charsznica', 'Stoughton', '90', '32-200', '30558082202137'),
    ('Pavel', 'Roseveare', 'Peru', None, 'Moche', 'Kings', '1', None, '5602223989763221'),
    ('Sallie', 'Gillions', 'Philippines', None, 'Bagong Barrio', 'Sundown', '5', '7209', '503869951121852674'),
    ('Keir', 'Frosdick', 'Philippines', None, 'Buenlag', 'Heath', '73', '2302', '3579266967756927'),
    ('Ora', 'Stave', 'Indonesia', None, 'Darunban', 'Elgar', '665', None, '5100141136862968'),
    ('Sallyann', 'Codlin', 'Nigeria', None, 'Katagum', 'Oxford', '94', None, '06041091062630014'),
    ('Jasmin', 'Timson', 'Russia', None, 'Pochinok', 'Prairie Rose', '9486', '216486', '6331105743722476'),
    ('Krishna', 'Chiene', 'Uzbekistan', None, 'Yangiyŭl', 'Loftsgordon', '29275', None, '5576786827670784'),
    ('Abigale', 'Angelo', 'Philippines', None, 'Paluan', 'Lakewood', '0', '5107', '5602233664424643'),
    ('Alleyn', 'Tough', 'Indonesia', None, 'Cikondang', 'Roth', '7534', None, '3581128214207722'),
    ('Wynn', 'Kasper', 'United States', 'Nevada', 'Las Vegas', 'Golf Course', '73050', '89110', '6709648084953223643'),
    ('Roselia', 'Noakes', 'Latvia', None, 'Strenči', 'South', '332', None, '201747741301835'),
    ('Kaleb', 'Plumer', 'Jamaica', None, 'Annotto Bay', 'Northfield', '1139', None, '3550696759145850'),
    ('Laura', 'Poznanski', 'Brazil', None, 'Forquilhinha', 'Myrtle', '442', '88850-000', '5497519810113900'),
    ('Wanids', 'Donaho', 'Croatia', None, 'Retkovci', 'Dayton', '873', '32282', '5218735281420792'),
    ('Jackqueline', 'Slinger', 'Greece', None, 'Irákleion', 'Randy', '9123', None, '374622053118963'),
    ('Ediva', 'Bellanger', 'Mexico', 'Tamaulipas', 'Guadalupe Victoria', 'Eagan', '5', '87086', '3541421210891527'),
    ('Valentina', 'Macveigh', 'China', None, 'Dongjiao', 'Morningstar', '40635', None, '3535134392916750'),
    ('Wilie', 'Dobrovsky', 'Nicaragua', None, 'La Concordia', 'Westridge', '82', None, '3561002059899519'),
    ('Enrique', 'Spicer', 'Indonesia', None, 'Piru', 'Cascade', '47859', None, '3569966870364774'),
    ('Byram', 'Thick', 'China', None, 'Jinzao', 'Annamark', '78710', None, '67639017697316927'),
    ('Celestyn', 'Blazhevich', 'Indonesia', None, 'Kemang', 'Eggendart', '5789', None, '4913549404705141'),
    ('Gisela', 'Bandiera', 'Philippines', None, 'Milagros', 'Gateway', '4808', '5410', '5602247155535832'),
    ('Lesly', 'Giovanitti', 'Afghanistan', None, 'Khūgyāṉī', 'Spaight', '798', None, '3551554444740115'),
    ('Staci', 'Sandifer', 'Indonesia', None, 'Tanjungagung', 'Fair Oaks', '900', None, '201420374221833'),
    ('Peggy', 'Torrijos', 'Poland', None, 'Malczyce', 'Maple', '796', '55-320', '3576538032917236'),
    ('Tate', 'Swindley', 'Democratic Republic of the Congo', None, 'Bondo', 'Helena', '202', None, '4905633135030720'),
    ('Hubey', 'Goacher', 'New Zealand', None, 'Kawakawa', 'Nobel', '4', '0243', '633330240338383772'),
    ('Connie', 'Fernanando', 'Ukraine', None, 'Trostyanets’', 'Kipling', '817', None, '3532427039397266'),
    ('Geordie', 'Berthelmot', 'Moldova', None, 'Bilicenii Vechi', 'Rieder', '9', 'MD-6214', '4864015248641164'),
    ('Daniela', 'Furze', 'Poland', None, 'Bielice', 'Haas', '4645', '74-202', '4175006854420823'),
    ('Curr', 'Aubri', 'Russia', None, 'Mikhaylovka', 'Meadow Vale', '41', '613384', '3572505779925361'),
    ('Sybilla', 'Pyson', 'Mongolia', None, 'Avdzaga', 'Blue Bill Park', '7', None, '3574620508206187'),
    ('Griffy', 'Jeffry', 'Poland', None, 'Grojec', 'Brown', '5', '32-615', '3536589505058312'),
    ('Beale', 'Balding', 'France', 'Franche-Comté', 'Besançon', 'Farragut', '171', '25024 CEDEX', '4844815827324081'),
    ('Gaspar', 'Dunsford', 'South Africa', None, 'Phuthaditjhaba', 'Hudson', '7', '9869', '5100138915704692'),
    ('Ferdinanda', 'Munson', 'Brazil', None, 'Salinas', 'Thackeray', '0421', '39560-000', '5018842526079147297'),
    ('Colver', 'Demchen', 'China', None, 'Shizuishan', 'Duke', '0696', None, '589328254833039639'),
    ('Beverlee', 'Deinert', 'China', None, 'Shuanghe', 'Sullivan', '07383', None, '3579818667482004'),
    ('Ronnie', 'Wallenger', 'Indonesia', None, 'Tembongraja', 'Golf Course', '80', None, '5602218167221760'),
    ('Deny', 'Hurdiss', 'China', None, 'Wuda', 'Jackson', '227', None, '4353235750246'),
    ('Loy', 'Candey', 'France', 'Languedoc-Roussillon', 'Nîmes', 'Tomscot', '5651', '30935 CEDEX 9', '3564439993936097'),
    ('Ingrim', 'Lefeuvre', 'Portugal', 'Ilha da Madeira', 'Canhas', 'Ryan', '2', '9360-305', '201900926828573'),
    ('Alie', 'Mowett', 'Armenia', None, 'Gyumri', 'Roth', '51', None, '3583891288766448'),
    ('Saloma', 'Filochov', 'China', None, 'Duanjia', 'Stone Corner', '4', None, '3588092179062899'),
    ('Yasmin', 'Prew', 'Philippines', None, 'San Pedro Apartado', 'Dennis', '1', '7024', '30094001876561'),
    ('Bernardine', 'Batchelder', 'Ireland', None, 'Bagenalstown', 'Erie', '5584', 'R21', '3531487641108924'),
    ('Othelia', 'Otter', 'Philippines', None, 'Orion', 'Grayhawk', '35720', '2102', '374288504480863'),
    ('Gus', 'Brosetti', 'Zambia', None, 'Namwala', 'Atwood', '727', None, '372301227899244'),
    ('Lamar', 'Asals', 'Portugal', 'Leiria', 'Boco', 'Eliot', '965', '2425-405', '5602244289784238'),
    ('Celie', 'Tollerton', 'Russia', None, 'Khanino', '5th', '317', '301420', '374288185417309'),
    ('Orlan', 'Roll', 'China', None, 'Zhenlong', 'Dayton', '15', None, '63041850340668877'),
    ('Wileen', 'Aldhouse', 'Russia', None, 'Novovladykino', 'Colorado', '08435', '659436', '201649096663001'),
    ('Paolo', 'Ginsie', 'Thailand', None, 'Uthai Thani', 'Paget', '3374', '81140', '5462844244361631'),
    ('Wendye', 'Craw', 'Norway', 'Sor-Trondelag', 'Trondheim', 'Fordem', '3', '7047', '3577829364575448'),
    ('Dominick', 'Stillgoe', 'China', None, 'Yunyang', 'Corry', '9', None, '3533836622744669'),
    ('Archaimbaud', 'Ajean', 'Indonesia', None, 'Bunirasa', 'Clyde Gallagher', '39425', None, '4971245266732898'),
    ('Audrey', 'Warrilow', 'Azerbaijan', None, 'Arıqıran', 'Northland', '3434', None, '3557731814100179'),
    ('Roman', 'Eric', 'Ukraine', None, 'Rudky', 'Stone Corner', '1261', None, '5602238297776491'),
    ('Ceil', 'Colisbe', 'China', None, 'Longgang', 'Almo', '8', None, '36135221040340'),
    ('Gaynor', 'Mathiassen', 'Poland', None, 'Popielów', 'Kenwood', '02', '46-090', '372301750630263'),
    ('Anderson', 'Creak', 'Japan', None, 'Miyakonojō', 'Brentwood', '01', '889-1912', '0604003153400267855'),
    ('Sophey', 'Van Arsdall', 'Finland', None, 'Saari', 'Anniversary', '7', '59511', '3562376468725369'),
    ('Erie', 'Wilse', 'China', None, 'Liangshan', 'Melody', '106', None, '3529164517668877'),
    ('Naomi', 'Mordy', 'Indonesia', None, 'Ponjen', 'Scoville', '233', None, '6397131583128393'),
    ('Phillip', 'Manby', 'Portugal', 'Coimbra', 'Serra da Boa Viagem', 'Ilene', '3', '3080-352', '4402377090525377'),
    ('Letta', 'Dyde', 'China', None, 'Zhoujia', 'Barnett', '85799', None, '6709962914731085880'),
    ('Orland', 'Ewell', 'Russia', None, 'Reutov', 'Farwell', '3525', '143969', '630495378267844005'),
    ('Enoch', 'Cordie', 'Sweden', 'Stockholm', 'Bandhagen', 'Ruskin', '8', '124 76', '67630637261747238'),
    ('Munroe', 'Wallman', 'Ukraine', None, 'Kotsyubyns’ke', 'Dwight', '359', None, '5204549053090436'),
    ('Lorena', 'Nicolson', 'Thailand', None, 'Photharam', 'Sycamore', '193', '70120', '3543116705311514'),
    ('Nikki', 'Trinkwon', 'China', None, 'Obo', 'Kipling', '4', None, '3549995000275589'),
    ('Ogdon', 'Khan', 'Comoros', None, 'Limbi', 'Utah', '043', None, '3528064641475952'),
    ('Genny', 'McBrearty', 'Russia', None, 'Valuyki', 'Arapahoe', '07', '309999', '3529388001984884'),
    ('Hugues', 'Tully', 'France', 'Auvergne', 'Issoire', 'Elgar', '0', '63504 CEDEX', '5108755192507746'),
    ('Stillmann', 'Cresswell', 'Denmark', 'Region Hovedstaden', 'København', 'Quincy', '90651', '1291', '56022461476234281'),
    ('Ingram', 'Briffett', 'Japan', None, 'Tsukumiura', 'Blue Bill Park', '892', '879-2413', '5100143790220962'),
    ('Borg', 'Greenhowe', 'China', None, 'Wubao', 'Dakota', '51', None, '67713557266318852'),
    ('Friedrick', 'Mathewes', 'Brazil', None, 'Paracuru', 'Holy Cross', '5560', '62680-000', '3570035799829379'),
    ('Theda', 'Filipychev', 'Thailand', None, 'Sahatsakhan', 'Muir', '30857', '46140', '502017936380647876'),
    ('Lu', 'MacKaig', 'Poland', None, 'Czarna', 'Quincy', '63039', '39-215', '6762655478250342222'),
    ('Guthrey', 'Spinage', 'Canada', 'Saskatchewan', 'North Battleford', 'Everett', '4', 'S9A', '3557139509827454'),
    ('Sherri', 'Hoofe', 'China', None, 'Xiayang', 'Brown', '56', None, '3559733743343506'),
    ('Lea', 'Janusz', 'Mexico', 'Tamaulipas', 'Guadalupe Victoria', 'Michigan', '13002', '87086', '3582723296277269'),
    ('Wallas', 'Learmonth', 'China', None, 'Jitian', 'Riverside', '32', None, '4917102074534775'),
    ('Cos', 'Huntall', 'China', None, 'Wangchang', 'Coleman', '9450', None, '3561092032444251'),
    ('Merrielle', 'Lamar', 'Argentina', None, 'Zárate', 'Hoepker', '6591', '3423', '630460485223584152'),
    ('Terrijo', 'Fonzo', 'Indonesia', None, 'Rokoy', 'Summit', '0557', None, '3589423490169635'),
    ('Josefina', 'Grieger', 'Portugal', 'Faro', 'Alcoutim', 'Fremont', '3', '8970-055', '3543450008578663'),
    ('Lucilia', 'Maddox', 'Japan', None, 'Tochio-honchō', 'Monica', '56', '955-0156', '3583950198712361'),
    ('Yulma', 'Britner', 'Brazil', None, 'Nova Venécia', 'Montana', '45', '29830-000', '5602242107396540'),
    ('Karla', 'Crews', 'Philippines', None, 'Allacapan', 'Towne', '87', '3523', '3536974441893875'),
    ('Hagen', 'Kennelly', 'Thailand', None, 'Hang Dong', 'Evergreen', '24', '50230', '3550367201463156'),
    ('Ainslee', 'Enion', 'China', None, 'Shifo', 'Mcbride', '9', None, '676286728440426672'),
    ('Lexy', 'Martill', 'Greece', None, 'Pelópion', 'Eggendart', '7', None, '6759602290082371406'),
    ('Amanda', 'Linton', 'France', 'Poitou-Charentes', 'Saint-Maixent-l''École', 'Delaware', '00797', '79404 CEDEX', '633487213115242181'),
    ('Madlen', 'Ziemke', 'Mauritius', None, 'Espérance Trébuchet', 'Paget', '8', None, '675988566100858815'),
    ('Adolphe', 'Binestead', 'Indonesia', None, 'Petung', 'Bunker Hill', '43', None, '633351975243247869'),
    ('Dina', 'Killough', 'China', None, 'Jiancheng', 'Riverside', '7', None, '5602217800594690'),
    ('Rae', 'Chainey', 'Brazil', None, 'Lago da Pedra', 'Schlimgen', '90959', '65715-000', '3551483392293127'),
    ('Jerome', 'Dorman', 'Venezuela', None, 'Anaco', 'Portage', '82', None, '3553207757119025'),
    ('Rene', 'Dutson', 'Azerbaijan', None, 'Qızılhacılı', 'Twin Pines', '0048', None, '3580635759107050'),
    ('Cornie', 'Brompton', 'Indonesia', None, 'Bayeman', '4th', '893', None, '3555724636808048'),
    ('Malcolm', 'Kindell', 'Philippines', None, 'Santo Domingo', 'Canary', '3', '4508', '3570197771654538'),
    ('Rafi', 'Barbrook', 'Belarus', None, 'Horad Krychaw', 'Tomscot', '5', None, '5610701385305614'),
    ('Tedmund', 'Courtonne', 'China', None, 'Chahe', 'Northland', '418', None, '3554198450318585'),
    ('Perceval', 'Tender', 'Bolivia', None, 'Camatindi', 'Meadow Vale', '67944', None, '633470385042962872'),
    ('Gordy', 'Yeats', 'Portugal', 'Porto', 'Barrosas', 'Melby', '8133', '4650-127', '3551830946431639'),
    ('Aguste', 'Kupisz', 'Botswana', None, 'Makoba', 'Bartelt', '135', None, '5602224379839555'),
    ('Mathias', 'Pounds', 'United States', 'Pennsylvania', 'Wilkes Barre', 'Goodland', '2', '18706', '5551615286944613'),
    ('Ryan', 'Juster', 'Indonesia', None, 'Sendung', 'Mayer', '358', None, '6762449444581105846'),
    ('Freida', 'Rowberry', 'United States', 'Nevada', 'Las Vegas', 'Red Cloud', '43160', '89193', '5038903899695949949'),
    ('Stacy', 'Antyukhin', 'Philippines', None, 'Magallon Cadre', 'Randy', '37010', '6132', '3580039222587354'),
    ('Regen', 'Caughey', 'North Korea', None, 'Namyang-dong', 'Spenser', '884', None, '3547916968951625'),
    ('Franky', 'Beddis', 'Thailand', None, 'Mae Charim', 'Elmside', '05576', '55170', '3585549754368101'),
    ('Bathsheba', 'Howell', 'China', None, 'Luoyang', 'Schurz', '74', None, '3530015588957085'),
    ('Winnah', 'Shortcliffe', 'China', None, 'Beigucheng', 'Clarendon', '5', None, '3547121369992365'),
    ('Charles', 'Oguz', 'Philippines', None, 'Odiongan', 'Buhler', '020', '5505', '30371448331222'),
    ('Kalila', 'Roney', 'Indonesia', None, 'Peukanbada', 'Swallow', '7393', None, '201993697083494'),
    ('Ysabel', 'Extill', 'United States', 'Illinois', 'Chicago', 'Vernon', '34', '60624', '372301401222254'),
    ('Rachael', 'Sawood', 'Canada', 'Québec', 'L''Assomption', 'Fisk', '86', 'J5W', '201631312634925'),
    ('Kelila', 'Polin', 'Poland', None, 'Krzanowice', 'Barnett', '174', '47-470', '5108756533497456'),
    ('Arlan', 'Rentcome', 'China', None, 'Yangxi', 'Autumn Leaf', '44', None, '4508428266017039'))

for Customer_Name, Customer_Surname, Customer_AddressCountry, Customer_AddressState, Customer_AddressCity, Customer_AddressStreet, Customer_AddressNumber, Customer_AddressPostCode, Customer_CCNumber in Customer_List:
    record_a_new_customer(Customer_Name, Customer_Surname, Customer_AddressCountry, Customer_AddressState, Customer_AddressCity, Customer_AddressStreet, Customer_AddressNumber, Customer_AddressPostCode, Customer_CCNumber)
print('customers imported')








record_a_new_company("Test company", "Test address 1","Test adress 2", "Test adress 3 ","Test adress 4","Test adress 5","Test postal code","Test VAT ID ", "Test bank account number ","Test bank account name")

testcompanyprint = dbase.execute('''SELECT * FROM Company LIKE Test company''')
print(testcompanyprint)




#-------------To close the database-------------
dbase.close()
print('database closed')
