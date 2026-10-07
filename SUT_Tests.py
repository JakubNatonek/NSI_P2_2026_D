from SUT_Help_Functions import (
    niezawodnosc_logger,
    poprawny_numer
)
from zespol_D import (
    BankSystem,
    KontoNieIstnieje,
    KontoZablokowane,
    ProcesorNiedostepny,
    ZewnetrznyProcesor,
)

from datetime import date
import random

#=========================================================================================
#utworz_konto
#=========================================================================================

def test_01_bank_system_utworz_konto_correct_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 01: {e}")


def test_02_bank_system_utworz_konto_incorrect_numer():
    bank = BankSystem()
    numer_konta = "1234567891" # Niepoprawny numer konta
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 02: {e}")

def test_03_bank_system_utworz_konto_short_numer():
    bank = BankSystem()
    numer_konta = "123456789" # Niepoprawny numer konta
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 03: {e}")

def test_04_bank_system_utworz_konto_empty_wlasciciel():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="",
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 04: {e}")

def test_05_bank_system_utworz_konto_special_characters_wlasciciel():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan !@#$%^&*()",
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 05: {e}")

def test_06_bank_system_utworz_konto_very_long_wlasciciel():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="A" * 10000,
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 06: {e}")

def test_07_bank_system_utworz_konto_negative_saldo_poczatkowe():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=-1000
        )
    except Exception  as e:
        print(f"Test 07: {e}")

def test_08_bank_system_utworz_konto_duplicate_numer():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta, 
            wlasciciel="Anna Kowalski", 
            saldo_poczatkowe=1000
        )
    except Exception  as e:
        print(f"Test 08: {e}")

#=========================================================================================
#wplac
#=========================================================================================

def test_09_bank_system_wplac_correct_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=500
        )

    except Exception  as e:
        print(f"Test 09: {e}")

def test_10_bank_system_wplac_negative_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=-500
        )

    except Exception  as e:
        print(f"Test 10: {e}")

def test_11_bank_system_wplac_zero_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=0
        )

    except Exception  as e:
        print(f"Test 11: {e}")

def test_12_bank_system_wplac_large_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=10000000000000000000000000
        )

    except Exception  as e:
        print(f"Test 12: {e}")


def test_13_bank_system_wplac_text_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota="500"
        )

    except Exception  as e:
        print(f"Test 13: {e}")


def test_14_bank_system_wplac_incorrect_numer():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer="1234567890",
            kwota="500"
        )

    except Exception  as e:
        print(f"Test 14: {e}")

def test_15_bank_system_wplac_blocked_account():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.zablokuj_konto)(
            numer=numer_konta
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota="500"
        )

        niezawodnosc_logger()(bank.odblokuj_konto)(
            numer=numer_konta
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota="500"
        )

    except Exception  as e:
        print(f"Test 15: {e}")

#=========================================================================================
#wyplac
#=========================================================================================

def test_16_bank_system_wyplac_correct_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota=500
        )
    except Exception  as e:
        print(f"Test 16: {e}")

def test_17_bank_system_wyplac_negative_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota=-500
        )
    except Exception  as e:
        print(f"Test 17: {e}")

def test_18_bank_system_wyplac_zero_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota=0
        )
    except Exception  as e:
        print(f"Test 18: {e}")


def test_19_bank_system_wyplac_large_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=10000000000000000000000000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota=10000000000000000000000000
        )
    except Exception  as e:
        print(f"Test 19: {e}")

def test_20_bank_system_wyplac_text_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota="500"
        )
    except Exception  as e:
        print(f"Test 20: {e}")

def test_21_bank_system_wyplac_incorrect_numer():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer="1234567890",
            kwota="500"
        )
    except Exception  as e:
        print(f"Test 21: {e}")

def test_22_bank_system_wyplac_blocked_account():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.zablokuj_konto)(
            numer=numer_konta
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota="500"
        )

        niezawodnosc_logger()(bank.odblokuj_konto)(
            numer=numer_konta
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota="500"
        )

    except Exception  as e:
        print(f"Test 22: {e}")


def test_23_bank_system_wyplac_more_than_available():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wyplac)(
            numer=numer_konta,
            kwota=2000
        )
    except Exception  as e:
        print(f"Test 23: {e}")

#=========================================================================================
#przelew
#=========================================================================================

def test_24_bank_system_przelew_correct():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_1,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_2,
            wlasciciel="Anna Nowak",
            saldo_poczatkowe=500
        )

        niezawodnosc_logger()(bank.przelew)(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=200
        )
    except Exception  as e:
        print(f"Test 24: {e}")

def test_25_bank_system_przelew_negative_amount():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_1,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_2,
            wlasciciel="Anna Nowak",
            saldo_poczatkowe=500
        )

        niezawodnosc_logger()(bank.przelew)(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=-200
        )
    except Exception  as e:
        print(f"Test 25: {e}")

def test_26_bank_system_przelew_to_nonexistent_account():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_1,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.przelew)(
            numer_z=numer_1,
            numer_do="987654321",
            kwota=200
        )
    except Exception  as e:
        print(f"Test 26: {e}")

def test_27_bank_system_przelew_from_nonexistent_account():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_1,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.przelew)(
            numer_z="987654321",
            numer_do=numer_1,
            kwota=200
        )
    except Exception  as e:
        print(f"Test 27: {e}")

#=========================================================================================
#odsetki
#=========================================================================================

def test_28_bank_system_nalicz_odsetki_correct():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.nalicz_odsetki)(
            numer=numer_konta,
            roczna_stopa_procentowa=6,
            miesiace=12
        )
    except Exception  as e:
        print(f"Test 28: {e}")

def test_29_bank_system_nalicz_odsetki_negative_roczna_stopa_procentowa():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.nalicz_odsetki)(
            numer=numer_konta,
            roczna_stopa_procentowa=-6,
            miesiace=12
        )
    except Exception  as e:
        print(f"Test 29: {e}")

def test_30_bank_system_nalicz_odsetki_negative_miesiace():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.nalicz_odsetki)(
            numer=numer_konta,
            roczna_stopa_procentowa=6,
            miesiace=-12
        )
    except Exception  as e:
        print(f"Test 30: {e}")

def test_31_bank_system_nalicz_odsetki_nonexistent_account():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.nalicz_odsetki)(
            numer=numer_konta,
            roczna_stopa_procentowa=6,
            miesiace=12
        )
    except Exception  as e:
        print(f"Test 31: {e}")

def test_32_bank_system_nalicz_odsetki_blocked_account():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.zablokuj_konto)(
            numer=numer_konta
        )

        niezawodnosc_logger()(bank.nalicz_odsetki)(
            numer=numer_konta,
            roczna_stopa_procentowa=6,
            miesiace=12
        )
    except Exception  as e:
        print(f"Test 32: {e}")

#=========================================================================================
#historia
#=========================================================================================

def test_33_historia():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=500
        )

        niezawodnosc_logger()(bank.historia_w_okresie)(
            numer=numer_konta,
            od=date.today(),
            do=date.today()
        )
    except Exception  as e:
        print(f"Test 33: {e}")

def test_34_wyciag():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        niezawodnosc_logger()(bank.wplac)(
            numer=numer_konta,
            kwota=500
        )

        niezawodnosc_logger()(bank.wyciag_miesieczny)(
            numer=numer_konta,
            rok=date.today().year,
            miesiac=date.today().month
        )
    except Exception  as e:
        print(f"Test 34: {e}")

#=========================================================================================
#ZewnetrznyProcesor
#=========================================================================================

def test_35_przelew_zewnetrzny():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)
    try:
        niezawodnosc_logger()(bank.utworz_konto)(
            numer=numer_konta,
            wlasciciel="Jan Kowalski",
            saldo_poczatkowe=1000
        )

        procesor = ZewnetrznyProcesor(
            prawdopodobienstwo_awarii=0.0
        )

        niezawodnosc_logger()(bank.przelew_zewnetrzny)(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=100,
            procesor=procesor
        )
    except Exception  as e:
        print(f"Test 35: {e}")

if __name__ == "__main__":
    #utworz_konto
    test_01_bank_system_utworz_konto_correct_konto()
    test_02_bank_system_utworz_konto_incorrect_numer()
    test_03_bank_system_utworz_konto_short_numer()
    test_04_bank_system_utworz_konto_empty_wlasciciel()
    test_05_bank_system_utworz_konto_special_characters_wlasciciel()
    test_06_bank_system_utworz_konto_very_long_wlasciciel()
    test_07_bank_system_utworz_konto_negative_saldo_poczatkowe()
    test_08_bank_system_utworz_konto_duplicate_numer()
    #wplac
    test_09_bank_system_wplac_correct_wplata()
    test_10_bank_system_wplac_negative_wplata()
    test_11_bank_system_wplac_zero_wplata()
    test_12_bank_system_wplac_large_wplata()
    test_13_bank_system_wplac_text_wplata()
    test_14_bank_system_wplac_incorrect_numer()
    test_15_bank_system_wplac_blocked_account()
    #wyplac
    test_16_bank_system_wyplac_correct_wplata()
    test_17_bank_system_wyplac_negative_wplata()
    test_18_bank_system_wyplac_zero_wplata()
    test_19_bank_system_wyplac_large_wplata()
    test_20_bank_system_wyplac_text_wplata()
    test_21_bank_system_wyplac_incorrect_numer()
    test_22_bank_system_wyplac_blocked_account()
    test_23_bank_system_wyplac_more_than_available()
    #przelew
    test_24_bank_system_przelew_correct()
    test_25_bank_system_przelew_negative_amount()
    test_26_bank_system_przelew_to_nonexistent_account()
    test_27_bank_system_przelew_from_nonexistent_account()
    #odsetki
    test_28_bank_system_nalicz_odsetki_correct()
    test_29_bank_system_nalicz_odsetki_negative_roczna_stopa_procentowa()
    test_30_bank_system_nalicz_odsetki_negative_miesiace()
    test_31_bank_system_nalicz_odsetki_nonexistent_account()
    test_32_bank_system_nalicz_odsetki_blocked_account()
    #zewnętrzny procesor
    test_33_historia()
    test_34_wyciag()
    test_35_przelew_zewnetrzny()