from decimal import InvalidOperation, Decimal
from datetime import date
import pytest
import time

from SUT_Help_Functions import (
    poprawny_numer
)

from zespol_D import (
    BankSystem,
    KontoNieIstnieje,
    KontoZablokowane,
    ProcesorNiedostepny,
    ZewnetrznyProcesor,
)

def test_is_working():
    assert True

#=========================================================================================
#utworz_konto
#=========================================================================================

def test_utworz_konto_poprawne():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    assert konto.numer == numer_konta
    assert konto.wlasciciel == "Jan Kowalski"
    assert konto.saldo == Decimal("1000")
    assert konto.status == "aktywne"
    assert bank.konta[numer_konta] is konto

def test_utworz_konto_niepoprawny_numer():
    bank = BankSystem()
    numer_konta = "12345678"

    with pytest.raises(ValueError):
        bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )

def test_utworz_konto_istniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto1 = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        konto2 = bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="Anna Nowak", 
            saldo_poczatkowe=500
        )

def test_utworz_konto_za_krotki_numer():
    bank = BankSystem()
    numer_konta = "12345678"

    with pytest.raises(ValueError):
        bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )

def test_utworz_konto_pusty_numer():
    bank = BankSystem()
    numer_konta = ""

    with pytest.raises(ValueError):
        bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=1000
        )

def test_utworz_konto_ujemne_saldo(): # saldo poczatkowe nie powino byc ujemne jednak jest mozliwe utworzenie
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(ValueError):
        bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="Jan Kowalski", 
            saldo_poczatkowe=-100
        )   

def test_utworz_konto_pusty_wlasciciel():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(ValueError):
        bank.utworz_konto(
            numer=numer_konta, 
            wlasciciel="", 
            saldo_poczatkowe=1000
        )

def test_utworz_konto_domyslne_saldo():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski"
    )

    assert konto.saldo == Decimal("0")


#=========================================================================================
#wyplac
#=========================================================================================

def test_wyplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    bank.wyplac(
        numer=numer_konta,
        kwota=100
    )

    assert konto.saldo == 900

def test_wyplata_zablokowane_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)

    with pytest.raises(KontoZablokowane):
        bank.wyplac(
            numer=numer_konta,
            kwota=100
        )

def test_wyplata_nieistniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(KontoNieIstnieje):
        bank.wyplac(
            numer=numer_konta,
            kwota=100
        )

def test_wyplata_niepoprawny_numer():
    bank = BankSystem()
    numer_konta = "12345678"

    with pytest.raises(KontoNieIstnieje):
        bank.wyplac(
            numer=numer_konta,
            kwota=100
        )

def test_wyplata_ujemna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=-100
        )

def test_wyplata_zero():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=0
        )

def test_wyplata_niepoprawny_typ_kwoty_blendna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(InvalidOperation):
        bank.wyplac(
            numer=numer_konta,
            kwota="10O"
        )

def test_wyplata_niepoprawny_typ_kwoty(): # wyplata pozwala na konwersje s str, ale wplac nie
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(TypeError):
        bank.wyplac(
            numer=numer_konta,
            kwota="100"
        )


def test_wyplata_niewystarczajace_srodki():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=2000
        )

    assert konto.saldo == Decimal("1000")

def test_wyplata_calego_salda():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    wynik = bank.wyplac(
        numer=numer_konta,
        kwota=1000
    )

    assert wynik == Decimal("0")
    assert konto.saldo == Decimal("0")

def test_wyplata_przekroczenie_limitu_dziennego():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=10000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=5001
        )

def test_wyplata_przekroczenie_limitu_dziennego_wielokrotne_wyplaty():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=10000
    )

    bank.wyplac(
        numer=numer_konta,
        kwota=3000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=2500
        )

#=========================================================================================
#wplac
#=========================================================================================

def test_wplata():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    bank.wplac(
        numer=numer_konta,
        kwota=100
    )

    assert konto.saldo == 1100

def test_wplata_zablokowane_konto(): # Można wypłacić z zablokowaneego konta
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)

    with pytest.raises(KontoZablokowane):
        bank.wplac(
            numer=numer_konta,
            kwota=100
        )
def test_wplata_nieistniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(KontoNieIstnieje):
        bank.wplac(
            numer=numer_konta,
            kwota=100
        )

def test_wplata_niepoprawny_numer():
    bank = BankSystem()
    numer_konta = "12345678"

    with pytest.raises(KontoNieIstnieje):
        bank.wplac(
            numer=numer_konta,
            kwota=100
        )

def test_wplata_ujemna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wplac(
            numer=numer_konta,
            kwota=-100
        )

def test_wplata_niepoprawny_typ_kwoty():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(TypeError): 
        bank.wplac(
            numer=numer_konta,
            kwota="100"
        )

def test_wplata_niepoprawny_typ_kwoty_blendna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(TypeError): # TypeError a nie InvalidOperation
        bank.wplac(
            numer=numer_konta,
            kwota="10O"
        )

def test_wplata_zero():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wplac(
            numer=numer_konta,
            kwota=0
        )
#=========================================================================================
#dodaj_wpis
#=========================================================================================

def test_dodaj_wpis_poprawny():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski"
    )

    data_operacji = date.today()
    kwota = Decimal("200")

    konto.dodaj_wpis(
        typ="wplata",
        kwota=kwota,
        data_operacji=data_operacji
    )

    assert len(konto.historia) == 1
    assert konto.historia[0] == (
        data_operacji,
        "wplata",
        Decimal("200")
    )

def test_dodaj_wpis_domyslna_data_operacji():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski"
    )

    kwota = Decimal("200")

    konto.dodaj_wpis(
        typ="wplata",
        kwota=kwota
    )

    assert len(konto.historia) == 1
    assert konto.historia[0][0] == date.today()
    assert konto.historia[0][1] == "wplata"
    assert konto.historia[0][2] == Decimal("200")


# =========================================================
# blokowanie i odblokowywanie konta
# =========================================================

def test_zablokuj_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)

    assert konto.status == "zablokowane"


def test_odblokuj_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)
    bank.odblokuj_konto(numer_konta)

    assert konto.status == "aktywne"


def test_zablokuj_nieistniejace_konto():
    bank = BankSystem()

    with pytest.raises(KontoNieIstnieje):
        bank.zablokuj_konto("1234567895")


def test_odblokuj_nieistniejace_konto():
    bank = BankSystem()

    with pytest.raises(KontoNieIstnieje):
        bank.odblokuj_konto("1234567895")

# =========================================================
# przelew
# =========================================================

def test_przelew_poprawny():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    bank.przelew(
        numer_z=numer_1,
        numer_do=numer_2,
        kwota=200
    )

    assert konto_z.saldo == Decimal("800")
    assert konto_do.saldo == Decimal("700")

def test_przelew_nieistniejace_konto_z():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(KontoNieIstnieje):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=200
        )

def test_przelew_nieistniejace_konto_do():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(KontoNieIstnieje):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=200
        )

def test_przelew_ujemna_kwota():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(ValueError):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=-100
        )

def test_przelew_zero_kwota():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(ValueError):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=0
        )

def test_przelew_globalny_limit_dziennego_przekroczony():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=10000000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(ValueError):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=1000000
        )

def test_przelew_niewystarczajace_srodki():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(ValueError):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=2000
        )

def test_przelew_zablokowane_konto_z():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    bank.zablokuj_konto(numer_1)

    with pytest.raises(KontoZablokowane):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=100
        )

def test_przelew_zablokowane_konto_do():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    bank.zablokuj_konto(numer_2)

    with pytest.raises(KontoZablokowane):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota=100
        )

def test_przelew_niepoprawny_typ_kwoty():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(TypeError):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota="100"
        )

def test_przelew_niepoprawny_typ_kwoty_blendna_kwota():
    bank = BankSystem()
    numer_1 = poprawny_numer(123456789)
    numer_2 = poprawny_numer(987654321)

    konto_z = bank.utworz_konto(
        numer=numer_1,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto_do = bank.utworz_konto(
        numer=numer_2,
        wlasciciel="Anna Nowak",
        saldo_poczatkowe=500
    )

    with pytest.raises(InvalidOperation):
        bank.przelew(
            numer_z=numer_1,
            numer_do=numer_2,
            kwota="10O"
        )

# =========================================================
# naliczanie odsetek
# =========================================================

def test_nalicz_odsetki_poprawne():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    wynik = bank.nalicz_odsetki(
        numer=numer_konta,
        roczna_stopa_procentowa=12,
        miesiace=1
    )

    assert wynik == Decimal("1010.00")
    assert konto.saldo == Decimal("1010.00")

def test_nalicz_odsetki_zero_miesiecy():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    wynik = bank.nalicz_odsetki(
        numer=numer_konta,
        roczna_stopa_procentowa=12,
        miesiace=0
    )

    assert wynik == Decimal("1000")
    assert konto.saldo == Decimal("1000")


def test_nalicz_odsetki_zero_stopa_procentowa():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    wynik = bank.nalicz_odsetki(
        numer=numer_konta,
        roczna_stopa_procentowa=0,
        miesiace=12
    )

    assert wynik == Decimal("1000")
    assert konto.saldo == Decimal("1000")

def test_nalicz_odsetki_nieistniejace_konto():
    bank = BankSystem()

    with pytest.raises(KontoNieIstnieje):
        bank.nalicz_odsetki(
            numer=poprawny_numer(123456789),
            roczna_stopa_procentowa=6,
            miesiace=12
        )

def test_nalicz_odsetki_zablokowane_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)

    with pytest.raises(KontoZablokowane):
        bank.nalicz_odsetki(
            numer=numer_konta,
            roczna_stopa_procentowa=6,
            miesiace=12
        )

def test_nalicz_odsetki_ujemna_stopa_procentowa():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.nalicz_odsetki(
            numer=numer_konta,
            roczna_stopa_procentowa=-5,
            miesiace=12
        )

def test_nalicz_odsetki_ujemna_liczba_miesiecy():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.nalicz_odsetki(
            numer=numer_konta,
            roczna_stopa_procentowa=5,
            miesiace=-12
        )

def test_nalicz_odsetki_niepoprawny_typ_stopy_procentowej():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(TypeError):
        bank.nalicz_odsetki(
            numer=numer_konta,
            roczna_stopa_procentowa="5",
            miesiace=12
        )

def test_nalicz_odsetki_niepoprawny_typ_miesiecy():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    with pytest.raises(TypeError):
        bank.nalicz_odsetki(
            numer=numer_konta,
            roczna_stopa_procentowa=5,
            miesiace="12"
        )

# =========================================================
# historia i wyciąg
# =========================================================

def test_historia_w_okresie():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.wplac(numer_konta, 200)
    bank.wyplac(numer_konta, 100)

    historia = bank.historia_w_okresie(
        numer=numer_konta,
        od=date.today(),
        do=date.today()
    )

    assert len(historia) == 2
    assert historia[0][1] == "wplata"
    assert historia[1][1] == "wyplata"

def test_historia_w_okresie_nieistniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(KontoNieIstnieje):
        bank.historia_w_okresie(
            numer=numer_konta,
            od=date.today(),
            do=date.today()
        )

def test_historia_w_okresie_brak_operacji():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    historia = bank.historia_w_okresie(
        numer=numer_konta,
        od=date.today(),
        do=date.today()
    )

    assert len(historia) == 0

def test_wyciag_miesieczny():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.wplac(numer_konta, 200)
    bank.wyplac(numer_konta, 100)

    wyciag = bank.wyciag_miesieczny(
        numer=numer_konta,
        rok=date.today().year,
        miesiac=date.today().month
    )

    assert wyciag["wplaty"] == Decimal("200")
    assert wyciag["wyplaty"] == Decimal("100")
    assert wyciag["saldo_koncowe"] == Decimal("1100")

def test_wyciag_miesieczny_nieistniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    with pytest.raises(KontoNieIstnieje):
        bank.wyciag_miesieczny(
            numer=numer_konta,
            rok=date.today().year,
            miesiac=date.today().month
        )

def test_wyciag_miesieczny_brak_operacji():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    wyciag = bank.wyciag_miesieczny(
        numer=numer_konta,
        rok=date.today().year,
        miesiac=date.today().month
    )

    assert wyciag["wplaty"] == Decimal("0")
    assert wyciag["wyplaty"] == Decimal("0")
    assert wyciag["saldo_koncowe"] == Decimal("1000")

def test_wyciag_miesieczny_sumuje_wyplaty_i_przelewy():
    bank = BankSystem()
    numer = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=5000
    )

    konto.dodaj_wpis(
        "wyplata", Decimal("200"), date(2025, 5, 5)
    )
    konto.dodaj_wpis(
        "przelew_wychodzacy", Decimal("300"), date(2025, 5, 10)
    )
    konto.dodaj_wpis(
        "wplata", Decimal("100"), date(2025, 5, 15)
    )

    wynik = bank.wyciag_miesieczny(numer, 2025, 5)

    assert wynik["wyplaty"] == Decimal("500")
    assert wynik["wplaty"] == Decimal("100")
    assert wynik["saldo_koncowe"] == Decimal("5000")

def test_wyciag_miesieczny_filtruje_miesiac_i_rok():
    bank = BankSystem()
    numer = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    konto.dodaj_wpis(
        "wplata", Decimal("200"), date(2025, 5, 10)
    )
    konto.dodaj_wpis(
        "wplata", Decimal("300"), date(2025, 6, 10)
    )
    konto.dodaj_wpis(
        "wplata", Decimal("400"), date(2024, 5, 10)
    )

    wynik = bank.wyciag_miesieczny(numer, 2025, 5)

    assert wynik["wplaty"] == Decimal("200")
    assert wynik["wyplaty"] == Decimal("0")
    assert wynik["saldo_koncowe"] == Decimal("1000")

def test_historia_w_okresie_zakres_dat():
    bank = BankSystem()
    numer = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    data_przed = date(2025, 1, 1)
    data_w_zakresie = date(2025, 1, 15)
    data_po = date(2025, 2, 1)

    konto.dodaj_wpis("wplata", Decimal("100"), data_przed)
    konto.dodaj_wpis("wplata", Decimal("200"), data_w_zakresie)
    konto.dodaj_wpis("wyplata", Decimal("50"), data_po)

    wynik = bank.historia_w_okresie(
        numer,
        date(2025, 1, 10),
        date(2025, 1, 20)
    )

    assert len(wynik) == 1
    assert wynik[0] == (
        data_w_zakresie,
        "wplata",
        Decimal("200")
    )

# =========================================================
# przelew zewnętrzny
# =========================================================

def test_przelew_zewnetrzny_poprawny():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    wynik = bank.przelew_zewnetrzny(
        numer_z=numer_konta,
        numer_konta_docelowego_zewn="1111111111",
        kwota=100,
        procesor=procesor
    )

    assert wynik["status"] == "zaksiegowano"
    assert konto.saldo == Decimal("900")
    assert procesor.licznik_wywolan == 1

def test_przelew_zewnetrzny_awaria_procesora():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=1.0
    )

    with pytest.raises(ProcesorNiedostepny):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=100,
            procesor=procesor
        )

    assert konto.saldo == Decimal("1000")

def test_przelew_zewnetrzny_nieistniejace_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(KontoNieIstnieje):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=100,
            procesor=procesor
        )
def test_przelew_zewnetrzny_zablokowane_konto():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    bank.zablokuj_konto(numer_konta)

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(KontoZablokowane):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=100,
            procesor=procesor
        )

def test_przelew_zewnetrzny_ujemna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(ValueError):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=-100,
            procesor=procesor
        )

def test_przelew_zewnetrzny_zero_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(ValueError):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=0,
            procesor=procesor
        )

def test_przelew_zewnetrzny_niepoprawny_typ_kwoty():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(TypeError):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota="100",
            procesor=procesor
        )

def test_przelew_zewnetrzny_niepoprawny_typ_kwoty_blendna_kwota():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(InvalidOperation):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota="10O",
            procesor=procesor
        )

def test_przelew_zewnetrzny_opoznienie():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0,
        opoznienie_s=2
    )

    start_time = time.time()
    wynik = bank.przelew_zewnetrzny(
        numer_z=numer_konta,
        numer_konta_docelowego_zewn="1111111111",
        kwota=100,
        procesor=procesor
    )
    end_time = time.time()

    assert wynik["status"] == "zaksiegowano"
    assert konto.saldo == Decimal("900")
    assert procesor.licznik_wywolan == 1
    assert end_time - start_time >= 2

def test_przelew_zewnetrzny_niewystarczajace_srodki():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta,
        wlasciciel="Jan Kowalski",
        saldo_poczatkowe=100
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    with pytest.raises(ValueError):
        bank.przelew_zewnetrzny(
            numer_z=numer_konta,
            numer_konta_docelowego_zewn="1111111111",
            kwota=200,
            procesor=procesor
        )

# =========================================================
# Dodane testy dla mutantów
# =========================================================

def test_wplata_kwoty_jeden_i_wartosc_zwracana():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    wynik = bank.wplac(
        numer=numer_konta,
        kwota=1
    )

    assert konto.saldo == 1001
    assert wynik == Decimal("1001")

def test_wyplata_kwoty_jeden_i_wartosc_zwracana():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    wynik = bank.wyplac(
        numer=numer_konta,
        kwota=1
    )

    assert konto.saldo == 999
    assert wynik == Decimal("999")

def test_wyplata_calego_salda_jest_odrzucana():

    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    with pytest.raises(ValueError):
        bank.wyplac(
            numer=numer_konta,
            kwota=1000
        )
    
    assert konto.saldo == Decimal("1000")
    assert konto.historia == []

def test_wyplata_dokladnie_do_limitu_dziennego():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=10000
    )

    wynik = bank.wyplac(
        numer=numer_konta,
        kwota=5000
    )

    assert konto.saldo == Decimal("5000")
    assert wynik == Decimal("5000")

def test_suma_dzisiejszych_wyplat_pomija_stare_operacje():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=10000
    )

    dzis = date.today()
    wczoraj = date.fromordinal(dzis.toordinal() - 1)

    konto.dodaj_wpis("wyplata", Decimal("3000"), wczoraj)
    konto.dodaj_wpis("wplata", Decimal("200"), dzis)

    assert bank._suma_dzisiejszych_wyplat(konto) == Decimal("0")


def test_przelew_zewnetrzny_na_cale_saldo():
    bank = BankSystem()
    numer_konta = poprawny_numer(123456789)

    konto = bank.utworz_konto(
        numer=numer_konta, 
        wlasciciel="Jan Kowalski", 
        saldo_poczatkowe=1000
    )

    procesor = ZewnetrznyProcesor(
        prawdopodobienstwo_awarii=0.0
    )

    wynik = bank.przelew_zewnetrzny(
        numer_z=numer_konta,
        numer_konta_docelowego_zewn="1111111111",
        kwota=1000,
        procesor=procesor
    )
    
    assert wynik["status"] == "zaksiegowano"
    assert konto.saldo == Decimal("0")
    assert konto.historia[-1][1:] == (
        "przelew_zewnetrzny", Decimal("1000")
    )
