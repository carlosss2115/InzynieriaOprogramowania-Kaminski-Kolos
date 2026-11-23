import os
import sqlite3
from datetime import datetime
import click
from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import DATABASE_PATH, get_db, init_db

app = Flask(__name__)
app.secret_key = "optomed-v1-lokalny-klucz-sesji"

KATEGORIE = ["Korekcyjne", "Przeciwsłoneczne", "Soczewki kontaktowe", "Akcesoria"]
ODDZIALY = ["Olsztyn Centrum", "Olsztyn Zatorze"]
SPECJALISCI = [
    "mgr J. Kowal (Optometrysta)",
    "mgr M. Zielińska (Optometrysta)",
]


@app.cli.command("init-db")
def init_db_command():
    """Inicjalizuje lokalną bazę SQLite danymi demonstracyjnymi OptoMed v1."""
    init_db()
    click.echo(f"Zainicjalizowano bazę danych OptoMed w pliku: {DATABASE_PATH}")


@app.before_request
def load_logged_in_user():
    if not os.path.exists(DATABASE_PATH):
        init_db()

    g.user = None
    g.pacjent = None
    user_id = session.get("user_id")
    if user_id is not None:
        conn = get_db()
        g.user = conn.execute(
            "SELECT id_uzytkownika, login, rola FROM uzytkownik WHERE id_uzytkownika = ?",
            (user_id,),
        ).fetchone()
        if g.user and g.user["rola"] == "Pacjent":
            g.pacjent = conn.execute(
                "SELECT * FROM pacjent WHERE id_uzytkownika = ?",
                (user_id,),
            ).fetchone()
        conn.close()


@app.context_processor
def inject_globals():
    return {"current_user": g.user, "current_pacjent": g.pacjent}


# W01 + F02: Strona Główna i Katalog Produktów
@app.route("/")
def index():
    wybrana_kategoria = request.args.get("kategoria", "").strip()
    fraza = request.args.get("q", "").strip()

    conn = get_db()
    query = "SELECT * FROM okulary WHERE 1=1"
    params = []

    if wybrana_kategoria and wybrana_kategoria in KATEGORIE:
        query += " AND kategoria = ?"
        params.append(wybrana_kategoria)

    if fraza:
        query += " AND (LOWER(marka) LIKE LOWER(?) OR LOWER(model) LIKE LOWER(?) OR LOWER(typ_szkiel) LIKE LOWER(?))"
        like_param = f"%{fraza}%"
        params.extend([like_param, like_param, like_param])

    query += " ORDER BY id_okularow ASC"
    okulary = conn.execute(query, params).fetchall()
    conn.close()

    return render_template(
        "index.html",
        okulary=okulary,
        kategorie=KATEGORIE,
        wybrana_kategoria=wybrana_kategoria,
        fraza=fraza,
    )


# W02 + F01: Formularz Logowania i Rejestracji
@app.route("/logowanie", methods=["GET", "POST"])
def logowanie():
    if request.method == "POST":
        tryb = request.form.get("tryb", "login")

        if tryb == "login":
            email = request.form.get("email", "").strip()
            haslo = request.form.get("haslo", "")

            if not email or not haslo:
                flash("Wprowadź adres e-mail oraz hasło.", "error")
                return render_template("login.html")

            conn = get_db()
            user = conn.execute(
                "SELECT * FROM uzytkownik WHERE login = ?",
                (email,),
            ).fetchone()
            conn.close()

            if user is None or not check_password_hash(user["haslo"], haslo):
                flash("Nieprawidłowy login lub hasło.", "error")
                return render_template("login.html")

            session["user_id"] = user["id_uzytkownika"]
            flash(f"Zalogowano pomyślnie jako {user['login']} (Rola: {user['rola']}).", "success")

            if user["rola"] == "Optyk":
                return redirect(url_for("panel_optyka"))
            if user["rola"] == "Specjalista":
                return redirect(url_for("panel_specjalisty"))
            return redirect(url_for("wizyty"))

        elif tryb == "register":
            imie = request.form.get("imie", "").strip()
            nazwisko = request.form.get("nazwisko", "").strip()
            email = request.form.get("reg_email", "").strip()
            telefon = request.form.get("telefon", "").strip()
            adres = request.form.get("adres", "").strip()
            haslo = request.form.get("reg_haslo", "")

            if not all([imie, nazwisko, email, telefon, adres, haslo]):
                flash("Wypełnij wszystkie pola formularza rejestracji.", "error")
                return render_template("login.html")

            conn = get_db()
            try:
                cur = conn.execute(
                    "INSERT INTO uzytkownik (login, haslo, rola) VALUES (?, ?, 'Pacjent')",
                    (email, generate_password_hash(haslo)),
                )
                user_id = cur.lastrowid
                conn.execute(
                    """
                    INSERT INTO pacjent (id_uzytkownika, imie, nazwisko, telefon, adres)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, imie, nazwisko, telefon, adres),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                flash("Konto o podanym adresie e-mail już istnieje.", "error")
                return render_template("login.html")

            conn.close()
            session["user_id"] = user_id
            flash("Konto pacjenta zostało utworzone. Zalogowano automatycznie.", "success")
            return redirect(url_for("wizyty"))

    return render_template("login.html")


@app.route("/demo/<rola>")
def demo_login(rola):
    login_map = {
        "pacjent": "jan.kowalski@email.com",
        "optyk": "optyk@optomed.pl",
        "specjalista": "specjalista@optomed.pl",
        "admin": "admin@optomed.pl",
    }
    target_login = login_map.get(rola)
    if not target_login:
        flash("Nieznany profil demonstracyjny.", "error")
        return redirect(url_for("index"))

    conn = get_db()
    user = conn.execute(
        "SELECT id_uzytkownika, login, rola FROM uzytkownik WHERE login = ?",
        (target_login,),
    ).fetchone()
    conn.close()

    if user:
        session["user_id"] = user["id_uzytkownika"]
        flash(f"Aktywowano profil demo: {user['login']} (Rola: {user['rola']}).", "success")
        if user["rola"] == "Optyk":
            return redirect(url_for("panel_optyka"))
        if user["rola"] == "Specjalista":
            return redirect(url_for("panel_specjalisty"))
    return redirect(url_for("wizyty"))


@app.route("/wyloguj")
def wyloguj():
    session.clear()
    flash("Wylogowano z systemu OptoMed.", "success")
    return redirect(url_for("index"))


# W03 + F03: Kalendarz i Rezerwacja Wizyty u Optometrysty
@app.route("/wizyty", methods=["GET", "POST"])
def wizyty():
    conn = get_db()

    if request.method == "POST":
        if not g.user or g.user["rola"] != "Pacjent" or not g.pacjent:
            conn.close()
            flash("Zaloguj się jako Pacjent (np. Demo Pacjent #1), aby zarezerwować wizytę.", "error")
            return redirect(url_for("logowanie"))

        oddzial = request.form.get("oddzial", "").strip()
        specjalista = request.form.get("specjalista", "").strip()
        poczatek_raw = request.form.get("poczatek", "").strip()
        koniec_raw = request.form.get("koniec", "").strip()

        if not oddzial or not specjalista or not poczatek_raw or not koniec_raw:
            conn.close()
            flash("Wszystkie pola formularza rezerwacji są wymagane.", "error")
            return redirect(url_for("wizyty"))

        try:
            dt_poczatek = datetime.fromisoformat(poczatek_raw)
            dt_koniec = datetime.fromisoformat(koniec_raw)
        except ValueError:
            conn.close()
            flash("Nieprawidłowy format daty lub godziny.", "error")
            return redirect(url_for("wizyty"))

        if dt_poczatek >= dt_koniec:
            conn.close()
            flash("Godzina rozpoczęcia musi być wcześniejsza niż godzina zakończenia.", "error")
            return redirect(url_for("wizyty"))

        poczatek_str = dt_poczatek.strftime("%Y-%m-%d %H:%M")
        koniec_str = dt_koniec.strftime("%Y-%m-%d %H:%M")

        # Reguła kolizji terminów: nowy_poczatek < istniejacy_koniec AND nowy_koniec > istniejacy_poczatek
        kolizja = conn.execute(
            """
            SELECT id_wizyty FROM wizyta
            WHERE oddzial = ?
              AND specjalista = ?
              AND status = 'Zaplanowana'
              AND ? < koniec
              AND ? > poczatek
            """,
            (oddzial, specjalista, poczatek_str, koniec_str),
        ).fetchone()

        if kolizja:
            conn.close()
            # Dokładny komunikat błędu z W03 w roadmap-v1.md
            flash("Wybrany termin jest zajęty. Wybierz inną godzinę.", "error")
            return redirect(url_for("wizyty"))

        conn.execute(
            """
            INSERT INTO wizyta (id_pacjenta, oddzial, specjalista, poczatek, koniec, status)
            VALUES (?, ?, ?, ?, ?, 'Zaplanowana')
            """,
            (g.pacjent["id_pacjenta"], oddzial, specjalista, poczatek_str, koniec_str),
        )
        conn.commit()
        conn.close()
        # Dokładny komunikat sukcesu z W03 w roadmap-v1.md
        flash("Wizyta została pomyślnie zarezerwowana.", "success")
        return redirect(url_for("wizyty"))

    wszystkie_wizyty = conn.execute(
        """
        SELECT w.*, p.imie, p.nazwisko
        FROM wizyta w
        JOIN pacjent p ON w.id_pacjenta = p.id_pacjenta
        ORDER BY w.poczatek ASC
        """
    ).fetchall()

    moje_recepty = []
    if g.pacjent:
        moje_recepty = conn.execute(
            """
            SELECT * FROM badanie_recepta
            WHERE id_pacjenta = ?
            ORDER BY data_badania DESC, id_wpisu DESC
            """,
            (g.pacjent["id_pacjenta"],),
        ).fetchall()

    conn.close()

    return render_template(
        "wizyty.html",
        wizyty=wszystkie_wizyty,
        moje_recepty=moje_recepty,
        oddzialy=ODDZIALY,
        specjalisci=SPECJALISCI,
    )


@app.route("/wizyty/<int:id_wizyty>/anuluj", methods=["POST"])
def anuluj_wizyte(id_wizyty):
    if not g.user or g.user["rola"] != "Pacjent" or not g.pacjent:
        flash("Zaloguj się jako Pacjent, aby odwołać wizytę.", "error")
        return redirect(url_for("logowanie"))

    conn = get_db()
    wizyta = conn.execute(
        "SELECT * FROM wizyta WHERE id_wizyty = ? AND id_pacjenta = ?",
        (id_wizyty, g.pacjent["id_pacjenta"]),
    ).fetchone()

    if not wizyta:
        conn.close()
        flash("Nie znaleziono wskazanej wizyty przypisanej do Twojego konta.", "error")
        return redirect(url_for("wizyty"))

    if wizyta["status"] == "Anulowana":
        conn.close()
        flash("Ta wizyta została już wcześniej odwołana.", "error")
        return redirect(url_for("wizyty"))

    conn.execute(
        "UPDATE wizyta SET status = 'Anulowana' WHERE id_wizyty = ?",
        (id_wizyty,),
    )
    conn.commit()
    conn.close()
    flash("Wizyta została odwołana, a termin ponownie zwolniony.", "success")
    return redirect(url_for("wizyty"))


# F04: Panel Optyka – zarządzanie bazą produktową i stanami magazynowymi
@app.route("/optyk", methods=["GET", "POST"])
def panel_optyka():
    if not g.user or g.user["rola"] not in ("Optyk", "Administrator"):
        flash("Dostęp wymaga zalogowania na konto Optyka lub Administratora.", "error")
        return redirect(url_for("logowanie"))

    conn = get_db()

    if request.method == "POST":
        akcja = request.form.get("akcja")

        if akcja == "dodaj_produkt":
            marka = request.form.get("marka", "").strip()
            model = request.form.get("model", "").strip()
            kategoria = request.form.get("kategoria", "").strip()
            typ_szkiel = request.form.get("typ_szkiel", "").strip()
            cena = request.form.get("cena", type=float)
            stan = request.form.get("stan_magazynowy", type=int)

            if not all([marka, model, typ_szkiel]) or kategoria not in KATEGORIE or cena is None or cena < 0 or stan is None or stan < 0:
                conn.close()
                flash("Uzupełnij poprawnie wszystkie dane nowego produktu.", "error")
                return redirect(url_for("panel_optyka"))

            conn.execute(
                """
                INSERT INTO okulary (marka, model, kategoria, typ_szkiel, cena, stan_magazynowy)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (marka, model, kategoria, typ_szkiel, round(cena, 2), stan),
            )
            conn.commit()
            flash(f"Dodano nowy produkt do katalogu: {marka} {model}.", "success")

        elif akcja == "aktualizuj_stan":
            id_okularow = request.form.get("id_okularow", type=int)
            nowy_stan = request.form.get("stan_magazynowy", type=int)

            if id_okularow is None or nowy_stan is None or nowy_stan < 0:
                conn.close()
                flash("Stan magazynowy musi być liczbą całkowitą nieujemną.", "error")
                return redirect(url_for("panel_optyka"))

            conn.execute(
                "UPDATE okulary SET stan_magazynowy = ? WHERE id_okularow = ?",
                (nowy_stan, id_okularow),
            )
            conn.commit()
            flash("Zaktualizowano stan magazynowy produktu.", "success")

        conn.close()
        return redirect(url_for("panel_optyka"))

    okulary = conn.execute("SELECT * FROM okulary ORDER BY id_okularow ASC").fetchall()
    conn.close()
    return render_template("optyk.html", okulary=okulary, kategorie=KATEGORIE)


# F05: Panel Specjalisty (Optometrysty) – kartoteka pacjentów, historia badań i recepty
@app.route("/specjalista", methods=["GET", "POST"])
def panel_specjalisty():
    if not g.user or g.user["rola"] not in ("Specjalista", "Administrator"):
        flash("Dostęp wymaga zalogowania na konto Specjalisty lub Administratora.", "error")
        return redirect(url_for("logowanie"))

    conn = get_db()

    if request.method == "POST":
        id_pacjenta = request.form.get("id_pacjenta", type=int)
        data_badania = request.form.get("data_badania", "").strip()
        opis_badania = request.form.get("opis_badania", "").strip()
        sfera_op = request.form.get("sfera_op", "").strip()
        cylinder_op = request.form.get("cylinder_op", "").strip()
        os_op = request.form.get("os_op", "").strip()
        sfera_ol = request.form.get("sfera_ol", "").strip()
        cylinder_ol = request.form.get("cylinder_ol", "").strip()
        os_ol = request.form.get("os_ol", "").strip()
        zalecenia = request.form.get("zalecenia", "").strip()

        if not id_pacjenta or not all([data_badania, opis_badania, sfera_op, cylinder_op, os_op, sfera_ol, cylinder_ol, os_ol, zalecenia]):
            conn.close()
            flash("Wypełnij wszystkie pola karty badania oraz parametrów recepty.", "error")
            return redirect(url_for("panel_specjalisty"))

        conn.execute(
            """
            INSERT INTO badanie_recepta (
                id_pacjenta, specjalista, data_badania, opis_badania,
                sfera_op, cylinder_op, os_op, sfera_ol, cylinder_ol, os_ol, zalecenia
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id_pacjenta,
                g.user["login"],
                data_badania,
                opis_badania,
                sfera_op,
                cylinder_op,
                os_op,
                sfera_ol,
                cylinder_ol,
                os_ol,
                zalecenia,
            ),
        )
        conn.commit()
        conn.close()
        flash("Zapisano wpis w historii badań oraz wystawiono receptę dla pacjenta.", "success")
        return redirect(url_for("panel_specjalisty"))

    pacjenci = conn.execute(
        """
        SELECT p.*, u.login AS email
        FROM pacjent p
        LEFT JOIN uzytkownik u ON p.id_uzytkownika = u.id_uzytkownika
        ORDER BY p.nazwisko ASC
        """
    ).fetchall()

    historia = conn.execute(
        """
        SELECT b.*, p.imie, p.nazwisko
        FROM badanie_recepta b
        JOIN pacjent p ON b.id_pacjenta = p.id_pacjenta
        ORDER BY b.data_badania DESC, b.id_wpisu DESC
        """
    ).fetchall()

    nadchodzace_wizyty = conn.execute(
        """
        SELECT w.*, p.imie, p.nazwisko
        FROM wizyta w
        JOIN pacjent p ON w.id_pacjenta = p.id_pacjenta
        WHERE w.status = 'Zaplanowana'
        ORDER BY w.poczatek ASC
        """
    ).fetchall()

    conn.close()
    return render_template(
        "specjalista.html",
        pacjenci=pacjenci,
        historia=historia,
        wizyty=nadchodzace_wizyty,
        dzisiaj=datetime.now().strftime("%Y-%m-%d"),
    )


if __name__ == "__main__":
    app.run(debug=True)
