# coding=utf-8
from datetime import date

import pytest
from sqlalchemy.exc import DataError, IntegrityError

import models.common.enums as enums
import models.common.overview as mco
import models.common.personnel as mcp


def test_person_generic_insert(session, person_data):
    """Person 001: Insert generic personnel data into Persons model and verify data."""
    generic_person = mcp.Persons(**person_data['generic'])
    session.add(generic_person)
    record = session.query(mcp.Persons).one()
    assert record.full_name == u"John Doe"
    assert record.official_name == u"John Doe"
    assert record.age(date(2010, 1, 1)) == 30
    assert record.exact_age(date(2010, 3, 15)) == (30, 74)
    assert repr(record) == u"<Person(name=John Doe, country=Portlandia, DOB=1980-01-01)>"


def test_person_middle_naming_order(session, person_data):
    """Person 002: Return correct format of Person's name with Western Middle naming order."""
    persons = [mcp.Persons(**data) for key, records in person_data.items()
               for data in records if key in ['player', 'manager', 'referee']]
    session.add_all(persons)

    person_from_db = session.query(mcp.Persons).filter(mcp.Persons.order == enums.NameOrderType.middle).one()
    assert person_from_db.full_name == u"Miguel Ángel Ponce"
    assert person_from_db.official_name == u"Miguel Ángel Ponce Briseño"


def test_person_eastern_naming_order(session, person_data):
    """Person 003: Return correct format of Person's name with Eastern naming order."""
    persons = [mcp.Persons(**data) for key, records in person_data.items()
               for data in records if key in ['player', 'manager', 'referee']]
    session.add_all(persons)

    person_from_db = session.query(mcp.Persons).filter(mcp.Persons.order == enums.NameOrderType.eastern).one()
    assert person_from_db.full_name == u"Son Heung-Min"
    assert person_from_db.full_name == person_from_db.official_name


def test_person_nickname(session, person_data):
    """Person 004: Return correct name of Person with nickname."""
    persons = [mcp.Persons(**data) for key, records in person_data.items()
               for data in records if key in ['player'] and 'nick_name' in data]
    session.add_all(persons)

    person_from_db = session.query(mcp.Persons).one()

    assert person_from_db.full_name == u"Cristiano Ronaldo"
    assert person_from_db.official_name == u"Cristiano Ronaldo Aveiro dos Santos"


def test_person_missing_first_name_error(session, person_data):
    """Person 005: Verify error if first name is missing from Persons data."""
    generic_data_without_first = {key: value for key, value in person_data['generic'].items() if key != 'first_name'}
    generic_person = mcp.Persons(**generic_data_without_first)
    with pytest.raises(IntegrityError):
        session.add(generic_person)
        session.commit()


def test_person_missing_last_name_error(session, person_data):
    """Person 006: Verify error if last name is missing from Persons data."""
    generic_data_without_last = {key: value for key, value in person_data['generic'].items() if key != 'last_name'}
    generic_person = mcp.Persons(**generic_data_without_last)
    with pytest.raises(IntegrityError):
        session.add(generic_person)
        session.commit()


def test_person_missing_birth_date_error(session, person_data):
    """Person 007: Verify error if birth date is missing from Persons data."""
    generic_data_without_dob = {key: value for key, value in person_data['generic'].items() if key != 'birth_date'}
    generic_person = mcp.Persons(**generic_data_without_dob)
    with pytest.raises(IntegrityError):
        session.add(generic_person)
        session.commit()


def test_person_age_query(session, person_data):
    """Person 008: Verify record retrieved when Persons is queried for matching ages."""
    reference_date = date(2015, 7, 1)
    persons = [mcp.Persons(**data) for key, records in person_data.items()
               for data in records if key in ['player', 'manager', 'referee']]
    session.add_all(persons)
    records = session.query(mcp.Persons).filter(mcp.Persons.age(reference_date) == 22)

    assert records.count() == 1

    son_hm = records.all()[0]
    assert son_hm.age(reference_date) == 22
    assert son_hm.exact_age(reference_date) == (22, 358)


def test_position_insert(session):
    """Positions 001: Insert generic data into Positions model and verify data."""
    left_fb = mcp.Positions(name="Left full-back", type=enums.PositionType.defender)
    session.add(left_fb)

    position_from_db = session.query(mcp.Positions).one()
    assert repr(position_from_db) == u"<Position(name=Left full-back, type=Defender)>"


def test_position_blank_error(session):
    """Positions 002: Verify error if blank name in Positions model."""
    left_fb = mcp.Positions(type=enums.PositionType.defender)
    with pytest.raises(IntegrityError):
        session.add(left_fb)
        session.commit()


def test_player_insert(session, person_data, position_data):
    player_data = [data for key, records in person_data.items() for data in records if key in ['player']]
    for player, position in zip(player_data, position_data):
        player['position'] = position
    players = [mcp.Players(**data) for data in player_data]
    session.add_all(players)

    players_from_db = session.query(mcp.Players)
    assert players_from_db.count() == len(players)


def test_player_representation(session, person_data, position_data):
    player_data = [data for key, records in person_data.items() for data in records if key in ['player']]
    for player, position in zip(player_data, position_data):
        player['position'] = position
    players = [mcp.Players(**data) for data in player_data]
    session.add_all(players)

    korean_player = session.query(mcp.Players).join(mco.Countries).\
        filter(mco.Countries.name == u"Korea Republic").one()
    assert repr(korean_player) == u"<Player(name=Son Heung-Min, DOB=1992-07-08, " \
                                  u"country=Korea Republic, position=Second striker)>"

    ronaldo = session.query(mcp.Players).filter(mcp.Players.nick_name == u"Cristiano Ronaldo").one()
    assert repr(ronaldo) == u"<Player(name=Cristiano Ronaldo, DOB=1985-02-05, " \
                            u"country=Portugal, position=Forward)>"

    mexican_player = session.query(mcp.Players).join(mco.Countries).filter(mco.Countries.name == u"Mexico").one()
    assert unicode(mexican_player) == u"<Player(name=Miguel Ángel Ponce, DOB=1989-04-12, " \
                                      u"country=Mexico, position=Left back)>"


def test_manager_insert(session, person_data):
    manager_data = [mcp.Managers(**data) for key, records in person_data.items()
                    for data in records if key in ['manager']]
    session.add_all(manager_data)

    managers_from_db = session.query(mcp.Managers)
    assert managers_from_db.count() == len(manager_data)

    persons_from_db = session.query(mcp.Persons)
    assert persons_from_db.count() == managers_from_db.count()


def test_manager_representation(session, person_data):
    manager_data = [mcp.Managers(**data) for key, records in person_data.items()
                    for data in records if key in ['manager']]
    session.add_all(manager_data)

    zico = session.query(mcp.Managers).filter(mcp.Managers.full_name == u"Zico").one()
    assert repr(zico) == u"<Manager(name=Zico, DOB=1953-03-03, country=Brazil)>"

    wenger = session.query(mcp.Managers).filter(mcp.Managers.last_name == u"Wenger").one()
    assert unicode(wenger) == u"<Manager(name=Arsène Wenger, DOB=1949-10-22, country=France)>"


def test_referee_insert(session, person_data):
    referees = [mcp.Referees(**data) for key, records in person_data.items()
                for data in records if key in ['referees']]
    session.add_all(referees)

    referees_from_db = session.query(mcp.Referees)
    assert referees_from_db.count() == len(referees)

    persons_from_db = session.query(mcp.Persons)
    assert persons_from_db.count() == referees_from_db.count()


def test_referee_representation(session, person_data):
    referees = [mcp.Referees(**data) for key, records in person_data.items()
                for data in records if key in ['referee']]
    session.add_all(referees)

    english_referee = session.query(mcp.Referees).join(mco.Countries).filter(mco.Countries.name == u"England").one()
    assert unicode(english_referee) == u"<Referee(name=Christopher Foy, DOB=1962-11-20, country=England)>"

    turkish_referee = session.query(mcp.Referees).join(mco.Countries).filter(mco.Countries.name == u"Turkey").one()
    assert unicode(turkish_referee) == u"<Referee(name=Cüneyt Çakır, DOB=1976-11-23, country=Turkey)>"


def test_player_history_insert(session, person_data, player_history_data):
    player_data = dict(position=mcp.Positions(name='Central Midfielder', type=enums.PositionType.midfielder),
                       **person_data['generic'])
    generic_player = mcp.Players(**player_data)
    player_history = [mcp.PlayerHistory(**dict(player=generic_player, **data)) for data in player_history_data]
    session.add_all(player_history)

    history_from_db = session.query(mcp.PlayerHistory).join(mcp.Players).\
        filter(mcp.Players.last_name == u"Doe")

    assert history_from_db.count() == len(player_history)


def test_player_history_representation(session, person_data, player_history_data):
    player_data = dict(position=mcp.Positions(name='Central Midfielder', type=enums.PositionType.midfielder),
                       **person_data['generic'])
    generic_player = mcp.Players(**player_data)
    player_history = [mcp.PlayerHistory(**dict(player=generic_player, **data)) for data in player_history_data]
    session.add_all(player_history)

    history_from_db = session.query(mcp.PlayerHistory).join(mcp.Players).\
        filter(mcp.Players.last_name == u"Doe", mcp.PlayerHistory.date == date(1998, 7, 15)).one()

    assert repr(history_from_db) == u"<PlayerHistory(name=John Doe, date=1998-07-15, height=1.74, weight=76)>"
