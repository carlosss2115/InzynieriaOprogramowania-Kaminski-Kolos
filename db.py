import os
import sqlite3
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "optomed.db")


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE uzytkownik (
            id_uzytkownika INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            haslo TEXT NOT NULL,
            rola TEXT NOT NULL CHECK (rola IN ('Pacjent', 'Optyk', 'Specjalista', 'Administrator'))
        );

        CREATE TABLE pacjent (
            id_pacjenta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_uzytkownika INTEGER UNIQUE,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            telefon TEXT NOT NULL,
            adres TEXT NOT NULL,
            FOREIGN KEY (id_uzytkownika) REFERENCES uzytkownik(id_uzytkownika) ON DELETE SET NULL
        );

        CREATE TABLE okulary (
            id_okularow INTEGER PRIMARY KEY AUTOINCREMENT,
            marka TEXT NOT NULL,
            model TEXT NOT NULL,
            kategoria TEXT NOT NULL,
            typ_szkiel TEXT NOT NULL,
            cena REAL NOT NULL CHECK (cena >= 0),
            stan_magazynowy INTEGER NOT NULL DEFAULT 0 CHECK (stan_magazynowy >= 0)
        );

        CREATE TABLE wizyta (
            id_wizyty INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pacjenta INTEGER NOT NULL,
            oddzial TEXT NOT NULL,
            specjalista TEXT NOT NULL,
            poczatek TEXT NOT NULL,
            koniec TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Zaplanowana' CHECK (status IN ('Zaplanowana', 'Zrealizowana', 'Anulowana')),
            FOREIGN KEY (id_pacjenta) REFERENCES pacjent(id_pacjenta) ON DELETE CASCADE
        );

        CREATE TABLE badanie_recepta (
            id_wpisu INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pacjenta INTEGER NOT NULL,
            specjalista TEXT NOT NULL,
            data_badania TEXT NOT NULL,
            opis_badania TEXT NOT NULL,
            sfera_op TEXT NOT NULL,
            cylinder_op TEXT NOT NULL,
            os_op TEXT NOT NULL,
            sfera_ol TEXT NOT NULL,
            cylinder_ol TEXT NOT NULL,
            os_ol TEXT NOT NULL,
            zalecenia TEXT NOT NULL,
            FOREIGN KEY (id_pacjenta) REFERENCES pacjent(id_pacjenta) ON DELETE CASCADE
        );
        """
    )

    # Konta dla wszystkich ról z roadmap-v1.md (Pacjent demo nr 1, Optyk, Specjalista, Administrator)
    users_seed = [
        ("jan.kowalski@email.com", generate_password_hash("tajnehaslo123"), "Pacjent"),
        ("optyk@optomed.pl", generate_password_hash("optyk123"), "Optyk"),
        ("specjalista@optomed.pl", generate_password_hash("specjalista123"), "Specjalista"),
        ("admin@optomed.pl", generate_password_hash("admin123"), "Administrator"),
    ]
    cursor.executemany(
        "INSERT INTO uzytkownik (login, haslo, rola) VALUES (?, ?, ?)",
        users_seed,
    )

    # Profil pacjenta demonstracyjnego nr 1 (id_uzytkownika = 1)
    cursor.execute(
        """
        INSERT INTO pacjent (id_uzytkownika, imie, nazwisko, telefon, adres)
        VALUES (?, ?, ?, ?, ?)
        """,
        (1, "Jan", "Kowalski", "123-456-789", "ul. Słoneczna 15/2, 10-001 Olsztyn"),
    )
    pacjent_id = cursor.lastrowid

    # Katalog oprawek okularowych i produktów optycznych (tabela Okulary)
    okulary_seed = [
        ("Ray-Ban", "Aviator RX6489", "Korekcyjne", "Korekcyjne jednoogniskowe", 450.00, 8),
        ("Persol", "PO3007V", "Korekcyjne", "Korekcyjne z powłoką antyrefleksyjną", 680.00, 3),
        ("Oakley", "Holbrook", "Przeciwsłoneczne", "Przeciwsłoneczne z polaryzacją", 520.00, 5),
        ("Acuvue", "Oasys 1-Day (30 szt.)", "Soczewki kontaktowe", "Soczewki jednodniowe hydrożelowe", 119.00, 14),
        ("OptoCare", "Zestaw mikrofibra + płyn", "Akcesoria", "Pielęgnacja soczewek", 35.00, 20),
    ]
    cursor.executemany(
        """
        INSERT INTO okulary (marka, model, kategoria, typ_szkiel, cena, stan_magazynowy)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        okulary_seed,
    )

    # Przykładowa zaplanowana wizyta u optometrysty
    cursor.execute(
        """
        INSERT INTO wizyta (id_pacjenta, oddzial, specjalista, poczatek, koniec, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            pacjent_id,
            "Olsztyn Centrum",
            "mgr J. Kowal (Optometrysta)",
            "2026-11-26 10:00",
            "2026-11-26 11:00",
            "Zaplanowana",
        ),
    )

    # Przykładowy wpis w kartotece pacjenta i recepta (F05)
    cursor.execute(
        """
        INSERT INTO badanie_recepta (
            id_pacjenta, specjalista, data_badania, opis_badania,
            sfera_op, cylinder_op, os_op, sfera_ol, cylinder_ol, os_ol, zalecenia
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            pacjent_id,
            "mgr J. Kowal (Optometrysta)",
            "2026-10-15",
            "Badanie ostrości wzroku oraz refrakcji komputerowej. Lekka krótkowzroczność.",
            "-1.25",
            "-0.50",
            "90",
            "-1.00",
            "0.00",
            "0",
            "Okulary do dali z powłoką antyrefleksyjną do pracy przy komputerze.",
        ),
    )

    conn.commit()
    conn.close()
