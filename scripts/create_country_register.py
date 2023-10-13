import locale
from users.models import County
lst = ['Əfqanıstan', 'Albaniya', 'Əlcəzair', 'Anqola',
        'Antiqua və Barbuda', 'Argentina', 'Ermənistan', 'Avstraliya',
        'Avstriya', 'Azərbaycan', 'Baham adaları', 'Banqladeş', 'Barbados',
        'Belarus', 'Belçika', 'Beliz', 'Benin', 'Butan', 'Boliviya',
        "Bosniya və Herseqovina", "Botsvana", "Braziliya", "Bruney",
        'Bolqarıstan', 'Burkina Faso', 'Burundi', 'Kamboca', 'Kamerun',
        'Kanada', 'Kabo Verde', 'Mərkəzi Afrika Respublikası', 'Çad',
        'Çili', 'Çin', 'Kolumbiya', 'Komor', 'Kosta Rika', 'Xorvatiya',
        'Kipr', 'Çexiya', 'Danimarka', 'Cibuti', 'Ekvador', 'Misir',
        'El Salvador', 'Ekvatorial Qvineya', 'Estoniya', 'Efiopiya', 'Fici',
        'Finlandiya', 'Fransa', 'Qabon', 'Qambiya', 'Gürcüstan', 'Almaniya',
        'Qana', 'Yunanıstan', 'Qrenada', 'Qvineya', 'Qvineya-Bisau', 'Qayana',
        'Honduras', 'Çin, P.R.: Honq Konq', 'Macarıstan', 'İslandiya',
        'Hindistan', 'İndoneziya', 'İran', 'İraq', 'İrlandiya', 'İsrail', 'İtaliya',
        'Fildişi Sahili', 'Yamayka', 'Yaponiya', 'İordaniya', 'Qazaxıstan', 
'Keniya', 'Küveyt', 'Qırğızıstan', 'Laos', 'Latviya', 'Livan', 'Lesoto',
        'Liberiya', 'Liviya', 'Litva', 'Lüksemburq',
        'Çin, P.R.: Makao', 'Madaqaskar', 'Malavi', 'Malayziya',
        'Maldiv adaları', 'Mali', 'Malta', 'Mavritaniya', 'Meksika', 'Mikroneziya',
        'Moldova', 'Monqolustan', 'Monteneqro', 'Mərakeş', 'Mozambik',
        'Namibiya', 'Hollandiya', 'Yeni Zelandiya', 'Nikaraqua', 'Niger',
        'Nigeriya', 'Şimali Makedoniya', 'Norveç', 'Oman', 'Pakistan',
        "Palau", "Fələstin", "Panama", "Papua Yeni Qvineya", "Paraqvay",
        'Peru', 'Filippin', 'Polşa', 'Portuqaliya', 'Qətər', 'Rumıniya',
        "Rusiya", "Ruanda", "St. Lucia", 'St. Vinsent və Qrenadinlər',
        'Samoa', 'San Marino', 'Səudiyyə Ərəbistanı', 'Seneqal', 'Serbiya',
        'Seyşel adaları', 'Sierra Leone', 'Sinqapur', 'Slovakiya', 'Sloveniya',
        "Solomon adaları", "Cənubi Afrika", "Cənubi Koreya", "İspaniya",
        'Şri Lanka', 'Sudan', 'Surinam', 'Esvatini', 'İsveç',
        'İsveçrə', 'Suriya', 'Tacikistan', 'Tanzaniya', 'Tayland',
        'Toqo', 'Tonqa', 'Trinidad və Tobaqo', 'Tunis', 'Türkiyə',
        'Uqanda', 'Ukrayna', 'Birləşmiş Ərəb Əmirlikləri', 'Birləşmiş Krallıq',
        "Uruqvay", "Özbəkistan", "Vanuatu", "Venesuela", "Vyetnam",
        'Yəmən', 'Zambiya', 'Zimbabve', 'Aruba', 'Qvatemala', 'Kiribati',
        'Nepal', 'Sao Tome və Prinsipi', 'Birma (Myanma)', 'Haiti',
        'Konqo Respublikası', 'Andorra', 'Bəhreyn', 'Bermuda', 'Eritreya',
        'Farer adaları', 'Cəbəllütariq', 'Lixtenşteyn', 'Monako',
        'Yeni Kaledoniya', 'Puerto Riko', 'Amerika Birləşmiş Ştatları', 'Somali',
        'Türkmənistan', 'Tuvalu', 'Şimali Koreya', 'Dominikan Respublikası',
        'Tayvan', 'İnsan Adası', 'Kuba', 'Kayman Adaları', 'Mavrikiy',
        'Amerika Birləşmiş Ştatları Virgin Adaları', 'Qrenlandiya',
        'St. Martin (Fransız hissəsi)', 'Quam', 'Myanma', 'Kosovo',
        'Fransız Polinezyası', 'Timor-Leste', 'Konqo Dem. Rep.',
        'Cənubi Sudan', 'St. Kitts və Nevis', 'Dominika',
        'Marşal Adaları', 'Sint Maarten (Hollandiya hissəsi)', 'Kurasao',
        'Amerika Samoası', 'Şimali Mariana Adaları',
        'Britaniya Virgin Adaları', 'Turks və Kaykos Adaları', 'Nauru',
        'Montserrat', 'Norfolk Island', 'Anguilla',
        'Müqəddəs Taxt (Vatikan)', 'Kanal Adaları']
def azerbaijani_locale_sort(country_names):
    # Set the locale to Azerbaijani (az_AZ)
    locale.setlocale(locale.LC_COLLATE, 'az_AZ.UTF-8')
    # Sort the country names using the Azerbaijani locale
    sorted_country_names = sorted(country_names, key=locale.strxfrm)
    return sorted_country_names


def run():
    print("HELLO")
    country_names = lst
    sorted_country_names = azerbaijani_locale_sort(country_names)

    for country in sorted_country_names:

        County.objects.create(name=country)
    
    

    

